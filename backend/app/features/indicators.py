import pandas as pd
import talib

def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    df must have columns: open, high, low, close, volume
    """
    result = df.copy()
    c = result["close"]
    h = result["high"]
    l = result["low"]
    v = result["volume"]

    result["rsi_14"] = talib.RSI(c, timeperiod=14)
    macd, macd_signal, macd_hist = talib.MACD(c, fastperiod=12, slowperiod=26, signalperiod=9)
    result["macd"] = macd
    result["macd_signal"] = macd_signal
    result["macd_hist"] = macd_hist

    upper, middle, lower = talib.BBANDS(c, timeperiod=20, nbdevup=2, nbdevdn=2)
    result["bb_upper"] = upper
    result["bb_middle"] = middle
    result["bb_lower"] = lower
    result["bb_position"] = (c - lower) / (upper - lower)  # 0 = at lower band, 1 = at upper band

    result["atr_14"] = talib.ATR(h, l, c, timeperiod=14)

    result["sma_10"] = talib.SMA(c, timeperiod=10)
    result["sma_20"] = talib.SMA(c, timeperiod=20)
    result["sma_50"] = talib.SMA(c, timeperiod=50)
    result["ema_10"] = talib.EMA(c, timeperiod=10)

    result["volume_change_pct"] = v.pct_change() * 100
    result["volume_avg_20"] = v.rolling(window=20).mean()

    return result