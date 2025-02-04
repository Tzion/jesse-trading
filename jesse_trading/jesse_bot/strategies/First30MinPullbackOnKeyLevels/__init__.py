from jesse.strategies import Strategy, cached
import jesse.indicators as ta
from jesse import utils
import jesse.services.logger as logger
from datetime import datetime as dt
import talib

"""
Mark the highs and low level based on the first 30 minutes of trading

Entry conditions:
- Level is breached by 1 full candle closed above the level
- Send order to the level - buy on pullback
- set stop when 1 minute candles is closing below the level
- 1:2 ratio
Buy (Sell) 

"""


TIME_IDX = 0
OPEN_IDX = 1
CLOSE_IDX = 2
HIGH_IDX = 3
LOW_IDX = 4
VOLUME_IDX = 5

class First30MinPullbackOnKeyLevels(Strategy):

    def __init__(self):
        super().__init__()
        self.risk_amount = 50
        self.proceed_stop = True
        self.max_open_trades = 3
        self.volume_lookback = 4
        self.volume_factor = 2
        

    def during_trading_hours(self):
        return '10:00' <= dt.fromtimestamp(self.candles[-1][TIME_IDX]/1000).time().strftime('%H:%M') <= '11:30'
    
    def break_up(self, level):
        high_volume = self.candles[:self.volume_lookback, VOLUME_IDX].mean() * self.volume_factor
        close_above_level = self.candles[-1][CLOSE_IDX] > level
        return high_volume and close_above_level

    def should_long(self) -> bool:

        self.resistance = max(self.candles[:30, HIGH_IDX])
        support = min(self.candles[:30, LOW_IDX])
        current = self.candles[-1]
        if self.during_trading_hours():
            if self.break_up(self.resistance):
                # if self.pullback(resistance):
                    self.go_long()

        current[TIME_IDX].time()
        dt.time


    def should_cancel_entry(self) -> bool:
        pass

    def go_long(self):
        # buy on the level, stop is lowest of last 4 candles, take profit is 2x stop
        self.stop_price = min(self.candles[:-5][LOW_IDX])
        self.stop_length = self.resistance - self.stop_price
        self.qty = self.risk_amount / self.stop_length
        position_size = self.qty * self.price
        self.buy = self.qty, self.resistance
        pass


    def on_open_position(self, order):
        pass

    def update_position(self):
        pass