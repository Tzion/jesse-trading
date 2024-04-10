from jesse.strategies import Strategy, cached
import jesse.indicators as ta
from jesse import utils


OPEN_IDX = 1
CLOSE_IDX = 2
HIGH_IDX = 3
LOW_IDX = 4
VOLUME_IDX = 5

class EngulfingStrategy(Strategy):
    def should_long(self) -> bool:
        ema_200 = ta.ema(self.candles, period=200, source_type='close', sequential=True)
        rsi_9 = ta.rsi(self.candles, period=9, sequential=True)
        previous = self.candles[-2]
        current = self.candles[-1]
        assert current[CLOSE_IDX] == self.close
        assert current[OPEN_IDX] == self.open
        assert current[HIGH_IDX] == self.high
        assert current[LOW_IDX] == self.low

        # Rule 1: price is above EMA 200
        uptrend = current[CLOSE_IDX] > ema_200[-1]
        rsi_above_midpoint = rsi_9[-1] > 50
        # Rule 3: Bullish engulfing candle
        engulfing_candle = current[CLOSE_IDX] >= previous[OPEN_IDX] > previous[CLOSE_IDX] >= current[OPEN_IDX]
        return uptrend and rsi_above_midpoint and engulfing_candle

    def should_cancel_entry(self) -> bool:
        return False

    def go_long(self):
        # Calculate stop and profit levels
        stop = 2 * (self.high - self.low)
        take_profit = 2 * stop
        risk_in_usd = 20
        risk = risk_in_usd / self.price
        qty = risk_in_usd / stop

        # Place order
        self.buy = qty, self.price
        self.pending_stop_loss = self.price - stop
        self.pending_take_profit = self.price + take_profit

    def on_open_position(self, order):
        qty = self.position.qty
        self.stop_loss = qty, self.pending_stop_loss
        self.take_profit = qty, self.pending_take_profit
