import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from signal_generator import generate_signal
def ema_calculator(N,data):
    sma = data['Close'].rolling(window=N).mean()
    initial_EMA = sma.iloc[N - 1]
    EMA = pd.Series(np.nan,index = data.index)
    EMA.iat[N - 1] = initial_EMA
    alpha = 2 / (N + 1)
    for i in range(N,len(data)):
        prev_EMA = EMA.iloc[i - 1]
        close_price = data['Close'].iloc[i]
        EMA.iat[i] = close_price * alpha + prev_EMA * (1 - alpha)
    return EMA
def display_indicators(data):
        plt.figure(figsize = (12,6))
        plt.plot(data.index,data['MACD'],label = "MACD",color = "blue")
        plt.plot(data.index,data['Signal'],label = "Signal",color = "magenta")
        plt.title("MACD Vs Signal")
        plt.xlabel("Date")
        plt.ylabel("Value")
        plt.legend()
        plt.grid(True)
        plt.show()
        plt.figure(figsize = (12,6))
        plt.plot(data.index,data['Close'],label = "Close_Price",color = "red")
        plt.plot(data.index,data['UB'],label = "Upper_Band",color = "blue")
        plt.plot(data.index,data['LB'],label = "Lower_Band",color = "black")
        plt.title("Close_Price Vs Upper_Band Vs Lower_Band")
        plt.xlabel("Date")
        plt.ylabel("Value")
        plt.legend()
        plt.grid(True)
        plt.show()
        plt.figure(figsize = (12,6))
        plt.plot(data.index,data['Close'],label = "Close_Price",color = "blue")
        plt.plot(data.index,data['rsi'],label = "RSI",color = "red")
        plt.title("Close_Price Vs RSI")
        plt.xlabel("Date")
        plt.ylabel("Value")
        plt.legend()
        plt.grid(True)
        plt.show()

def create_indicators(data):
    delta = data['Close'].diff()
    gain = delta.where(delta > 0,0)
    loss = - delta.where(delta < 0,0)
    avg_gain = gain.rolling(window = 14).mean()
    avg_loss = loss.rolling(window = 14).mean()
    RS = avg_gain/avg_loss
    RSI = 100 - (100 / (1 + RS))
    data['rsi'] = RSI
    data['5_day_MA'] = data['Close'].rolling(window = 5).mean()
    data['50_day_MA'] = data['Close'].rolling(window = 50).mean()
    data['200_day_MA'] = data['Close'].rolling(window = 200).mean()
    data['avg_volume_5'] = data['Volume'].rolling(window = 5).mean()
    data['EMA_12_day'] = ema_calculator(12,data)
    data['EMA_26_day'] = ema_calculator(26,data)
    data['EMA_9_day'] = ema_calculator(9,data)
    data['MACD'] = data['EMA_12_day'] - data['EMA_26_day']
    data['MB'] = data['Close'].rolling(window = 20).mean()
    data['STD'] = data['Close'].rolling(window = 20).std()
    data['UB'] = data['MB'] + 2 * data['STD']
    data['LB'] = data['MB'] - 2 * data['STD'] 
    macd_temp = pd.DataFrame({'Close': data['MACD']})
    macd_no_nan = macd_temp['Close'].dropna()
    data['Signal'] = ema_calculator(9,pd.DataFrame({'Close' : macd_no_nan}))
    display_indicators(data)
    generate_signal(data)
    
 
 