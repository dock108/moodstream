from fastapi import APIRouter
from pydantic import BaseModel

from ..services import get_supabase

router = APIRouter()


@router.get("/recommendations")
async def get_recommendations():
    """Return placeholder recommendations."""
    return {"recommendations": []}


class MoodRequest(BaseModel):
    mood: str


@router.post("/recommendations")
async def post_recommendations(payload: MoodRequest):
    """Accept a mood string and return placeholder recommendations."""
    return {"recommendations": [], "mood": payload.mood}


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
