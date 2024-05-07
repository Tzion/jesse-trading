import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from analyzers.candle_patterns import is_bearish_reversal_pattern
import numpy as np

class TestReversalPattern(unittest.TestCase):
    def test_is_reversal_pattern(self):
        # Define the test candle data

        candles = np.array([
            [1629878400, 14.0, 15.0, 9.0, 10.0, 1000.0],
            [1629878400, 12.0, 14.0, 11.0, 13.0, 1000.0],
            [1629878400, 11.0, 13.0, 10.0, 12.0, 1000.0],
            [1629878400, 15.0, 16.0, 14.0, 17.0, 1000.0]
        ])

        OPEN_IDX = 1
        CLOSE_IDX = 2
        HIGH_IDX = 3
        LOW_IDX = 4
        VOLUME_IDX = 5

        # Call the function with the test data
        result = is_bearish_reversal_pattern(candles)

        # Assert the result
        self.assertTrue(result, "Reversal pattern not detected")

if __name__ == '__main__':
    unittest.main()