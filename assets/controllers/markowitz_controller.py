from datetime import datetime
import datetime as dt
import yfinance as yf
import numpy as np
from scipy.optimize import minimize
import matplotlib
matplotlib.use('Agg')  # Set non-GUI backend before importing pyplot
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import io
import base64

def get_optimal_allocations(tickers):
    data_atual = datetime.now()

    dia = data_atual.day
    mes = data_atual.month
    ano = data_atual.year

    inicio = dt.date(2004, 1, 1)
    final = dt.date(ano, mes, dia)

    df = yf.download(tickers, inicio, final)['Close']

    ret = df.pct_change().apply(lambda x: np.log(1+x)).dropna()
    media_retornos = ret.mean()
    matriz_cov = ret.cov()

    retornos_esperados, volatilidades_esperadas, tabela_sharpe, tabela_pesos = run_simulations(tickers, media_retornos, matriz_cov)

    i_sharpe_max = tabela_sharpe.argmax()
    alocacao_ideal = tabela_pesos[i_sharpe_max]

    portfolio = dict(zip(tickers, alocacao_ideal))

    plot = get_optimal_allocation_plot(tickers, retornos_esperados, volatilidades_esperadas, tabela_sharpe, i_sharpe_max, media_retornos, matriz_cov)
    image_base64 = convert_to_base64(plot)
    return portfolio, image_base64

def run_simulations(tickers, media_retornos, matriz_cov):
    N = 10000
    retornos_esperados = np.zeros(N)
    volatilidades_esperadas = np.zeros(N)
    tabela_sharpe = np.zeros(N)
    tabela_pesos = np.zeros((N,len(tickers)))

    for k in range(N):
        pesos = np.random.random(len(tickers))
        pesos = pesos/np.sum(pesos)
        tabela_pesos[k, :] = pesos

        retornos_esperados[k] = np.sum(media_retornos * pesos * 252)
        volatilidades_esperadas[k] = np.sqrt(np.dot(pesos.T, np.dot(matriz_cov*252, pesos)))
        tabela_sharpe[k] = retornos_esperados[k]/volatilidades_esperadas[k]
    
    return retornos_esperados, volatilidades_esperadas, tabela_sharpe, tabela_pesos

def get_optimal_allocation_plot(tickers, retornos_esperados, volatilidades_esperadas, tabela_sharpe, i_sharpe_max, media_retornos, matriz_cov):
    plt.style.use('dark_background')  # Use dark theme
    fig, ax = plt.subplots(figsize=(10, 6))  # Set figure size

    # Plot scatter points
    scatter = ax.scatter(volatilidades_esperadas, np.exp(retornos_esperados) - 1, 
                        c=tabela_sharpe, cmap='viridis', alpha=0.6)
    
    # Plot optimal point
    ax.scatter(volatilidades_esperadas[i_sharpe_max], 
              np.exp(retornos_esperados[i_sharpe_max]) - 1, 
              c='red', s=100, marker='*', label='Optimal Portfolio')

    # Calculate and plot efficient frontier
    retornos_esperados_arit = np.exp(retornos_esperados) - 1
    eixo_y_fronteira_eficiente = np.linspace(retornos_esperados_arit.min(), 
                                            retornos_esperados_arit.max(), 50)
    
    peso_inicial = [1/len(tickers)] * len(tickers)
    limites = tuple([(0,1) for _ in tickers])
    eixo_x_fronteira_eficiente = []

    for retorno_possivel in eixo_y_fronteira_eficiente:
        restricoes = (
            {'type': 'eq', 'fun': lambda w: np.sum(w) - 1},
            {'type': 'eq', 'fun': lambda w: (np.exp(np.sum(media_retornos * w) * 252) - 1) - retorno_possivel}
        )
        result = minimize(
            lambda w: np.sqrt(np.dot(w.T, np.dot(matriz_cov*252, w))),
            peso_inicial,
            method='SLSQP',
            bounds=limites,
            constraints=restricoes
        )
        eixo_x_fronteira_eficiente.append(result['fun'])

    # Plot efficient frontier
    ax.plot(eixo_x_fronteira_eficiente, eixo_y_fronteira_eficiente, 
            'w--', label='Efficient Frontier')

    # Customize plot
    ax.set_xlabel('Expected Volatility')
    ax.set_ylabel('Expected Return')
    ax.xaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    ax.grid(True, alpha=0.2)
    ax.legend()

    # Add colorbar
    plt.colorbar(scatter, label='Sharpe Ratio')

    plt.tight_layout()
    return plt

def convert_to_base64(plot):
    buf = io.BytesIO()
    plot.savefig(buf, format='png', facecolor='#1a1a1a', edgecolor='none')
    plt.close()  # Close the figure to free memory

    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()

    return image_base64