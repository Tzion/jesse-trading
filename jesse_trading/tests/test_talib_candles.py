import unittest
import talib
import numpy as np
import matplotlib.pyplot as plt
import numpy as np

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import charts

class TestEngulfingCandles(unittest.TestCase):
    def test_engulfing_candle(self):
        # Define the test candle data

        candles = {
            'open': [ 7.9, 8.0, 7.2,],
            'high': [ 8.8, 9.7, 9.4, ],
            'low': [7.1, 7.0, 7.1, ],
            'close': [ 7.7, 7.3, 9.3,]
        }


        # Convert the candle data to numpy arrays
        open_prices = np.array(candles['open'])
        high_prices = np.array(candles['high'])
        low_prices = np.array(candles['low'])
        close_prices = np.array(candles['close'])

        # Calculate the engulfing pattern using TA-Lib
        engulfing_pattern = talib.CDLENGULFING(open_prices, high_prices, low_prices, close_prices)

        # Check if the last candle is engulfing
        last_candle_engulfing = engulfing_pattern[-1] != 0

        # Assert the result
        if not last_candle_engulfing:
            charts.plot_candles_simple(candles)
            self.fail("Engulfing candle pattern was not detected")



if __name__ == '__main__':
    unittest.main()
