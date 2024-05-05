import mplfinance as mpf
import pandas as pd

def plot_candles_simple(candles):
    df = pd.DataFrame(candles)

    # Convert the index to a datetime index (required by mplfinance)
    if df.index.dtype != 'datetime64[ns]':
        df.index = pd.date_range(start=pd.Timestamp.today().strftime('%Y-%m-%d'), periods=len(df))

    mpf.plot(df, type='candle', style='charles', title='Candlestick Chart', ylabel='Price')