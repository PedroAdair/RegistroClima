import pandas as pd
import numpy as np
import datetime
import yfinance as yf
from pypfopt.efficient_frontier import EfficientFrontier
import math

import yaml
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

def min_volatility(portfolio:list, max_len_portfolio:int, type_prize:str, period:str):
  """
  Obtain a portfolio with minimal volatility. Given a price type and a period

  
| Var               |type           | Description                     |example |
|-------------------|---------------|---------------------------------|--------|
| portfolio         |List of strings| List withs companies name key   |  ['AAPL',	'MSFT',	'AMZN',	'TSLA'] for Apple, Microsoft, Amazon and Tesla |
| max_len_portfolio | int           |   maximum length of a portfolio | 10 |
|type_prize         | str           | type or price fos companies     | 'Close' 'Open'	'High'	'Low'	'Close'|
|period             | str |         | history time interval           |    '5y' |
    """
  if len(portfolio) > max_len_portfolio:
    raise Exception (f'El número máximo de activos en el portafolio es de {max_len_portfolio}')
  else:
      stock_prices = pd.DataFrame()
      stock_returns = pd.DataFrame()

      for x in portfolio:
          stock = yf.Ticker(x)
          close_price = stock.history(period=period)[type_prize]

          # Se insertan datos en stock_prices y stock_returns
          stock_prices = pd.concat([stock_prices, close_price], axis=1)
          # Con pct_change() obtenemos los rendimientos (cambio porcentual)
          stock_returns = pd.concat([stock_returns, close_price.pct_change()], axis=1)

  # Asignamos nombre de acciones a las columnas de cada DataFrame

  stock_prices.columns = portfolio
  stock_returns.columns = portfolio

  # Eliminamos valores nulos de las columnas con dropna()
  # (El primer valor de rendimiento es nulo)

  stock_returns = stock_returns.dropna()

  # # Ver los datos generados:
  # print('Precios diarios, últimos 5 años (máximo)')
  # display(stock_prices)
  # print('Rendimientos diarios, últimos 5 años (máximo)')
  # display(stock_returns)

  # Rendimiento esperado de activos
  expected_stock_returns = []

  # Riesgo individual de activos
  individual_stock_risk = []

  for x, y in stock_returns.iteritems():
    # En cada iteración se obtiene el rendimiento esperado y riesgo individual
    # de cada activo (media y desviación estándar)
    expected_stock_returns.append(y.mean())
    individual_stock_risk.append(y.std())

  stock_returns_cov_matrix = np.array(stock_returns.cov())

  ### OPTIMIZACION DE MARKOWITZ ###
  ef = EfficientFrontier(expected_stock_returns, stock_returns_cov_matrix, weight_bounds=(0,1))
  ratios = ef.min_volatility()
  cleaned_ratios = pd.Series(ratios)
  cleaned_ratios.index = portfolio

  optimal_portfolio = np.expand_dims(cleaned_ratios, axis=0)

  # Rendimiento esperado
  opt_portfolio_expected_return = np.matmul(optimal_portfolio, expected_stock_returns)

  # Varianza del portafolio
  opt_portfolio_var = np.matmul(optimal_portfolio, \
                                np.matmul(stock_returns_cov_matrix, optimal_portfolio.transpose()))

  # Riesgo del portafolio
  opt_portfolio_risk = math.sqrt(opt_portfolio_var)

  # # Ver datos obtenidos y Portafolio Óptimo de Markowitz:
  # print('PORTAFOLIO ÓPTIMO DE MARKOWITZ:')
  # print(f'Rendimiento esperado: {opt_portfolio_expected_return*100}')
  # print(f'Varianza del portafolio: {opt_portfolio_var*100}')
  # print(f'Riesgo del portafolio: {opt_portfolio_risk*100}')

  # print('\n\nDel 100% de tu capital, el modelo sugiere\
  # invertir las siguientes proporciones en cada activo:')
  # print(cleaned_ratios*100)
  output  = {'Rendimiento': opt_portfolio_expected_return*100,
              'Varianza': opt_portfolio_var*100,
              'Riesgo':opt_portfolio_risk*100,
               'Proporciones': cleaned_ratios*100
              }
  return output