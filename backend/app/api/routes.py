from fastapi import APIRouter
from pydantic import BaseModel

from ..services import (
    get_supabase,
    get_game_by_id,
    search_games_by_genre_or_keyword,
)

router = APIRouter()


@router.get("/recommendations")
async def get_recommendations():
    """Return placeholder recommendations."""
    return {"recommendations": []}


class AuthRequest(BaseModel):
    email: str
    password: str


@router.post("/auth/signup")
async def signup(payload: AuthRequest):
    """Create a new user using Supabase auth."""
    sb = get_supabase()
    result = sb.auth.sign_up({"email": payload.email, "password": payload.password})
    return {"user": result.user}


@router.post("/auth/login")
async def login(payload: AuthRequest):
    """Log in a user and return the session."""
    sb = get_supabase()
    result = sb.auth.sign_in_with_password({"email": payload.email, "password": payload.password})
    return {"session": result.session, "user": result.user}


@router.get("/games/{igdb_id}")
async def game_by_id(igdb_id: int):
    game = await get_game_by_id(igdb_id)
    return {"game": game}


@router.get("/games/search")
async def search_games(q: str):
    results = await search_games_by_genre_or_keyword(q)
    return {"results": results}
