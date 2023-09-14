# candlestick.py
import os
import talib
import pandas as pd

# Define candlestick patterns to detect
candlestick_patterns = {
    'CDL2CROWS': 'Two Crows',
    'CDL3BLACKCROWS': 'Three Black Crows',
    # Add more candlestick patterns as needed
}

# Function to detect candlestick patterns for a given symbol
def detect_candlestick_patterns(symbol, data_dir):
    pattern_results = {}
    
    # Load historical price data
    data_file = os.path.join(data_dir, '1wk-data', f'{symbol}_data.csv')
    if not os.path.exists(data_file):
        print(f"Data file for {symbol} not found. Skipping...")
        return pattern_results
    
    data = pd.read_csv(data_file, index_col=0)
    
    for pattern_code, pattern_name in candlestick_patterns.items():
        try:
            pattern_function = getattr(talib, pattern_code)
            pattern_results[pattern_name] = pattern_function(data['Open'], data['High'], data['Low'], data['Close']).iloc[-1]
        except Exception as e:
            print(f"Failed to detect {pattern_name} for {symbol}: {e}")
            pattern_results[pattern_name] = None
    
    return pattern_results
