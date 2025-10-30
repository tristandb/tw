"""Tasks for fetching and processing earnings call data."""

from datetime import datetime
import logging
from typing import Any

import pandas as pd
import yfinance as yf
from celery import states
from celery.utils.log import get_task_logger
from sqlmodel import select

from tw.celery_app import celery_app
from tw.db import session_scope
from tw.model.earnings import EarningsCall
from tw.model.stock import Stock


logger = get_task_logger(__name__)


@celery_app.task(
    bind=True,
    name="tw.earnings.fetch",
    max_retries=3,
    default_retry_delay=60,
)
def fetch_earnings_calls(self, stock_id: int) -> dict[str, Any]:
    """Fetch the latest earnings call transcripts for a stock.
    
    This task is triggered after a successful stock metadata fetch.
    It will:
    1. Get basic earnings info from Yahoo Finance
    2. Fetch detailed transcripts (placeholder for now)
    3. Store in the database with proper fiscal period mapping
    """
    with session_scope() as session:
        stock = session.get(Stock, stock_id)
        if stock is None:
            logger.warning("Stock %s not found for earnings fetch", stock_id)
            return {"status": "not_found", "stock_id": stock_id}

        logger.info("Fetching earnings calls for %s (#%s)", stock.ticker, stock.id)

        try:
            ticker = yf.Ticker(stock.ticker)
            # Get historical earnings data
            earnings_history = ticker.get_earnings_history()
            logger.info("Earnings history for %s: %s", stock.ticker, earnings_history)
            
            if earnings_history is None:
                logger.info("No earnings history found for %s", stock.ticker)
                return {
                    "status": "no_data",
                    "stock_id": stock_id,
                    "ticker": stock.ticker,
                }
                
            if not isinstance(earnings_history, (list, pd.DataFrame)):
                logger.error("Unexpected earnings history type: %s", type(earnings_history))
                return {
                    "status": "error",
                    "stock_id": stock_id,
                    "ticker": stock.ticker,
                    "error": "Invalid data format"
                }
                
            # Convert DataFrame to records while preserving the index
            if isinstance(earnings_history, pd.DataFrame):
                # Reset index to make 'quarter' a regular column
                earnings_history = earnings_history.reset_index()
                earnings_records = earnings_history.to_dict('records')
            else:
                earnings_records = earnings_history

            # Process each earnings event
            earnings_added = 0
            for earning in earnings_records:
                # Log the earning record for debugging
                logger.debug("Processing earning record: %s", earning)
                
                try:
                    # Convert pandas Timestamp to datetime
                    report_date = pd.Timestamp(earning['quarter']).to_pydatetime()
                    
                    # Calculate fiscal period from the date
                    fiscal_quarter = ((report_date.month - 1) // 3) + 1
                    year = report_date.year
                    quarter = f"{year}Q{fiscal_quarter}"
                except (KeyError, ValueError) as e:
                    logger.warning("Failed to parse earnings data: %s", e)
                    continue
                
                # Check if we already have this earnings call
                existing = session.exec(
                    select(EarningsCall)
                    .where(EarningsCall.stock_id == stock_id)
                    .where(EarningsCall.quarter == quarter)
                ).first()
                
                if existing:
                    logger.debug("Earnings call for %s %s already exists", stock.ticker, quarter)
                    continue
                
                # Create new earnings call entry
                earnings_call = EarningsCall(
                    stock_id=stock_id,
                    date=report_date,
                    quarter=quarter,
                    fiscal_year=year,
                    fiscal_quarter=fiscal_quarter,
                    title=f"{stock.name} ({stock.ticker}) Q{fiscal_quarter} {year} Earnings Call",
                    content=f"Earnings Details:\n"
                           f"EPS Estimate: {earning['epsEstimate']}\n"
                           f"EPS Actual: {earning['epsActual']}\n"
                           f"EPS Difference: {earning['epsDifference']}\n"
                           f"Surprise %: {earning['surprisePercent'] * 100:.2f}%",
                )
                
                session.add(earnings_call)
                earnings_added += 1
            
            if earnings_added > 0:
                session.commit()
            
            result = {
                "status": "ok",
                "stock_id": stock_id,
                "ticker": stock.ticker,
                "earnings_added": earnings_added
            }
            
            logger.info("Added earnings call for %s: %s", stock.ticker, result)
            self.update_state(state=states.SUCCESS, meta=result)
            return result
            
        except Exception as exc:
            logger.exception("Earnings call fetch failed for %s", stock.ticker)
            raise self.retry(exc=exc)