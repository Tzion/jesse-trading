import talib


OPEN_IDX = 1
CLOSE_IDX = 2
HIGH_IDX = 3
LOW_IDX = 4

def is_reversal_pattern(candles):
    patterns = [
        talib.CDLENGULFING,
        talib.CDLHARAMI,
        talib.CDLHARAMICROSS,
        talib.CDLDOJI,
        talib.CDLDOJISTAR,
        talib.CDLDRAGONFLYDOJI,
        talib.CDLEVENINGDOJISTAR,
        talib.CDLEVENINGSTAR,
        talib.CDLHAMMER,
        talib.CDLHANGINGMAN,
        talib.CDLINVERTEDHAMMER,
        talib.CDLKICKING,
        talib.CDLKICKINGBYLENGTH,
        talib.CDLLADDERBOTTOM,
        talib.CDLLONGLEGGEDDOJI,
        talib.CDLLONGLINE,
        talib.CDLMARUBOZU,
        talib.CDLMATCHINGLOW,
        talib.CDLMORNINGDOJISTAR,
        talib.CDLMORNINGSTAR,
        talib.CDLPIERCING,
        talib.CDLRICKSHAWMAN,
        talib.CDLRISEFALL3METHODS,
        talib.CDLSEPARATINGLINES,
        talib.CDLSHOOTINGSTAR,
        talib.CDLSHORTLINE,
        talib.CDLSPINNINGTOP,
        talib.CDLSTALLEDPATTERN,
        talib.CDLSTICKSANDWICH,
        talib.CDLTAKURI,
        talib.CDLTASUKIGAP,
        talib.CDLTHRUSTING,
        talib.CDLTRISTAR,
        talib.CDLUNIQUE3RIVER,
        talib.CDLUPSIDEGAP2CROWS,
        talib.CDLXSIDEGAP3METHODS
    ]
    for pattern in patterns:
        result = pattern(candles[:, OPEN_IDX], candles[:, HIGH_IDX], candles[:, LOW_IDX], candles[:, CLOSE_IDX])
        if result[-1] != 0:
            return True
    return False
