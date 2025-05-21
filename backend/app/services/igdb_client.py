"""Utilities for querying the IGDB API."""

from __future__ import annotations

import time
from typing import Any, Dict, List, Optional

import httpx

from ..config import settings

_token: Optional[str] = None
_token_expiry: float = 0.0


async def _fetch_token() -> str:
    """Retrieve a new OAuth token from Twitch."""
    if not settings.twitch_client_id or not settings.twitch_client_secret:
        raise RuntimeError("Twitch credentials are not configured")

    data = {
        "client_id": settings.twitch_client_id,
        "client_secret": settings.twitch_client_secret,
        "grant_type": "client_credentials",
    }
    async with httpx.AsyncClient() as client:
        response = await client.post("https://id.twitch.tv/oauth2/token", data=data, timeout=10)
        response.raise_for_status()
        body = response.json()
    global _token, _token_expiry
    _token = body["access_token"]
    _token_expiry = time.time() + body.get("expires_in", 0)
    return _token


async def _get_token() -> str:
    """Return a cached OAuth token refreshing if necessary."""
    if _token and time.time() < _token_expiry - 60:
        return _token
    return await _fetch_token()


async def _igdb_request(endpoint: str, query: str) -> List[Dict[str, Any]]:
    token = await _get_token()
    headers = {
        "Client-ID": settings.twitch_client_id,
        "Authorization": f"Bearer {token}",
    }
    url = f"https://api.igdb.com/v4/{endpoint}"
    async with httpx.AsyncClient() as client:
        response = await client.post(url, data=query, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()


def _parse_game(data: Dict[str, Any]) -> Dict[str, Any]:
    title = data.get("name", "Unknown")
    genres = [g.get("name") for g in data.get("genres", []) if g.get("name")]
    cover = data.get("cover", {}).get("url")
    if cover and cover.startswith("//"):
        cover = "https:" + cover
    summary = data.get("summary", "")
    platforms = [p.get("name") for p in data.get("platforms", []) if p.get("name")]
    return {
        "id": data.get("id"),
        "title": title,
        "genres": genres or ["Unknown"],
        "cover_image": cover or None,
        "summary": summary,
        "platforms": platforms,
    }


async def get_game_by_id(igdb_id: int) -> Optional[Dict[str, Any]]:
    """Fetch a single game by its IGDB ID."""
    query = (
        f"fields id,name,genres.name,cover.url,summary,platforms.name; "
        f"where id = {igdb_id};"
    )
    results = await _igdb_request("games", query)
    if not results:
        return None
    return _parse_game(results[0])


async def search_games_by_genre_or_keyword(keyword: str) -> List[Dict[str, Any]]:
    """Search for games using a keyword or genre name."""
    query = (
        f'search "{keyword}"; '
        "fields id,name,genres.name,cover.url,summary,platforms.name; limit 5;"
    )
    results = await _igdb_request("games", query)
    return [_parse_game(game) for game in results]

