from pydantic import BaseModel, Field
from typing import Optional

class SimulationRequest(BaseModel):
    meal_type: Optional[str] = None
    carbs_g: float = Field(default=0, ge=0, le=200)
    steps_15m: int = Field(default=0, ge=0, le=10000)
    sleep_hours: float = Field(default=7, ge=0, le=24)

class ForecastRequest(BaseModel):
    meal_type: Optional[str] = None
    carbs_g: float = Field(default=0, ge=0, le=200)
    steps_15m: int = Field(default=0, ge=0, le=10000)
    sleep_hours: float = Field(default=7, ge=0, le=24)
    threshold_mg_dl: float = Field(default=180, ge=120, le=350)

class ScenarioRequest(BaseModel):
    meal_type: str = "Roti + dal"
    carbs_g: float = Field(default=55, ge=0, le=200)
    steps_15m: int = Field(default=300, ge=0, le=10000)
    sleep_hours: float = Field(default=7, ge=0, le=24)
    threshold_mg_dl: float = Field(default=180, ge=120, le=350)
