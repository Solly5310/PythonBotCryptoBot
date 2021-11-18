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
RSI = talib.RSI(np_closes, 50)


#first graph
ax1 = plt.subplot(311)
ax1.set_ylabel('Closing Price')
plt.plot(time, np_closes, label="Closing Price")
plt.plot(time, SMAST, label="SMA Short Term")
plt.plot(time, SMALT, label="SMA Long Term")
plt.setp(ax1.get_xticklabels(), visible=False)


#second graph
ax2 = plt.subplot(312, sharex=ax1)
plt.plot(time, RSI, color = 'tab:red')
ax2.set_ylabel('Closing Price')
ax2.set_xlabel('RSI')
plt.legend()
plt.show()


#This should help with this - https://www.earthdatascience.org/courses/scientists-guide-to-plotting-data-in-python/plot-with-matplotlib/introduction-to-matplotlib-plots/customize-plot-colors-labels-matplotlib/