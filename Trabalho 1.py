import numpy as np
import yahoo_fin
from ipywidgets import interact
from yahoo_fin.stock_info import get_data
from scipy.optimize import minimize
from pandas_datareader import data as pdr
import pandas as pd


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




itsa4['retorno'] = itsa4['adjclose'].pct_change().apply(lambda x: np.log(1+x)).dropna()



dfs_secundarios = [itsa4, tasa4, taee3]
df_names = ['itsa4', 'tasa4', 'taee3']

for df, df_name in zip(dfs_secundarios, df_names):
    df = df.reset_index()
    df = df.rename(columns={'close': f'{df_name}_close'})
    bbas3 = bbas3.merge(df[['data', f'{df_name}_close']], on='data', how='left')

df_ticker = bbas3.drop(['open','adjclose', 'high', 'low','volume', 'ticker'], axis = 1)
df_tickers = df_ticker.rename(columns={"close":"bbas3_close"})
df_tickers = df_tickers.set_index('data')

df_returns = df_tickers.pct_change().apply(lambda x: np.log(1+x)).dropna()
media_retornos = df_returns.mean()
matriz_cov = df_returns.cov()



