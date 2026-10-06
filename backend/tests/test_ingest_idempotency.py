# backend/tests/test_config.py
from app.config import TICKERS

def test_tickers_not_empty():
    assert len(TICKERS) > 0

def test_tickers_are_strings():
    assert all(isinstance(t, str) for t in TICKERS)