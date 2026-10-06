import yfinance as yf
from sqlalchemy.dialects.postgresql import insert as pg_insert
from .db import SessionLocal
from .models_orm import OHLCV
from ..config import TICKERS

def ingest_ticker(ticker: str, period: str = "5y"):
    df = yf.download(ticker, period=period, auto_adjust=True)
    if df.empty:
        print(f"No data returned for {ticker}, skipping")
        return

    session = SessionLocal()
    rows = []
    for date, row in df.iterrows():
        rows.append({
            "ticker": ticker,
            "date": date.date(),
            "open": float(row["Open"].iloc[0]) if hasattr(row["Open"], "iloc") else float(row["Open"]),
            "high": float(row["High"].iloc[0]) if hasattr(row["High"], "iloc") else float(row["High"]),
            "low": float(row["Low"].iloc[0]) if hasattr(row["Low"], "iloc") else float(row["Low"]),
            "close": float(row["Close"].iloc[0]) if hasattr(row["Close"], "iloc") else float(row["Close"]),
            "volume": float(row["Volume"].iloc[0]) if hasattr(row["Volume"], "iloc") else float(row["Volume"]),
        })

    # Upsert: insert new rows, do nothing on conflict (ticker, date already exists)
    stmt = pg_insert(OHLCV).values(rows)
    stmt = stmt.on_conflict_do_nothing(index_elements=["ticker", "date"])
    session.execute(stmt)
    session.commit()
    session.close()
    print(f"Ingested/updated {len(rows)} rows for {ticker}")

def ingest_all():
    for ticker in TICKERS:
        ingest_ticker(ticker)

if __name__ == "__main__":
    ingest_all()