#data science
from sklearn import metrics
#data manitulation
import numpy as np
import pandas as pd
from datetime import datetime #date manipulation
#time serie ARIMA, SARIMA and SARIMAX
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller
# time series Auto-Arima
from pmdarima import auto_arima

#data visualization
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
# import hvplot.pandas
from statsmodels.graphics.tsaplots import plot_pacf, plot_acf
import plotly.express as px
import plotly.graph_objects as go



def eval_model(y_true, y_pred):
    print("Evaluacion de modelo:-")
    print(f"MSE: {metrics.mean_squared_error(y_true=y_true, y_pred=y_pred)}")
    print(f"RMSE: {np.sqrt(metrics.mean_squared_error(y_true=y_true, y_pred=y_pred))}")
    print(f"MAPE: {metrics.mean_absolute_percentage_error(y_true=y_true, y_pred=y_pred)}")
    print(f"R2: {metrics.r2_score(y_true=y_true, y_pred=y_pred)}")
    print(f"MAE: {metrics.mean_absolute_error(y_true=y_true, y_pred=y_pred)}")

df = pd.read_csv('/home/PedroSci/Documents/RegistroClima/Streamlit/dataAdjClose.csv')
df['Date'] = pd.to_datetime(df['Date'])
df = df.set_index("Date")
# print(df.info())
# print(df)


df = df[['AAPL']]
df = df.dropna()
def Augmented_Dickeyy_Fuller_Test_funf(series, col_name):
    print(f"Resultaados del test de Duckey Fuller para la columna {col_name}")
    dftest = adfuller(series, autolag='AIC')
    dfoutput = pd.Series(dftest[0:4], index=['Test Stadistic', 'p-value', 'N° LAgs Used', 'N° observaciones utilizadas'])
    for key, value in dftest[4].items():
        dfoutput['Critical Value (%s)'%key] = value
    print(dfoutput)
    if dftest[1]<=0.05: #p-valor del 5%
        print('Conclusion:======>')
        print('Rechazar la hipotesis nula')
        print('Los datos son estacionarios')
    else:
        print('Conclusion:======>')
        print('No se puede rechazar la hipotesis nula')
        print('Los datos no son estacionarios')


# Augmented_Dickeyy_Fuller_Test_funf(df['AAPL'],'AAPL')

# train_data= df[:len(df)-16]
# test_data = df[len(df)-16:]
# test = test_data.copy()
# train_data.shape, test_data.shape
# modelo_auto= auto_arima(train_data, start_p=0,start_q=0, max_p=4, max_d=2, max_q=4, start_P=0,
#                     D=1,start_Q=0, max_P=2, max_D=1,
#                     max_Q=2,m=12,seasonal=True,
#                     error_action ='warn', trace=True,
#                     suppress_warnings=True,stepwise=True,
#                     random_state=20,n_fits=50
#                     )
# # print(modelo_auto)

# # print(modelo_auto.summary())

# # pred = modelo_auto.predict(start = len(train_data), end= len(df)-1, typ='levels')
# arima_model = SARIMAX(train_data['AAPL'], order=(2, 1, 0), seasonal_order=(2, 1, 0, 12)).fit()
# residuals =pd.DataFrame(arima_model.resid)
# residuals.plot(figsize=(16,5))
# plt.show()
# plt.savefig('appl predictionEE')

# modelo_auto.plot_diagnostics(figsize=(20,8))
# plt.show()
# plt.savefig('appl residuales')
