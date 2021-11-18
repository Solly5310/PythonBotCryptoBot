import csv
import talib, numpy as np
from datetime import datetime

buySwitch = 0
closes = []
time = []

#open historical trade data
with open('data.csv', newline='') as csvfile:
   filereader = csv.reader(csvfile, delimiter=',', quotechar='|')
   next(csvfile, None)
   for row in filereader:
      date = datetime.fromtimestamp(int(row[1])/1000.0)
      time.append(date)
      closes.append(float(row[5]))

Q=0
C = 5000
S = 0

#apply a range of Moving Average based analysis
np_closes = np.array(closes)
SMAST = talib.SMA(np_closes, 100)
SMALT = talib.SMA(np_closes, 1000)
RSI = talib.RSI(np_closes, 30)

#create a list of all indicators over period
indicator = [-1]*(len(SMALT))

#from there we then go over the historical period
for x in range(len(np_closes)):
   #if short term average is greater than long term average it indicates a buy
   #only occurs once until an additional sell occurs
   if SMAST[x] > SMALT[x]:
      if buySwitch == 0:
         print("\nBuy")
         indicator[x] = 1
         buySwitch = 1
         C = C - np_closes[x]
         Q = 1
         print("At ", time[x], "stock was bought at price: ", np_closes[x])
         print("Cash at end:", C)
         print("Shares at end:",Q * np_closes[x])
         print("Sum:",C + (Q * np_closes[x]))
   #if short term average is less than long term average it indicates a sell
   #only occurs once until an additional buy occurs
   elif SMAST[x] < SMALT[x]:
      if buySwitch == 1:
         print("\nSell")
         indicator[x] = 0
         buySwitch = 0
         C = C + np_closes[x]
         Q=0
         print("At ", time[x], "stock was sold at price: ", np_closes[x])
         print("Cash at end:", C)
         print("Shares at end:", Q * np_closes[x])
         print("Sum:",C + (Q * np_closes[x]))

#total of equity and available cash at the end of the peiod
print("\n\nCash at end:", C)
print("Shares at end:", Q * np_closes[-1])
print("Sum:",C + (Q * np_closes[-1]))