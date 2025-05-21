"""GPT-4 powered recommendation logic."""

from __future__ import annotations

import json
import os
from typing import Any, Dict, List, Optional

from ..config import settings
from .tmdb import search_movie_by_title, search_movies_by_genre_or_mood
from .igdb_client import search_games_by_genre_or_keyword


async def get_gpt_recommendations(mood: str) -> List[Dict[str, Any]]:
    """Return raw GPT-4 recommendations for the provided mood."""
    try:
        import openai  # type: ignore
    except Exception as exc:  # pragma: no cover - openai missing
        raise RuntimeError("openai package is required") from exc

    api_key = settings.gpt_api_key or os.getenv("GPT_API_KEY") or os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OpenAI API key is not configured")

    openai.api_key = api_key
    messages = [
        {
            "role": "system",
            "content": (
                "You are an entertainment recommendation engine. "
                "Given a user's mood, return exactly three JSON objects in a list. "
                "Each object must have: type (movie or game), title, genre, reason."
            ),
        },
        {"role": "user", "content": mood},
    ]

    response = await openai.ChatCompletion.acreate(
        model="gpt-4",
        messages=messages,
        temperature=0.7,
    )

    text = response["choices"][0]["message"]["content"]
    try:
        data = json.loads(text)
        if isinstance(data, dict):
            data = [data]
    except Exception as exc:  # pragma: no cover - network parsing errors
        raise ValueError("Invalid GPT response") from exc

    return data


async def _validate_item(item: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Validate a GPT recommendation against TMDB/IGDB."""
    typ = item.get("type", "").lower()
    title = item.get("title", "")
    reason = item.get("reason", "")

    if typ in {"movie", "film"}:
        movie = await search_movie_by_title(title)
        if movie:
            return {
                "title": movie["title"],
                "type": "movie",
                "genre": ", ".join(movie.get("genres", [])),
                "reason": reason,
                "metadata": movie,
            }

    if typ in {"game", "video game"}:
        games = await search_games_by_genre_or_keyword(title)
        if games:
            game = games[0]
            return {
                "title": game["title"],
                "type": "game",
                "genre": ", ".join(game.get("genres", [])),
                "reason": reason,
                "metadata": game,
            }

    return None


async def fallback_recommendations(mood: str) -> List[Dict[str, Any]]:
    """Simple fallback using TMDB genre search."""
    movies = await search_movies_by_genre_or_mood(mood)
    recs: List[Dict[str, Any]] = []
    for movie in movies[:3]:
        recs.append(
            {
                "title": movie["title"],
                "type": "movie",
                "genre": ", ".join(movie.get("genres", [])),
                "reason": f"Popular {', '.join(movie.get('genres', []))} movie for mood '{mood}'.",
                "metadata": movie,
            }
        )
    return recs


async def recommend_for_mood(mood: str) -> List[Dict[str, Any]]:
    """Generate and validate recommendations for a mood."""
    try:
        raw = await get_gpt_recommendations(mood)
    except Exception:
        return await fallback_recommendations(mood)

    validated: List[Dict[str, Any]] = []
    for item in raw:
        valid = await _validate_item(item)
        if valid:
            validated.append(valid)
        if len(validated) == 3:
            break

    if not validated:
        return await fallback_recommendations(mood)

    return validated


async def recommend(user_id: str) -> List[Dict[str, Any]]:
    """Legacy placeholder."""
    return await fallback_recommendations("Happy")
