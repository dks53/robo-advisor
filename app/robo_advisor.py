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
    """
    API request logic - uses the API to request a web URL and returns data to be used in the rest of the model.
    Source: "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={API_KEY}
    Param: ticker for e.g.: MSFT or AAPL
    Example: get_url(MSFT)
    Returns: a dictionary called parsed_response which holds all the information available about the given stock.
    """

def user_input(all_symbols):
    if len(selected_symbols) == 0:
        feedback = "You didn't input a stock ticker/symbol. At least one symbol is required to run this program."
    else:
        feedback = f"Your entered: {selected_symbols}"
    return feedback
    """
    Checks to see if the user has not entered a stock to be evaluated. Returns the selected stocks or returns an alert message. 
    Param: selected_symbols for e.g.: ['MSFT','AAPL','TSLA] OR 
           no symbols selected for e.g.: []
    Example: get_url(['MSFT','AAPL','TSLA']) OR 
             get_url([])
    Returns: You entered:['MSFT','AAPL','TSLA] OR 
             You didn't input a stock ticker/symbol. At least one symbol is required to run this program.
    """    

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
    '''
    Converts the dictionary with all stock data into a list so that it can be used more efficiently in the code
    Source: "https://github.com/prof-rossetti/georgetown-opim-243-201901/blob/master/notes/python/datatypes/dictionaries.md"
    Source: "https://www.geeksforgeeks.org/python-convert-dictionary-to-list-of-tuples/"
    Param: selected_response[i] which holds all the stock data for a single given stock in the loop.
    Example: dict_to_list(selected_response[0])
    Returns: all_days list with all the stock data sorted by date
    '''

def get_latest_day(all_days):
    latest_day = all_days[0]
    return latest_day
    '''
    Uses the all_days list and pulls the 1st element of the list [0], which contains the latest_day data
    Param: all_days list which holds all the stock data for a single given stock in the loop.
    Example: get_latest_day(all_days)
    Returns: {'timestamp': '2020-04-14', 'open': '698.9700', 'high': '741.8800', 'low': '692.4300', 'close': '709.8900', 'volume': '29685359'}
    '''    

def get_yesterday(all_days):
    yesterday = all_days[1]
    return yesterday
    '''
    Uses the all_days list and pulls the 2nd element of the list [1], which contains the data on the day before the latest day
    Param: all_days list which holds all the stock data for a single given stock in the loop.
    Example: get_yesterday(all_days)
    Returns: {'timestamp': '2020-04-13', 'open': '590.1600', 'high': '652.0000', 'low': '580.5300', 'close': '650.9500', 'volume': '22475421'}
    '''

def get_highs(all_days):
    high_prices = []
    for one_day in all_days:
        day_high = one_day["high"]
        high_prices.append(day_high)
    return high_prices
    '''
    Uses the all_days list and creates a list with all the daily highs of the given stock
    Param: all_days list which holds all the stock data for a single given stock in the loop.
    Example: get_highs(all_days)
    Returns: list of all the "high" price values available for that stock
    '''       

def get_lows(all_days):
    low_prices = []
    for one_day in all_days:
        day_low = one_day["low"]
        low_prices.append(day_low)
    return low_prices
    '''
    Uses the all_days list and creates a list with all the daily lows of the given stock
    Param: all_days list which holds all the stock data for a single given stock in the loop.
    Example: get_lows(all_days)
    Returns: list of all the "low" price values available for that stock
    '''  

def get_recommendation(latest_close, recent_high, recent_low):
    recommendation = "N/A"

    if latest_close < (recent_low * 1.2): # If the stock's latest closing price is less than 20% above its recent low, "Buy"
        recommendation_decision = "Buy!"
    elif (recent_high - recent_low) > 50: # If the difference between the recent high and recent low is greater than 50, "Buy"
        recommendation_decision = "Buy!"
    else: # Else, "Don't Buy"
        recommendation_decision = "Don't buy!"
    return recommendation_decision
    '''
    Uses various values from the data such as latest closing price, recent high, recent low to run a calculation
    Param: latest_close, recent_high, recent_low
    Example: get_recommendation(47.00, 60.00, 40.00)
    Returns: recommendation_decision = "Buy!"
    '''  

def get_reco_reason(latest_close, recent_high, recent_low):
    recommendation_reasoning = "N/A"

    if latest_close < (recent_low * 1.2): # If the stock's latest closing price is less than 20% above its recent low, "Buy"
        recommendation_reasoning = "The stock's latest closing price is less than 20% above its recent low. Prices are likely to go up soon."
    elif (recent_high - recent_low) > 50: # If the difference between the recent high and recent low is greater than 50, "Buy"
        recommendation_reasoning = "There is a significant gap between the recent high and low which means that it is not a volatile stock at the moment. It would be a safe investment"
    else: # Else, "Don't Buy"
        recommendation_reasoning = "It's risky to buy this stock as the moment. Wait until the market becomes more predictable."
    return recommendation_reasoning
    '''
    Uses various values from the data such as latest closing price, recent high, recent low to run a calculation
    Param: latest_close, recent_high, recent_low
    Example: get_reco_reason(47.00, 60.00, 40.00)
    Returns: recommendation_reasoning = "The stock's latest closing price is less than 20% above its recent low. Prices are likely to go up soon.!"
    '''  

def write_to_csv(csv_file_path, all_days):
    csv_headers = ["timestamp", "open", "high", "low", "close", "volume"]

    with open(csv_file_path, "w") as csv_file: # "w" means "open the file for writing"
        writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
        writer.writeheader() # uses fieldnames set above

        # loop through all data to write into different rows
        for one_day in all_days:
            writer.writerow(one_day)
        '''
        Takes the pre-determined file path and all stock data and organizes it into individual rows, written onto a csv file.
        Param: csv_file_path, all_days
        Example: write_to_csv(csv_file_path, all_days)
        Returns: a CSV file saved in the data folder.
        '''  
                    
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

# PROCESSING
    for i in range(0,len(selected_symbols)):
        ticker = selected_symbols[i]

        # variable holding latest refreshed date
        latest_refreshed = selected_response[i]["Meta Data"]["3. Last Refreshed"]
        
        # invoking the dict_to_list function
        all_days = dict_to_list(selected_response[i])

        # invoking the get_latest_day function and determine the latest_close
        latest_day = get_latest_day(all_days)
        latest_close = latest_day["close"]
        
        # invoking the get_latest_day function and determine the latest_close
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

# OUTPUT

        # writing data to a csv file

        csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", f"{ticker.upper()}_prices.csv")

        write_to_csv(csv_file_path,all_days)

        # print results ------------------------------------------------------------------

        print("")
        print("--------------------------------")
        print("SELECTED SYMBOL: ", ticker.upper())
        print("--------------------------------")
        print("REQUESTING STOCK MARKET DATA...")
        print(timestamp(datetime.now()))
        print("--------------------------------")
        print(f"LATEST DAY   : {latest_refreshed}")
        print(f"LATEST CLOSE : {to_usd(latest_close)}")
        print(f"RECENT HIGH  : {to_usd(recent_high)}")
        print(f"RECENT LOW   : {to_usd(recent_low)}")
        print("--------------------------------")
        print(f"RECOMMENDATION : {recommendation_decision}")
        print("")
        print(f"RECOMMENDATION REASON: {recommendation_reasoning}")
        print("--------------------------------")
        print("WRITING DATA TO CSV FILE...")
        print(csv_file_path)
        print("--------------------------------")
        print("")
        print("********************************")
        print("       HAPPY INVESTING!")
        print("********************************")
        print("")