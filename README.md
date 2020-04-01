# Darshil Shah : robo-advisor-project

This document walks you (the user) through this robo-advisor project. It will help you setup your environment to run the code successfully. 

## What does this code do?

This is a financial planning business which helps customers make investment decisions.

This is an automated tool that is built to provide you with stock trading recommendations.

Specifically, the system accepts one or more stock symbols as information inputs, then it requests real live historical trading data from the internet, and finally provides a recommendation as to whether or not you should purchase the given stock(s).

## Functionality

### Information Input Requirements

The system will prompt you to input a stock symbol (e.g. "DIS", "MSFT", "AAPL", etc.). It will then allow you to continue to input multiple symbols, one-by-one, for as many stocks you wish to explore. Once you have entered all the stocks you wish to learn about, go ahead and hit "Enter" or "Return".

### Data Validation

The program will then conduct a two-step validation to ensure that the symbol you entered was correct and that data for that stock is available in the database. Once validations are completed, the program will run the necessary calculations and create an output.

> See "Prerequisits" in order to gain access to the database.

### Information Output

The program will provide the following output:

```sh
--------------------------------
SELECTED SYMBOL:  DIS
--------------------------------
REQUESTING STOCK MARKET DATA...
REQUEST AT: 2020-2-24 11:36:38
--------------------------------
LATEST DAY   : 2020-02-24 11:36:02
LATEST CLOSE : $ 131.95
RECENT HIGH  : $ 153.41
RECENT LOW   : $ 127.54
--------------------------------
RECOMMENDATION : Buy!

RECOMMENDATION REASON: (Reason)
--------------------------------

```
In addition to the summary and recommendation, the program will write a csv file containing the historical data of the stock for the last 100 days. This csv file will be called "symbol_prices.csv" (for e.g.: DIS_prices.csv) and can be found within the "data" folder of your repository. 

In addition to writing the historical stock prices to a CSV file, your program should also display a line graph of the stock prices over time. This graph should automaticlly open on your web browser, and can also be found within the "data" folder of your repository.

### Calculations and recommendations

The latest closing price = the stock's "close" price on the latest available day of trading data.
The recent high price = the maximum daily "high" price over approximately the past 100 available days of trading data.
The recent low price = the minimum daily "low" price over approximately the past 100 available days of trading data.

Based on an proprietary algorithm, the program will display its recommendation and reasnoning for that recommendation.

## Setup
Use GitHub Desktop software or the command-line to download or "clone" the repository onto your computer. Choose a familiar download location like the Desktop.

After cloning the repo, navigate there from the command-line: 

```sh
cd ~/Desktop/robo-advisor/app
```

## Prerequisits

First, create a new ".env" file in your repository.

### Stock Data API

Your program will need an API Key to issue requests to the AlphaVantage API. Get your own API Key by visiting: https://www.alphavantage.co/support/#api-key. Once you have your API Key, add the following contents to your .env file and edit it to work with your API Key.

```sh
ALPHAVANTAGE_API_KEY = "________(Your API key)________" 
```
### Email API

First, sign up for a free account at: https://signup.sendgrid.com/
Then click the link in a confirmation email to verify your account. 
Then create an API Key with "full access" permissions at: https://app.sendgrid.com/settings/api_keys

Store the API Key value in an environment variable called SENDGRID_API_KEY. Also set an environment variable called MY_EMAIL_ADDRESS to be the email address you just associated with your SendGrid account (e.g. "abc123@gmail.com").

```sh
SENDGRID_API_KEY = "________(Your API key)________" 
MY_EMAIL_ADDRESS = "________(Your email address)________" 
```

## Environment setup

Create and activate a new Anaconda virtual environment:

```sh
conda create -n stocks-env python=3.7 # (first time only)
conda activate stocks-env
```

From within the virtual environment, install the required packages specified in the "requirements.txt"

```sh
pip install -r requirements.txt
```

From within a virtual environment, install sendgrid:

```sh
pip install sendgrid==6.0.5
```

Once you have the entire program set-up, from within the virtual environment, demonstrate your ability to run the Python script from the command-line:

```sh
python app/robo-advisor.py
```