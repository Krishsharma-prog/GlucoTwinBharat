# Model evaluation report

**Scope:** internal evaluation on held-out synthetic virtual-patient groups generated from the same stylized process as the training data. These figures are not clinical validation.

- Synthetic training rows: 7200
- Synthetic test rows: 1800
- Held-out virtual patients: 24

| Forecast horizon | Random Forest MAE (mg/dL) | Random Forest RMSE (mg/dL) | Persistence baseline MAE (mg/dL) | Persistence baseline RMSE (mg/dL) |
|---:|---:|---:|---:|---:|
| +15 min | 2.01 | 2.63 | 3.94 | 5.06 |
| +30 min | 2.40 | 3.16 | 6.98 | 8.62 |
| +60 min | 3.21 | 4.22 | 12.67 | 15.36 |
| +120 min | 3.66 | 4.77 | 18.69 | 23.02 |

## Interpretation

The persistence baseline assumes future glucose equals the latest observed glucose. Results quantify fit to synthetic generated targets only. A lower synthetic MAE does not imply real-world clinical utility. The training and evaluation targets share the same generator assumptions, so evaluation is useful for software and pipeline checks, not evidence of generalization. Before real use, evaluate against appropriately licensed independent data with participant-level separation, calibration assessment, subgroup error analysis and clinical oversight.
