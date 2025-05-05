def calculate_fibonacci_buy_levels(data, stock):
    # print(data)
    high_price = data['High'].max()[stock]
    low_price = data['Low'].min()[stock]
    difference = high_price - low_price

    # levels = {
    #     '0%': low_price,
    #     '23.6%': high_price - 0.236 * difference,
    #     '38.2%': high_price - 0.382 * difference,
    #     '50%': (high_price + low_price) / 2,
    #     '61.8%': high_price - 0.618 * difference,
    #     '100%': high_price
    # }

    levels = {
        '0%': low_price,
        '23.6%': low_price + 0.236 * difference,
        '38.2%': low_price + 0.382 * difference,
        '50%': (high_price + low_price) / 2,
        '61.8%': low_price + 0.618 * difference,
        '100%': high_price,
        '161.8%': high_price + 0.618 * difference,
        '200%': high_price + 1.0 * difference,
        '261.8%': high_price + 1.618 * difference
    }
    return levels

def calculate_fibonacci_sell_levels(data, stock):
    high_price = data['High'].max()[stock]
    low_price = data['Low'].min()[stock]
    difference = high_price - low_price

    levels = {
        '0%': high_price,
        '23.6%': high_price - 0.236 * difference,
        '38.2%': high_price - 0.382 * difference,
        '50%': (high_price + low_price) / 2,
        '61.8%': high_price - 0.618 * difference,
        '100%': low_price,
        '161.8%': low_price - 0.618 * difference,
        '200%': low_price - 1.0 * difference,
        '261.8%': low_price - 1.618 * difference
    }
    return levels
