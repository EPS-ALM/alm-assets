from fastapi import APIRouter, HTTPException
from assets.models.forecast_sarima_model import ForecastRequest, ForecastResponse
from assets.controllers.forecast_sarima_controller import generate_forecast

forecast_sarima = APIRouter()

@forecast_sarima.post("/forecast_sarima/", response_model=ForecastResponse)
async def forecast_stocks(request: ForecastRequest):
    """
    Generate stock price forecasts using SARIMA model
    """
    try:
        result = await generate_forecast(request)
        return ForecastResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 