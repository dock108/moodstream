import logging
from datetime import date
from typing import Dict

logger = logging.getLogger(__name__)

_analytics: Dict[str, Dict[str, int]] = {
    "calls_per_day": {},
    "mood_counts": {},
}


def record_mood(mood: str) -> None:
    """Update analytics counters for a given mood."""
    today = date.today().isoformat()
    _analytics["calls_per_day"][today] = _analytics["calls_per_day"].get(today, 0) + 1
    _analytics["mood_counts"][mood] = _analytics["mood_counts"].get(mood, 0) + 1
    logger.info("Generating recommendations for mood '%s'", mood)


def get_analytics() -> Dict[str, Dict[str, int]]:
    """Return the in-memory analytics dictionary."""
    return _analytics
