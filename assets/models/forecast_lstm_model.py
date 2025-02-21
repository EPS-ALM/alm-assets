from pydantic import BaseModel
from typing import List

class TimeSeriesData(BaseModel):
    dates: List[str]
    values: List[float]

class ForecastRequest(BaseModel):
    data: TimeSeriesData
    ticker: str  # Added ticker field
    n_steps: int = 7  # Default to 7 days since that's what the models are trained for
    sequence_length: int = 60  # Default value
    n_features: int = 1  # Default value for univariate time series
    n_layers: int = 2  # Default value
    n_units: int = 50  # Default value
    epochs: int = 100  # Default value
    batch_size: int = 32  # Default value 