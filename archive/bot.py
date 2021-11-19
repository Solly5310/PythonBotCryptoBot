import websocket, json, pprint, talib, numpy
import config
from binance.client import Client
from binance.enums import *

SOCKET = "wss://stream.binance.com:9443/ws/ethaud@kline_1h"

#this is an array that is used to store all of the closing values of ETH
closes = []

RSI_PERIOD = 14 #Period to calculate RSI
RSI_OVERBOUGHT = 70 #Threshold to trigger a buy order
RSI_OVERSOLD = 30 #Threshold to trigger a sell order
TRADE_SYMBOL = 'ETHAUD'
TRADE_QUANTITY = 0.004
in_position = False


#did not need tld as you are based in AU
client = Client(config.API_KEY, config.API_SECRET)

#here is the order function
def order(side, quantity, symbol,order_type=ORDER_TYPE_MARKET):
    try:
        print("sending order")
        order = client.create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
        print(order)
    except Exception as e:
        print("an exception occured - {}".format(e))
        return False

    return True



def on_open(ws):
   print('Opened conection')

def on_close(ws):
   print("Closed connection")

def on_message(ws, message):
   #declare of global variable to store close values
   global closes, in_position

   #print("Received message")
   json_messsage = json.loads(message) #convert json into a dictionary
   #pprint used to print info in dictionary nicely
   pprint.pprint(json_messsage)

   candle = json_messsage['k']
   is_candle_closed = candle['x']
   close = candle['c']

   if is_candle_closed:
      print("candle closed at {}".format(close))
      #adding the close value to the list
      #casting the string to a float so TA can be applied
      closes.append(float(close))
      print("closes:")
      print(closes)

      if len(closes) > RSI_PERIOD:
         np_closes = numpy.array(closes)
         rsi = talib.RSI(np_closes, RSI_PERIOD) #RSI Function, which takes a numpy array as first argument, RSI PERIOD is 14 by default, we have also stated this as the argument from our constant
         print("All RSI's calculated so far:")
         print(rsi)
         last_rsi = rsi[-1] #here we put the last RSI calculation to determine if it is a a potential buy or sell action
         print("the current rsi is {}".format(last_rsi))

         if last_rsi > RSI_OVERBOUGHT:
            if in_position:
               print("Overbought - Sell!")
               #put binance sell order logic here
               order_succeeded = order(SIDE_SELL, TRADE_QUANTITY, TRADE_SYMBOL)
               if order_succeeded:
                  in_position=False
            else:
               print("Already sold nothing to do")
               
         elif last_rsi < RSI_OVERSOLD:
            if in_position:
               print("Oversold, already bought nothing to do")
            else:
               print("Oversold, Buy!")
               #put binance buy order logic here
               order_succeeded = order(SIDE_BUY, TRADE_QUANTITY, TRADE_SYMBOL)
               if order_succeeded:
                  in_position = True


#We need a stream for it to read:
ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)

ws.run_forever()


# true will tell you its the final value of the candlestick at closure
# Average Directional Index
# Moving Average Convergence Divergence (You also have the simplte moving average)
# RSA


yes
