from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .twin import store
from .model import get_model_bundle
from .schemas import SimulationRequest, ForecastRequest, ScenarioRequest

app=FastAPI(title="GlucoTwin Bharat API",version="1.0.0",description="Synthetic-data proof-of-concept for meal-aware glucose trajectory forecasting. Not for clinical use.")
app.add_middleware(CORSMiddleware,allow_origins=["http://localhost:5173","http://127.0.0.1:5173"],allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
@app.get('/api/health')
def health(): return {"status":"ok","app":"GlucoTwin Bharat","data_mode":"synthetic","clinical_use":False}
@app.get('/api/patients')
def patients(): return store.list_patients()
@app.get('/api/patients/{pid}')
def patient(pid:str):
 p=store.get_patient(pid)
 if p is None: raise HTTPException(404,'Patient not found')
 return p
@app.get('/api/patients/{pid}/observations')
def observations(pid:str,limit:int=288):
 if store.get_patient(pid) is None: raise HTTPException(404,'Patient not found')
 rows=store.obs(pid,limit=limit)
 # Chart records can be downsampled by client; return scalar data only.
 return {"patient_id":pid,"count":len(rows),"observations":rows}
@app.post('/api/patients/{pid}/simulate')
def simulate(pid:str,request:SimulationRequest):
 try:return {"patient_id":pid,"new_observation":store.append_simulation(pid,request.meal_type,request.carbs_g,request.steps_15m,request.sleep_hours)}
 except KeyError: raise HTTPException(404,'Patient not found')
@app.post('/api/patients/{pid}/forecast')
def forecast_endpoint(pid:str,request:ForecastRequest):
 try:return store.create_forecast(pid,request.model_dump())
 except KeyError: raise HTTPException(404,'Patient not found')
@app.post('/api/patients/{pid}/scenario')
def scenario(pid:str,request:ScenarioRequest):
 try:return store.scenario(pid,request.model_dump())
 except KeyError: raise HTTPException(404,'Patient not found')
@app.post('/api/demo/reset')
def reset(): return store.reset()
@app.get('/api/model/metrics')
def metrics(): return get_model_bundle()['metrics']
