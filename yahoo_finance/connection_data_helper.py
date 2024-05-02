import requests
import time
import pandas as pd
def get_raw_data(url, symbol, interval, period):
        link = url + symbol
        params = {
        'interval': interval,
        'range': period
        }
        headers = {
        'User-Agent': 'Mozilla/5.0',
        'From': 'majed.alhanash@gewan.ai' 
        }
        raw_data, error = None, None
        for attempt in range(5):  # Retry up to 5 times
            response = requests.get(link, params=params, headers=headers)
            if response.status_code == 200:
                raw_data = response.json()
                return raw_data, None 
            elif response.status_code == 429:
                time.sleep(2 ** attempt)  # Exponential back-off
            else:
                error = response.status_code
                return None, error
        if raw_data is None:
            error = "429 unknow request code"
            return None, error
        return raw_data, error

def get_data(url, symbol, interval, period):
     chart_data, currency, regular_market_time, timezone, previous_close, high, low = None, None, None, None, None, None, None
     data, error = get_raw_data(url, symbol, interval, period)
     if error is None:
          chart_data, currency, regular_market_time, timezone, previous_close, high, low = process_data(data, interval)
     return error, chart_data, currency, regular_market_time, timezone, previous_close, high, low
def process_data(data,interval):
     result = data['chart']['result'][0]
     meta = result['meta']
     indicators = result['indicators']
     timestamp = result['timestamp']
     numerical_data = indicators['quote'][0]
     currency = meta['currency']
     regular_market_time = meta['regularMarketTime']
     timezone = meta['exchangeTimezoneName']
     high, low, previous_close = get_high_low_close(meta, numerical_data, interval)
     chart_data = pd.DataFrame({'Date':timestamp,
                   'High':numerical_data['high'],
                   'Close':numerical_data['close'],
                   'Volume':numerical_data['volume'],
                   'Low':numerical_data['low'],
                   'Open':numerical_data['open']})
     chart_data['Date'] = chart_data['Date'].apply(pd.Timestamp, unit='s', tz=timezone)
     return chart_data, currency, regular_market_time, timezone, previous_close, high, low
    
     
def get_high_low_close(meta, numerical_data, interval):
    previous_close, high, low = None, None, None
    if interval == '1m':
        previous_close = meta['previousClose']
        high = meta['regularMarketDayHigh']
        low = meta['regularMarketDayLow']
    else:
        previous_close = meta['chartPreviousClose']
        high = max(list(filter(lambda item: item is not None, numerical_data['high'])))
        low = max(list(filter(lambda item: item is not None, numerical_data['low'])))
    return high, low, previous_close


     