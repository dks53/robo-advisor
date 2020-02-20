# app/robo_advisor.py

import requests
import json
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def to_usd(my_price):
    return f"$ {my_price:,.2f}" #> $12,000.71
    """
    Converts a numeric value to usd-formatted string, for printing and display purposes.
    Source: https://github.com/prof-rossetti/intro-to-python/blob/master/notes/python/datatypes/numbers.md#formatting-as-currency
    Param: my_price (int or float) like 4000.444444
    Example: to_usd(4000.444444)
    Returns: $4,000.44
    """

# variables in the URL
API_KEY = os.getenv("ALPHAVANTAGE_API_KEY", default = "OOPS") # X55IRTRY70EOOESP
symbol = input("Please enter the ticker (e.g.: AAPL) for the stock you would like to learn about: ")
#symbol = "MSFT"

# preliminary validation checking if input is <4 characters and contains only alphabets
if len(symbol) < 5 and symbol.isalpha():
    print("")
    print("*******************************************************")
    print(f"Looking up the internet for {symbol.upper()} stock data ...")
    print("*******************************************************")
    print("")
else:
    print("Are you sure you entered the correct symbol? Try again!")
    exit()

# loads URL to be looked up for data
request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}"
print("--------------------------------------------------------------------------------------------------------")
print("URL:", request_url)
print("--------------------------------------------------------------------------------------------------------")
print("")

response = requests.get(request_url) # checks whether the request for the URL succeeded or not

#  secondary validation to see if the stock symbol exists ~ handle response errors:
if "Error Message" in response.text:
    print("OOPS, couldn't find that symbol! Please try again")
    exit()

parsed_response = json.loads(response.text)

# Date/time of request
DateTime = datetime.now()

request_at = (f"{DateTime.year}-{DateTime.month}-{DateTime.day} {DateTime.hour}:{DateTime.minute}:{DateTime.second}")

# variable holding latest refreshed date
latest_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]

tsd = parsed_response["Time Series (Daily)"]
#print(tsd)

# storing the most recent date in a variable
dates = list(tsd.keys())
latest_day = dates[0]

# closing price for latest date
latest_close = tsd[latest_day]["4. close"]

# maximum/minimum daily high/low in the last 100 days
high_prices = []
low_prices = []

for date in dates:
    day_high = tsd[date]["2. high"]
    high_prices.append(day_high)
    day_low = tsd[date]["3. low"]
    low_prices.append(day_low)

recent_high = max(high_prices)
recent_low = min(low_prices)
    
# print results ------------------------------------------------------------------

print("--------------------------------")
print("SELECTED SYMBOL: ", symbol.upper())
print("--------------------------------")

print("REQUESTING STOCK MARKET DATA...")
print(f"REQUEST AT: {request_at}")
print("--------------------------------")

print(f"LATEST DAY   : {latest_refreshed}")
print(f"LATEST CLOSE : {to_usd(float(latest_close))}")
print(f"RECENT HIGH  : {to_usd(float(recent_high))}")
print(f"RECENT LOW   : {to_usd(float(recent_low))}")
print("--------------------------------")

print("RECOMMENDATION : BUY!")
print("")
print("RECOMMENDATION REASON: TODO")
print("")

print("********************************")
print("       HAPPY INVESTING!")
print("********************************")
print("")
