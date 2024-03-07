import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import os
import warnings
from portfolioSelection import *
warnings.filterwarnings('ignore')


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
        file_name = 'dataOpen.csv'
        table = createDataset(path=file_name, stocks=companies_select)
        fecha_minima = table.index.min()
        fecha_seleccionada = st.date_input("Selecciona una fecha posterior a " + str(fecha_minima), fecha_minima)
        fecha_seleccionada = pd.Timestamp(fecha_seleccionada)
        df3.index = pd.to_datetime(df3.index)
        if fecha_seleccionada:
            df3 = df3[df3.index >= fecha_seleccionada]
        startDate = fecha_seleccionada
        portfolio_info = display_simulated_ef_with_random(path=file_name,  stocks=companies_select,startDate=startDate, num_portfolios=n_samples, risk_free_rate=0.001)
    elif not region:
        df3 = pd.read_csv(filepath_or_buffer='dataOpen.csv')
        file_name = 'dataOpen.csv'
        table = createDataset(path=file_name, stocks=companies_select)
        fecha_minima = table.index.min()
        fecha_seleccionada = st.date_input("Selecciona una fecha posterior a " + str(fecha_minima), fecha_minima)
        fecha_seleccionada = pd.Timestamp(fecha_seleccionada)
        df3.index = pd.to_datetime(df3.index)
        if fecha_seleccionada:
            df3 = df3[df3.index >= fecha_seleccionada]
        startDate = fecha_seleccionada

        portfolio_info = display_simulated_ef_with_random(path=file_name,  stocks=companies_select,startDate=startDate, num_portfolios=n_samples, risk_free_rate=0.001)
    elif not companies_select:
        file_name = 'dataOpen.csv'
        df3 = pd.read_csv(filepath_or_buffer='dataOpen.csv', parse_dates=['Date'], dayfirst=True, index_col='Date')
        df3 = df3[['AAPL', 'MSFT', 'GOOGL']]

        companies_select = ['AAPL', 'MSFT', 'GOOGL']
        table = createDataset(path=file_name, stocks=companies_select)
        fecha_minima = table.index.min()
        fecha_seleccionada = st.date_input("Selecciona una fecha posterior a " + str(fecha_minima), fecha_minima)
        fecha_seleccionada = pd.Timestamp(fecha_seleccionada)
        df3.index = pd.to_datetime(df3.index)
        if fecha_seleccionada:
            df3 = df3[df3.index >= fecha_seleccionada]
        startDate = fecha_seleccionada
        portfolio_info = display_simulated_ef_with_random(path=file_name,  stocks=companies_select,startDate=startDate, num_portfolios=n_samples, risk_free_rate=0.001)
    else: 
        file_name = f'data{region}.csv'
        df = pd.read_csv(file_name, parse_dates=['Date'], dayfirst=True, index_col='Date')
        df3 = df[companies_select]
        df3 = df3.dropna()
        table = createDataset(path=file_name, stocks=companies_select)

        fecha_minima = table.index.min()
        fecha_seleccionada = st.date_input("Selecciona una fecha posterior a " + str(fecha_minima), fecha_minima)
        fecha_seleccionada = pd.Timestamp(fecha_seleccionada)
        df3.index = pd.to_datetime(df3.index)
        if fecha_seleccionada:
            df3 = df3[df3.index >= fecha_seleccionada]
        startDate = fecha_seleccionada
    
    st.write(df3.head())
    portfolio_info = display_simulated_ef_with_random(path=file_name,  stocks=companies_select,startDate=startDate, num_portfolios=n_samples, risk_free_rate=0.001)



    #Plot Timeserie action price for companies
    st.   subheader('Companies value')
    fig = px.line(df3.reset_index(), x=df3.index, y=df3.columns, labels={'value': 'Value', 'Date': 'Date'},
                title='Time Series Plot')
    st.plotly_chart(fig, use_container_width=True)

    df_port_samples = portfolio_info['PortafoliosAleatorios']

    st.subheader('Cambio porcentual')
    returns = df3.pct_change()
    fig = go.Figure()
    for column in returns.columns:
        fig.add_trace(go.Scatter(x=returns.index, y=returns[column], mode='lines', name=column))

    fig.update_layout(title='Serie de Tiempo',
                    xaxis_title='Fecha',
                    yaxis_title='Cambio %',
                    hovermode='x unified')
    st.plotly_chart(fig,  theme="streamlit", use_container_width=True)


    # plot Investment portfolio
    st.subheader('Investment portfolio')
    #markowitz portfolio
    max_sr_returns = portfolio_info['MarkowitzPortfolio']['retorno']
    max_sr_volatility = portfolio_info['MarkowitzPortfolio']['volatilidad']
    markowittz_portfolio = portfolio_info['MarkowitzPortfolio']['composicion']
    # PortafolioMinVolatilidad
    min_sr_returns = portfolio_info['PortafolioMinVolatilidad']['retorno']
    min_sr_volatility = portfolio_info['PortafolioMinVolatilidad']['volatilidad']
    PortafolioMinVolatilidad = portfolio_info['PortafolioMinVolatilidad']['composicion']

    fig = px.scatter(df_port_samples, 'Volatilidad', 'Retorno')
    fig.add_trace(go.Scatter(x=[max_sr_volatility], y=[max_sr_returns], mode='markers', marker=dict(color='red', size=11), name='Markowitz portfolio'))
    fig.add_trace(go.Scatter(x=[min_sr_volatility], y=[min_sr_returns], mode='markers', marker=dict(color='green', size=11), name='Portafolio Min Volatilidad'))

    st.plotly_chart(fig, theme="streamlit", use_container_width=True)


    st.subheader('Info')
    col1, col2 = st.columns((2))
    with col2:
        with st.expander('investment percentage:'):
            df_port_samples = portfolio_info['PortafoliosAleatorios']
            # df_investment_percentage = pd.DataFrame(portfolio_invertion, columns=['Companies', 'investment percentage'])
            st.write(df_port_samples)
            # csv = df_investment_percentage.to_csv()
            # st.download_button('Download Data', data= csv, file_name='investment_percentage.csv', mime='text/csv', help='Click here to download the data as a CSV file')
        with col1:
            df_inversion = pd.concat([markowittz_portfolio, PortafolioMinVolatilidad], keys=['markowittz_portfolio', 'PortafolioMinVolatilidad'])
            with st.expander('Results:'):
                st.write(df_inversion)
                csv = df_inversion.to_csv()
                st.download_button('Download Data', data= csv, file_name='Results.csv', mime='text/csv', help='Click here to download the data as a CSV file')