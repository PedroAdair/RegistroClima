import pandas as pd
import numpy as np
import datetime
import yfinance as yf

import yaml
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

def load_DB(path:str):
    'load a csv database'
    data = pd.read_csv(filepath_or_buffer=path)
    return data