import logging

from fastapi import FastAPI

from controller.api import router as api_router
from repository.etf_repository import ETFRepository
from service.etf_service import ETFService

if __name__ == "main":
    app = FastAPI()
    app.include_router(api_router)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s: %(message)s")
    repository = ETFRepository()
    service = ETFService(repository)
