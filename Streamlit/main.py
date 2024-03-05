# app.py
import streamlit as st
import pandas as pd
import numpy as np
import datetime
import yfinance as yf
import scipy.optimize as optimize
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go


from func import *
from func2 import *

st.set_page_config(page_title= 'financialServices', page_icon= 'bar_chart:', layout='wide')
st.title(' :bar_chart: Financial Services')
st.markdown('<style>div.block-container{padding-top:1rem}</style>',unsafe_allow_html=True)
tabs = st.tabs([
    'Seleción de portafolio', 'Predicciones', '... ', '...'
])

with tabs[0]:
    df = pd.read_csv('dataAdjClose.csv')
    #select filter for price
    data = [['Open'], ['Close'], ['AdjClose']]
    df_price = pd.DataFrame(data, columns=['Price option'])

    st.sidebar.header('Choose your filter')
    region = st.sidebar.selectbox('Pick your price option', df_price['Price option'].unique())

    #select filter for enterprise
    columns = df.columns
    companies = list(columns)[1:]
    df_companies = pd.DataFrame(companies, columns=['companies'])
    companies_select = st.sidebar.multiselect('Pick the companies', df_companies['companies']) #only one option
    n_samples = st.slider("Número de Simulaciones:", min_value=10, max_value=1000, value=100) #n_samples for companies election
    
    if not region and not companies_select:
        df3 = pd.read_csv(filepath_or_buffer='dataOpen.csv')
        companies_select = ['AAPL', 'MSFT', 'GOOGL']
    elif not region:
        df3 = pd.read_csv(filepath_or_buffer='dataOpen.csv')
    elif not companies_select:
        df3 = pd.read_csv(filepath_or_buffer='dataOpen.csv', parse_dates=['Date'], dayfirst=True, index_col='Date')
        df3 = df3[['AAPL', 'MSFT', 'GOOGL']]
        companies_select = ['AAPL', 'MSFT', 'GOOGL']
    else: 
        file_name = f'data{region}.csv'
        df = pd.read_csv(file_name, parse_dates=['Date'], dayfirst=True, index_col='Date')
        df3 = df[companies_select]
        df3 = df3.dropna()
    ##########################################################
    #Plot Timeserie action price for companies
    st.   subheader('Companies value')
    fig = px.line(df3.reset_index(), x='Date', y=df3.columns, labels={'value': 'Value', 'Date': 'Date'},
                title='Time Series Plot - All Columns')
    st.plotly_chart(fig, use_container_width=True)

    ##########################################################
    # plot Investment portfolio
    st.subheader('Investment portfolio')

    asssets = [item for item in companies_select if item != 'Date']

    ideal_portfolio, port_samples, portfolio_invertion =OptimalPortafolio(df=df3, asssets=asssets, n_samples=n_samples)

    df_port_samples = pd.DataFrame(port_samples)

    port_returns =  port_samples['port_returns']
    port_volts = port_samples['port_volts']
    sharpe = port_returns / port_volts

    # Find the maximum Sharpe ratio
    max_sr_returns = port_returns[sharpe.argmax()]
    max_sr_volatility = port_volts[sharpe.argmax()]

    fig = px.scatter(df_port_samples, x='port_volts', y='port_returns')
    fig.add_trace(go.Scatter(x=[max_sr_volatility], y=[max_sr_returns], mode='markers', marker=dict(color='red', size=11), name='Max Sharpe Ratio'))
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)

    ##########################################################
    st.subheader('Info')
    col1, col2 = st.columns((2))

    with col1:
        df_ideal_portfolio = pd.DataFrame(list(ideal_portfolio.items()), columns=['Description', 'Value'])
        with st.expander('Results:'):
            st.write(df_ideal_portfolio)
            csv = df_ideal_portfolio.to_csv()
            st.download_button('Download Data', data= csv, file_name='Results.csv', mime='text/csv', help='Click here to download the data as a CSV file')

    # print(portfolio_invertion)
            
    with col2:
        with st.expander('investment percentage:'):
            df_investment_percentage = pd.DataFrame(portfolio_invertion, columns=['Companies', 'investment percentage'])
            st.write(df_investment_percentage)
            csv = df_investment_percentage.to_csv()
            st.download_button('Download Data', data= csv, file_name='investment_percentage.csv', mime='text/csv', help='Click here to download the data as a CSV file')


    

# # ----- Proporcion ----- #
# with tabs[1]:
#     cols = st.columns([0.05, 0.4, 0.5, 0.05])
#     with cols[1]:
#         # Filtrar mes
#         meses = {
#             'Abril':4,
#             'Mayo':5,
#             'Junio':6
#         }
#         mes = st.selectbox(
#             'Elegir mes',
#             ('Abril', 'Mayo', 'Junio'),
#             key=3
#         )

#         mes_num = meses.get(mes)
#         # Filtrar tienda
#         tienda = st.selectbox(
#         )