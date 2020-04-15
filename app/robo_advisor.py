# app/robo_advisor.py

import requests
import json
import os
from dotenv import load_dotenv
from datetime import datetime
import csv
import plotly
import plotly.graph_objs as go

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
def prelim_validation(ticker):
    if len(ticker) < 5 and ticker.isalpha():
        return symbol
    else:
        return print (f"Are you sure you entered the correct symbol? Try again!")

def get_url_data(ticker):
    request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={API_KEY}"
    response = requests.get(request_url) # checks whether the request for the URL succeeded or not
    parsed_response = json.loads(response.text)
    return parsed_response

def user_input(all_symbols):
    if len(selected_symbols) == 0:
        print("You didn't input a stock ticker/symbol. At least one symbol is required to run the code.")
        exit()
    else:
        return print(f"Your entered: {selected_symbols}")

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

            symbol = prelim_validation(symbol) # preliminary validation checking if input is <4 characters and contains only alphabets

            parsed_response = get_url_data(symbol) # accesses the URL and collects the requested data for that stock.    

            selected_symbols.append(symbol) # adds stock symbol to a list of stock symbols requested by the user
            selected_response.append(parsed_response) # adds stock info to a list of all the info of stocks requested by the user

    # OUTPUT: Summary of user input
    user_input(selected_symbols) #> You entered: ["AAPL, "GOOG", "MSFT", "TSLA"]

    for i in range(0,len(selected_symbols)):
        ticker = selected_symbols[i]

        # variable holding latest refreshed date
        latest_refreshed = selected_response[i]["Meta Data"]["3. Last Refreshed"]

        tsd = selected_response[i]["Time Series (Daily)"]
        #print(tsd)

        # storing the most recent date in a variable
        dates = list(tsd.keys())
        latest_day = dates[0]
        yesterday = dates[1]

        # closing price for latest date
        latest_close = tsd[latest_day]["4. close"]
        yesterday_close = tsd[yesterday]["4. close"]

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

        # recommendation algorithm

        recommendation = "N/A"
        recommendation_reason = "N/A"

        # converting to float in order to do calculations
        recent_high = float(recent_high)
        recent_low = float(recent_low)
        latest_close = float(latest_close)

        if latest_close < (recent_low * 1.2): # If the stock's latest closing price is less than 20% above its recent low, "Buy"
            recommendation = "Buy!"
            recommendation_reason = "The stock's latest closing price is less than 20% above its recent low. Prices are likely to go up soon."
        elif (recent_high - recent_low) > 50: # If the difference between the recent high and recent low is greater than 50, "Buy"
            recommendation = "Buy!"
            recommendation_reason = "There is a significant gap between the recent high and low which means that it is not a volatile stock at the moment. It would be a safe investment"
        else: # Else, "Don't Buy"
            recommendation = "Don't buy!"
            recommendation_reason = "It's risky to buy this stock as the moment. Wait until the market becomes more predictable."

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

        # plot graph of stock

        x=[]
        y=[]
        for date in dates:
            x.append(date)
            y.append(tsd[date]["4. close"])

        plot_file_path = os.path.join(os.path.dirname(__file__), "..", "data", f"{ticker.upper()}_chart.html")

        plotly.offline.plot({
            "data": [go.Scatter(x=x, y=y)],
            "layout": go.Layout(title=f"Daily Closing Price of {ticker.upper()} Stock", yaxis_title = "Price ($)", xaxis_title = "Date")
        }, filename=plot_file_path, auto_open=True)

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
        print(f"PLOTTING GRAPH FOR {ticker.upper()} STOCK")
        print("--------------------------------")

    print("")
    print("********************************")
    print("       HAPPY INVESTING!")
    print("********************************")
    print("")