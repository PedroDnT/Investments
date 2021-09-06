from analysis import StockPrice
import pandas as pd

ibov_tickers = pd.read_csv('../data/ibov_tickers.csv')

analysis = StockPrice()
analysis.candlestick(ibov_tickers.iloc[0])