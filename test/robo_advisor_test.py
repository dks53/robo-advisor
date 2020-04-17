# test/robo_advisor_test.py

import pytest
import os
import requests
import json
from datetime import datetime

from app.robo_advisor import to_usd, timestamp, get_url_data, user_input, get_latest_day, get_yesterday, get_highs 
from app.robo_advisor import get_lows, get_recommendation, get_reco_reason, write_to_csv, dict_to_list

# test to_usd
def test_to_usd():
    result = to_usd(13673.239020)
    assert result == "$ 13,673.24"
    '''
    Tests the to_usd function for formatting - displays the $ sign, 
    rounds to and displays 2 decimals and inserts thousands separator.
    '''

# test timestamp
def test_timestamp():
    datetime_example = datetime(2020, 4, 16, 18, 22, 36)
    assert timestamp(datetime_example) == "Request at: 2020-04-16 18:22:36"
    '''
    Tests the timestamp function by checking if a easily understandable date format is printed.
    Example: datetime(2020, 4, 16, 18, 22, 36)
    Result: 2020-04-16 18:22:36
    '''

# test get_url_data
def test_get_url_data():
    ticker = "MSFT"
    stock_data = get_url_data(ticker)
    assert stock_data["Meta Data"]["2. Symbol"] == ticker
    '''
    Tests the get URL function to see if a user selected stock exists on the API.
    Example: get_url_data("MSFT")
    Result: Dictionary with key value pairs including all the data from the API about the given stock.
    This test compares the API's "Meta Stock" and "Symbol" Keys and the corresponding stock symbol and passes if they are the same.
    '''

# test user_input
def test_user_input():
    selected_symbols = []
    feedback = user_input(selected_symbols)
    assert feedback == "You didn't input a stock ticker/symbol. At least one symbol is required to run this program."
    '''
    Tests the test_user_input function to see if the user has entered a stock. 
    If it sees an empty list, it alerts the user. If there are stocks in the list, it will let the user know as well.
    Example: feedback = user_input(selected_symbols)
    Result: You entered: ['MSFT','TSLA','GOOG']
    '''

# test dict_to_list
def test_dict_to_list():
    
    stock_data_dict = {
        'Meta Data': 
        {
            '1. Information': 'Daily Prices (open, high, low, close) and Volumes',
            '2. Symbol': 'TSLA',
            '3. Last Refreshed': '2020-04-16',
            '4. Output Size': 'Compact',
            '5. Time Zone': 'US/Eastern'
        }, 
        'Time Series (Daily)': 
        {
            '2020-04-16': {'1. open': '716.9400', '2. high': '759.4500', '3. low': '706.7150', '4. close': '745.2100', '5. volume': '19748358'},
            '2020-04-15': {'1. open': '742.0000', '2. high': '753.1300', '3. low': '710.0000', '4. close': '729.8300', '5. volume': '23577001'},
            '2020-04-14': {'1. open': '698.9700', '2. high': '741.8800', '3. low': '692.4300', '4. close': '709.8900', '5. volume': '30576511'},
            '2020-04-13': {'1. open': '590.1600', '2. high': '652.0000', '3. low': '580.5300', '4. close': '650.9500', '5. volume': '22475421'}
        }
    }

    tsd = stock_data_dict["Time Series (Daily)"]
    stock_data_list = []

    for date, stock_price in tsd.items():
        one_day = {
            "timestamp": date,
            "open": float(stock_price["1. open"]),
            "high": float(stock_price["2. high"]),
            "low": float(stock_price["3. low"]),
            "close": float(stock_price["4. close"]),
            "volume": float(stock_price["5. volume"])
        }
        stock_data_list.append(one_day)

        stock_data_list = [
            {'timestamp': '2020-04-16', 'open': 716.94, 'high': 759.45, 'low': 706.715, 'close': 745.21, 'volume': 19748358.0}, 
            {'timestamp': '2020-04-15', 'open': 742.0, 'high': 753.13, 'low': 710.0, 'close': 729.83, 'volume': 23577001.0}, 
            {'timestamp': '2020-04-14', 'open': 698.97, 'high': 741.88, 'low': 692.43, 'close': 709.89, 'volume': 30576511.0}, 
            {'timestamp': '2020-04-13', 'open': 590.16, 'high': 652.0, 'low': 580.53, 'close': 650.95, 'volume': 22475421.0}
        ]

        assert dict_to_list(stock_data_dict) == stock_data_list

    '''
    Tests the dict_to_list function so that the list can be used by other functions to perform calculations and make recommendations.
    Example: stock_data_dict = 
            '2020-04-16': {
                '1. open': '716.9400', 
                '2. high': '759.4500', 
                '3. low': '706.7150', 
                '4. close': '745.2100', 
                '5. volume': '19748358'
                }
    Result: [
        {'timestamp': '2020-04-16', 
        'open': 716.94, 
        'high': 759.45, 
        'low': 706.715, 
        'close': 745.21, 
        'volume': 19748358.0},
        ]
    '''

# test get_latest_day
def test_get_latest_day():
    all_days_example = [
        {'timestamp': '2020-04-16', 'open': 716.94, 'high': 759.45, 'low': 706.715, 'close': 745.21, 'volume': 19748358.0}, 
        {'timestamp': '2020-04-15', 'open': 742.0, 'high': 753.13, 'low': 710.0, 'close': 729.83, 'volume': 23577001.0}, 
        {'timestamp': '2020-04-14', 'open': 698.97, 'high': 741.88, 'low': 692.43, 'close': 709.89, 'volume': 30576511.0}, 
        {'timestamp': '2020-04-13', 'open': 590.16, 'high': 652.0, 'low': 580.53, 'close': 650.95, 'volume': 22475421.0}
    ]

    latest_day = get_latest_day(all_days_example)
    assert latest_day == {'timestamp': '2020-04-16', 'open': 716.94, 'high': 759.45, 'low': 706.715, 'close': 745.21, 'volume': 19748358.0}

    '''
    Tests the get_latest_day function which takes the first item in the stock data list and stores it in the variable "latest_day" 
    Example: feedback = get_latest_day(all_days)
    Result: {'timestamp': '2020-04-16', 'open': 716.94, 'high': 759.45, 'low': 706.715, 'close': 745.21, 'volume': 19748358.0}
    '''

# test get_yesterday
def test_get_yesterday():
    all_days_example = [
        {'timestamp': '2020-04-16', 'open': 716.94, 'high': 759.45, 'low': 706.715, 'close': 745.21, 'volume': 19748358.0}, 
        {'timestamp': '2020-04-15', 'open': 742.0, 'high': 753.13, 'low': 710.0, 'close': 729.83, 'volume': 23577001.0}, 
        {'timestamp': '2020-04-14', 'open': 698.97, 'high': 741.88, 'low': 692.43, 'close': 709.89, 'volume': 30576511.0}, 
        {'timestamp': '2020-04-13', 'open': 590.16, 'high': 652.0, 'low': 580.53, 'close': 650.95, 'volume': 22475421.0}
    ]

    yesterday = get_yesterday(all_days_example)
    assert yesterday == {'timestamp': '2020-04-15', 'open': 742.0, 'high': 753.13, 'low': 710.0, 'close': 729.83, 'volume': 23577001.0}

    '''
    Tests the get_yesterday function which takes the second item in the stock data list and stores it in the variable "yesterday" 
    Example: feedback = get_yesterday(all_days)
    Result: {'timestamp': '2020-04-15', 'open': 742.0, 'high': 753.13, 'low': 710.0, 'close': 729.83, 'volume': 23577001.0}
    '''
# test get_highs
def test_get_highs():
    all_days_example = [
        {'timestamp': '2020-04-16', 'open': 716.94, 'high': 759.45, 'low': 706.715, 'close': 745.21, 'volume': 19748358.0}, 
        {'timestamp': '2020-04-15', 'open': 742.0, 'high': 753.13, 'low': 710.0, 'close': 729.83, 'volume': 23577001.0}, 
        {'timestamp': '2020-04-14', 'open': 698.97, 'high': 741.88, 'low': 692.43, 'close': 709.89, 'volume': 30576511.0}, 
        {'timestamp': '2020-04-13', 'open': 590.16, 'high': 652.0, 'low': 580.53, 'close': 650.95, 'volume': 22475421.0}
    ]

    high_prices_list = []
    
    for one_day_example in all_days_example:
        one_day_high = one_day_example["high"]
        high_prices_list.append(one_day_high)
    
    assert high_prices_list == [759.45, 753.13, 741.88, 652.0]

    '''
    Tests the get_highs function which loops through the stock data list and 
    stores all the "high" prices in the list "high_prices_list"  
    Example: high_prices_list = get_highs(all_days)
    Result: [759.45, 753.13, 741.88, 652.0]
    '''

# test get_lows
def test_get_lows():
    all_days_example = [
        {'timestamp': '2020-04-16', 'open': 716.94, 'high': 759.45, 'low': 706.715, 'close': 745.21, 'volume': 19748358.0}, 
        {'timestamp': '2020-04-15', 'open': 742.0, 'high': 753.13, 'low': 710.0, 'close': 729.83, 'volume': 23577001.0}, 
        {'timestamp': '2020-04-14', 'open': 698.97, 'high': 741.88, 'low': 692.43, 'close': 709.89, 'volume': 30576511.0}, 
        {'timestamp': '2020-04-13', 'open': 590.16, 'high': 652.0, 'low': 580.53, 'close': 650.95, 'volume': 22475421.0}
    ]

    low_prices_list = []
    
    for one_day_example in all_days_example:
        one_day_low = one_day_example["low"]
        low_prices_list.append(one_day_low)
    
    assert low_prices_list == [706.715, 710.0, 692.43, 580.53]

    '''
    Tests the get_lows function which loops through the stock data list and 
    stores all the "low" prices in the list "low_prices_list"  
    Example: low_prices_list = get_lows(all_days)
    Result: [706.715, 710.0, 692.43, 580.53]
    '''

# test get_recommendation
def test_get_recommendation():
    latest_close_example = 45
    recent_high_example = 60
    recent_low_example = 40

    recommendation_decision = get_recommendation(latest_close_example,recent_high_example,recent_low_example)
    assert recommendation_decision == "Buy!"

    '''
    Tests the get_recommendation function which takes the latest_close, recent_high and recent_low values and 
    runs through calculations to make a recommendation on whether or not to buy the stock
    Example: get_recommendation(45, 60, 40)
    Result: "Buy!"
    '''

# test get_reco_reason
def test_get_reco_reason():
    latest_close_example = 45
    recent_high_example = 60
    recent_low_example = 40

    recommendation_reasoning = get_reco_reason(latest_close_example,recent_high_example,recent_low_example)
    assert recommendation_reasoning == "The stock's latest closing price is less than 20% above its recent low. Prices are likely to go up soon."

    '''
    Tests the get_recommendation function which takes the latest_close, recent_high and recent_low values and 
    runs through calculations to make a recommendation on whether or not to buy the stock
    Example: get_reco_reason(45, 60, 40)
    Result: "The stock's latest closing price is less than 20% above its recent low. Prices are likely to go up soon."
    '''

# test write_to_csv
def test_write_to_csv():
    
    sample_csv_file_path = os.path.join(os.path.dirname(__file__), "..", "test/test_csv", f"testing_prices.csv")

    all_days_example = [
        {'timestamp': '2020-04-16', 'open': 716.94, 'high': 759.45, 'low': 706.715, 'close': 745.21, 'volume': 19748358.0}, 
        {'timestamp': '2020-04-15', 'open': 742.0, 'high': 753.13, 'low': 710.0, 'close': 729.83, 'volume': 23577001.0}, 
        {'timestamp': '2020-04-14', 'open': 698.97, 'high': 741.88, 'low': 692.43, 'close': 709.89, 'volume': 30576511.0}, 
        {'timestamp': '2020-04-13', 'open': 590.16, 'high': 652.0, 'low': 580.53, 'close': 650.95, 'volume': 22475421.0}
    ]

    write_to_csv(sample_csv_file_path,all_days_example)
    
    '''
    Tests the write_to_csv function which takes the pre-decided file path and list of all stock data for a given 
    stock and sorts it into individual rows of a csv file, and saves it in the test_csv folder.
    Example: write_to_csv(csv_file_path, all_days)
    Result: Writes the csv file to the test_csv file.
    '''