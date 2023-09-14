import os
import yfinance as yf
import pandas as pd

def download_data(symbol, start_date, end_date):
    data = yf.download(symbol, start=start_date, end=end_date, interval="1wk")
    return data

def save_data(data, data_dir, symbol):
    data.to_csv(os.path.join(data_dir, '1wk-data', f'{symbol}_data.csv'))
