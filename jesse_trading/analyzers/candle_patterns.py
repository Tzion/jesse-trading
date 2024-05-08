import numpy as np

class IntraDayCandlePattern():
    @staticmethod
    def shooting_star(open: np.array, high: np.array, low: np.array, close: np.array, volume: np.array, **kwargs) -> np.array:
        lookback = kwargs.get('lookback', 1)
        lookforward = kwargs.get('lookforward', 0)

        # check if the candle is a shooting star
        shooting_star = np.where(
            (high[:-lookforward] - open[:-lookforward] > 2 * (open[:-lookforward] - close[:-lookforward])) &
            (high[:-lookforward] - close[:-lookforward] > 2 * (open[:-lookforward] - close[:-lookforward])) &
            (high[:-lookforward] - low[:-lookforward] > 3 * (open[:-lookforward] - close[:-lookforward])) &
            (volume[:-lookforward] > volume[:-lookforward].mean()), 100, 0
        )
        pass

