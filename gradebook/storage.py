"""JSON persistence helpers for the gradebook.

Provides `load_data` and `save_data` which operate on a simple dict
structure: {"students": [...], "courses": [...], "enrollments": [...]}
"""
import json
import logging
from pathlib import Path
from typing import Dict, Any

LOGGER = logging.getLogger(__name__)


def default_path() -> Path:
    return Path("data") / "gradebook.json"


def load_data(path: Path | str | None = None) -> Dict[str, Any]:
    p = Path(path) if path else default_path()
    if not p.exists():
        LOGGER.info("Data file not found, starting with empty gradebook: %s", p)
        return {"students": [], "courses": [], "enrollments": []}
    try:
        with p.open("r", encoding="utf-8") as fh:
            return json.load(fh)
    except json.JSONDecodeError as exc:
        LOGGER.error("Failed to decode JSON from %s: %s", p, exc)
        raise


def save_data(data: Dict[str, Any], path: Path | str | None = None) -> None:
    p = Path(path) if path else default_path()
    p.parent.mkdir(parents=True, exist_ok=True)
    try:
        with p.open("w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2)
        LOGGER.info("Saved gradebook data to %s", p)
    except Exception:
        LOGGER.exception("Failed to save gradebook data to %s", p)
        raise
