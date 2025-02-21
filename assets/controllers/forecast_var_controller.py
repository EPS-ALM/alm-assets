import pandas as pd
import numpy as np
import yfinance as yf
from statsmodels.tsa.api import VAR

def fetch_data(tickers, period="10y"):
    """Obtém dados históricos dos ativos usando yfinance."""
    data = yf.download(tickers, period=period)
    if data.empty:
        raise ValueError("Nenhum dado foi retornado para os tickers fornecidos.")
    
    # Get only Close prices and handle multi-level columns
    if isinstance(data.columns, pd.MultiIndex):
        data = data['Close']
    
    data = data.dropna()  # Remove valores NaN
    data.index = pd.to_datetime(data.index)  # Garantir que o índice seja datetime
    if not data.index.inferred_freq:
        data = data.asfreq('B')  # Define frequência como dias úteis, se não houver
    data = data.ffill()  # Preenche valores ausentes com forward fill
    
    # Ensure we have data for all tickers
    if len(data.columns) != len(tickers):
        missing = set(tickers) - set(data.columns)
        raise ValueError(f"Dados ausentes para os tickers: {missing}")
        
    return data

def calculate_metrics(data):
    returns = data.pct_change(fill_method=None).dropna()  # Evitar preenchimento automático
    annualized_return = returns.mean() * 252
    annualized_volatility = returns.std() * np.sqrt(252)
    metrics = pd.DataFrame({
        "Retorno Anualizado (%)": annualized_return * 100,
        "Volatilidade Anualizada (%)": annualized_volatility * 100
    })
    return metrics

def calculate_allocation(metrics):
    if "Retorno Anualizado (%)" not in metrics.columns or "Volatilidade Anualizada (%)" not in metrics.columns:
        raise ValueError("Métricas esperadas não encontradas nos dados fornecidos.")
    sharpe_ratios = metrics["Retorno Anualizado (%)"] / metrics["Volatilidade Anualizada (%)"]
    weights = sharpe_ratios / sharpe_ratios.sum()
    allocation = pd.DataFrame({
        "Ativo": metrics.index,
        "Peso Sugerido (%)": weights * 100
    }).reset_index(drop=True)
    return allocation

def forecast_with_var(data, steps=252):
    """Realiza previsão usando Modelos Vetoriais Autoregressivos (VAR)."""
    try:
        # Calculate returns and handle NaN values
        returns = data.pct_change(fill_method=None).dropna()
        
        if returns.empty or len(returns) < 2:
            raise ValueError("Insufficient data for VAR analysis")
            
        # Fit VAR model
        model = VAR(returns)
        
        # Find optimal lag order (using AIC)
        max_lags = min(15, int(len(returns) / 5))  # Rule of thumb
        if max_lags < 1:
            max_lags = 1
            
        results = model.fit(maxlags=max_lags, ic='aic')
        
        # Generate forecast
        forecast = results.forecast(returns.values[-results.k_ar:], steps)
        forecast_df = pd.DataFrame(forecast, columns=returns.columns)
        
        # Calculate metrics
        forecast_mean = forecast_df.mean() * 252
        forecast_volatility = forecast_df.std() * np.sqrt(252)
        
        forecast_metrics = pd.DataFrame({
            "Retorno Anualizado (%)": forecast_mean * 100,
            "Volatilidade Anualizada (%)": forecast_volatility * 100
        })
        
        return forecast_metrics
        
    except Exception as e:
        raise ValueError(f"Erro na previsão VAR: {str(e)}")

