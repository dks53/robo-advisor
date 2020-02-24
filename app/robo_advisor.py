# app/robo_advisor.py

import requests
import json
import os
from dotenv import load_dotenv
from datetime import datetime
import csv
import plotly
import plotly.graph_objs as go
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

## ----------------------------------------------------------------------------------------------

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

selected_symbols = [] # list of the symbols the user wishes to learn about
selected_response = [] # list consisting of all the data about a given symbol from the database

while True:
    symbol = input("Please enter the ticker symbol (e.g.: AAPL) for a stock you would like to learn about. Or, if you are done entering the stocks, hit 'enter': ")
    #symbol = "MSFT"

    if symbol == "":
        break
    else:
        # preliminary validation checking if input is <4 characters and contains only alphabets
        if len(symbol) < 5 and symbol.isalpha():
            print("")
            print("*******************************************************")
            print(f"Looking up the internet for {symbol.upper()} stock data ...")
            print("*******************************************************")
            print("")

            # loads URL to be looked up for data
            request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}"
            #print("--------------------------------------------------------------------------------------------------------")
            #print("URL:", request_url)
            #print("--------------------------------------------------------------------------------------------------------")
            #print("")

            response = requests.get(request_url) # checks whether the request for the URL succeeded or not

            #  secondary validation to see if the stock symbol exists ~ handle response errors:
            if "Error Message" in response.text:
                print("OOPS, couldn't find that symbol! Please try again")
                
            parsed_response = json.loads(response.text)

            selected_symbols.append(symbol)
            selected_response.append(parsed_response)

            #print(selected_symbols)
            #print(selected_response)

        else:
            print("Are you sure you entered the correct symbol? Try again!")

      
print("")

# if statement to make sure the user entered at least one stock.
if len(selected_symbols) == 0:
    print("You didn't input a stock ticker/symbol. At least one symbol is required to run the code.")
    print("")
    exit()
else:
    print(f"Your entered: {selected_symbols}")

#breakpoint()

for i in range(0,len(selected_symbols)):
    ticker = selected_symbols[i]
    # Date/time of request
    
    DateTime = datetime.now()

    request_at = (f"{DateTime.year}-{DateTime.month}-{DateTime.day} {DateTime.hour}:{DateTime.minute}:{DateTime.second}")

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
    print(f"REQUEST AT: {request_at}")
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

    # calculation for percentage change in closing price of stock on latest day and the day before
    
    price_change = (float(latest_close)-float(yesterday_close))/float(yesterday_close)
    print(price_change)
    price_change_percent = round((price_change * 100),2)
    print(price_change_percent)
    price_change = abs(price_change)
    print(price_change)


    # condition to determine whether or not to send the email. If change is > 5%, send email, otherwise break.
    if (price_change > 0.05):
        SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY", "OOPS, please set env var called 'SENDGRID_API_KEY'")
        MY_ADDRESS = os.environ.get("MY_EMAIL_ADDRESS", "OOPS, please set env var called 'MY_EMAIL_ADDRESS'")
        client = SendGridAPIClient(SENDGRID_API_KEY) #> <class 'sendgrid.sendgrid.SendGridAPIClient>

        subject = f"{symbol} Stock Movement Alert"

        html_content = f"The {ticker.upper()} stock changed by {price_change_percent}% since yesterday"
        
        message = Mail(from_email=MY_ADDRESS, to_emails=MY_ADDRESS, subject=subject, html_content=html_content)

        try:
            response = client.send(message)

        except Exception as e:
            print("OOPS", e.message)
    else:
        print("")


print("********************************")
print("       HAPPY INVESTING!")
print("********************************")
print("")


