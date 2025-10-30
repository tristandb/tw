from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from tw.db import get_session
from tw.model.stock import Stock, StockCreate, StockRead
from tw.tasks import fetch_stock_snapshot


router = APIRouter(prefix="/api")


@router.get("/stocks", response_model=list[StockRead])
def list_stocks(session: Session = Depends(get_session)) -> list[Stock]:
    result = session.exec(select(Stock))
    return result.all()


@router.post("/stocks", response_model=dict[str, str], status_code=status.HTTP_202_ACCEPTED)
def create_stock(
    ticker: str, session: Session = Depends(get_session)
) -> dict[str, str]:
    """Create a new stock entry and immediately fetch its data from Yahoo Finance.
    
    Args:
        ticker: The stock ticker symbol (e.g., 'AAPL', 'GOOGL')
    """
    ticker = ticker.upper()
    existing = session.exec(select(Stock).where(Stock.ticker == ticker)).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ticker exists")

    # Create minimal stock entry with just the ticker
    stock = Stock(ticker=ticker)
    session.add(stock)
    session.commit()
    session.refresh(stock)

    # Immediately trigger data fetch
    task = fetch_stock_snapshot.delay(stock.id)
    return {
        "status": "accepted",
        "ticker": ticker,
        "stock_id": str(stock.id),
        "task_id": task.id
    }


@router.post(
    "/stocks/{stock_id}/start",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Trigger a stock refresh job",
)
def start_stock_refresh(
    stock_id: int, session: Session = Depends(get_session)
) -> dict[str, str]:
    stock = session.get(Stock, stock_id)
    if stock is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    task = fetch_stock_snapshot.delay(stock.id)
    return {"status": "accepted", "task_id": task.id}
