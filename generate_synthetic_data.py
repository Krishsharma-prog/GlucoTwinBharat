"""Regenerate the committed synthetic CGM/lifestyle time-series seed data."""
from datetime import datetime, timedelta
from pathlib import Path
import csv, json, math, random

DATA = Path(__file__).resolve().parents[1] / "data"
patients = json.loads((DATA / "patients.json").read_text(encoding="utf-8"))
now = datetime.now().replace(second=0, microsecond=0)
meals = [(465, "Poha", 48), (765, "Roti + dal", 62), (990, "Idli", 42), (1185, "Rice + sabzi", 70)]
rng = random.Random(517)
rows = []
for pi, patient in enumerate(patients):
    start = now - timedelta(hours=24)
    baseline = float(patient["baseline_glucose_mg_dl"])
    sensitivity = float(patient["twin_parameters"]["carb_sensitivity"])
    for idx in range(288):
        timestamp = start + timedelta(minutes=5 * idx)
        minute_of_day = timestamp.hour * 60 + timestamp.minute
        angle = 2 * math.pi * minute_of_day / 1440
        meal_effect = 0.0
        meal_type = ""
        carbs = 0
        for meal_minute, name, amount in meals:
            elapsed = (minute_of_day - meal_minute) % 1440
            if elapsed < 240:
                curve = (1 - math.exp(-elapsed / 22)) * math.exp(-elapsed / 125)
                meal_effect += amount * sensitivity * 0.92 * curve
            if elapsed < 5:
                meal_type, carbs = name, amount
        circadian = 5 * math.sin(angle - 1.2) + 3 * math.sin(2 * angle)
        noise = rng.gauss(0, 2.8 + (pi % 3) * 0.7)
        activity_drop = 4 if 17 * 60 < minute_of_day < 18 * 60 else 0
        glucose = max(65, min(330, baseline + circadian + meal_effect - activity_drop + noise))
        steps = int(rng.choice([0, 0, 30, 80, 120, 200, 350, 500]))
        rows.append({
            "patient_id": patient["patient_id"],
            "timestamp": timestamp.isoformat(timespec="minutes"),
            "glucose_mg_dl": round(glucose, 1),
            "carbs_g": carbs,
            "meal_type": meal_type,
            "steps_15m": steps,
            "sleep_hours": round(max(3.5, min(9.2, rng.gauss(6.9, 0.8))), 1),
            "activity_level": "moderate" if steps > 180 else ("light" if steps > 0 else "sedentary"),
        })
with (DATA / "observations.csv").open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)
print(f"Wrote {len(rows)} synthetic observations for {len(patients)} virtual patients to {DATA / 'observations.csv'}")
