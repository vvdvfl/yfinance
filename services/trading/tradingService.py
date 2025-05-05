from services.upstox.upstoxService import *
from services.yfinance.service import *
from stratagy.Fibonacci import *
from datetime import datetime


def trading_service(payload):    # print(access_token)
    stock_name = payload.get('stock_type')
    automated = payload.get('automated')
    instruments_code = filter_instruments_with_pandas_filtered(stock_name)
    action = payload.get('action')
    quantity = payload.get('quantity')
    historical_data = get_historic_data_service(7, stock_name)
    buy_levels = calculate_fibonacci_buy_levels(historical_data, stock_name + ".NS")
    sell_levels = calculate_fibonacci_sell_levels(historical_data, stock_name + ".NS")
    # get curret price from yfinance
    current_price_yfinance = get_current_price(stock_name)
    order_status = ""
    action_taken = action
    automated_action = "MANUAL" if automated == False else "AUTOMATED"

    if current_price_yfinance >= buy_levels['61.8%']:
        # action = "Buy Signal (Enter Long)"
        if action == "buy" or automated == True:
            action_taken = "BUY"
            order_response = place_order(quantity, "D", "DAY", current_price_yfinance, instruments_code, "MARKET", action_taken)
            print("*********************BUY**************************")
            print(order_response)
            order_status = order_response['status']
        action = "Buy"
    elif current_price_yfinance <= sell_levels['61.8%']:
        # action = "Strong Sell Signal (Enter Short)
        if action == "sell" or automated == True:
            action_taken = "SELL"
            order_response = place_order(quantity, "D", "DAY", current_price_yfinance, instruments_code, "MARKET", action_taken)
            print("*********************SELL**************************")
            print(order_response)
            order_status = order_response['status']
        action = "Strong Sell"
    elif current_price_yfinance <= sell_levels['161.8%']:
        # action = "Sell Extension Hit – Consider Full Exit or Trail SL"
        if action == "sell" or automated == True:
            action_taken = "SELL"
            order_response = place_order(quantity, "D", "DAY", current_price_yfinance, instruments_code, "MARKET", action_taken)
            print(order_response)
            order_status = order_response['status']
        action = "Full exit(SL)"

    else:
        action_taken = "NO ACTION"
        action = "No strong signal"

    action_taken = automated_action + " " + action_taken
    current_datetime = datetime.now()
    current_datetime_formated = current_datetime.strftime("%d-%m-%Y %H:%M:%S")
    levels = {
        "message": action,
        "dateTime": current_datetime_formated,
        "currentPrice": current_price_yfinance,
        "buy_levels": buy_levels,
        "sell_levels": sell_levels,
        "stock_name": stock_name,
        "action_taken": action_taken,
        "order_status": order_status
    }
    #get_trades_of_day(instruments_code, stock_name)
    return levels
