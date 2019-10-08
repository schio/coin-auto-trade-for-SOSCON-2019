import requests
from pprint import pprint as p
import pandas as pd
import json
import time
import os
from datetime import datetime, timedelta

class UpbitTargetMerketCrawler():
  def __init__(self):
    self.base_url = "https://api.upbit.com/v1"
    markets = self.get_merkets()
    candles = self.get_candle(markets)
    
    file_name = f"./data/{int(time.time())}.pkl"
    pd.to_pickle(candles, file_name)
    print(f"save df {candles.shape} to {file_name}", end='\t')

  def get_candle(self, markets):
    minutes_candle = self._minutes_candle(markets)
    return minutes_candle

  def _minutes_candle(self, markets):
    minutes = [1, 3, 5, 15, 10, 30, 60, 240]
    result = pd.DataFrame()
    for market in markets:
      for minute in minutes:
        candle = []
        url = f"{self.base_url}/candles/minutes/{minute}"
        query_string = {"market":market,"count":"200"}
        candle = requests.request("GET", url, params=query_string).json()
        df = pd.DataFrame((list(map(self._json_to_df, candle))))
        df.columns = [f'{market}_m{minute}_o', f'{market}_m{minute}_h',
                f'{market}_m{minute}_l', f'{market}_m{minute}_c',
                f'{market}_m{minute}_v', f'{market}_m{minute}_t']
        result = pd.concat([result, df], axis=1)
        time.sleep(0.4)
    return result

  def _json_to_df(self, candle):
    try:
      return [candle['opening_price'], candle['high_price'],
          		candle['low_price'], candle['trade_price'],
          		candle['candle_acc_trade_volume'], candle['candle_acc_trade_price'],
          		candle['timestamp']]
    except Exception as e:
      print(f"**** ERROR {e} ****")
      print(candle)


  def get_merkets(self):
    all_flag = 0
    if all_flag:
      print("### EXTRACT MARKETS")
      url = f"{self.base_url}/market/all"
      response = requests.request("GET", url)    
      market_codes = json.loads(response.text)
      return list(map(lambda market_code: market_code["market"], market_codes))
    else:
      markets = ["KRW-BTC", "KRW-XRP", "KRW-ETH", "KRW-XLM",
          "KRW-HBAR", "KRW-EOS", "KRW-ADA", "KRW-BCH","KRW-TRX",
          "KRW-BSV", "KRW-BTT", "KRW-SNT", "KRW-SBD", "KRW-CRE",
          "KRW-LTC", "KRW-TSHP", "KRW-QTUM", "KRW-QKC", "KRW-GRS",
          "KRW-STEEM", "KRW-ATOM", "KRW-SOLVE", "KRW-COSM", "KRW-ETC"]
      return markets

class UpbitMinuteCandleCrawler():
  def __init__(self):
    self.base_url = "https://api.upbit.com/v1/candles/minutes/1"
    markets = self.get_merkets(["KRW-XRP", "KRW-ETH", "KRW-XLM",
                                "KRW-EOS", "KRW-ADA", "KRW-BCH","KRW-TRX",
                                "KRW-LTC", "KRW-QTUM", "KRW-STEEM", "KRW-ETC"])
    self.get_minute_candle(markets)

  def get_minute_candle(self, markets):
    now_backup = datetime.now()
    for market in markets:
      now = now_backup
      while True:
        to = str(now).split('.')[0]
        querystring = {"market":market, "to":to, "count":"200"}
        response = requests.request("GET",
																		self.base_url,
																		params=querystring).json()
        # 더 이상 가져올 candle이 없으면 break
        if len(response) == 0:
          print(f"**** {market} crawling is done")
          break
        else:
          candle = pd.DataFrame(list(map(self._json_to_df, response)))
          candle.columns = [f'{market}_o', f'{market}_h',
														f'{market}_l', f'{market}_c',
														f'{market}_tv', f'{market}_tc',
														f'{market}_ts']

          # 190분 감소          
          now = now + timedelta(minutes=-190)
          
          file_name = f"./data/{market}_{to.split(' ')[0]}_{to.split(' ')[1]}.pkl"
          pd.to_pickle(candle, file_name)
          print(f"save candle.shape {candle.shape} to {file_name} || {datetime.now()}")

          time.sleep(5)


  def _json_to_df(self, candle):
    try:
      return [candle['opening_price'], candle['high_price'],
							candle['low_price'], candle['trade_price'],
							candle['candle_acc_trade_volume'], candle['candle_acc_trade_price'],
							candle['timestamp']]
    except Exception as e:
      print(f"**** ERROR {e} ****")
      print(candle)

  def get_merkets(self, selected_markets=None):
    if selected_markets is None:
      print("### EXTRACT MARKETS")
      url = f"{self.base_url}/market/all"
      response = requests.request("GET", url)    
      market_codes = json.loads(response.text)
      return list(map(lambda market_code: market_code["market"], market_codes))
    else:
      return selected_markets

def main():
  if not os.path.exists("./data"):
    os.makedirs("./data") 
  UpbitMinuteCandleCrawler()

if __name__ == "__main__":
  main()