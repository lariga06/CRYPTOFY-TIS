from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd

# PRIOR USING THIS SCRIPT, download locally discord messages using DiscordChatExporter

# UPDATE the STB_file path with your
STB_file = r"C:\Development\TIS\STB\Cryptofy-STB-sample.html"


token_selector = "div > div.chatlog__embed-content-container > div.chatlog__embed-content > div.chatlog__embed-text > div.chatlog__embed-title > div"
last_price_selector = "div > div.chatlog__embed-content-container > div.chatlog__embed-content > div.chatlog__embed-text > div.chatlog__embed-fields > div:nth-child(1) > div.chatlog__embed-field-value > div"
date_selector = "div > div.chatlog__embed-content-container > div.chatlog__embed-footer > span"
last_prices = []
token_names = []
token_ids = []
tis_dates = []
timestamps = []


soup = BeautifulSoup(open(STB_file, encoding="utf8"), "html.parser")

for item in soup.select(last_price_selector):
    last_prices.append(item.getText())

for item in soup.select(date_selector):
    tis_date = item.getText()
    tis_date = tis_date.split()[6]
    print(tis_date)
    tis_date = datetime.strptime(tis_date, "%d/%m/%Y")
    timestamp = datetime.timestamp(tis_date) * 1000
    timestamps.append(timestamp)
    tis_dates.append(tis_date)


for item in soup.select(token_selector):
    token_info = item.getText()
    token_info = token_info.split(")")[0].split("(")
    token_names.append(token_info[0])
    token_ids.append(token_info[1])


tis_dict = {
    "tis_date": tis_dates,
    "timestamp": timestamps,
    "token_id": token_ids,
    "token_name": token_names,
    "last_price": last_prices,
    "signal": "STB",
}

df = pd.DataFrame(tis_dict)

# print(df.head())
# UPDATE your path to generate the file
df.to_csv("./TIS/DISCORD/STB-DISCORD.csv", index=False)


