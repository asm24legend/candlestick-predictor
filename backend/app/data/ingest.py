import yfinance as yf
from .db import SessionLocal
from .models_orm import OHLCV

def ingest_ticker(ticker: str, period: str = "5y"):
    df = yf.download(ticker, period=period)
    session = SessionLocal()
    for date, row in df.iterrows():
        record = OHLCV(
            ticker=ticker,
            date=date.date(),
            open=float(row["Open"]),
            high=float(row["High"]),
            low=float(row["Low"]),
            close=float(row["Close"]),
            volume=float(row["Volume"]),
        )
        session.add(record)
    session.commit()
    session.close()
    print(f"Ingested {len(df)} rows for {ticker}")

if __name__ == "__main__":
    ingest_ticker("AAPL")