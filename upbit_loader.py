import requests
from pprint import pprint as p
import pandas as pd

class UpbitLoader():
    def __init__(self):
        self.base_url = "https://api.upbit.com/v1"
        self.get_candle()
        # p(self.result)

    def get_candle(self):
        self._minutes_candle()

    def _minutes_candle(self):
        minutes = [1, 3, 5, 15, 10, 30, 60, 240]
        result = []
        for minute in minutes:
            candle = []
            url = f"{self.base_url}/candles/minutes/{minute}"
            query_string = {"market":"KRW-BTC","count":"200"}
            candle = requests.request("GET", url, params=query_string).json()
            df = pd.DataFrame((list(map(self._json_to_df, candle))))
            df.columns = [f'm{minute}_o', f'm{minute}_h', f'm{minute}_l', f'm{minute}_c', f'm{minute}_v']
            result.append(df)
        p(pd.concat(result, axis=1))
    
    def _json_to_df(self, candle):    
        return [candle['opening_price'], candle['high_price'], candle['low_price'], candle['trade_price'], candle['candle_acc_trade_volume']]    
UpbitLoader()