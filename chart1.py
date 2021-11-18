import csv
import talib, numpy as np
from datetime import datetime
import matplotlib.pyplot as plt


closes = []
time = []

#open the CSV
with open('data.csv', newline='') as csvfile:
   filereader = csv.reader(csvfile, delimiter=',', quotechar='|')
   next(csvfile, None)
   for row in filereader:
      #convert timestamp into a date
      date = datetime.fromtimestamp(int(row[1])/1000.0)
      time.append(date)
      #collect all closing prices
      closes.append(float(row[5]))      

#apply a range of Moving Average based analysis
np_closes = np.array(closes)
SMAST = talib.SMA(np_closes, 100)
SMALT = talib.SMA(np_closes, 1000)
EMA = talib.EMA(np_closes, 100)


#Create a graph and all indicators to it
plt.plot(time, np_closes, label="Closing Price")
plt.plot(time, SMAST, label="SMA Short Term")
plt.plot(time, SMALT, label="SMA Long Term")
plt.plot(time, EMA, label="EMA")
plt.xlabel('Date')
plt.ylabel('Closing Price')
plt.legend()

plt.show()

