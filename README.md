# GlucoTwin Bharat

**Indian meal-aware personalized glucose-excursion Digital Twin — proof of concept**

> Research/engineering prototype only. This project uses synthetic patient and sensor data and is not validated for diagnosis, treatment, medication decisions, or clinical care.

## Team and challenge details
- **Team leader:** Krish Sharma (confirm spelling for the submission)
- **College / institution:** NMIMS Mukesh Patel School of Technology Management & Engineering (MPSTME), Mumbai (confirm the exact institution label used during registration)
- **Team size:** 1
- **Team folder naming for submission:** `GlucoTwinBharat_NMIMS_MPSTME_Mumbai` (adjust to the exact team name and official college name)
- **Challenge:** Happiest Health Digital Twin Challenge 2026
- **Project title:** GlucoTwin Bharat
- **Contact:** Add the team leader's correct email and phone number in the submission form. Do not place private contact details in this public repository unless required and intentionally approved.

## Problem statement and healthcare use case
Many conventional glucose dashboards show historical readings but do not demonstrate how a patient's evolving state can be used to forecast potential glucose excursions. GlucoTwin Bharat demonstrates a narrowly scoped digital twin: it combines synthetic historical EHR attributes with a timestamped simulated CGM/lifestyle stream, updates an in-memory virtual patient state, forecasts glucose at 15, 30, 60, and 120 minutes, estimates the model-ensemble frequency of crossing a configurable threshold, and enables hypothetical Indian-meal scenarios.

The modeled outcome is a possible elevated-glucose excursion. This is a synthetic-data proof of concept, not a clinical prediction system.

## What is implemented
- Six fictional patients with demographics, simulated diagnoses, lab history, and patient-specific simulation parameters.
- 24 hours of five-minute synthetic glucose and lifestyle observations for each patient.
- FastAPI REST backend for EHR, observations, simulated sensor updates, forecasts, scenario comparisons, health status, and reset.
- React/Vite clinical-style dashboard with glucose chart, patient profile, sensor simulator, Indian meal selector, activity/sleep inputs, threshold slider, forecast outputs, what-if comparison, model metrics, and safety disclaimer.
- Four Random Forest regression models, one for each forecast horizon (15, 30, 60 and 120 minutes), trained on generated synthetic trajectory examples.
- Synthetic group holdout model evaluation reported as MAE/RMSE.
- Automated backend tests.

## Technical stack
- Frontend: React, Vite, Recharts, Lucide icons, CSS.
- Backend: Python, FastAPI, Pydantic, pandas, NumPy.
- AI/ML: scikit-learn `RandomForestRegressor` with multiple horizons; evaluation using grouped held-out synthetic virtual patients, MAE and RMSE.
- Data formats: JSON synthetic EHR and CSV time series.

## System architecture
See `docs/architecture.pdf`, `docs/architecture.svg`, `docs/presentation.pptx`, `docs/presentation.pdf`, `docs/model-card.md`, and `docs/evaluation.md`.

## Run locally
Requirements: Python 3.10+ and Node.js 18+. On Windows, run `start_backend_windows.bat` and `start_frontend_windows.bat` in two separate terminals after extracting the project. The first run downloads dependencies and therefore needs internet access.

### 1. Backend
```bash
cd backend
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
Open `http://127.0.0.1:8000/docs` for the interactive API docs.

### 2. Frontend (new terminal)
```bash
cd frontend
npm install
npm run dev
```
Open the Vite URL printed in the terminal (normally `http://localhost:5173`). The frontend expects the API at `http://127.0.0.1:8000/api`; change `frontend/.env.example` to a `.env` file to override it.

### 3. Tests
```bash
cd backend
pip install -r requirements.txt
pip install -r requirements-dev.txt
python -m pytest -q
```
The first forecast call trains the synthetic-data models and can take a short time. The backend keeps the trained models cached in memory for subsequent calls.

## Key API endpoints
| Method | Path | Purpose |
|---|---|---|
| `GET` | `/api/health` | Service status and synthetic-data mode |
| `GET` | `/api/patients` | Patient index |
| `GET` | `/api/patients/{id}` | Synthetic EHR profile |
| `GET` | `/api/patients/{id}/observations?limit=288` | Timestamped readings |
| `POST` | `/api/patients/{id}/simulate` | Append the next synthetic five-minute sensor reading |
| `POST` | `/api/patients/{id}/forecast` | Forecast 15/30/60/120 minutes |
| `POST` | `/api/patients/{id}/scenario` | Compare a hypothetical meal/activity with a no-new-meal baseline |
| `GET` | `/api/model/metrics` | Held-out synthetic performance metrics |
| `POST` | `/api/demo/reset` | Restore the synthetic stream to seed state |

## Dataset provenance and limitations
All contents of `backend/data/patients.json` and `backend/data/observations.csv` are generated for this project. They are not sourced from real people, a clinical database, a wearable, or a glucose device. The synthetic generator uses simple stylized response curves and random variation to exercise the pipeline. The provided metrics measure fit against a held-out synthetic population generated from the same synthetic process; they are not independent clinical evidence. No clinical performance claim should be made from these numbers.

## Model methodology
The training pipeline generates 9,000 feature rows across 120 simulated profiles. At each row it samples current glucose, baseline, HbA1c, BMI, age, meal carbohydrate estimate, time since meal, recent slope, step count, sleep duration and synthetic individual response parameters. Four random forests predict future glucose at 15/30/60/120 minutes. A group holdout by virtual-patient ID reduces patient leakage between train/test partitions. Predictions are clipped to a broad output range for UI stability; that clipping is not a clinical safety guarantee.

The UI's “estimated excursion frequency” is computed from the fraction of estimator trees that predict a threshold crossing across the horizons. This tree frequency is an uncalibrated model signal, not a clinically calibrated probability. It must not be presented to patients as a validated risk score.

## Safety, privacy and intended use
- Synthetic data only; no real patient details should be committed.
- No diagnosis, treatment, medication, or emergency advice.
- A real clinical deployment would require clinician oversight, appropriate consent and privacy controls, independent prospective validation, clinical risk analysis, and applicable regulatory review.
- No sensor vendor integrations are implemented; sensor updates are simulated.
- No authentication or production security controls are included. Do not expose this development server to the public internet with real data.

## Reproducibility and limitations
- The seed EHR and initial time series are committed in `backend/data/`. To regenerate the time series, run `cd backend` then `python -m app.generate_synthetic_data` (timestamp window refreshes; RNG sequence is seeded).
- Model generation uses random seeds for reproducible training metrics in an unchanged environment.
- The simulated `POST /simulate` endpoint appends records in process memory; restarting the backend resets the stream.
- The what-if comparison is a model sensitivity demonstration, not proof an intervention causes that outcome.
- Meal carb values are illustrative estimates and not nutritional advice.

## Challenge timeline
The public [Happiest Health Digital Twin Challenge 2026 listing](https://api.unstop.com/hackathons/digital-twin-challenge-2026-happiest-health-1757873) lists Prototype & Code Submission through **20 October 2026, 7:00 PM IST**. Verify the active submission portal before final upload.

## Challenge submission checklist
- [ ] Add/confirm the official team name and college/incubator naming.
- [ ] Confirm team leader name and enter correct phone/email in the challenge submission form.
- [ ] Push the complete repository to GitHub and set it Public.
- [ ] Re-run setup and tests from a clean environment.
- [ ] Review `docs/presentation.pdf` and `docs/architecture.pdf`.
- [ ] Record and upload the live app demonstration using `docs/demo-script.md` (minimum 20 minutes per listing).
- [ ] Add the final public demo video URL here.
- [ ] Submit the public GitHub URL and the team leader details using the official challenge portal.

## License
This project is released under the MIT License; see `LICENSE`.
