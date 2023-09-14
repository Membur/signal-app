import my_candlestick  # Import the candlestick module


def detect_and_print_candlestick_patterns(data_dir):
    with open('datasets/symbols.csv') as f:
        for line in f:
            if "," not in line:
                continue
            symbol = line.split(",")[0]
            
            pattern_results = my_candlestick.detect_candlestick_patterns(symbol, data_dir)
            
            print(f"Candlestick Patterns for {symbol}:")
            for pattern, result in pattern_results.items():
                if result > 0:
                    print(f"{pattern}: Bullish")
                elif result < 0:
                    print(f"{pattern}: Bearish")
                else:
                    print(f"{pattern}: No signal")

if __name__ == "__main__":
    data_dir = 'C:/Users/Sean/Documents/Python Scripts/new-signal-printer/charts'
    detect_and_print_candlestick_patterns(data_dir)