import pandas as pd
from sqlalchemy import text
from ..data.db import engine
from .patterns import detect_patterns
from .indicators import add_indicators

def load_ticker(ticker: str) -> pd.DataFrame:
    query = text("SELECT date, open, high, low, close, volume FROM ohlcv WHERE ticker = :ticker ORDER BY date")
    df = pd.read_sql(query, engine, params={"ticker": ticker})
    df.set_index("date", inplace=True)
    return df

if __name__ == "__main__":
    df = load_ticker("AAPL")
    print(f"Loaded {len(df)} rows for AAPL")

    df = detect_patterns(df)
    df = add_indicators(df)

    # Show rows where any pattern fired (non-zero)
    pattern_cols = [c for c in df.columns if c.startswith("pattern_")]
    fired = df[(df[pattern_cols] != 0).any(axis=1)]
    print(f"\n{len(fired)} rows had at least one pattern fire")
    print(fired[pattern_cols + ["rsi_14", "macd"]].tail(10))