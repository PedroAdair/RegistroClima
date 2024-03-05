import pandas as pd
import numpy as np
import datetime
import yfinance as yf
import yaml
import scipy.optimize as optimize
import matplotlib.pyplot as plt
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

def get_data(ticker:str,price:str):
    """
    Obtener los precios historicos  de una accion
    |Var   |type| Example|
    |-----|-----|--------| 
    |ticker|str | 'NVDA',  'MSFT', 'AMZN', 'AAPL'|
    |price |str | ['Open'	'High'	'Low	Close'	'Adj Close']|

    A continuacion se describen las opciones sobre el precio de las acciones

    * Open: El precio de apertura de las acciones en ese día.
    * High: El precio más alto alcanzado por las acciones durante el día.
    * Low: El precio más bajo alcanzado por las acciones durante el día.
    * Close: El precio de cierre de las acciones en ese día.
    * Adj Close: El precio de cierre ajustado, que tiene en cuenta eventos como dividendos, divisiones de acciones, etc. Es considerado como el precio real de cierre.

    La salida consiste en un DataFrame que nos sera util para formar una base de datos sobre los precios historicos.
    """
    data = yf.download(ticker)[price]
    return data

def get_DB(tickers:list, price:str, save=False):
    """From config file in the argument 'Empresas', return historical data from action price, if save= True, save as cvs file.
    * Open: El precio de apertura de las acciones en ese día.
    * High: El precio más alto alcanzado por las acciones durante el día.
    * Low: El precio más bajo alcanzado por las acciones durante el día.
    * Close: El precio de cierre de las acciones en ese día.
    * Adj Close: El precio de cierre ajustado, que tiene en cuenta eventos como dividendos, divisiones de acciones, etc. Es considerado como el precio real de cierre."""
    data =  pd.DataFrame()
    for ticker in tickers:
        print(ticker)
        data[ticker] = get_data(ticker=ticker, price=price)
    if save:
        print(f'Archivo guardado: data{price.replace(" ", "")}.csv')
        data.to_csv(f'data{price.replace(" ", "")}.csv')
    return data

# data = get_DB(tickers=config['Empresas'], price=config['price'],save=True)

def load_DB(path:str):
    'load a csv database'
    data = pd.read_csv(filepath_or_buffer=path)
    return data

def FilterPortfolio(n_samples:int, data:pd.DataFrame, asssets:list):
    """
    Input: list of asserts, 

    return: port_returns and port volatility
    """
    df =data[asssets]
    df1 = df.copy()
    data = df1.dropna()

    log_returns = np.log(1+data.pct_change())

    port_returns = []
    port_volts = []


    for i in range(n_samples):
        num_assets = len(asssets)
        weigths = np.random.random(num_assets)
        weigths /= np.sum(weigths)
        print(weigths, np.sum(weigths))
        port_returns.append(np.sum(weigths*log_returns.mean())*252)
        port_volts.append(np.sqrt(np.dot(weigths.T, np.dot(log_returns.cov()*252, weigths))))

    port_returns = np.array(port_returns)
    port_volts = np.array(port_volts)

    return log_returns, port_returns, port_volts

def portfolio_stats(weigths, log_returns):
    port_returns = np.sum(weigths*log_returns.mean())*252 #covariance
    port_volts   = np.sqrt(np.dot(weigths.T, np.dot(log_returns.cov()*252, weigths))) #252 por la media anualizada

    sharpe =  port_returns/port_volts
    return {'Return': port_returns, 'Volatility': port_volts, 'Sharpe': sharpe}


def minimize_sharpe(weigths, log_returns):
    return - portfolio_stats(weigths=weigths, log_returns=log_returns)['Sharpe']

def OptimalPortafolioComplete(path:str, asssets:list, n_samples:int):

    #load db
    df = load_DB(path=path)
    #filter 
    log_returns, port_returns, port_volts = FilterPortfolio(n_samples=n_samples, data=df, asssets=asssets)
    num_assets = len(asssets)


    initializer = num_assets*[1./num_assets,]
    bounds = tuple((0,1) for x in range(num_assets))
    optimar_sharpe = optimize.minimize(minimize_sharpe, initializer, method='SLSQP', args=(log_returns,), bounds=bounds)
    optimar_sharpe_weights = optimar_sharpe['x'].round(3)


    print(f'Los pesos optimos en la cartera son: {list(zip(asssets, list(optimar_sharpe_weights*100)))}')
    print(np.sum(optimar_sharpe_weights))
    optimal_stats  = portfolio_stats(optimar_sharpe_weights, log_returns=log_returns)
    optimal_return = np.round(optimal_stats['Return']*100,3)
    
    optimal_volatility = np.round(optimal_stats['Volatility']*100,3)
    optimal_sharpe = np.round(optimal_stats['Sharpe'],3)
    ideal_portfolio = {'optimal_return': optimal_return,
                       'optimal_volatility':optimal_volatility,
                       'optimal_sharpe': optimal_sharpe}
    port_samples = {'port_volts': port_volts,
                    'port_returns': port_returns}
    #plot 
    sharpe = port_returns/port_volts
    max_sr_returns = port_returns[sharpe.argmax()]
    max_sr_volatility = port_volts[sharpe.argmax()]
    plt.figure(figsize=(12,6))
    plt.scatter(port_volts, port_returns, c= (port_returns/port_volts))
    plt.scatter(max_sr_volatility,max_sr_returns, c= 'red', s=30)
    plt.colorbar(label = 'Sharpe Ratio, rf=0')
    plt.xlabel('Volatilidad de la cartera')
    plt.ylabel('Retorno de la cartera')
    plt.savefig('foo.png')

    return ideal_portfolio, port_samples

def OptimalPortafolio(df:pd.DataFrame, asssets:list, n_samples:int):

    #filter 
    log_returns, port_returns, port_volts = FilterPortfolio(n_samples=n_samples, data=df, asssets=asssets)
    num_assets = len(asssets)


    constraints = ({'type' : 'eq', 'fun': lambda x: np.sum(x) -1})
    bounds = tuple((0,1) for x in range(num_assets))
    initializer = num_assets * [1./num_assets,]
    optimar_sharpe = optimize.minimize(minimize_sharpe, 
                                       initializer, 
                                       method='L-BFGS-B', 
                                       args=(log_returns,), 
                                       bounds=bounds, 
                                       constraints=constraints)
    
    optimar_sharpe_weights = optimar_sharpe['x'].round(4)


    print(f'Los pesos optimos en la cartera son: {list(zip(asssets, list(optimar_sharpe_weights*100)))}')
    print(np.sum(optimar_sharpe_weights))

    optimal_stats  = portfolio_stats(optimar_sharpe_weights, log_returns=log_returns)
    optimal_return = np.round(optimal_stats['Return']*100,3)
    
    optimal_volatility = np.round(optimal_stats['Volatility']*100,3)
    optimal_sharpe = np.round(optimal_stats['Sharpe'],3)
    ideal_portfolio = {'optimal_return': optimal_return,
                       'optimal_volatility':optimal_volatility,
                       'optimal_sharpe': optimal_sharpe}
    port_samples = {'port_volts': port_volts,
                    'port_returns': port_returns}
    portfolio_invertion = list(zip(asssets, list(optimar_sharpe_weights*100)))
    #plot 
    # sharpe = port_returns/port_volts
    # max_sr_returns = port_returns[sharpe.argmax()]
    # max_sr_volatility = port_volts[sharpe.argmax()]
    # plt.figure(figsize=(12,6))
    # plt.scatter(port_volts, port_returns, c= (port_returns/port_volts))
    # plt.scatter(max_sr_volatility,max_sr_returns, c= 'red', s=30)
    # plt.colorbar(label = 'Sharpe Ratio, rf=0')
    # plt.xlabel('Volatilidad de la cartera')
    # plt.ylabel('Retorno de la cartera')
    # plt.savefig('foo.png')

    return ideal_portfolio, port_samples, portfolio_invertion

# df2 =   pd.read_csv(filepath_or_buffer='dataAdjClose.csv')
# df3 =   df2[['Date','AAPL']] #Apple por default
# df3.set_index('Date', inplace=True)
# df3 = df3.dropna()
# print(df3)

# a,b = OptimalPortafolio(path='dataAdjClose.csv', asssets=['AAPL', 'XOM','MSFT', 'AMZN'],n_samples=100)
# get_DB(tickers=config['Empresas'], price='Open',save=True)
# print(a,b)