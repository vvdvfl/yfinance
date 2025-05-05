import yfinance as yf
import datetime
from datetime import datetime, timedelta


def get_historic_data_service(days: int = 15, stock: str = "SBIN"):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    data = yf.download(stock + ".NS", start=start_date, end=end_date)
    return data


def get_current_price(instrument_token):
    ticker = yf.Ticker(instrument_token + ".NS")  # NSE example (India)
    # Fetch current quote data
    info = ticker.fast_info
    current_price_yfinance = info["lastPrice"]  # This is the live market price
    # print("Current Price from yfinance:", current_price_yfinance)
    return current_price_yfinance