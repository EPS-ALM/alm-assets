from fastapi import APIRouter, HTTPException
import pandas as pd
from assets.models.forecast_request import ForecastRequest
from assets.controllers.forecast_lstm_controller import forecast_lstm, get_avaible_models

forecast_lstm  = APIRouter()

@forecast_lstm.post("/forecast_lstm/")
async def forecast_lstm_root(forecast_request: ForecastRequest):
    try:
        # Obter os dados históricos
        data = forecast_lstm(forecast_request.ticker)

        return {
            "ticker": forecast_request.ticker,
            "forecast": data.to_dict()
        }
    except Exception as e:
        import traceback
        traceback.print_exc()  # Exibe o rastreamento completo no log do console
        raise HTTPException(status_code=400, detail=str(e))
    
@forecast_lstm.get("/forecast_lstm/models")
async def forecast_lstm_models():
    try:
        models = get_avaible_models()
        return {
            "models": models
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
