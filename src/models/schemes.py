from pydantic import BaseModel
from typing import List, Dict



class HellowRequest(BaseModel):
    names: list[str]

class PredictRequest(BaseModel):
    df: List[Dict]
    time_column: str
    col_target: str
    forecast_horizon_time: str

