from fastapi import APIRouter, HTTPException
from assets.models.forecast_lstm_model import ForecastRequest
from assets.controllers.forecast_lstm_controller import generate_forecast

forecast_lstm = APIRouter()

@forecast_lstm.post("/forecast_lstm/")
async def forecast_stocks(request: ForecastRequest):
    """
    Generate stock price forecasts using LSTM model
    """
    try:
        result = await generate_forecast(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 