import unittest
import numpy as np
from jesse_trading.analyzers.candle_patterns import IntraDayCandlePattern

class TestIntraDayCandlePattern(unittest.TestCase):
    def test_shooting_star(self):
        # Create dummy data
        open_prices = np.array([0.6192, 0.6114, 0.6155])
        high_prices = np.array([0.6194, 0.6157, 0.6172])
        low_prices = np.array([0.6055, 0.6108, 0.6146])
        close_prices = np.array([0.6114, 0.6156, 0.6162])
        volume = np.array([1000, 2000, 1500])

        # Call the function with the dummy data
        result = IntraDayCandlePattern.shooting_star(open_prices, high_prices, low_prices, close_prices, volume)

        # Check the result
        # This will depend on what you expect the function to return
        # For example, if you expect it to return an array of zeros:
        np.testing.assert_array_equal(result, np.array([0, 0, 0]))
