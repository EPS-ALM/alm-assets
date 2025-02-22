from pydantic import BaseModel, validator
from typing import List, Optional, Tuple

class StockData(BaseModel):
    dates: List[str]
    values: List[float]

    @validator('dates')
    def validate_dates(cls, v):
        if not v:
            raise ValueError("dates list cannot be empty")
        return v

    @validator('values')
    def validate_values(cls, v):
        if not v:
            raise ValueError("values list cannot be empty")
        if len(v) < 4:  # SARIMA needs more data points
            raise ValueError("At least 4 data points are required")
        return v

class ForecastRequest(BaseModel):
    ticker: str
    n_steps: int
    order: Optional[Tuple[int, int, int]] = (2, 1, 2)
    seasonal_order: Optional[Tuple[int, int, int, int]] = (1, 1, 1, 5)
    days: Optional[int] = 100  # Number of historical days to fetch

    @validator('n_steps')
    def validate_n_steps(cls, v):
        if v < 1:
            raise ValueError("n_steps must be greater than 0")
        return v

    @validator('days')
    def validate_days(cls, v):
        if v < 10:
            raise ValueError("days must be at least 10")
        return v

class ForecastResponse(BaseModel):
    forecast_dates: List[str]
    forecast_values: List[float]
    metrics: Optional[dict] = None
    plot_base64: Optional[str] = None