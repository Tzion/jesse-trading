from jesse.strategies import Strategy, cached
from jesse import utils
import jesse.indicators as ta
import jesse.services.logger as logger
from datetime import datetime



TIME_IDX = 0
OPEN_IDX = 1
CLOSE_IDX = 2
HIGH_IDX = 3
LOW_IDX = 4
VOLUME_IDX = 5

DAY_START_TIME = '00:00'

class FibRetracement(Strategy):

    def __init__(self) -> None:
        super().__init__()
        self.reversal_day = None

    def before(self):
        daily_candles = self.get_candles(self.exchange, self.symbol, '1D')
        self.start_of_day = daily_candles[-1][TIME_IDX]
        self.yest_high = daily_candles[-2][HIGH_IDX]
        self.yest_low = daily_candles[-2][LOW_IDX]
        logger.info(f"yest_high: {self.yest_high}, yest_low: {self.yest_low}")
        
        ema_fast = ta.ema(daily_candles, 20, sequential=True)
        ema_meduim = ta.ema(daily_candles, 70, sequential=True)
        ema_slow = ta.ema(daily_candles, 200, sequential=True)
        self.trend_up = ema_fast[-1] > ema_meduim[-1] #> ema_slow[-1]
        self.trend_down = ema_fast[-1] < ema_meduim[-1]# < ema_slow[-1]

        self.yest_range = abs(self.yest_high - self.yest_low)
        if self.trend_up:
            self.fib_38 = self.yest_high - self.yest_range * 0.382
            self.fib_50 = self.yest_high - self.yest_range * 0.5
            self.fib_61 = self.yest_high - self.yest_range * 0.618

        if self.trend_down:
            self.fib_38 = self.yest_low + self.yest_range * 0.382
            self.fib_50 = self.yest_low + self.yest_range * 0.5
            self.fib_61 = self.yest_low + self.yest_range * 0.618
            if self.candles[-1][LOW_IDX] <= self.yest_low and datetime.fromtimestamp(self.candles[-1][TIME_IDX]/1000).date() != self.reversal_day:
                highest = self.candles[-1][HIGH_IDX]
                lowest = self.candles[-1][LOW_IDX]
                i = -2
                while self.candles[i][TIME_IDX] >= self.start_of_day:
                    highest = max(self.candles[i][HIGH_IDX], highest)
                    lowest = min(self.candles[i][LOW_IDX], lowest)
                    i -= 1
                self.reversal_day = datetime.fromtimestamp(self.candles[-1][TIME_IDX]/1000).date()
                if highest >= self.fib_61:
                    logger.info("reversal higher than 61.8%")
                elif highest <= self.fib_38:
                    logger.info("reversal lower than 38.2%")
                else:
                    logger.info("reversal in beetween fibo levels")
                if lowest >= self.yest_low:
                    logger.info("reversal low is higher than yesterday's low")
                logger.info(f"reversal took {i} candles")
        
        
        
    def should_long(self) -> bool:
        # if self.trend_down:
        #     if self.candles[-1][LOW_IDX] <= self.yest_low:
        #         i = -2
        #         while self.candles[i][TIME_IDX] >= self.start_of_day:
        #             if self.candles[i][LOW_IDX] < self.yest_low or self.candles[i][HIGH_IDX] > self.fib_61:
        #                 logger.error(f"Low of candle {i} is below yesterday's low or high is above 61.8%")
        #                 return
        #             else: 
        #                 i -= 1
        #         logger.info("candles in range")
        return False

    
    def go_long(self):
        pass

    
    def should_short(self) -> bool:
        daily_open = self.get_candles(self.exchange, self.symbol,'1D')[-1][OPEN_IDX] 
        open_around_yesterdays_low = daily_open + self.yest_range * 0.1 <= daily_open <= daily_open - self.yest_range * 0.1
        reversal_pattern = None # TODO 

        if self.trend_down and open_around_yesterdays_low and reversal_pattern:
            return True

        return False

    
    def go_short(self):
        # For futures trading only
        pass

    
    def should_cancel_entry(self) -> bool:
        return True