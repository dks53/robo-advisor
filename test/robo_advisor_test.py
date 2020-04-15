# test/robo_advisor_test.py

import pytest
import os
import requests
import json
from datetime import datetime

from app.robo_advisor import to_usd, timestamp, get_url_data, user_input

# test to_usd
def test_to_usd():
    result = to_usd(13673.239020)
    assert result == "$ 13,673.24"
    '''
    Tests the to_usd function for formatting - displays the $ sign, rounds to and displays 2 decimals and inserts thousands separator.
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

def test_get_url_data():
    sample_symbol = "TSLA"
    parsed_response = get_url_data(sample_symbol)
    assert parsed_response["Meta Data"]["2. Symbol"] == sample_symbol

#def test_user_input():
#    user_input(selected_symbols)
#    assert print("You didn't input a stock ticker/symbol. At least one symbol is required to run this program.")
