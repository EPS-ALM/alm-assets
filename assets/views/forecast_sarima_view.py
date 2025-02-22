from fastapi import APIRouter, HTTPException
from assets.models.forecast_sarima_model import ForecastRequest, ForecastResponse
from assets.controllers.forecast_sarima_controller import generate_forecast
import traceback

forecast_sarima = APIRouter()

@forecast_sarima.post("/forecast_sarima/", response_model=ForecastResponse)
async def forecast_stocks(request: ForecastRequest):
    """
    Generate stock price forecasts using SARIMA model
    
    Parameters:
    - ticker: Stock ticker symbol (e.g., "AAPL", "MSFT")
    - n_steps: Number of steps to forecast
    - order: SARIMA order parameters (p,d,q)
    - seasonal_order: Seasonal order parameters (P,D,Q,s)
    - days: Number of historical days to use for training (default: 100)
    """
    try:
        if request.n_steps < 1:
            raise ValueError("n_steps must be greater than 0")
            
        result = await generate_forecast(request)
        return ForecastResponse(**result)
    except ValueError as e:
        # Handle validation errors
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Log the full error for debugging
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Error generating forecast: {str(e)}"
        ) 