from . import connection_data_helper
class Ticker:
    def __init__(self, symbol, interval, period ) -> None:
        self.url = "https://query1.finance.yahoo.com/v8/finance/chart/"
        self.interval = interval
        self.symbol = symbol
        self.period = period
        self.error = None
        self.raw_data = None
        self.get_data()

    def get_data(self):
        error, chart_data, currency, regular_market_time, timezone, previous_close, high, low = connection_data_helper.get_data(self.url, self.symbol, self.interval, self.period)
        self.error = error
        self.data = chart_data
        self.currency = currency
        self.regular_market_time = regular_market_time
        self.timezone = timezone
        self.previous_close = previous_close
        self.high = high
        self.low = low
    
        
