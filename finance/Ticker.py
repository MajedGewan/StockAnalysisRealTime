import json
import pandas as pd
class Ticker:
    def __init__(self, data) -> None:
        d = json.dumps(data['Data'])
        self.data = pd.read_json(d)
        self.currency = data['meta']['Currency']
        self.regular_market_time = data['meta']['RegularMarketTime']
        self.timezone = data['meta']['Timezone']
        self.previous_close = data['meta']['PreviousClose']
        self.high = data['meta']['High']
        self.low = data['meta']['Low']
        self.website = data['meta']['Website']
        self.symbol = data['meta']['Symbol']
        self.description = data['meta']['Description']