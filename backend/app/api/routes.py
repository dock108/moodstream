from fastapi import APIRouter

router = APIRouter()


@router.get("/recommendations")
async def get_recommendations():
    """Return placeholder recommendations."""
    return {"recommendations": []}
