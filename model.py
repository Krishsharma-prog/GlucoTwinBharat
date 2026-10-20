"""Synthetic-data-trained forecasting model. Not validated for clinical use."""
from functools import lru_cache
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GroupShuffleSplit
from sklearn.metrics import mean_absolute_error, mean_squared_error

FEATURES = ["current", "baseline", "hba1c", "bmi", "age", "carbs", "meal_minutes", "slope", "steps", "sleep", "carb_sensitivity", "activity_sensitivity"]
HORIZONS = [15, 30, 60, 120]

def response_curve(t):
    t = max(0.0, float(t))
    return (1.0 - np.exp(-t / 24.0)) * np.exp(-t / 135.0)

def target_from_features(x, horizon):
    current, baseline, hba1c, bmi, age, carbs, meal_min, slope, steps, sleep, sens, act_sens = x
    elapsed = max(0.0, meal_min)
    future = elapsed + horizon
    recovery = baseline + (current - baseline) * np.exp(-horizon / (165 + max(0, hba1c-6)*18))
    meal_delta = carbs * sens * (response_curve(future) - response_curve(elapsed)) * 0.92
    trend_delta = np.clip(slope, -0.8, 0.8) * min(horizon, 60) * 0.22
    activity_delta = -min(steps, 2500) * act_sens * min(horizon / 30.0, 2.0) * 0.5
    sleep_adjustment = max(0, 6.0 - sleep) * 0.65 * (horizon / 60)
    metabolic_adjustment = max(0, hba1c-7.0) * 0.45 * (horizon/60)
    return float(np.clip(recovery + meal_delta + trend_delta + activity_delta + sleep_adjustment + metabolic_adjustment, 55, 400))

def create_synthetic_training_data(n=9000, seed=2026):
    rng=np.random.default_rng(seed)
    X=[];Y=[];groups=[]
    # Group identifiers imitate held-out virtual patients. All generated data remain synthetic.
    n_people=120
    profiles=[]
    for pid in range(n_people):
        baseline=float(rng.uniform(88,175));hba1c=float(rng.uniform(5.9,9.0));bmi=float(rng.uniform(20,34));age=float(rng.integers(30,75));sens=float(rng.uniform(.40,1.05));act=float(rng.uniform(.006,.016))
        profiles.append((pid,baseline,hba1c,bmi,age,sens,act))
    for i in range(n):
        pid,base,hba1c,bmi,age,sens,act=profiles[i%n_people]
        meal_min=float(rng.uniform(0,180));carbs=float(rng.choice([0.0,rng.uniform(15,100)],p=[.22,.78]))
        current=float(np.clip(base+rng.normal(0,24)+carbs*sens*response_curve(meal_min)*.78,60,330))
        slope=float(rng.normal(0,0.22));steps=int(rng.integers(0,1000));sleep=float(rng.uniform(4,9.5))
        features=[current,base,hba1c,bmi,age,carbs,meal_min,slope,steps,sleep,sens,act]
        ys=[target_from_features(features,h)+rng.normal(0,2.0) for h in HORIZONS]
        X.append(features);Y.append(ys);groups.append(pid)
    return np.asarray(X,dtype=float), np.asarray(Y,dtype=float), np.asarray(groups)

@lru_cache(maxsize=1)
def get_model_bundle():
    X,Y,groups=create_synthetic_training_data()
    split=GroupShuffleSplit(n_splits=1,test_size=.2,random_state=42)
    train_idx,test_idx=next(split.split(X,Y,groups))
    models=[]; per_horizon=[]
    for j,h in enumerate(HORIZONS):
        model=RandomForestRegressor(n_estimators=70,min_samples_leaf=3,max_features=.9,n_jobs=-1,random_state=100+j)
        model.fit(X[train_idx],Y[train_idx,j])
        pred=model.predict(X[test_idx]);truth=Y[test_idx,j]
        mae=float(mean_absolute_error(truth,pred));rmse=float(np.sqrt(mean_squared_error(truth,pred)))
        persistence=np.clip(X[test_idx,0],55,400)
        baseline_mae=float(mean_absolute_error(truth,persistence));baseline_rmse=float(np.sqrt(mean_squared_error(truth,persistence)))
        per_horizon.append({"minutes":h,"mae_mg_dl":round(mae,2),"rmse_mg_dl":round(rmse,2),"persistence_mae_mg_dl":round(baseline_mae,2),"persistence_rmse_mg_dl":round(baseline_rmse,2)})
        models.append(model)
    return {"models":models,"metrics":{"evaluation":"Held-out synthetic virtual-patient groups only; not clinical validation.","train_rows":int(len(train_idx)),"test_rows":int(len(test_idx)),"held_out_virtual_patients":int(len(np.unique(groups[test_idx]))),"per_horizon":per_horizon}}

def build_features(patient, observations, request):
    hist=observations[-6:]
    vals=[float(o["glucose_mg_dl"]) for o in hist]
    current=vals[-1] if vals else float(patient["baseline_glucose_mg_dl"])
    slope=(vals[-1]-vals[0])/(max(1,len(vals)-1)*5) if len(vals)>1 else 0.0 # mg/dL per minute
    last_meal=None; carbs=0.0
    for o in reversed(observations[-72:]):
        if float(o.get("carbs_g") or 0)>0:
            last_meal=o;carbs=float(o["carbs_g"]);break
    elapsed=180.0
    if last_meal:
        from datetime import datetime
        try:
            elapsed=(datetime.fromisoformat(observations[-1]["timestamp"])-datetime.fromisoformat(last_meal["timestamp"])).total_seconds()/60
        except Exception: elapsed=60.0
    # If user supplies a meal in the request, treat it as a new meal at t=0.
    if request.get("carbs_g",0)>0:
        carbs=float(request["carbs_g"]);elapsed=0.0
    latest=observations[-1] if observations else {}
    steps=int(request.get("steps_15m", latest.get("steps_15m",0)) or 0)
    sleep=float(request.get("sleep_hours",latest.get("sleep_hours",7)) or 7)
    tp=patient["twin_parameters"]
    f=[current,float(patient["baseline_glucose_mg_dl"]),float(patient["hba1c_percent"]),float(patient["bmi"]),float(patient["age"]),carbs,elapsed,slope*5,steps,sleep,float(tp["carb_sensitivity"]),float(tp["activity_sensitivity"])]
    return f,{"current_glucose_mg_dl":round(current,1),"recent_slope_mg_dl_per_5m":round(slope*5,2),"carbs_g":round(carbs,1),"minutes_since_meal":round(elapsed,1),"steps_15m":steps,"sleep_hours":sleep}

def forecast(patient, observations, request):
    bundle=get_model_bundle();features,context=build_features(patient,observations,request);X=np.asarray(features,dtype=float).reshape(1,-1)
    points=[];tree_preds=[]
    for h,model in zip(HORIZONS,bundle["models"]):
        # Predictions across trees provide a rough ensemble spread; not calibrated clinical probabilities.
        vals=np.array([tree.predict(X)[0] for tree in model.estimators_],dtype=float)
        pred=float(np.clip(np.mean(vals),55,400))
        spread=float(np.std(vals))
        points.append({"minutes_ahead":h,"glucose_mg_dl":round(pred,1),"ensemble_std_mg_dl":round(spread,1)})
        tree_preds.append(vals)
    threshold=float(request.get("threshold_mg_dl",180))
    common=min(len(a) for a in tree_preds)
    event_frequency=float(np.mean([any(tree_preds[j][i]>=threshold for j in range(len(tree_preds))) for i in range(common)]))
    risk="elevated" if event_frequency>=.65 else ("watch" if event_frequency>=.30 else "lower in this model")
    return {"patient_id":patient["patient_id"],"generated_at":__import__('datetime').datetime.now().isoformat(timespec='seconds'),"horizon_minutes":120,"prediction_points":points,"threshold_mg_dl":threshold,"estimated_excursion_frequency_pct":round(event_frequency*100,1),"model_risk_label":risk,"input_context":context,"model_note":"Synthetic-data-trained random forest ensemble. Tree frequency is an uncalibrated model signal, not a clinically validated probability or diagnosis.","metrics":bundle["metrics"]}
