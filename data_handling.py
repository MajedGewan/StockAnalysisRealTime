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

datasets = ['JPY=X', 'SALIK.AE', 'TSLA','META']
def get_data(dataset_input, datet_type):
    if datet_type == '1D':
        interval, period = '1m', '1d'
    elif datet_type == '1M':
        interval, period = '1d', '1mo'
    elif datet_type == '1Y':
        interval, period = '1d', '1y'
    elif datet_type == '5Y':
        interval, period = '1d', '5y'
    else:
        raise Exception
    finance = Ticker(dataset_input, interval=interval, period=period)
    finance.data['Prev High'] = finance.data['High'].shift(1)
    finance.data.loc[0, 'Prev High'] = finance.data.loc[0,'High']
    finance.data['Prev Low'] = finance.data['Low'].shift(1)
    finance.data.loc[0, 'Prev Low'] = finance.data.loc[0,'Low']
    finance.data['Prev Close'] = finance.data['Close'].shift(1)
    finance.data.loc[0, 'Prev Close'] = finance.data.loc[0,'Close']
    
    return finance 

def get_datasets():
    return datasets
