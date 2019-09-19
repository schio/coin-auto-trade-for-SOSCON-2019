import requests
from pprint import pprint as p
import pandas as pd
import json

class UpbitLoader():
    def __init__(self):
        self.base_url = "https://api.upbit.com/v1"
        markets = self.get_merkets()
        print(f"NUM OF MARKET: {len(markets)}")
        candles = self.get_candle(markets)

    def get_candle(self, markets):
        self._minutes_candle(markets)

    def _minutes_candle(self, markets):
        minutes = [1, 3, 5, 15, 10, 30, 60, 240]
        result = []
        for market in markets:
            for minute in minutes:
                candle = []
                url = f"{self.base_url}/candles/minutes/{minute}"
                query_string = {"market":market,"count":"200"}
                candle = requests.request("GET", url, params=query_string).json()
                df = pd.DataFrame((list(map(self._json_to_df, candle))))
                df.columns = [f'{market}_m{minute}_o', f'{market}_m{minute}_h', f'{market}_m{minute}_l', f'{market}_m{minute}_c', f'{market}_m{minute}_v']
                result.append(df)
        return pd.concat(result, axis=1)

    def _json_to_df(self, candle):    
        return [candle['opening_price'], candle['high_price'], candle['low_price'], candle['trade_price'], candle['candle_acc_trade_volume']]    

    def get_merkets(self):
        print("### EXTRACT MARKETS")
        url = f"{self.base_url}/market/all"
        response = requests.request("GET", url)        
        market_codes = json.loads(response.text)
        return list(map(lambda market_code: market_code["market"], market_codes))

UpbitLoader()