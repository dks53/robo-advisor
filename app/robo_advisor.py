# app/robo_advisor.py

import requests
import json
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def to_usd(my_price):
    return f"${my_price:,.2f}" #> $12,000.71
    """
    Converts a numeric value to usd-formatted string, for printing and display purposes.
    Source: https://github.com/prof-rossetti/intro-to-python/blob/master/notes/python/datatypes/numbers.md#formatting-as-currency
    Param: my_price (int or float) like 4000.444444
    Example: to_usd(4000.444444)
    Returns: $4,000.44
    """

print("REQUESTING SOME DATA FROM THE INTERNET...")

# variables in the URL
API_KEY = os.getenv("ALPHAVANTAGE_API_KEY", default = "OOPS") # X55IRTRY70EOOESP
#symbol = input("Please enter the ticker (e.g.: AAPL) for the stock you would like to learn about: ")
symbol = "MSFT"

request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}"
print("URL:", request_url)

response = requests.get(request_url)
#print(type(response))
#print(response.status_code)
#print(type(response.text)) #>string


# handle response errors:
if "Error Message" in response.text:
    print("OOPS, couldn't find that symbol! Please try again")
    exit()

parsed_response = json.loads(response.text)
#print(type(parsed_response)) #> dict
#print(parsed_response)

#breakpoint()

latest_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]
latest_close = parsed_response["Time Series (Daily)"]["2020-02-20"]["4. close"]



# ----------------------------------------------
# ----------------------------------------------

print("------------------------------")
print("SELECTED SYMBOL: ", symbol)
print("------------------------------")

print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT: 2018-02-20 02:00pm")
print("------------------------------")

print(f"LATEST DAY: {latest_refreshed}")
print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
print("RECENT HIGH: $101,000.00")
print("RECENT LOW: $99,000.00")
print("------------------------------")

print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")

print("------------------------------")
print("HAPPY INVESTING!")
print("------------------------------")