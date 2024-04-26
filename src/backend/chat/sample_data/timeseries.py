import pandas as pd
import pandas_datareader as pdr
import yfinance as yf

def aapl_data(start_date, end_date):
  shares_df = yf.download('AAPL', start=start_date, end=end_date)
  return shares_df