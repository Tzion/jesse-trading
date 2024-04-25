from jesse.strategies import Strategy, cached
import jesse.indicators as ta
from jesse import utils
import jesse.services.logger as logger
import talib


OPEN_IDX = 1
CLOSE_IDX = 2
HIGH_IDX = 3
LOW_IDX = 4
VOLUME_IDX = 5

class EngulfingStrategy(Strategy):

    def __init__(self):
        super().__init__()
        self.risk_amount = 50
        self.proceed_stop = False
        self.max_open_trades = False

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
        downtrend = current[CLOSE_IDX] < ema_200[-1]
        # Rule 2: RSI is above 50
        rsi_above_midpoint = rsi_9[-1] > 50
        # Rule 3: Bullish engulfing candle
        engulfing_candle = current[CLOSE_IDX] >= previous[OPEN_IDX] > previous[CLOSE_IDX] >= current[OPEN_IDX]
        # engulfing_candle = current[CLOSE_IDX] > previous[HIGH_IDX] and previous[LOW_IDX] >= current[OPEN_IDX] and previous[OPEN_IDX] > previous[CLOSE_IDX]
        # Rule 4: TR is greater than 2 * ATR
        atr = ta.atr(self.candles, period=30)
        tr = ta.trange(self.candles)
        big_candle = tr > 2 * atr

        # Prices
        self.stop_length = 1 * (self.high - self.low)
        self.take_profit_length = 2 * self.stop_length
        self.qty = self.risk_amount / self.stop_length
        position_size = self.qty * self.price

        # Entry Rule
        if uptrend and rsi_above_midpoint and engulfing_candle and big_candle:
            if position_size > 0.4 * self.portfolio_value:
                logger.error(f"Position size of {self.symbol} is too large: {position_size}")
                return False
            if position_size > self.balance:
                logger.error(f"Position size of {self.symbol} is greater than balance: {self.balance}")
                return False
            if self.trades_count >= self.max_open_trades and self.max_open_trades:
                logger.error(f"Max open trades reached: {self.trades_count}")
                return False
            return True

    def should_cancel_entry(self) -> bool:
        pass

    def go_long(self):
        # logger.info('open trades {}'.format(self.trades_count))
        self.buy = self.qty, self.price
        # Prapare prices for next orders (can be placed only after order execution)
        self.pending_stop_loss = self.price - self.stop_length
        self.pending_take_profit = self.price + self.take_profit_length


    def on_open_position(self, order):
        qty = self.position.qty
        self.stop_loss = qty, self.pending_stop_loss
        self.take_profit = qty, self.pending_take_profit

    def update_position(self):
        # proceed stop to entry price after movement of 1-risk
        if self.proceed_stop:
            if self.price - self.position.entry_price >= self.stop_length:
                self.stop_loss = self.position.qty, self.position.entry_price