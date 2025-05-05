import requests
import json
import pandas as pd
from flask import session
import re

def place_order(quantity, product, validity, price, instrument_token, order_type, transaction_type):
    url = "https://api-hft.upstox.com/v3/order/place"

    payload = {
        "quantity": quantity,
        "product": product,
        "validity": validity,
        "price": price,
        "tag": "string",
        "instrument_token": instrument_token,
        "order_type": order_type,
        "transaction_type": transaction_type,
        "disclosed_quantity": 0,
        "trigger_price": 0,
        "is_amo": False,
        "slice": True
    }
    access_token = session.get('access_token')


    headers = {
        'Content-Type': 'application/json', 'Authorization': access_token
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    return response.json()  # Returns JSON response instead of printing

def filter_instruments_with_pandas_filtered(trading_symbol):
    """
    Filters instruments from a JSON file using Pandas and stores the output in a variable.

    Parameters:
    - file_path (str): Path to the JSON file.
    - segment (str): The segment to filter by (e.g., "NSE_EQ", "NSE_FO").
    - instrument_type (str): The instrument type to filter by (e.g.,  ""EQ", "CE", "PE").
    - trading_symbol (str): The trading symbol to filter by (e.g., "RELIANCE" , "TCS 3550 CE 26 DEC 24").

    Returns:
    - list: Filtered JSON data as a list of dictionaries.
    """
    file_path = "complete.json"
    segment = "NSE_EQ"
    instrument_type = "EQ"
    try:
        # Load the JSON data from the file
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Convert the JSON data to a Pandas DataFrame
        df = pd.DataFrame(data)

        # Filter the DataFrame
        filtered_df = df[
            (df['segment'] == segment) &
            (df['instrument_type'] == instrument_type) &
            (df['trading_symbol'] == trading_symbol)
            ]

        # Convert the filtered DataFrame back to a JSON-compatible list of dictionaries
        filtered_json = filtered_df.to_dict(orient='records')

        return filtered_json

    except Exception as e:
        print(f"Error: {e}")
        return []


def send_request(url, method="GET", headers=None, payload=None):
    """
    Sends an HTTP request using the Requests library.

    :param url: The API endpoint URL.
    :param method: HTTP method (default is "GET").
    :param headers: Dictionary of headers (default is None).
    :param payload: Dictionary of data to send (default is None).
    :return: Response text from the request.
    """
    access_token = session.get('access_token')
    print(access_token)
    if headers is None:
        headers = {'Accept': 'application/json', 'Authorization': access_token}

    if payload is None:
        payload = {}

    response = requests.request(method, url, headers=headers, data=payload)
    return response.text



def get_trades_of_day(instruments_code, stock_name):
    # Example Usage
    api_url = "https://api.upstox.com/v2/order/trades/get-trades-for-day"
    api_response = send_request(api_url)
    # Example Usage
    trade_symbol = stock_name
    # matched_trade = find_trade_details(api_response, trade_symbol)
    # print(matched_trade)
    return send_request(api_url)



def find_trade_details(response, trade_symbol):
    """
    Iterates through the response data and returns details
    for the matching trade symbol.

    :param response: Dictionary containing trade data
    :param trade_symbol: The trading symbol to search for
    :return: Matching trade details or None if not found
    """
    return next((trade for trade in response.get("data", []) if re.search(trade_symbol, trade.get("trading_symbol"), re.IGNORECASE)), None)

