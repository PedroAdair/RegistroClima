import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title= 'financialServices', page_icon= 'bar_chart:', layout='wide')
st.title(' :bar_chart: Portafiolios de inversion')
st.markdown('<style>div.block-container{padding-top:1rem}</style>',unsafe_allow_html=True)

fl = st.file_uploader(':file_folder: Upload a file', type= (['csv', 'txt', 'xlsl', 'xls']))

if fl is not None:
    filename = fl.name
    df = pd.read_csv(filename)
else:
    # os.chdir(r'')
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

if not companies_select:
    df3 =   df2['AAPL'] #AAple por default
else:
    df3 = df2[companies_select]
    # region_name = region[0]
    # patn_selct = f'data{region_name}.csv'
    # df2 = pd.read_csv(filepath_or_buffer=patn_selct)
# print(df3)