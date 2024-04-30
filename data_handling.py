from datetime import datetime
import yfinance as yf
import pandas as pd
from yahoo_finance.Ticker import Ticker

def get_row(data):
    l = data.iloc[-1].to_list()
    tz = l[0].tz
    time = pd.Timestamp(datetime.now().replace(second=0, microsecond=0), tz = tz)
    l[0] = time
    return l

datasets = ['META','SALIK.AE', 'TSLA', 'JPY=X']
def get_data(dataset_input):
    finance = Ticker(dataset_input, interval='1m', period='1d')
    finance.data['Prev High'] = finance.data['High'].shift(1)
    finance.data.loc[0, 'Prev High'] = finance.data.loc[0,'High']
    finance.data['Prev Low'] = finance.data['Low'].shift(1)
    finance.data.loc[0, 'Prev Low'] = finance.data.loc[0,'Low']
    finance.data['Prev Close'] = finance.data['Close'].shift(1)
    finance.data.loc[0, 'Prev Close'] = finance.data.loc[0,'Close']
    print(finance.data)
    
    return finance 

def get_datasets():
    return datasets
