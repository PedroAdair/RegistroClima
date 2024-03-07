import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns



def load_DB(path:str):
    'load a csv database'
    data = pd.read_csv(filepath_or_buffer=path)
    return data

def createDataset(path:str, stocks:list):
    df_complete = load_DB(path=path)  
    df_complete['Date'] = pd.to_datetime(df_complete['Date']) #change str to datetime Date column
    df_complete= df_complete.set_index('Date') # return the date column as index
    filter_df   = df_complete[stocks] # filter about assets list 
    table =  filter_df.dropna() #drop NA records
    return table

def table_retusns_cov(table):
    returns = table.pct_change()
    mean_returns = returns.mean()
    cov_matrix = returns.cov()
    return returns, mean_returns, cov_matrix

def portfolio_annualised_performance(weights, mean_returns, cov_matrix):
    returns = np.sum(mean_returns*weights)*252  #252 dias habiles en la bolsa
    std = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))) * np.sqrt(252)
    return std, returns

def random_portfolios(n_companies:int, num_portfolios:int, mean_returns, cov_matrix, risk_free_rate):
    results = np.zeros((3,num_portfolios))
    weights_record = []
    for i in range(num_portfolios):
        weights = np.random.random(n_companies)
        weights /= np.sum(weights)
        weights_record.append(weights)

        portfolio_std_dev, portfolio_return = portfolio_annualised_performance(weights=weights, mean_returns=mean_returns,cov_matrix=cov_matrix)
        results[0,i] = portfolio_std_dev
        results[1,i] = portfolio_return
        results[2,i] = (portfolio_return-risk_free_rate) / portfolio_std_dev
    
    return results, weights_record

def display_simulated_ef_with_random(path:str, stocks:list,startDate,  num_portfolios, risk_free_rate):
    table = createDataset(path=path, stocks=stocks)
    table = table[table.index >= startDate]
    n_companies = len(stocks)
    returns, mean_returns, cov_matrix = table_retusns_cov(table)
    results, weights = random_portfolios(n_companies=n_companies, num_portfolios=num_portfolios, mean_returns=mean_returns, cov_matrix=cov_matrix, risk_free_rate=risk_free_rate)

    max_sharpe_idx = np.argmax(results[2])
    sdp, rp = results[0, max_sharpe_idx], results[1, max_sharpe_idx]
    max_sharpe_allocation = pd.DataFrame(weights[max_sharpe_idx], index=table.columns, columns=['allocation'])
    max_sharpe_allocation.allocation = [round(i*100,2) for i in max_sharpe_allocation.allocation]
    max_sharpe_allocation = max_sharpe_allocation.T

    min_sharpe_idx = np.argmin(results[0])
    sdp_min, rp_min = results[0, min_sharpe_idx], results[1, min_sharpe_idx]
    min_vol_allocation = pd.DataFrame(weights[min_sharpe_idx], index=table.columns, columns=['allocation'])
    min_vol_allocation.allocation = [round(i*100,2) for i in min_vol_allocation.allocation]
    min_vol_allocation = min_vol_allocation.T

    df2 = pd.DataFrame(weights, columns=stocks)

    df1 = pd.DataFrame(results.T, columns=['Volatilidad', 'Retorno', 'Riesgo'])
    df = pd.concat([df1, df2], axis=1)
    output = {
        'MarkowitzPortfolio':{
            'retorno': round(rp,2),
            'volatilidad': round(sdp,2),
            'composicion':pd.DataFrame(max_sharpe_allocation)
        },
        'PortafolioMinVolatilidad':{
            'retorno': round(rp_min,2),
            'volatilidad': round(sdp_min,2),
            'composicion':pd.DataFrame(min_vol_allocation)
        },
        'PortafoliosAleatorios': df
    }
    # print('-'*40)
    # print('max sharpe ratio portfolio allocation\n')
    # print('anual return', round(rp,2))
    # print('anual volatilidad', round(sdp,2))
    # print('\n')
    # print(max_sharpe_allocation)
    # print('-'*40)
    # print('min volatility portfolio allocation\n')
    # print('anual return', round(rp_min,2))
    # print('anual volatilidad', round(sdp_min,2))
    # print('\n')

    # plt.figure(figsize=(10,7))
    # plt.scatter(results[0,:], results[1,:], cmap='YlGnBu', marker='o', s=10, alpha=0.3)
    # plt.colorbar()
    # plt.scatter(sdp,rp, marker='*', color='r', s=500, label='Max sharpe ratio')
    # plt.scatter(sdp_min,rp_min, marker='*', color='g', s=500, label='min volatility')
    # plt.title('Simulacion de portafolio optimo   basado en la frontera efficeinte')
    # plt.xlabel('volatilidad anual')
    # plt.ylabel('retorno anualizado')
    # plt.legend(labelspacing=0.8)
    # plt.savefig('markor-portfolio')

    return output


# path = '/home/PedroSci/Documents/RegistroClima/PortfolioSelection/dataAdjClose.csv'
# stocks = ['KO',	'NFLX',	'TSLA', 'AMZN']
# num_portfolios = 500
# risk_free_rate = 0.0178

# a = display_simulated_ef_with_random(path=path, stocks=stocks,  num_portfolios=num_portfolios, risk_free_rate=risk_free_rate)
# b = a['PortafolioMinVolatilidad']['composicion']

# print(b[['KO']])
