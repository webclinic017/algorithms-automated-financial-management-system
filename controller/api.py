from fastapi import APIRouter
from controller.etf_controller import router as algo_router

router = APIRouter()
router.include_router(algo_router)
