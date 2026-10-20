from pathlib import Path
from datetime import datetime, timedelta
import csv, json, random, math
import pandas as pd
from .model import forecast

BASE=Path(__file__).resolve().parents[1]
DATA=BASE/'data'
class TwinStore:
    def __init__(self):
        self.patients=json.loads((DATA/'patients.json').read_text(encoding='utf-8'))
        self.observations=pd.read_csv(DATA/'observations.csv').fillna('')
        self.observations['timestamp']=self.observations['timestamp'].astype(str)
        self._seed=self.observations.copy()
        self.tick=0
    def list_patients(self):
        return [{k:p[k] for k in ['patient_id','display_name','age','sex','bmi','condition','hba1c_percent','baseline_glucose_mg_dl']} for p in self.patients]
    def get_patient(self,pid):
        for p in self.patients:
            if p['patient_id']==pid:return p
        return None
    def obs(self,pid,limit=288):
        df=self.observations[self.observations.patient_id==pid].tail(max(1,min(limit,2000)))
        return df.to_dict(orient='records')
    def append_simulation(self,pid,meal_type=None,carbs_g=0,steps_15m=0,sleep_hours=7):
        patient=self.get_patient(pid)
        if not patient: raise KeyError(pid)
        prior=self.observations[self.observations.patient_id==pid]
        last=prior.iloc[-1].to_dict()
        last_time=datetime.fromisoformat(str(last['timestamp']))
        dt=last_time+timedelta(minutes=5)
        current=float(last['glucose_mg_dl']);base=float(patient['baseline_glucose_mg_dl']);tp=patient['twin_parameters']
        meal_effect=0.0
        # Use new meal event at the simulated timestamp; small step response demonstrates changing twin state.
        if carbs_g>0:
            meal_effect=float(carbs_g)*float(tp['carb_sensitivity'])*0.08
        recent_vals=prior.tail(6)['glucose_mg_dl'].astype(float).tolist()
        slope=(recent_vals[-1]-recent_vals[0])/max(1,len(recent_vals)-1) if len(recent_vals)>1 else 0
        recovery=(base-current)*0.014
        activity_effect=-min(int(steps_15m),1000)*float(tp['activity_sensitivity'])*0.04
        noise=random.Random(f"{pid}-{dt.isoformat()}-{self.tick}").uniform(-1.2,1.2)
        g=max(55,min(400,current+recovery+meal_effect+slope*0.10+activity_effect+noise))
        row={'patient_id':pid,'timestamp':dt.isoformat(timespec='minutes'),'glucose_mg_dl':round(g,1),'carbs_g':float(carbs_g),'meal_type':meal_type or '', 'steps_15m':int(steps_15m),'sleep_hours':float(sleep_hours),'activity_level':'moderate' if steps_15m>180 else ('light' if steps_15m>0 else 'sedentary')}
        self.observations=pd.concat([self.observations,pd.DataFrame([row])],ignore_index=True)
        self.tick+=1
        return row
    def reset(self):
        self.observations=self._seed.copy();self.tick=0
        return {"message":"Synthetic sensor stream reset to its seed state.","observations":len(self.observations)}
    def create_forecast(self,pid,request):
        p=self.get_patient(pid)
        if p is None: raise KeyError(pid)
        return forecast(p,self.obs(pid,limit=288),request)
    def scenario(self,pid,request):
        p=self.get_patient(pid)
        if p is None: raise KeyError(pid)
        base_req={"carbs_g":0,"steps_15m":request.get('steps_15m',0),"sleep_hours":request.get('sleep_hours',7),"threshold_mg_dl":request.get('threshold_mg_dl',180)}
        scen_req={**request}
        baseline=self.create_forecast(pid,base_req);scenario=self.create_forecast(pid,scen_req)
        compare=[]
        for a,b in zip(baseline['prediction_points'],scenario['prediction_points']):
            compare.append({"minutes_ahead":a['minutes_ahead'],"baseline_mg_dl":a['glucose_mg_dl'],"scenario_mg_dl":b['glucose_mg_dl'],"delta_mg_dl":round(b['glucose_mg_dl']-a['glucose_mg_dl'],1)})
        return {"patient_id":pid,"scenario_label":request.get('meal_type','Hypothetical meal'),"carbs_g":request.get('carbs_g',0),"comparison":compare,"baseline":baseline,"scenario":scenario,"interpretation":"Model-only what-if result on synthetic data. It is not a prediction of treatment benefit or a clinical recommendation."}
store=TwinStore()
