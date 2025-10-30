"""Stock-related Celery tasks."""

from typing import Any

import yfinance as yf
from celery import states
from celery.utils.log import get_task_logger
from sqlmodel import select

from tw.celery_app import celery_app
from tw.db import session_scope
from tw.model.stock import Stock


logger = get_task_logger(__name__)


@celery_app.task(bind=True, name="tw.stock.fetch", max_retries=3, default_retry_delay=60)
def fetch_stock_snapshot(self, stock_id: int) -> dict[str, Any]:
    """Fetch the latest stock metadata from Yahoo Finance."""

    with session_scope() as session:
        stock = session.get(Stock, stock_id)
        if stock is None:
            logger.warning("Stock %s not found for refresh", stock_id)
            return {"status": "not_found", "stock_id": stock_id}

        logger.info("Refreshing ticker %s (#%s)", stock.ticker, stock.id)

        try:
            ticker = yf.Ticker(stock.ticker)
            info = ticker.info or {}
        except Exception as exc:  # pragma: no cover - network errors
            logger.exception("yfinance lookup failed for %s", stock.ticker)
            raise self.retry(exc=exc)

        name = info.get("longName") or info.get("shortName") or stock.name
        exchange = info.get("exchange") or info.get("fullExchangeName") or stock.exchange

        stock.name = name
        stock.exchange = exchange
        session.add(stock)

        snapshot = {
            "status": "ok",
            "stock_id": stock.id,
            "ticker": stock.ticker,
            "exchange": stock.exchange,
            "name": stock.name,
        }

        logger.info("Updated ticker %s -> %s", stock.ticker, snapshot)
        self.update_state(state=states.SUCCESS, meta=snapshot)
        
        # Trigger earnings fetch after successful metadata update
        from tw.tasks.earnings import fetch_earnings_calls
        fetch_earnings_calls.delay(stock.id)
        
        return snapshot