import yfinance as yf 

ticker = yf.Ticker("TCS.NS")
data = ticker.history(period ="1y",interval ="1d")
print(data.head())