import unittest
import numpy as np
from jesse_trading.analyzers.candle_patterns import IntraDayCandlePattern
from jesse_trading.charts import plot_candles_simple as plot

class TestIntraDayCandlePattern(unittest.TestCase):
    def verify_pattern(self, candles, pattern_func, detection_idx=-1):
        recognition = pattern_func(candles['open'], candles['high'], candles['low'], candles['close'])
        expected = np.array([False] * len(candles['open']))
        expected[detection_idx] = True
        try:
            np.testing.assert_array_equal(recognition, expected)
        except AssertionError as e:
            plot(candles)
            self.fail(f"{e}: Pattern was not detected at index {detection_idx}")

    def test_shooting_star(self):
        candles = {
            'open': np.array([8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 7.9, 8.2, 9.0, 9]),
            'high': np.array([8.8, 8.8, 8.8, 8.8, 8.8, 8.8, 8.8, 8.8, 9.0, 9.0, 10.5, 9.0]),
            'low': np.array([7.5, 7.5, 7.5, 7.5, 7.5, 7.5, 7.5, 7.5, 7.8, 7.9, 9.2, 8.0]),
            'close': np.array([8.5, 8.7, 8.7, 8.7, 8.7, 8.7, 8.7, 8.7, 8.1, 9.0, 9.2, 8.0]),
        }
        self.verify_pattern(candles, IntraDayCandlePattern.shooting_star, -2)
    
