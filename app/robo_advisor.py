# app/robo_advisor.py

import requests
import json
import os
from dotenv import load_dotenv
from datetime import datetime
import csv

load_dotenv()

# variables, empty lists etc.
API_KEY = os.getenv("ALPHAVANTAGE_API_KEY", default = "demo")
selected_symbols = [] # list of the symbols the user wishes to learn about
selected_response = [] # list consisting of all the data about a given symbol from the database

# function definitions
def to_usd(my_price):
    return f"$ {my_price:,.2f}" #> $12,000.71
    """
    Converts a numeric value to usd-formatted string, for printing and display purposes.
    Source: https://github.com/prof-rossetti/intro-to-python/blob/master/notes/python/datatypes/numbers.md#formatting-as-currency
    Param: my_price (int or float) like 4000.444444
    Example: to_usd(4000.444444)
    Returns: $ 4,000.44
    """

def timestamp(current_datetime):
    datetime_str = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    return f"Request at: {datetime_str}"
    """
    Formats and returns the current date/time
    Param: current_datetime takes information from the datetime module
    Example: timestamp(datetime().now)
    Returns: 2020-04-16 11:15:35
    """

def get_url_data(ticker):
    request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={API_KEY}"
    response = requests.get(request_url) # checks whether the request for the URL succeeded or not
    if "Error Message" in response.text:
        print("OOPS, couldn't find that symbol! Please try running the program again!")
        return exit()
    else:
        parsed_response = json.loads(response.text)
        return parsed_response

def user_input(all_symbols):
    if len(selected_symbols) == 0:
        feedback = "You didn't input a stock ticker/symbol. At least one symbol is required to run this program."
    else:
        feedback = f"Your entered: {selected_symbols}"
    return feedback

def dict_to_list(all_stock_data):
    tsd = all_stock_data["Time Series (Daily)"]
    all_days = []
    for date, stock_price in tsd.items():
        one_day = {
            "timestamp": date,
            "open": float(stock_price["1. open"]),
            "high": float(stock_price["2. high"]),
            "low": float(stock_price["3. low"]),
            "close": float(stock_price["4. close"]),
            "volume": float(stock_price["5. volume"])
        }
        all_days.append(one_day)

    return all_days

def get_latest_day(all_days):
    latest_day = all_days[0]
    return latest_day

def get_yesterday(all_days):
    yesterday = all_days[1]
    return yesterday

def get_highs(all_days):
    high_prices = []
    for one_day in all_days:
        day_high = one_day["high"]
        high_prices.append(day_high)
    return high_prices

def get_lows(all_days):
    low_prices = []
    for one_day in all_days:
        day_low = one_day["low"]
        low_prices.append(day_low)
    return low_prices

def get_recommendation(latest_close, recent_high, recent_low):
    recommendation = "N/A"

    if latest_close < (recent_low * 1.2): # If the stock's latest closing price is less than 20% above its recent low, "Buy"
        recommendation_decision = "Buy!"
    elif (recent_high - recent_low) > 50: # If the difference between the recent high and recent low is greater than 50, "Buy"
        recommendation_decision = "Buy!"
    else: # Else, "Don't Buy"
        recommendation_decision = "Don't buy!"
    return recommendation_decision


def get_reco_reason(latest_close, recent_high, recent_low):
    recommendation_reasoning = "N/A"

    if latest_close < (recent_low * 1.2): # If the stock's latest closing price is less than 20% above its recent low, "Buy"
        recommendation_reasoning = "The stock's latest closing price is less than 20% above its recent low. Prices are likely to go up soon."
    elif (recent_high - recent_low) > 50: # If the difference between the recent high and recent low is greater than 50, "Buy"
        recommendation_reasoning = "There is a significant gap between the recent high and low which means that it is not a volatile stock at the moment. It would be a safe investment"
    else: # Else, "Don't Buy"
        recommendation_reasoning = "It's risky to buy this stock as the moment. Wait until the market becomes more predictable."
    return recommendation_reasoning


# TODO: create CSV file function

if __name__ == "__main__":

# USER INPUT    
    while True:
        symbol = input("Please enter the ticker symbol (e.g.: AAPL) for a stock you would like to learn about. Or, if you are done entering the stocks, hit 'enter': ")
        #symbol = "MSFT"

        if symbol == "":
            break
        else:
            print("")
            print("*******************************************************")
            print(f"Looking up the internet for {symbol.upper()} stock data ...")
            print("*******************************************************")
            print("")

            parsed_response = get_url_data(symbol) # accesses the URL and collects the requested data for that stock.    

            selected_symbols.append(symbol) # adds stock symbol to a list of stock symbols requested by the user
            selected_response.append(parsed_response) # adds stock info to a list of all the info of stocks requested by the user

    # OUTPUT: Summary of user input
    feedback = user_input(selected_symbols) #> You entered: ["AAPL, "GOOG", "MSFT", "TSLA"]
    print(feedback)

    for i in range(0,len(selected_symbols)):
        ticker = selected_symbols[i]

        # variable holding latest refreshed date
        latest_refreshed = selected_response[i]["Meta Data"]["3. Last Refreshed"]
        
        all_days = dict_to_list(selected_response[i])

        latest_day = get_latest_day(all_days)
        latest_close = latest_day["close"]

        yesterday = get_yesterday(all_days)
        yesterday_close = yesterday["close"]

        # maximum/minimum daily high/low in the last 100 days

        high_prices = get_highs(all_days)
        low_prices = get_lows(all_days)

        recent_high = max(high_prices)
        recent_low = min(low_prices)

        # recommendation algorithm

        recommendation_decision = get_recommendation(latest_close, recent_high, recent_low)
        recommendation_reasoning = get_reco_reason(latest_close, recent_high, recent_low)

        # writing data to a csv file

        csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", f"{ticker.upper()}_prices.csv")
        csv_headers = ["timestamp", "open", "high", "low", "close", "volume"]

        with open(csv_file_path, "w") as csv_file: # "w" means "open the file for writing"
            writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
            writer.writeheader() # uses fieldnames set above

            # loop through all data to write into different rows
            for date in dates:
                writer.writerow({
                    "timestamp": date,
                    "open": tsd[date]["1. open"],
                    "high": tsd[date]["2. high"],
                    "low": tsd[date]["3. low"],
                    "close": tsd[date]["4. close"],
                    "volume": tsd[date]["5. volume"],
                })

        # print results ------------------------------------------------------------------

        print("")
        print("--------------------------------")
        print("SELECTED SYMBOL: ", ticker.upper())
        print("--------------------------------")
        print("REQUESTING STOCK MARKET DATA...")
        print(timestamp(datetime.now()))
        print("--------------------------------")
        print(f"LATEST DAY   : {latest_refreshed}")
        print(f"LATEST CLOSE : {to_usd(float(latest_close))}")
        print(f"RECENT HIGH  : {to_usd(float(recent_high))}")
        print(f"RECENT LOW   : {to_usd(float(recent_low))}")
        print("--------------------------------")
        print(f"RECOMMENDATION : {recommendation}")
        print("")
        print(f"RECOMMENDATION REASON: {recommendation_reason}")
        print("--------------------------------")
        print("WRITING DATA TO CSV FILE...")
        print(csv_file_path)
        print("--------------------------------")
        print("")
        print("********************************")
        print("       HAPPY INVESTING!")
        print("********************************")
        print("")