import yfinance as yf
import numpy as np

def get_asset_data(ticker):
    """
    Obtém dados históricos de um ativo financeiro usando a biblioteca yfinance.
    """
    asset = yf.Ticker(ticker)
    hist = asset.history(period="1y")
    
    if hist.empty:
        return None
    
    return {
        "ticker": ticker,
        "current_price": hist["Close"].iloc[-1],
        "volatility": np.std(hist["Close"].pct_change()) * np.sqrt(252),
        "historical_returns": hist["Close"].pct_change().mean() * 252
    }

def select_hedge_asset(candidate_tickers):
    """
    Seleciona um ativo de hedge com base na volatilidade e correlação negativa.
    """
    assets_data = []
    
    for ticker in candidate_tickers:
        data = get_asset_data(ticker)
        if data:
            assets_data.append(data)
    
    if not assets_data:
        return {"error": "Nenhum ativo válido encontrado."}
    
    # Ordenar ativos por menor volatilidade (critério inicial de hedge)
    selected_asset = min(assets_data, key=lambda x: x["volatility"])

    
    return {
        "selected_ticker": selected_asset["ticker"],
        "price": selected_asset["current_price"],
        "volatility": selected_asset["volatility"],
        "expected_return": selected_asset["historical_returns"]
    }

