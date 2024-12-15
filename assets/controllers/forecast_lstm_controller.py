from ...stocks_forecasting.modelos.LSTM import forecast_with_lstm

def forecast(ticker:str):
    """Realiza previsão de retornos de um ativo usando LSTM."""
    forecast = forecast_with_lstm(ticker)
    