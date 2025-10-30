from fastapi import FastAPI

from tw.db import init_db
from tw.api.stock import router as stock_router


app = FastAPI()
app.include_router(stock_router)

@app.on_event("startup")
def on_startup() -> None:
    init_db()

