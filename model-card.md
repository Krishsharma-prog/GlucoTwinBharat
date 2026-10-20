# Model card: GlucoTwin Bharat synthetic forecasting model

## Model purpose
Demonstrate the plumbing and UI of a patient-specific glucose trajectory forecasting Digital Twin in a student proof-of-concept. The model is not suitable for clinical use.

## Model family
Four scikit-learn `RandomForestRegressor` models predict glucose at 15, 30, 60, and 120 minutes. Each model has 70 trees and is trained from generated synthetic feature/target pairs.

## Input features
Current glucose, synthetic patient baseline, HbA1c, BMI, age, estimated carbohydrates, minutes since meal, recent glucose slope, steps, sleep, and synthetic individual response parameters.

## Data
Generated with an explicitly stylized simulation process; seed data in `backend/data/`. Training samples are generated in `backend/app/model.py`, with 9,000 examples across 120 synthetic virtual patient profiles. Train/test evaluation uses a group split by virtual-patient identity.

## Intended use
Educational demonstration of EHR + time-series feature fusion, forecast API behavior, synthetic evaluation and a doctor-facing dashboard.

## Out-of-scope use
Diagnosis, treatment recommendations, medicine dosing, emergency triage, real patient decisions, fitness-for-clinical-purpose claims, or deployment with patient data.

## Evaluation
Metrics are calculated on held-out synthetic profiles generated from the same modeling assumptions as training. This is a pipeline check, not independent external validation. A persistence baseline is reported for reference. See `evaluation.md` for the measured metrics in this run.

## Known limitations
- Simulation assumptions define the target; the model may simply learn the data generator.
- There is no validation on a real-world dataset.
- The tree-vote excursion signal is not a calibrated probability.
- No uncertainty interval has been calibrated to empirical clinical error.
- Meal carbohydrate amounts are user-editable illustrative estimates.
- No real sensor integration, authentication, or production-grade security is included.

## Responsible deployment requirements
Before any real clinical use, the project would need appropriately licensed and representative data, patient-separated external validation, calibration and subgroup error analysis, clinical review, privacy/security controls, prospective evaluation and applicable regulatory assessment.
