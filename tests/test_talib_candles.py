import unittest
import talib
import numpy as np
import pandas as pd
import pandas_ta as pta

from jesse_trading import charts

class TestCandlesRegocnition(unittest.TestCase):

    def verify_pattern(self, pattern_func, candles, detection_idx=-1, force_chart=False, **pattern_func_args):
        open_prices = pd.Series(candles['open'])
        high_prices = pd.Series(candles['high'])
        low_prices = pd.Series(candles['low'])
        close_prices = pd.Series(candles['close'])
        pattern_detection = pattern_func(open_prices, high_prices, low_prices, close_prices, **pattern_func_args)
        last_candle_detection = pattern_detection.iloc[detection_idx] != 0
        print(pattern_detection)

        if not last_candle_detection:
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
            'open': [8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 7.9, 8.2, 9.4, 9],
            'high': [8.0, 8.8, 8.8, 8.8, 8.8, 8.8, 8.8, 8.8, 8.8, 9.0, 9.0, 10.5, 9.0],
            'low': [8.0, 7.5, 7.5, 7.5, 7.5, 7.5, 7.5, 7.5, 7.5, 7.8, 7.9, 9.2, 8.0],
            'close': [8.0, 8.5, 8.7, 8.7, 8.7, 8.7, 8.7, 8.7, 8.7, 8.1, 9.0, 9.2, 8.0]
        }
        self.verify_pattern(talib.CDLSHOOTINGSTAR, candles, detection_idx=-2)


    def test_pandas_ta_shooting_star(self):
        candles = {
            'open': pd.Series([ 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 7.9, 8.2, 9.4, 9.0]),
            'high': pd.Series([ 8.8, 8.8, 8.8, 8.8, 8.8, 8.8, 8.8, 8.8, 9.0, 9.0, 10.5, 9.0]),
            'low': pd.Series([ 7.5, 7.5, 7.5, 7.5, 7.5, 7.5, 7.5, 7.5, 7.8, 7.9, 9.2, 8.0]),
            'close': pd.Series([ 8.5, 8.7, 8.7, 8.7, 8.7, 8.7, 8.7, 8.7, 8.1, 9.0, 9.2, 8.0])
        }
        pattern_detection = pta.cdl_pattern(candles['open'], candles['high'], candles['low'], candles['close'], name='shootingstar', talib=False)
        last_candle_detection = pattern_detection.iloc[-2] != 0

        if not last_candle_detection.bool():
            print(pattern_detection)
            charts.plot_candles_simple(candles)
            self.fail("Pattern was not detected")
