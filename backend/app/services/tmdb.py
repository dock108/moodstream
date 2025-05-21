"""Utilities for interacting with The Movie Database (TMDB) API."""

from __future__ import annotations

import os
import time
from typing import Any, Dict, List, Optional

import httpx

from ..config import settings

TMDB_BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"

# Predefined movie genre id map from TMDB
GENRES: Dict[int, str] = {
    28: "Action",
    12: "Adventure",
    16: "Animation",
    35: "Comedy",
    80: "Crime",
    99: "Documentary",
    18: "Drama",
    10751: "Family",
    14: "Fantasy",
    36: "History",
    27: "Horror",
    10402: "Music",
    9648: "Mystery",
    10749: "Romance",
    878: "Science Fiction",
    10770: "TV Movie",
    53: "Thriller",
    10752: "War",
    37: "Western",
}

# Mapping of mood/keywords to preferred genre names
MOOD_TO_GENRES: Dict[str, List[str]] = {
    "Happy": ["Comedy", "Family", "Romance"],
    "Sad": ["Drama"],
    "Excited": ["Action", "Adventure", "Thriller"],
    "Scared": ["Horror", "Thriller"],
    "Curious": ["Documentary", "Mystery"],
    "Fantastical": ["Fantasy", "Science Fiction"],
}

# simple in-memory cache for genre searches: mood -> (timestamp, results)
_CACHE: Dict[str, tuple[float, List[Dict[str, Any]]]] = {}
CACHE_TTL = 3600  # seconds


async def _request(path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Perform a GET request to TMDB and return the parsed JSON."""
    api_key = settings.tmdb_api_key or os.getenv("TMDB_API_KEY")
    if not api_key:
        raise RuntimeError("TMDB API key is not configured")

    url = f"{TMDB_BASE_URL}{path}"
    params = params or {}
    params["api_key"] = api_key
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params, timeout=10)
        if response.status_code == 404:
            raise ValueError("Not found")
        response.raise_for_status()
        return response.json()


def _parse_movie(data: Dict[str, Any]) -> Dict[str, Any]:
    """Convert TMDB movie payload to a simplified dict."""
    genres = [g["name"] for g in data.get("genres", [])]
    if not genres and data.get("genre_ids"):
        genres = [GENRES.get(gid) for gid in data["genre_ids"] if gid in GENRES]
    poster_path = data.get("poster_path")
    poster_url = f"{IMAGE_BASE_URL}{poster_path}" if poster_path else None
    release_date = data.get("release_date") or data.get("first_air_date") or ""

    return {
        "id": data.get("id"),
        "title": data.get("title") or data.get("name"),
        "year": release_date[:4] if release_date else None,
        "poster_url": poster_url,
        "genres": genres,
        "description": data.get("overview"),
    }


async def get_movie_by_id(tmdb_id: int) -> Dict[str, Any]:
    """Fetch a single movie by TMDB ID."""
    try:
        data = await _request(f"/movie/{tmdb_id}")
    except ValueError:
        raise
    return _parse_movie(data)


async def search_movies_by_genre_or_mood(mood: str) -> List[Dict[str, Any]]:
    """Return a list of movies that fit the given mood or genre."""
    key = mood.lower()
    now = time.time()
    cached = _CACHE.get(key)
    if cached and now - cached[0] < CACHE_TTL:
        return cached[1]

    # determine genre ids from mood
    genre_names = MOOD_TO_GENRES.get(mood.capitalize(), [mood.capitalize()])
    genre_ids = [gid for gid, name in GENRES.items() if name in genre_names]

    params: Dict[str, Any]
    if genre_ids:
        params = {
            "with_genres": ",".join(str(g) for g in genre_ids),
            "sort_by": "popularity.desc",
        }
        payload = await _request("/discover/movie", params=params)
    else:
        # fallback to keyword search
        params = {"query": mood, "include_adult": False}
        payload = await _request("/search/movie", params=params)

    movies = [_parse_movie(item) for item in payload.get("results", [])]
    _CACHE[key] = (now, movies)
    return movies
