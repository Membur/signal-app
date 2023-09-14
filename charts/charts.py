import os
import plotly.graph_objs as go
from indicators.indicators import get_most_recent_signal
import yfinance as yf

def generate_chart(symbol, start_date, end_date, data_dir, min_volume, min_indicators=1, rsi_check=True, macd_check=True, stoch_check=True, cci_check=True, mfi_check=True):
    data = yf.download(symbol, start=start_date, end=end_date, interval="1wk")

    # Check the minimum volume threshold
    if data['Volume'].iloc[-1] < min_volume:
        print(f"Volume for {symbol} is below the minimum threshold. Skipping...")
        return


    signals = get_most_recent_signal(data, rsi_check, macd_check, stoch_check, cci_check, mfi_check)

    # Check if at least min_indicators indicators generated signals
    active_signals = [indicator for indicator, signal in signals if signal]
    if len(active_signals) < min_indicators:
        print(f"Not enough active signals ({len(active_signals)}) for {symbol}. Skipping...")
        return

    data.to_csv(os.path.join(data_dir, '1wk-data', f'{symbol}_data.csv'))

    fig = go.Figure()

    candlestick = go.Candlestick(
        x=data.index.astype(str),
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        name='Candlestick',
        increasing_line_color='green',
        decreasing_line_color='red'
    )

    fig.add_trace(candlestick)

    vertical_offset = 0  # Initialize vertical offset

    for indicator, signal in signals:
        if 'Buy' in indicator and signal:
            signal_arrow = go.Scatter(
                x=[data.index[-1]],
                y=[data['Low'].iloc[-1] + vertical_offset],  # Apply vertical offset
                mode='markers+text',
                marker=dict(symbol='triangle-up', size=12, color='green'),
                text=['BUY'],
                textposition="bottom center",
                name=f'{indicator} Signal'
            )

            fig.add_trace(signal_arrow)

            vertical_offset += 0.5  # Adjust the vertical offset for the next indicator

        if 'Sell' in indicator and signal:
            signal_arrow = go.Scatter(
                x=[data.index[-1]],
                y=[data['Low'].iloc[-1] - vertical_offset],  # Apply vertical offset
                mode='markers+text',
                marker=dict(symbol='triangle-down', size=12, color='red'),
                text=['SELL'],
                textposition="bottom center",
                name=f'{indicator} Signal'
            )

            fig.add_trace(signal_arrow)

            vertical_offset += 0.5  # Adjust the vertical offset for the next indicator

    title_text = f'<a href="https://www.tradingview.com/symbols/{symbol}/" target="_blank">{symbol}</a> 1 Week Signals'

    fig.update_layout(
        title=title_text,
        xaxis_title="Date",
        yaxis_title="Price",
        showlegend=True,
        template='plotly_dark'
    )

    chart_file = os.path.join(data_dir, '1wk-charts', f'{symbol}_signals_1wk.html')
    fig.write_html(chart_file)
    print(f"Chart saved as {chart_file}")
