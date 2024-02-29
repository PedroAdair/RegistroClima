import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import os
import warnings
from func import *
warnings.filterwarnings('ignore')

st.set_page_config(page_title= 'financialServices', page_icon= 'bar_chart:', layout='wide')
st.title(' :bar_chart: Portafiolios de inversion')
st.markdown('<style>div.block-container{padding-top:1rem}</style>',unsafe_allow_html=True)

# fl = st.file_uploader(':file_folder: Upload a file', type= (['csv', 'txt', 'xlsl', 'xls']))

# if fl is not None:
#     filename = fl.name
#     df = pd.read_csv(filename)
# else:
#     # os.chdir(r'')
#     df = pd.read_csv('dataAdjClose.csv')

df = pd.read_csv('dataAdjClose.csv')
col1, col2 = st.columns((2))
df['Date'] = pd.to_datetime(df['Date'])
#get min and max date 

startDate =  pd.to_datetime(df['Date']).min()
endDate =  pd.to_datetime(df['Date']).max()

with col1:
    date1 = pd.to_datetime(st.date_input('Start date', startDate))

with col2:
    date2 = pd.to_datetime(st.date_input('End date', endDate))          

df = df[(df['Date'] >= date1) & (df['Date']<= date1)].copy()

#select filter for price
data = [['Open'], ['Close'], ['AdjClose']]
df_price = pd.DataFrame(data, columns=['Price option'])


st.sidebar.header('Choose your filter')
region = st.sidebar.multiselect('Pick your price option', df_price['Price option'].unique())
if not region:
    df2 =   pd.read_csv(filepath_or_buffer='dataAdjClose.csv')
else:
    region_name = region[0]
    patn_selct = f'data{region_name}.csv'
    df2 = pd.read_csv(filepath_or_buffer=patn_selct)

#select filter for enterprise
columns = df2.columns
companies = list(columns)[1:]
df_companies = pd.DataFrame(companies, columns=['companies'])
companies_select = st.sidebar.multiselect('Pick the companies', df_companies['companies'])

#filter the data for companie
if not companies_select:
    companies_select = ['APPL']
    df3 =   df2[['Date','AAPL']] #Apple por default
    df3.set_index('Date', inplace=True)
    df3 = df3.dropna()
else:
    df_index_list = companies_select.insert(0, 'Date')
    df3 = df2[companies_select]
    df3['Date'] = pd.to_datetime(df2['Date'])
    df3.set_index('Date', inplace=True)
    df3 = df3.dropna()


################################################################
################################################################
################################################################


st.subheader('Companies value')
fig = px.line(df3.reset_index(), x='Date', y=df3.columns, labels={'value': 'Value', 'Date': 'Date'},
            title='Time Series Plot - All Columns')
st.plotly_chart(fig, use_container_width=True)


st.subheader('Investment portfolio')

asssets = [item for item in companies_select if item != 'Date']

ideal_portfolio, port_samples, portfolio_invertion =OptimalPortafolio(df=df3, asssets=asssets, n_samples=100)

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


#################################33

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