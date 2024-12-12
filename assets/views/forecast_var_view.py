from fastapi import APIRouter, HTTPException
import pandas as pd
from models.asset_request import AssetRequest
from controllers.forecast_var_controller import fetch_data, calculate_metrics, calculate_allocation, forecast_with_var

forecast_var  = APIRouter()

@forecast_var.post("/forecast_var/")
async def forecast_var_root(asset_request: AssetRequest):
    try:
        # Obter os dados históricos
        data = fetch_data(asset_request.tickers)

        # Processar métricas e alocações baseadas em dados históricos
        metrics = calculate_metrics(data)
        allocation = calculate_allocation(metrics)

        # Gerar previsões e alocações baseadas no modelo VAR
        forecast = forecast_with_var(data)
        forecast_allocation = calculate_allocation(forecast)


        return {
            "historical_metrics": metrics.to_dict(),
            "historical_allocation": allocation.to_dict(orient="records"),
            "forecast_metrics": forecast.to_dict(),
            "forecast_allocation": forecast_allocation.to_dict(orient="records")
        }
    except Exception as e:
        import traceback
        traceback.print_exc()  # Exibe o rastreamento completo no log do console
        raise HTTPException(status_code=400, detail=str(e))
