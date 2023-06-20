import plotly.graph_objects as go
import numpy as np
import yahoo_fin
from ipywidgets import interact
from yahoo_fin.stock_info import get_data
from scipy.optimize import minimize


ticker_list = ["bbas3.sa", "tasa4.sa", "taee3.sa", "itsa4.sa"]
historical_datas = {}
for ticker in ticker_list:
    historical_datas[ticker] = get_data(ticker, start_date="01/01/2018", end_date="01/01/2023", index_as_date= True, interval="1d")



