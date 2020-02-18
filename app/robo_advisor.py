# app/robo_advisor.py

import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

print("REQUESTING SOME DATA FROM THE INTERNET...")

# variables in the URL
API_KEY = os.getenv("ALPHAVANTAGE_API_KEY", default = "OOPS") # X55IRTRY70EOOESP
selected_ticker = input("Please enter the ticker (e.g.: AAPL) for the stock you would like to learn about: ")

request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={selected_ticker}&interval=5min&apikey={API_KEY}"
print("URL:", request_url)

response = requests.get(request_url)
print(type(response))
print(response.status_code)
print(type(response.text)) #>string

# handle response errors:
if "Error Message" in response.text:
    print("OOPS, couldn't find that symbol! Please try again")
    exit()

parsed_response = json.loads(response.text)
print(type(parsed_response)) #> dict

print(parsed_response)

# ----------------------------------------------
# ----------------------------------------------

print("------------------------------")
print("SELECTED SYMBOL: ", selected_ticker)
print("------------------------------")

print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT: 2018-02-20 02:00pm")
print("------------------------------")

print("LATEST DAY: 2018-02-20")
print("LATEST CLOSE: $100,000.00")
print("RECENT HIGH: $101,000.00")
print("RECENT LOW: $99,000.00")
print("------------------------------")

print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")

print("------------------------------")
print("HAPPY INVESTING!")
print("------------------------------")