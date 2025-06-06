import yfinance as yf

from indicators import create_indicators
def fetch_stock_data(ticker):
    ticker_obj = yf.Ticker(ticker)
    data = ticker_obj.history(period = "1y", interval="1d")
    create_indicators(data)
