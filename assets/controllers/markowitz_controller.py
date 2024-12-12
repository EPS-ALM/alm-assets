from datetime import datetime
import datetime as dt
import yfinance as yf
import numpy as np
from scipy.optimize import minimize
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

    df = yf.download(tickers, inicio, final)['Adj Close']

    ret = df.pct_change().apply(lambda x: np.log(1+x)).dropna()
    media_retornos = ret.mean()
    matriz_cov = ret.cov()

    retornos_esperados, volatilidades_esperadas, tabela_sharpe, tabela_pesos = run_simulations(tickers, media_retornos, matriz_cov)

    i_sharpe_max = tabela_sharpe.argmax()
    alocacao_ideal = tabela_pesos[i_sharpe_max]

    portfolio = dict(zip(tickers, alocacao_ideal))

    plot = get_optimal_allocation_plot(tickers, retornos_esperados,  volatilidades_esperadas, tabela_sharpe, i_sharpe_max, media_retornos, matriz_cov)
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



def get_optimal_allocation_plot(tickers, retornos_esperados,  volatilidades_esperadas, tabela_sharpe, i_sharpe_max, media_retornos, matriz_cov):
    retornos_esperados_arit = np.exp(retornos_esperados) - 1
    eixo_y_fronteira_eficiente = np.linspace(retornos_esperados_arit.min(), retornos_esperados_arit.max(), 50)

    peso_inicial = [1/len(tickers)] * len(tickers)
    limites = tuple([(0,1) for ativo in tickers])

    eixo_x_fronteira_eficiente = []

    def get_retorno(peso_teste):
        peso_teste = np.array(peso_teste)
        retorno = np.sum(media_retornos * peso_teste) * 252
        retorno = np.exp(retorno) - 1

        return retorno

    def check_soma_pesos(peso_teste):
        return np.sum(peso_teste) -1

    def get_vol(peso_teste):
        peso_teste = np.array(peso_teste)
        vol = np.sqrt(np.dot(peso_teste.T, np.dot(matriz_cov*252, peso_teste)))

        return vol

    for retorno_possivel in eixo_y_fronteira_eficiente:
        restricoes = ({'type': 'eq', 'fun': check_soma_pesos}, {'type': 'eq', 'fun': lambda w: get_retorno(w) - retorno_possivel})

        result = minimize(get_vol, peso_inicial, method='SLSQP', bounds=limites, constraints=restricoes)

        eixo_x_fronteira_eficiente.append(result['fun'])
    
    fig, ax = plt.subplots()

    ax.scatter(volatilidades_esperadas, retornos_esperados_arit, c=tabela_sharpe)
    plt.xlabel("Volatilidade esperada")
    plt.ylabel("Restorno esperado")
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.scatter(volatilidades_esperadas[i_sharpe_max], retornos_esperados_arit[i_sharpe_max], c="red")
    ax.plot(eixo_x_fronteira_eficiente, eixo_y_fronteira_eficiente)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(1,0))
    ax.xaxis.set_major_formatter(mtick.PercentFormatter(1,0))
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')

    return plt

def convert_to_base64(plot):
    buf = io.BytesIO()
    plot.savefig(buf, format="png")
    plot.close()  

    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()

    return image_base64