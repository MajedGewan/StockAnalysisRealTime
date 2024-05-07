from datetime import datetime
import pandas as pd
from yahoo_finance.Ticker import Ticker

def get_row(data):
    l = data.iloc[-1].to_list()
    tz = l[0].tz
    time = pd.Timestamp(datetime.now().replace(second=0, microsecond=0), tz = tz)
    l[0] = time
    return l

datasets = pd.read_csv('./yahoo_finance/data_scrapping/data.csv')
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
    
    return finance 

def get_datasets():
    return datasets[['Symbol','Name']].set_index('Symbol')
