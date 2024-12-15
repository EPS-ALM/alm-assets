from ...stocks_forecasting.modelos.LSTM import forecast_with_lstm, get_avaible_models

def forecast_lstm(ticker:str):
    """Realiza previsão de retornos de um ativo usando LSTM."""
    avaible_models = get_avaible_models()
    if ticker not in avaible_models:
        raise ValueError(f"Modelo para {ticker} não encontrado.")
    
    return forecast_with_lstm(ticker)
    