import pandas as pd
import numpy as np

# Define the indicators
def moving_average(price, period):
    return price.rolling(window=period).mean()

def relative_strength_index(price, period):
    delta = price.diff()
    up, down = delta.copy(), delta.copy()
    up[up < 0] = 0
    down[down > 0] = 0
    roll_up = up.rolling(window=period).mean()
    roll_down = down.rolling(window=period).mean().abs()
    RS = roll_up / roll_down
    RSI = 100.0 - (100.0 / (1.0 + RS))
    return RSI

def bollinger_bands(price, period, std_dev):
    ma = moving_average(price, period)
    std = price.rolling(window=period).std()
    upper_bb = ma + std_dev * std
    lower_bb = ma - std_dev * std
    return upper_bb, lower_bb

# Generate trade signals
def generate_trade_signals(price, trend, ma_50, ma_200, rsi, upper_bb, lower_bb):
    if trend == 'up' and ma_50 > ma_200 and rsi < 30 and price > lower_bb:
        return 'buy'
    elif trend == 'down' and ma_50 < ma_200 and rsi > 70 and price < upper_bb:
        return 'sell'
    else:
        return None

# Example usage
price_data = pd.read_csv('price_data.csv')
price = price_data['close']
trend = 'up'  # or 'down'

ma_50 = moving_average(price, 50)
ma_200 = moving_average(price, 200)
rsi = relative_strength_index(price, 14)
upper_bb, lower_bb = bollinger_bands(price, 20, 2)

trade_signal = generate_trade_signals(price, trend, ma_50, ma_200, rsi, upper_bb, lower_bb)

print(trade_signal)
