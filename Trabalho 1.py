import numpy as np
import yahoo_fin
from ipywidgets import interact
from yahoo_fin.stock_info import get_data
from scipy.optimize import minimize
from pandas_datareader import data as pdr
import pandas as pd
import matplotlib.pyplot as plt

selic = pd.read_csv("taxa_selic_apurada.csv", sep = ';')
ticker_list = ["bbas3.sa", "tasa4.sa", "taee3.sa", "itsa4.sa"]
historical_datas = {}
for ticker in ticker_list:
    historical_datas[ticker] = get_data(ticker, start_date="01/01/2018", end_date="01/01/2023", index_as_date= True, interval="1d")

bbas3 = (historical_datas.get("bbas3.sa"))
bbas3 = bbas3.reset_index()
bbas3 = bbas3.rename(columns={'index': 'data'})

itsa4 = (historical_datas.get("itsa4.sa"))
itsa4 = itsa4.reset_index()
itsa4 = itsa4.rename(columns={'index': 'data'})

tasa4 = (historical_datas.get("tasa4.sa"))
tasa4 = tasa4.reset_index()
tasa4 = tasa4.rename(columns={'index': 'data'})

taee3 = (historical_datas.get("taee3.sa"))
taee3 = taee3.reset_index()
taee3 = taee3.rename(columns={'index': 'data'})

selic = selic.get(['data','Taxa (% a.d)'])

    
#Calculo do retorno

df_bbas3 = bbas3.drop(['open','adjclose', 'high', 'low','volume', 'ticker'], axis = 1)
df_bbas3_t = df_bbas3.set_index('data')
df_bbas3_t1 = df_bbas3_t.shift(1)
df_bbas3_return = (df_bbas3_t - df_bbas3_t1)/df_bbas3_t
df_bbas3_return = df_bbas3_return.reset_index()
df_bbas3_return = df_bbas3_return.rename(columns={'index': 'data'})

df_itsa4 = itsa4.drop(['open','adjclose', 'high', 'low','volume', 'ticker'], axis = 1)
df_itsa4_t = df_itsa4.set_index('data')
df_itsa4_t1 = df_itsa4_t.shift(1)
df_itsa4_return = (df_itsa4_t - df_itsa4_t1)/df_itsa4_t
df_itsa4_return = df_itsa4_return.reset_index()
df_itsa4_return = df_itsa4_return.rename(columns={'index': 'data'})

df_tasa4 = tasa4.drop(['open','adjclose', 'high', 'low','volume', 'ticker'], axis = 1)
df_tasa4_t = df_tasa4.set_index('data')
df_tasa4_t1 = df_tasa4_t.shift(1)
df_tasa4_return = (df_tasa4_t - df_tasa4_t1)/df_tasa4_t
df_tasa4_return = df_tasa4_return.reset_index()
df_tasa4_return = df_tasa4_return.rename(columns={'index': 'data'})

df_taee3 = taee3.drop(['open','adjclose', 'high', 'low','volume', 'ticker'], axis = 1)
df_taee3_t = df_taee3.set_index('data')
df_taee3_t1 = df_taee3_t.shift(1)
df_taee3_return = (df_taee3_t - df_taee3_t1)/df_taee3_t
df_taee3_return = df_taee3_return.reset_index()
df_taee3_return = df_taee3_return.rename(columns={'index': 'data'})

df_selic = selic
df_selic_t = df_selic.set_index('data')
df_selic_t1 = df_selic_t.shift(1)
df_selic_return = (df_selic_t - df_selic_t1)/df_selic_t
df_selic_return = df_selic_return.reset_index()
df_selic_return = df_selic_return.rename(columns={'index': 'data'})




dfs_secundarios = [df_itsa4_return, df_tasa4_return, df_taee3_return]
df_names = ['df_itsa4_return', 'df_tasa4_return', 'df_taee3_return']

for df, df_name in zip(dfs_secundarios, df_names):
    df = df.reset_index()
    df = df.rename(columns={'close': f'{df_name}_close'})
    df_bbas3_return = df_bbas3_return.merge(df[['data', f'{df_name}_close']], on='data', how='left')

##ERRO
df_selic_return = df_selic_return.reset_index()
df_bbas3_return = df_bbas3_return.merge(df_selic_return, how='left', on='data')
df_returns = df_bbas3_return
df_returns = df_returns.rename(columns={"close":"bbas3_close"})
df_returns = df_returns.set_index('data')


#Media de Retonos
media_retornos = df_returns.mean()
bbas3_returns = -0.00029962414296355453
itsa4_returns = -0.0002132777319046077
tasa4_returns = 0.0001673411423648793
taee3_returns = 0.00020344987931162446

tickets_returns = np.array([bbas3_returns, itsa4_returns,tasa4_returns,taee3_returns]).reshape(4,1)


#Covariancia dos retornos
matriz_cov = df_returns.cov()



