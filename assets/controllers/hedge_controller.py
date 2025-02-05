import yfinance as yf
import pandas as pd
import numpy as np

def find_hedges(input_tickers, hedge_candidates, start_date='2020-01-01', end_date=None):
    if end_date is None:
        end_date = pd.Timestamp.today().strftime('%Y-%m-%d')
    
    hedge_results = {}
    
    for ticker in input_tickers:
        try:
            tkr_data = yf.download(ticker, start=start_date, end=end_date, progress=False)['Adj Close']
            if len(tkr_data) < 10:
                print(f"Not enough data for {ticker}. Skipping.")
                continue

            candidate_info = []
            
            for candidate in hedge_candidates:
                try:
                    c_data = yf.download(candidate, start=start_date, end=end_date, progress=False)['Adj Close']
                    if len(c_data) < 10:
                        continue

                    merged = pd.concat([tkr_data, c_data], axis=1).dropna()
                    merged.columns = [ticker, candidate]
                    
                    if len(merged) < 10:
                        continue

                    returns = merged.pct_change().dropna()
                    
                    if len(returns) < 5:
                        continue

                    correlation = returns.corr().iloc[0, 1]
                    volatility = returns[candidate].std()
                    
                    candidate_info.append({
                        'candidate': candidate,
                        'correlation': correlation,
                        'volatility': volatility
                    })
                
                except Exception as e:
                    continue

            if not candidate_info:
                hedge_results[ticker] = None
                continue

            df = pd.DataFrame(candidate_info)
            negative_df = df[df['correlation'] < 0]
            
            if not negative_df.empty:
                sorted_df = negative_df.sort_values(by=['correlation', 'volatility'], 
                                                  ascending=[True, True])
            else:
                sorted_df = df.sort_values(by=['correlation', 'volatility'], 
                                         ascending=[True, True])

            best = sorted_df.iloc[0]
            hedge_results[ticker] = {
                'ticker': ticker,
                'hedge_ticker': best['candidate'],
                'correlation': round(best['correlation'], 4),
                'volatility': round(best['volatility'], 6),
                'analysis_period': f"{start_date} to {end_date}"
            }
        
        except Exception as e:
            print(f"Error processing {ticker}: {str(e)}")
            hedge_results[ticker] = None
    
    return hedge_results

def get_hedges(tickers):
    hedge_candidates = ['TLT', 'IEF', 'SHY', 'VXX', 
                'XLU', 'XLP', 'GDX', 'SLV', 
                'USO', 'LQD', 'HYG', 'BND', 'JNK', 'SPXS', 'ETHU', 'TECL', 'USD']
    results = find_hedges(tickers, hedge_candidates, start_date='2018-01-01')
    return list(results.values())
