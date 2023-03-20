from fastapi import FastAPI
import logging

from repository.etf_repository import ETFRepository
from datetime import datetime

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


if __name__ == "main":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s: %(message)s")
    repository = ETFRepository()

    lista = repository.get_all()
    price_history_list = lista[0].get_price_history()
    last_price_timestamp = price_history_list[len(price_history_list) - 1]["timestamp"]
    print(last_price_timestamp)
    print(datetime.fromtimestamp(last_price_timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S'))

    now = datetime.now().timestamp()
    print(now)
    print(datetime.fromtimestamp(now).strftime('%Y-%m-%d %H:%M:%S'))
