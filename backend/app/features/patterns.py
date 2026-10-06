import pandas as pd
import talib

# Candlestick patterns to detect — name maps to the TA-Lib function
PATTERN_FUNCTIONS = {
    "doji": talib.CDLDOJI,
    "hammer": talib.CDLHAMMER,
    "hanging_man": talib.CDLHANGINGMAN,
    "engulfing": talib.CDLENGULFING,
    "morning_star": talib.CDLMORNINGSTAR,
    "evening_star": talib.CDLEVENINGSTAR,
    "shooting_star": talib.CDLSHOOTINGSTAR,
    "three_white_soldiers": talib.CDL3WHITESOLDIERS,
    "three_black_crows": talib.CDL3BLACKCROWS,
    "piercing_line": talib.CDLPIERCING,
    "dark_cloud_cover": talib.CDLDARKCLOUDCOVER,
    "harami": talib.CDLHARAMI,
    "spinning_top": talib.CDLSPINNINGTOP,
}

def detect_patterns(df: pd.DataFrame) -> pd.DataFrame:
    """
    df must have columns: open, high, low, close (lowercase, as stored in Postgres)
    Returns the same df with one new column per pattern.
    TA-Lib returns: 0 = no pattern, 100 = bullish signal, -100 = bearish signal
    """
    result = df.copy()
    o, h, l, c = result["open"], result["high"], result["low"], result["close"]

    for name, func in PATTERN_FUNCTIONS.items():
        result[f"pattern_{name}"] = func(o, h, l, c)

    return result