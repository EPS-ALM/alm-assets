from fastapi import APIRouter, HTTPException
import pandas as pd
from assets.models.asset_request import AssetRequest
from assets.controllers.forecast_var_controller import fetch_data, calculate_metrics, calculate_allocation, forecast_with_var

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

        ativos = set(asset_request.tickers)

        ativos_formatados = []
        for ativo in ativos:
            ativo_dados = {
                "ativo": ativo,
                "historical_metrics": {
                    categoria: next(
                        (item["valor"] for item in [
                            {"ativo": k, "valor": v} for k, v in valores.items()
                        ] if item["ativo"] == ativo), None
                    )
                    for categoria, valores in metrics.items()
                },
                "historical_allocation": next(
                    (item["Peso Sugerido (%)"] for item in allocation.to_dict(orient="records") if item["Ativo"] == ativo), 
                    None
                ),
                "forecast_metrics": {
                    categoria: next(
                        (item["valor"] for item in [
                            {"ativo": k, "valor": v} for k, v in valores.items()
                        ] if item["ativo"] == ativo), None
                    )
                    for categoria, valores in forecast.items()
                },
                "forecast_allocation": next(
                    (item["Peso Sugerido (%)"] for item in forecast_allocation.to_dict(orient="records") if item["Ativo"] == ativo),
                    None
                ),
            }
            ativos_formatados.append(ativo_dados)

        return {
            "data": ativos_formatados,
        }
    except Exception as e:
        import traceback
        traceback.print_exc()  # Exibe o rastreamento completo no log do console
        raise HTTPException(status_code=400, detail=str(e))
