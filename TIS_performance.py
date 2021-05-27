import pprint, os
import binance
from binance.client import Client
from datetime import datetime, timedelta
import pandas as pd
from pandas import DataFrame


# UPDATE the file path
FILE = "./TIS/DISCORD/STB-DISCORD.csv"

#ADD YOUR BINANCE KEYS
API_BINANCE_KEY = ""
API_BINANCE_SECRET = ""

# TIS Short trade between 2 days and 14 days
df = pd.read_csv(FILE)
df.drop(labels=['token_name', 'signal'], axis=1, inplace=True)
tis_dict = df.to_dict(orient="records")


# d = {'txn_date': '5/1/2021', 'timestamp': 1609780000000, 'token_id': 'POLY', 'token_name': 'Polymath Network ', 'last_price': 2.9e-06, 'signal': 'STB'}

client = Client(API_BINANCE_KEY, API_BINANCE_SECRET)


for tis in tis_dict:
    try:
        token_pair = f"{tis['token_id']}BTC"
        start_date = f"{tis['tis_date']}"
        from_date = datetime.strptime(tis['tis_date'],'%Y-%m-%d') + timedelta(days=2)
        from_date = from_date.strftime("%d %b, %Y")
        to_date = datetime.strptime(tis['tis_date'],'%Y-%m-%d') + timedelta(days=15)
        to_date = to_date.strftime("%d %b, %Y")
        klines = client.get_historical_klines(token_pair, Client.KLINE_INTERVAL_1DAY, from_date, to_date, limit=50)
        # print(f"DEBUG KLINES: {klines}")
        df = DataFrame(klines, columns=['open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
        # print(f"DEBUG DF: {df.head()}")
        # delete unnecessary columns
        df.drop(labels=['open_time', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'], axis=1, inplace=True)
        # find the highest price in df
        max_price = float(df.to_numpy().max())
        price_increase = "{:.2%}".format((max_price - tis['last_price']) / tis['last_price'])
        tis['price_increase'] = price_increase

    # ignore obsolete token
    except ValueError:
        with open("error.log", "a+") as error:
            error.write(f"ERROR with {tis}\n")


df = pd.DataFrame(tis_dict)

# UPDATE your path to generate the file
df.to_csv("./TIS/PERF/TIS-STB_result.csv", index=False)
