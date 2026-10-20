from fastapi.testclient import TestClient
from app.main import app

client=TestClient(app)
def test_health():
 r=client.get('/api/health');assert r.status_code==200;assert r.json()['data_mode']=='synthetic'
def test_patient_list():
 r=client.get('/api/patients');assert r.status_code==200;assert len(r.json())>=3
def test_observations():
 pid=client.get('/api/patients').json()[0]['patient_id']
 r=client.get(f'/api/patients/{pid}/observations?limit=12');assert r.status_code==200;assert r.json()['count']==12
def test_forecast():
 pid=client.get('/api/patients').json()[0]['patient_id']
 r=client.post(f'/api/patients/{pid}/forecast',json={'carbs_g':45,'meal_type':'Poha','threshold_mg_dl':180})
 assert r.status_code==200;assert len(r.json()['prediction_points'])==4
 assert all(55<=p['glucose_mg_dl']<=400 for p in r.json()['prediction_points'])
def test_scenario():
 pid=client.get('/api/patients').json()[0]['patient_id']
 r=client.post(f'/api/patients/{pid}/scenario',json={'meal_type':'Idli','carbs_g':42,'steps_15m':250})
 assert r.status_code==200;assert len(r.json()['comparison'])==4
def test_simulate():
 pid=client.get('/api/patients').json()[0]['patient_id']
 r=client.post(f'/api/patients/{pid}/simulate',json={'meal_type':'Dosa','carbs_g':40,'steps_15m':100})
 assert r.status_code==200;assert r.json()['new_observation']['carbs_g']==40
