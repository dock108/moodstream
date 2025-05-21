"""Supabase client utilities."""

from __future__ import annotations

import os
from typing import Optional

from supabase import Client, create_client

_supabase: Optional[Client] = None


def get_supabase() -> Client:
    """Return a cached Supabase client using service role credentials."""
    global _supabase

    if _supabase is None:
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
        if not url or not key:
            raise RuntimeError("Supabase credentials are not configured")
        _supabase = create_client(url, key)
    return _supabase
