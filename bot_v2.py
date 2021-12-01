import key, talib, numpy as np, pandas as pd
from binance.client import Client
from binance.enums import *
from datetime import datetime
import time


#We have our chosen crypto symbol
crypto_symbol = 'ETHAUD'

#smallest possible trade quantity to test
TRADE_QUANTITY = 0.004
client = Client(key.API_KEY, key.API_SECRET)

buy_switch = 0
order_history = []
#set the column headings for our csv file
df = pd.DataFrame(columns=['Date-Time', 'Price', 'Short Moving Average', 'Long Moving Average', 'Action'])
df.to_csv('test.csv',index=False)

#used to record decisions made by the bot
def record_result(date, closing_price, short_ma, long_ma, action):
   df = pd.DataFrame( { 'Date-Time': [date], 'Price': [closing_price], 'Short Moving Average': [short_ma], 'Long Moving Average': [long_ma],'Action': [action] })
   df.to_csv('test.csv', mode='a', index=False, header=False)
   
#finds the price data at 30 min intervals
#will then make a decision as to where to trade and record it
def get_price_data(c_symbol, switch):
      candles = client.get_klines(symbol=c_symbol, interval=Client.KLINE_INTERVAL_30MINUTE, limit = 1000)
      closes = []
      for x in candles:
         closes.append(float(x[4]))
      #receive all closing prices for the past 1000 instances of 30 min intervals   
      closes_np = np.array(closes)
      #will then calculate the short term and long term moving average
      MAST = talib.SMA(closes_np, 100)
      MALT = talib.SMA(closes_np, 1000)
      print("The STSMA is:", MAST[-1], "\nThe LTSMA is:", MALT[-1])
      #we then convert the timetsamp into a date
      date = datetime.fromtimestamp(int(candles[-1][0])/1000.0)
      print(date)
      if MAST[-1] > MALT[-1] and switch == 0:
         print("Buy Buy Buy")
         record_result(date, closes_np[-1], MAST[-1], MALT[-1], "Buy Order Placed")
         return 1
      elif (MAST[-1] > MALT[-1] and switch == 1):
         print("Already bought")
         record_result(date, closes_np[-1], MAST[-1], MALT[-1], "N/A")
         return 1
      elif MAST[-1] < MALT[-1] and switch ==1:
         print("Sell Sell Sell")
         record_result(date, closes_np[-1], MAST[-1], MALT[-1], "Sell Order Placed")
         return 0
      elif (MAST[-1] < MALT[-1] and switch == 0):
         print("Already sold")
         record_result(date, closes_np[-1], MAST[-1], MALT[-1], "N\A")
         return 0

#this program will run every 30 mins
while True:
   #here is where we analyse the data
   buy_switch = get_price_data(crypto_symbol, buy_switch)
   time.sleep(1800)
