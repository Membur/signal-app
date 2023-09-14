import os
import talib
import plotly.graph_objs as go
from my_candlestick import detect_and_print_candlestick_patterns # Replace 'my_candlestick' with your actual filename
from indicators.indicators import get_most_recent_signal, rsi_oversold, rsi_overbought, macd_threshold, stoch_oversold, stoch_overbought, cci_oversold, cci_overbought, mfi_oversold, mfi_overbought, min_volume
from data.data import download_data, save_data
from charts.charts import generate_chart
import yfinance as yf

def main():
    data_dir = 'C:/Users/Sean/Documents/Python Scripts/new-signal-printer/charts'
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(os.path.join(data_dir, '1wk-charts'), exist_ok=True)
    os.makedirs(os.path.join(data_dir, '1wk-data'), exist_ok=True)

    with open('datasets/symbols.csv') as f:
        for line in f:
            if "," not in line:
                continue
            symbol = line.split(",")[0]

            try:
                data = download_data(symbol, start_date="2022-10-01", end_date="2023-08-09")
                save_data(data, data_dir, symbol)

                signals = get_most_recent_signal(data, rsi_check=True, macd_check=True, stoch_check=True, cci_check=True, mfi_check=True)

                generate_chart(
                    symbol,
                    data,
                    data_dir,
                    signals,
                    min_volume=1000000,
                    min_indicators=1,
                    rsi_check=True,
                    macd_check=True,
                    stoch_check=True,
                    cci_check=True,
                    mfi_check=True
                    
                )

            except Exception as e:
                print(f"Failed to generate chart for symbol {symbol}: {e}")


if __name__ == "__main__":
    main()
