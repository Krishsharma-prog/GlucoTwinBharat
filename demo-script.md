# GlucoTwin Bharat — 20-minute demo recording script

**Recording note:** Record your actual running app and voice/video. This document is a timed runbook, not a pre-recorded video. The submission listing asks for a minimum 20-minute video. Upload it as an unlisted YouTube video or use the allowed presentation recording workflow, then put the share URL in README.md.

## Before recording (not part of 20-minute runtime)
1. Start backend and frontend using README instructions.
2. Open the app at the Vite URL; also open `http://127.0.0.1:8000/docs` in a separate tab.
3. Check the “API connected” indicator and run a forecast once so model training has completed.
4. Close popups, enlarge the browser, and keep synthetic-data disclaimer visible.
5. Have architecture diagram and presentation ready. Never enter real patient information.

## 0:00–2:00 — Introduction and problem
“Hello, I am presenting GlucoTwin Bharat, a student proof-of-concept for an Indian meal-aware glucose Digital Twin. A Digital Twin is more than a dashboard: it combines a represented patient's historical record with a changing stream of observations and uses the updated state to generate a forecast. Our target outcome is a potential glucose excursion over a two-hour horizon. This is a synthetic-data research prototype, not a medical device.”

Show title and top dashboard metrics. Define the use case and explain that the target is a potential elevated-glucose threshold crossing, not a diagnosis.

## 2:00–4:00 — Why Indian meal awareness
Point to the Poha, Idli, Dosa, Roti + dal and Rice + sabzi options. Explain that meal names are scenario labels; carbohydrate amount is an illustrative parameter in the demo catalogue, not a claim that a given serving always has that carbohydrate content. Different virtual patients have different synthetic baseline and response parameters.

## 4:00–6:00 — Architecture
Show `docs/architecture.pdf`. Explain the flow: synthetic EHR JSON + synthetic timestamped CGM/steps/sleep CSV → FastAPI → twin state and model → React dashboard. Note that the current version simulates a sensor stream and has no real device integration. Show API docs briefly if useful.

## 6:00–9:00 — Historical record and dynamic stream
Select patient GTB-002. Show age, BMI, simulated diagnoses, HbA1c and baseline. Point out the historical EHR and timestamped observations are different streams. Click “Advance simulated sensor by 5 minutes.” Explain the API adds a synthetic observation to the in-memory state and the dashboard reloads it. Repeat once if useful.

## 9:00–12:00 — Forecast model
Click “Update forecast.” Explain the forecast horizons of 15, 30, 60 and 120 minutes. The regression models are random forests trained on generated synthetic trajectories. Highlight the input context: current glucose, recent slope, time since meal, estimated carbs, steps, sleep and patient-specific synthetic parameters. Do not describe the forest-tree frequency as a clinically calibrated probability.

## 12:00–14:00 — Model evaluation
Scroll to the synthetic evaluation table. Explain MAE and RMSE in mg/dL and the grouped holdout of virtual-patient identities. State explicitly that these are internal synthetic evaluation metrics, not clinical validation, and that a real deployment would need an open-source or prospective clinical benchmark with an appropriate split and review.

## 14:00–17:00 — Scenario simulation
Choose “Poha” or “Roti + dal,” change the estimated carbs, adjust recent steps or sleep, and click “Compare scenario.” Point to the scenario forecast and the no-new-meal baseline. Explain the displayed deltas reflect the current model's sensitivity under its assumptions; they do not show causality or guarantee benefit from activity or meal substitution. Change the meal once to show how the scenario changes.

## 17:00–18:30 — API and reproducibility
Show `GET /api/health`, `GET /api/patients`, and a forecast endpoint in Swagger (`/docs`). Mention deterministic seed dataset files, local setup, tests and the public repository. Point to README, requirements, `.gitignore`, and MIT License.

## 18:30–20:00 — Impact, limitations and close
Summarize the innovation: EHR + dynamic data fusion, continuously updated virtual patient state, multi-horizon forecast, Indian meal-aware what-if comparison, and transparent synthetic evaluation. Discuss next steps: evaluate on an appropriately licensed open dataset, test calibration, add clinician review, implement secure data controls, and conduct prospective validation before any real clinical use. Close with the explicit statement that no real patients or medical decisions are involved in this proof-of-concept.

## Recording checklist
- [ ] Visible screen recording covers the actual working app, not slides only.
- [ ] Audio is clear and total runtime is 20+ minutes.
- [ ] Demo video access is unlisted/public as allowed, not private or blocked to jury.
- [ ] Video URL is added to README.md and checked in an incognito window.
