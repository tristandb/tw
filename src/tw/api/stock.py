from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from tw.db import get_session
from tw.model.stock import Stock, StockCreate, StockRead


router = APIRouter(prefix="/api")


@router.get("/stocks", response_model=list[StockRead])
def list_stocks(session: Session = Depends(get_session)) -> list[Stock]:
    result = session.exec(select(Stock))
    return result.all()


@router.post("/stocks", response_model=StockRead, status_code=status.HTTP_201_CREATED)
def create_stock(
    stock_in: StockCreate, session: Session = Depends(get_session)
) -> Stock:
    existing = session.exec(
        select(Stock).where(Stock.ticker == stock_in.ticker.upper())
    ).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ticker exists")

    stock = Stock.model_validate(stock_in)
    stock.ticker = stock.ticker.upper()
    session.add(stock)
    session.commit()
    session.refresh(stock)
    return stock
