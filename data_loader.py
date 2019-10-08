import pandas as pd
import numpy as np
# import FinanceDataReader as fdr
import os
from datetime import datetime
import time
import re
# UPBIT 거래수수료(부가세포함) 0.05%

# regex = re.compile("에러\s\d+")
# mc = regex.findall(text)
# print(mc)

class Candleloader():
  def __init__(self):
    self.path = "/home/scio/Workspace/coin-auto-trade-for-SOSCON-2019/data/"  

  def get_candles(self, market):
    pkl_paths = os.listdir(self.path)
    # print(pkl_paths)
    pattern = re.compile(f"{market}_.*")
    
    # load candles pikle
    candles = []
    for pkl_path in pkl_paths:
      pkl_path = pattern.findall(pkl_path)
      if len(pkl_path) == 0:
        pass
      else:
        pkl_df = pd.read_pickle(self.path + pkl_path[0])
        candles.append(pkl_df)

    # concat candles
    candles_df = pd.concat(candles, ignore_index=True)
    
    # drop duplicates
    candles_df = candles_df.drop_duplicates([f'{market}_ts'])
    candles_df = candles_df.sort_values(by=[f'{market}_ts'])
    candles_df = candles_df.dropna()
    print(f'candles_df.shape: {candles_df.shape}')   
    # time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(1347517370))
    return candles_df


  def get_indices(self):
    indices_code = ['KS11','DJI','IXIC','US500','JP225','STOXX50E','CSI300','HSI','FTSE','DAX','CAC']
    indices =[]
    for index in indices_code:
      index_df = fdr.DataReader(index, '2019').reset_index()
      indices.append(index_df)

    indices_df = pd.concat(indices, ignore_index=True)

    return indices_df


def main():
  candleloader = Candleloader()
  candles = candleloader.get_candles("KRW-BTC")
  print(candles)

if __name__ == "__main__":
  main()