# PythonBotCryptoBot
Personal Bot Project

The python bot is split into three functions:

1. Historical Data Set Collection and analysis
* Receives Historical data on a particular Cryptocurrency Exchange rate - found in bot_learn.py
* You can then run your trading strategy against this data set - found in sma-ltma_historical_analysis.py
  * I used a Short Moving Average vs Long Term Moving Average in my example

2. Visualisation of Trading Performance
* You can apply your trading strategy visualising any trading indiciators you would like to keep track of - found in Chart_1.py and Chart_2.py

3. Application of trading Strategy
* You can then run your strategy through bot_v2.py
* Your bot's decision making at each time interval is recorded in the activitylog.csv
* Your bot's orders at each time interval is recorded in orderbook.csv

**Notes**
* You will need to obtain your own API key from your Binance Trading account, you will then need to enter it in key.py
* In order for the program to run continously on a server, I created a Google Virtual Machine Instance and applied the bot_v2.py program there
  * This ensures continouity of the program and no local machine usage

**Further Improvements**

There is definately space for improvement and this is a Minimal Viable Attempt! An optimal version would involve a user interface that allows the user to enter in their own API credentials and trading strategy so that it is implemented automatically and without prior knowledge of python. I will be working towards this at a future point!
