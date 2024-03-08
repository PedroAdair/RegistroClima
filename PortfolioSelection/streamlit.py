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
        col1, col2 = st.columns((2))
        with col1:
            fecha_seleccionada = st.date_input("Selecciona una fecha posterior a " + str(fecha_minima), fecha_minima)
            fecha_seleccionada = pd.Timestamp(fecha_seleccionada)
            df3.index = pd.to_datetime(df3.index)
            if fecha_seleccionada:
                df3 = df3[df3.index >= fecha_seleccionada]
            startDate = fecha_seleccionada
        with col2:
            st.write(df3.head())
        portfolio_info = display_simulated_ef_with_random(path=file_name,  stocks=companies_select,startDate=startDate, num_portfolios=n_samples, risk_free_rate=0.001)
    elif not region:
        df3 = pd.read_csv(filepath_or_buffer='dataOpen.csv')
        file_name = 'dataOpen.csv'
        table = createDataset(path=file_name, stocks=companies_select)
        fecha_minima = table.index.min()
        col1, col2 = st.columns((2))
        with col1:
            fecha_seleccionada = st.date_input("Selecciona una fecha posterior a " + str(fecha_minima), fecha_minima)
            fecha_seleccionada = pd.Timestamp(fecha_seleccionada)
            df3.index = pd.to_datetime(df3.index)
            if fecha_seleccionada:
                df3 = df3[df3.index >= fecha_seleccionada]
            startDate = fecha_seleccionada
        with col2:
            st.write(df3.head())

        portfolio_info = display_simulated_ef_with_random(path=file_name,  stocks=companies_select,startDate=startDate, num_portfolios=n_samples, risk_free_rate=0.001)
    elif not companies_select:
        file_name = 'dataOpen.csv'
        df3 = pd.read_csv(filepath_or_buffer='dataOpen.csv', parse_dates=['Date'], dayfirst=True, index_col='Date')
        df3 = df3[['AAPL', 'MSFT', 'GOOGL']]

        companies_select = ['AAPL', 'MSFT', 'GOOGL']
        table = createDataset(path=file_name, stocks=companies_select)
        fecha_minima = table.index.min()
        col1, col2 = st.columns((2))
        with col1:
            fecha_seleccionada = st.date_input("Selecciona una fecha posterior a " + str(fecha_minima), fecha_minima)
            fecha_seleccionada = pd.Timestamp(fecha_seleccionada)
            df3.index = pd.to_datetime(df3.index)
            if fecha_seleccionada:
                df3 = df3[df3.index >= fecha_seleccionada]
            startDate = fecha_seleccionada
        with col2:
            st.write(df3.head())
        portfolio_info = display_simulated_ef_with_random(path=file_name,  stocks=companies_select,startDate=startDate, num_portfolios=n_samples, risk_free_rate=0.001)
    else: 
        file_name = f'data{region}.csv'
        df = pd.read_csv(file_name, parse_dates=['Date'], dayfirst=True, index_col='Date')
        df3 = df[companies_select]
        df3 = df3.dropna()
        table = createDataset(path=file_name, stocks=companies_select)

        fecha_minima = table.index.min()
        col1, col2 = st.columns((2))
        with col1:
            fecha_seleccionada = st.date_input("Selecciona una fecha posterior a " + str(fecha_minima), fecha_minima)
            fecha_seleccionada = pd.Timestamp(fecha_seleccionada)
            df3.index = pd.to_datetime(df3.index)
            if fecha_seleccionada:
                df3 = df3[df3.index >= fecha_seleccionada]
            startDate = fecha_seleccionada
        with col2:
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

    col1, col2 = st.columns((2))
    with col2:
        with st.expander('investment percentage:'):
            df_port_samples = portfolio_info['PortafoliosAleatorios']
            # df_investment_percentage = pd.DataFrame(portfolio_invertion, columns=['Companies', 'investment percentage'])
            # st.write(df_port_samples)
            # st.dataframe()
            columna_orden = st.selectbox("Seleccione la columna para ordenar", df_port_samples.columns)
            
            df_ordenado = df_port_samples.sort_values(by=columna_orden)
            columnas_a_multiplicar = df_ordenado.columns[3:]
            df_ordenado = df_ordenado[columnas_a_multiplicar] * 100
            columnas_a_incorporar = df_port_samples.columns[:3]
            df_ordenado[columnas_a_incorporar] = df_port_samples[columnas_a_incorporar]
            # Mostrar el DataFrame ordenado
            st.dataframe(df_ordenado, height=300)
            # csv = df_investment_percentage.to_csv()
            # st.download_button('Download Data', data= csv, file_name='investment_percentage.csv', mime='text/csv', help='Click here to download the data as a CSV file')
    with col1:
        df_inversion = pd.concat([markowittz_portfolio, PortafolioMinVolatilidad], keys=['markowittz_portfolio', 'PortafolioMinVolatilidad'])
        with st.expander('Results:'):
            st.write(df_inversion)
            csv = df_inversion.to_csv()
            st.download_button('Download Data', data= csv, file_name='Results.csv', mime='text/csv', help='Click here to download the data as a CSV file')

  
    st.subheader("Detalles de la Compra")
    col1, col2, col3= st.columns((3))
    with col1:
        nombre_comprador = st.text_input("Nombre del Comprador")
    with col2:
        ApellidoMat = st.text_input("Apellido Materno")
    with col3:
        ApellidoPat = st.text_input("Apellido Paterno")

    col1, col2, col3= st.columns((3))
    with col1:
        moneda = st.selectbox("Seleccione la Moneda", ["Dólares", "Pesos", "Libras"])
    with col2:
        total_inversion = st.number_input("Total de inversion", step=1)
    with col3:
        portafolio = st.selectbox("Seleccione el portafolio", ["Markowitz", "Min Volatilidad", "Personalizado"])
        if portafolio == "Personalizado":
            
            valor = 1 / len(companies_select)*100
            lista = [valor for _ in range(len(companies_select))]

            df_personal = pd.DataFrame(lista,index=companies_select, columns=['Porcentaje'] )
            df_editable  = st.data_editor(df_personal)
            suma_porcentajes = df_personal['Porcentaje'].sum()

            if st.button('Verificar suma de porcentajes'):
                df_modificado = df_editable
                if np.abs(suma_porcentajes - 100)<0.001:
                    st.success('La suma de los porcentajes es igual a 100%.')
                    df_personal['Inversión'] = df_modificado['Porcentaje'] / 100 * total_inversion
                    st.write(df_personal)
                else:
                    st.error('La suma debe de dar 100%')
        elif portafolio == "Markowitz":
            df_personal = markowittz_portfolio
            st.write(df_personal)
        elif portafolio == "Min Volatilidad":
            df_personal = PortafolioMinVolatilidad
            st.write(df_personal)

    if st.button("Efectuar"):
        if portafolio  in["Markowitz","Min Volatilidad"]:
            weights =df_personal.loc['allocation'].values
        elif portafolio == "Personalizado":
            # weights =df_personal.loc['Porcentaje'].values
            weights = np.array(df_personal.iloc[:, 0].tolist())

        portfolio_std_dev, portfolio_return  = PortafolioPersonal(stocks=companies_select, weights=weights,table=df3, startDate=startDate)  
        st.write(portfolio_std_dev, portfolio_return )