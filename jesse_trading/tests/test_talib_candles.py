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
            'open': [170.92, 187.07, 174.15, 175.47],
            'high': [182.87, 190.78, 196.48, 184.68],
            'low': [170.10, 176.94, 170.13, 169.16],
            'close': [170.70, 177.32, 192.34, 169.30]
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
        print(engulfing_pattern)

        # Assert the result
        if not last_candle_engulfing:
            charts.plot_candles_simple(candles)
            self.fail("Engulfing candle pattern was not detected")



if __name__ == '__main__':
    unittest.main()
