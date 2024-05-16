import numpy as np

class IntraDayCandlePattern():
    @staticmethod
    def shooting_star(open: np.array, high: np.array, low: np.array, close: np.array, **kwargs) -> np.array:
        lookback = kwargs.get('lookback', 10)
        real_body = np.abs(close - open)
        avg_real_body = np.convolve(real_body, np.ones(lookback) / lookback, 'valid')
        avg_real_body = np.pad(avg_real_body, (lookback-1, 0), constant_values=np.nan)
        upper_shadow = high - np.maximum(open, close)
        lower_shadow = np.minimum(open, close) - low
        prev_close = np.pad(close[:-1], (1,0), constant_values=np.nan)

        small_real_body = avg_real_body >= real_body * 3
        long_upper_shadow = upper_shadow >= real_body * 1.5
        very_short_lower_shadow = lower_shadow <= real_body * 0.1
        open_higher_equals_than_prev_close = open >= prev_close

        shooting_star = small_real_body & long_upper_shadow & very_short_lower_shadow & open_higher_equals_than_prev_close

        return shooting_star
