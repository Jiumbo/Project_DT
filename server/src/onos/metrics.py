from pydantic import BaseModel
from typing import ClassVar


class Metrics(BaseModel):
    param: ClassVar[str] = "metrics"
    counter: float
    mean_rate: float
    rate_1_min: float
    rate_5_min: float
    rate_15_min: float
    mean: float
    min: float
    max: float
    stddev: float
