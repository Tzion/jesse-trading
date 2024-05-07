import unittest
import talib
import numpy as np
import pandas_ta as pta

import sys
import os
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import charts

class TestEngulfingCandles(unittest.TestCase):

    def verify_pattern(self, pattern_func, candles, force_chart=False):
        open_prices = np.array(candles['open'])
        high_prices = np.array(candles['high'])
        low_prices = np.array(candles['low'])
        close_prices = np.array(candles['close'])
        pattern_detection = pattern_func(open_prices, high_prices, low_prices, close_prices)
        pattern_detection = pta.cdl_pattern(open_prices, high_prices, low_prices, close_prices, name='shooting_star')
        last_candle_detection = pattern_detection[-1] != 0

        if not last_candle_detection:
            print(pattern_detection)
            charts.plot_candles_simple(candles)
            self.fail("Pattern was not detected")
        if force_chart:
            charts.plot_candles_simple(candles)


    def test_engulfing_candle(self):
        candles = {
            'open': [ 7.9, 8.0, 7.2],
            'high': [ 8.8, 9.7, 9.4],
            'low': [7.1, 7.0, 7.1 ],
            'close': [ 7.7, 7.3, 9.3]
        }
        self.verify_pattern(talib.CDLENGULFING, candles)


    def test_shooting_star(self):
        candles = {
            'open': [8.0, 7.9, 8.2, 9.5, 9],
            'high': [8.8, 9.0, 8.7, 11.9, 7.2],
            'low': [7.5, 7.8, 7.9, 9.7, 6.9],
            'close': [8.2, 8.1, 9.0, 9.0, 6.9]
        }
        self.verify_pattern(talib.CDLSHOOTINGSTAR, candles, True)

if __name__ == '__main__':
    unittest.main()
