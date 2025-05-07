


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