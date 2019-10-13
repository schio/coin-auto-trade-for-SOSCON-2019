import numpy as np
import math
import re
import os
from random import *
import pandas as pd

# prints formatted price
def formatPrice(n):
  return ("-$" if n < 0 else "$") + "{0:.2f}".format(abs(n))

# returns the vector containing stock data from a fixed file
def getStockDataVec(market):
  path = "/home/scio/Workspace/coin-auto-trade-for-SOSCON-2019/data/"  
  pkl_paths = os.listdir(path)
  pattern = re.compile(f"{market}_.*")
  
  # load candles pikle
  candles = []
  for pkl_path in pkl_paths:
    pkl_path = pattern.findall(pkl_path)
    if len(pkl_path) == 0:
      pass
    else:
      pkl_df = pd.read_pickle(path + pkl_path[0])
      candles.append(pkl_df)

  # concat candles
  candles_df = pd.concat(candles, ignore_index=True)
  
  # drop duplicates
  candles_df = candles_df.drop_duplicates([f'{market}_ts'])
  candles_df = candles_df.sort_values(by=[f'{market}_ts'])
  candles_df = candles_df.dropna()
  print(f'candles_df.shape: {candles_df.shape}')
  # print(candles_df)
  # time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(1347517370))
  
  return candles_df.values

  # return vec

# returns the sigmoid
def sigmoid(x):
  return 1 / (1 + math.exp(-x))

# returns an an n-day state representation ending at time t
def getState(data, t, window_size, len_data):
  idx = randint(0, len_data - window_size)
  block = data[idx:idx+window_size]
  res = []
  block = block[:,1]

  for i in range(window_size - 1):
    # print(block[i + 1] - block[i])
    res.append(block[i + 1] - block[i])

  return np.array([res])