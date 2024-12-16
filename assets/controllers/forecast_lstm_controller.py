import yfinance as yf
import datetime as dt
from ...stocks_forecasting.modelos.LSTM import forecast_with_lstm, get_avaible_models, get_model_prediction

def forecast_lstm(ticker:str):
    """Realiza previsão de retornos de um ativo usando LSTM."""
    avaible_models = get_avaible_models()
    if ticker not in avaible_models:
        raise ValueError(f"Modelo para {ticker} não encontrado.")
    
    final = dt.datetime.now().date()
    inicial = dt.date(final.year - 20, 1, 1)
    
    df = yf.download(ticker, inicial, final)
    df.columns = [header_pos[0] for header_pos in df.columns]
    df = df.reset_index()
    #df.to_csv(f'../../stocks_forecasting/dados/raw/{ticker}.csv')
    
    lstm_forecast = get_model_prediction(ticker, df)
    
    return lstm_forecast
    