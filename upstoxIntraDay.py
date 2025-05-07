import requests
import pandas as pd

# ---- Method 1: Fetch intraday historical candle data ----
def fetch_upstox_candles():
    url = "https://api.upstox.com/v3/historical-candle/intraday/NSE_EQ|INE155A01022/minutes/1"

    headers = {
        'Api-Version': '2.0',
        'Accept': 'application/json',
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJrZXlfaWQiOiJza192MS4wIiwiYWxnIjoiSFMyNTYifQ.eyJzdWIiOiI0WUFQTjIiLCJqdGkiOiI2ODE5ODkzNTlmMzI1YjVjM2Y0NTUzYTciLCJpc011bHRpQ2xpZW50IjpmYWxzZSwiaXNQbHVzUGxhbiI6ZmFsc2UsImlhdCI6MTc0NjUwMzk4OSwiaXNzIjoidWRhcGktZ2F0ZXdheS1zZXJ2aWNlIiwiZXhwIjoxNzQ2NTY4ODAwfQ.eJJaCYl6DPp89w-sPcQ1Qh_oX3wEnAK17fGHUAaAWy0',
        'Cookie': '__cf_bm=oySnv_Nu9ZR72RurgYI4cvxJN_5wZVWXfF0YVsQbPYg-1746505847-1.0.1.1-pFD_v3E0eTbjJkTZcawfOZrxImKmp0hcNGpXui_9DZdHoJ8q2yy6BxTfFL3ep79E'
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Error fetching data: {response.status_code} - {response.text}")

    candles = response.json()["data"]["candles"]
    df = pd.DataFrame(candles, columns=["timestamp", "open", "high", "low", "close", "volume", "ignored"])
    df = df.sort_values("timestamp").reset_index(drop=True)
    return df

# ---- Method 2: Apply breakout + VWAP-based intraday strategy ----
def apply_intraday_strategy(df):
    print(df)
    if len(df) < 2:
        return "NOT_ENOUGH_DATA", None

    # Calculate VWAP
    df["tpv"] = df["close"] * df["volume"]
    df["cum_vol"] = df["volume"].cumsum()
    df["cum_tpv"] = df["tpv"].cumsum()
    df["vwap"] = df["cum_tpv"] / df["cum_vol"]

    first = df.iloc[-2]   # Previous candle
    second = df.iloc[-1]  # Latest candle
    vwap = second["vwap"]

    # Strategy logic
    if second["close"] > first["high"] and second["close"] > vwap:
        signal = "BUY"
    elif second["close"] < first["low"] and second["close"] < vwap:
        signal = "SELL"
    else:
        signal = "NO TRADE"

    return signal, {
        "prev_high": first["high"],
        "prev_low": first["low"],
        "close": second["close"],
        "vwap": vwap
    }

# ---- Main Execution ----
if __name__ == "__main__":
    try:
        df = fetch_upstox_candles()
        signal, details = apply_intraday_strategy(df)

        print(f"\n--- TRADE DECISION ---")
        print(f"Signal: {signal}")
        if details:
            print(f"Prev High: {details['prev_high']}, Prev Low: {details['prev_low']}")
            print(f"Current Close: {details['close']}, VWAP: {details['vwap']:.2f}")
    except Exception as e:
        print(f"Error: {e}")
