from jesse.strategies import Strategy, cached
import jesse.indicators as ta
from jesse import utils
import jesse.services.logger as logger
import talib

"""
Rules: bullish engulfing candle when rsi is above 50 and price is above EMA 200
"""


OPEN_IDX = 1
CLOSE_IDX = 2
HIGH_IDX = 3
LOW_IDX = 4
VOLUME_IDX = 5

class HammerStrategy(Strategy):

    def __init__(self):
        super().__init__()
        self.risk_amount = 50
        self.proceed_stop = True
        self.max_open_trades = 3

    def should_long(self) -> bool:
        ema_200 = ta.ema(self.candles, period=200, source_type='close', sequential=True)
        rsi_9 = ta.rsi(self.candles, period=9, sequential=True)
        candle = self.candles[-1]

        # Rule 1: price is above EMA 200
        uptrend = candle[CLOSE_IDX] > ema_200[-1]
        downtrend = candle[CLOSE_IDX] < ema_200[-1]
        # Rule 2: RSI is above 50
        rsi_above_midpoint = rsi_9[-1] > 50
        # Rule 3: Bullish engulfing candle
        self.hammer = talib.CDLHAMMER(self.candles[-2:, OPEN_IDX], self.candles[-2:, HIGH_IDX], self.candles[-2:, LOW_IDX], self.candles[-2:, CLOSE_IDX])
        candles_body = abs(candle[CLOSE_IDX] - candle[OPEN_IDX])
        upper_wick = candle[HIGH_IDX] - max(candle[OPEN_IDX], candle[CLOSE_IDX])
        lower_wick = min(candle[OPEN_IDX], candle[CLOSE_IDX]) - candle[LOW_IDX]
        hammer_candle = upper_wick == 0 and 3 * candles_body < lower_wick
        if (hammer_candle and self.hammer[-1] == 0):
            logger.error(f"Mismatch of hammer candle")
        # Rule 4: candle is big but not too big
        atr = ta.atr(self.candles, period=30)
        tr = ta.trange(self.candles)
        right_size_candle = 2 * atr < tr #< 4 * atr

        self.engulfing = talib.CDLENGULFING(self.candles[-2:, OPEN_IDX], self.candles[-2:, HIGH_IDX], self.candles[-2:, LOW_IDX], self.candles[-2:, CLOSE_IDX])

        # Prices
        self.stop_length = 1 * (self.high - self.low)
        # self.take_profit_length = 1 * self.stop_length
        self.qty = self.risk_amount / self.stop_length
        position_size = self.qty * self.price

        # Entry Rule
        if (
            # uptrend and
            # rsi_above_midpoint and 
            hammer_candle and 
            right_size_candle
        ):
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
        self.pending_take_profit_1 = self.price + 1 * self.stop_length
        self.pending_take_profit_2 = self.price + 2 * self.stop_length


    def on_open_position(self, order):
        qty = self.position.qty
        self.stop_loss = qty, self.pending_stop_loss
        self.take_profit = [(qty/2, self.pending_take_profit_1), (qty/2, self.pending_take_profit_2)]

    def update_position(self):
        # proceed stop to entry price after movement of 1-risk
        if self.proceed_stop:
            if self.price - self.position.entry_price >= self.stop_length * 1.2 and self.stop_loss[0][1] != self.position.entry_price:
                logger.info(f"Proceeding stop to entry price")
                self.stop_loss = self.position.qty, self.position.entry_price

        if self.engulfing[-1] == -100:
            new_stop_loss = self.candles[-2][LOW_IDX]
            logger.info(f"Bearish engulfing candle detected - setting stop to {new_stop_loss}")
            self.stop_loss = new_stop_loss