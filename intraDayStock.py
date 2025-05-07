import yfinance as yf
import pandas as pd
import numpy as np

def fetch_intraday_data(symbol, interval="15m", lookback_days=1):
    df = yf.download(
        tickers=symbol,
        interval=interval,
        period=f"{lookback_days}d",
        progress=False
    )
    df = df.reset_index()
    df = df.rename(columns={"Datetime": "DateTime"})
    return df

def calculate_vwap(df):
    df['TPV'] = df['Close'] * df['Volume']
    df['CumVol'] = df['Volume'].cumsum()
    df['CumTPV'] = df['TPV'].cumsum()
    df['VWAP'] = df['CumTPV'] / df['CumVol']
    return df

def breakout_vwap_strategy(df):
    df = calculate_vwap(df)

    first_candle = df.iloc[0]
    high_break = first_candle['High']
    low_break = first_candle['Low']

    for i in range(1, len(df)):
        row = df.iloc[i]
        price = row['Close']
        vwap = row['VWAP']

        if price > high_break and price > vwap:
            return f"BUY at {price:.2f} (Break above {high_break:.2f}, VWAP: {vwap:.2f})"
        elif price < low_break and price < vwap:
            return f"SELL at {price:.2f} (Break below {low_break:.2f}, VWAP: {vwap:.2f})"

    return "NO TRADE"

# --- MAIN SCRIPT ---
if __name__ == "__main__":
    symbol = "TATAMOTORS.NS"  # NSE example, use "AAPL" for US stocks
    interval = "15m"           # Can be "5m", "15m"
    lookback_days = 1         # Only fetch today's data

    df = fetch_intraday_data(symbol, interval, lookback_days)

    if not df.empty:
        signal = breakout_vwap_strategy(df)
        print(f"Stock: {symbol} | Interval: {interval} => Signal: {signal}")
    else:
        print("No data fetched. Try again later or check the symbol.")
