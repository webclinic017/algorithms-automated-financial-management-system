from fastapi import APIRouter

router = APIRouter(
    prefix="/algorithms",
)

@router.post("/beetle-swarm-optimization")
async def compute_recommendation_using_bso():
    return {"algo": "BSO"}

@router.post("/invasive-weed-optimization")
async def compute_recommendation_using_iwo():
    return {"algo": "IWO"}
