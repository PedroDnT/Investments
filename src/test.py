from catch_clean import BrazilianIndicators
from analysis import AnalysisSerieDaily
import pandas as pd


ibov = pd.read_csv('../data/ibov.csv')
ibov['date'] = pd.to_datetime(ibov['date'])

ticker = ['Price ABEV3.SA']
tickers = ['Price ABEV3.SA', 'Price B3SA3.SA']

analysis = AnalysisSerieDaily(ibov)
analysis.normalize_time_series(tickers)
