import talib
import yfinance as yf


# Define indicator thresholds
rsi_oversold = 30
rsi_overbought = 70
macd_threshold = 0
stoch_oversold = 20
stoch_overbought = 80
cci_oversold = -100
cci_overbought = 100
mfi_oversold = 30
mfi_overbought = 70
min_volume=1000000


def get_most_recent_signal(data, rsi_check=True, macd_check=True, stoch_check=True, cci_check=True, mfi_check=True):
    signals = []

    # Calculate RSI
    if rsi_check:
        data['RSI'] = talib.RSI(data['Close'])
        rsi_buy_signal = (data['RSI'].iloc[-1] < rsi_oversold)
        rsi_sell_signal = (data['RSI'].iloc[-1] > rsi_overbought)
        signals.append(('RSI Buy', rsi_buy_signal))
        signals.append(('RSI Sell', rsi_sell_signal))

    # Calculate MACD
    if macd_check:
        data['MACD'], _, _ = talib.MACD(data['Close'])
        macd_buy_signal = (data['MACD'].iloc[-1] > macd_threshold)
        macd_sell_signal = (data['MACD'].iloc[-1] < macd_threshold)
        signals.append(('MACD Buy', macd_buy_signal))
        signals.append(('MACD Sell', macd_sell_signal))

    # Calculate Stochastic Oscillator
    if stoch_check:
        data['Stochastic_K'], data['Stochastic_D'] = talib.STOCH(data['High'], data['Low'], data['Close'])
        stoch_buy_signal = (data['Stochastic_K'].iloc[-1] < stoch_oversold)
        stoch_sell_signal = (data['Stochastic_K'].iloc[-1] > stoch_overbought)
        signals.append(('Stochastic Buy', stoch_buy_signal))
        signals.append(('Stochastic Sell', stoch_sell_signal))

    # Calculate Commodity Channel Index (CCI)
    if cci_check:
        data['CCI'] = talib.CCI(data['High'], data['Low'], data['Close'])
        cci_buy_signal = (data['CCI'].iloc[-1] < cci_oversold)
        cci_sell_signal = (data['CCI'].iloc[-1] > cci_overbought)
        signals.append(('CCI Buy', cci_buy_signal))
        signals.append(('CCI Sell', cci_sell_signal))

    # Calculate Money Flow Index (MFI)
    if mfi_check:
        data['MFI'] = talib.MFI(data['High'], data['Low'], data['Close'], data['Volume'])
        mfi_buy_signal = (data['MFI'].iloc[-1] < mfi_oversold)
        mfi_sell_signal = (data['MFI'].iloc[-1] > mfi_overbought)
        signals.append(('MFI Buy', mfi_buy_signal))
        signals.append(('MFI Sell', mfi_sell_signal))

    return signals
