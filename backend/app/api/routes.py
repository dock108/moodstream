from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import date
import logging

from ..services import (
    get_supabase,
    get_game_by_id,
    search_games_by_genre_or_keyword,
    get_movie_by_id,
    search_movies_by_genre_or_mood,
)
from ..services.recommender import recommend_for_mood

logger = logging.getLogger(__name__)
analytics = {"calls_per_day": {}, "mood_counts": {}}

router = APIRouter()


@router.get("/recommendations")
async def get_recommendations():
    """Return placeholder recommendations."""
    return {"recommendations": []}


class MoodRequest(BaseModel):
    mood: str


@router.post("/recommendations")
async def post_recommendations(payload: MoodRequest):
    """Accept a mood string and return AI-driven recommendations."""
    today = date.today().isoformat()
    analytics["calls_per_day"][today] = analytics["calls_per_day"].get(today, 0) + 1
    analytics["mood_counts"][payload.mood] = analytics["mood_counts"].get(payload.mood, 0) + 1
    logger.info("Generating recommendations for mood '%s'", payload.mood)
    try:
        recs = await recommend_for_mood(payload.mood)
    except Exception:
        logger.exception("Recommendation generation failed")
        raise HTTPException(status_code=500, detail="Failed to generate recommendations")

    return {"recommendations": recs, "mood": payload.mood}


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

  
@router.get("/tmdb/movie/{tmdb_id}")
async def tmdb_movie(tmdb_id: int):
    """Fetch movie metadata from TMDB."""
    try:
        movie = await get_movie_by_id(tmdb_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Movie not found")
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to fetch movie data")
    return movie


@router.get("/tmdb/search")
async def tmdb_search(mood: str):
    """Search for movies by mood or genre."""
    try:
        return await search_movies_by_genre_or_mood(mood)
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to search movies")
