# test/robo_advisor_test.py

import pytest
import os
import requests
import json
from datetime import datetime

from app.robo_advisor import to_usd, timestamp, get_url_data, user_input, get_latest_day, get_yesterday, get_highs, get_lows, get_recommendation, get_reco_reason

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

# TODO
#def test_dict_to_list():

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

# test get_recommendation
def test_get_recommendation():
    latest_close_example = 45
    recent_high_example = 60
    recent_low_example = 40

    recommendation_decision = get_recommendation(latest_close_example,recent_high_example,recent_low_example)
    assert recommendation_decision == "Buy!"

# test get_reco_reason
def test_get_reco_reason():
    latest_close_example = 45
    recent_high_example = 60
    recent_low_example = 40

    recommendation_reasoning = get_reco_reason(latest_close_example,recent_high_example,recent_low_example)
    assert recommendation_reasoning == "The stock's latest closing price is less than 20% above its recent low. Prices are likely to go up soon."

# TODO
#def test_write_to_csv():