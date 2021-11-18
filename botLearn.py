import config
from binance.client import Client
from binance.enums import *
import pandas as pd

#initilise Client
client = Client(config.API_KEY, config.API_SECRET)

#Select the period you want
klines = client.get_historical_klines("ETHAUD", Client.KLINE_INTERVAL_30MINUTE, "20 Jul, 2021", "12 Nov, 2021")
klines_new = []


for x in klines:
    klines_new.append(x[0:7])

#Loads OHLCV data into a DataFrame:
df = pd.DataFrame(klines_new, columns=['Open Time', 'Open Price', 'High Price', 'Low Price', 'Close price', 'Volume', 'Close Time'])

print(df)

#We then save the dataframe in CSV Format
with open('data.csv', 'w') as csv_file:
    df.to_csv(path_or_buf=csv_file)
