from pydantic import BaseModel
from typing import List, Optional, Tuple

class StockData(BaseModel):
    dates: List[str]
    values: List[float]
    
class ForecastRequest(BaseModel):
    data: StockData
    n_steps: int
    order: Optional[Tuple[int, int, int]] = (2, 1, 2)
    seasonal_order: Optional[Tuple[int, int, int, int]] = (1, 1, 1, 5)

class ForecastResponse(BaseModel):
    forecast_dates: List[str]
    forecast_values: List[float]
    metrics: Optional[dict] = None 
    plot_base64: Optional[str] = None