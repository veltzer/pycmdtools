"""
Disk-persistent cache for JSON schemas fetched by URL.
Stores schemas as individual JSON files under ~/.cache/pycmdtools/schemas/.
"""
import hashlib
import json
import os
from pathlib import Path

import requests

CACHE_DIR = Path(os.path.expanduser("~/.cache/pycmdtools/schemas"))


def _url_to_filename(url: str) -> str:
    return hashlib.sha256(url.encode()).hexdigest() + ".json"


def _cache_path(url: str) -> Path:
    return CACHE_DIR / _url_to_filename(url)


def _read_entry(path: Path) -> dict:
    with open(path) as f:
        return json.load(f)


def fetch_schema(url: str, use_cache: bool, memory_cache: dict) -> dict:
    if url in memory_cache:
        return memory_cache[url]
    if use_cache:
        path = _cache_path(url)
        if path.exists():
            schema = _read_entry(path)
            memory_cache[url] = schema
            return schema
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    schema = response.json()
    memory_cache[url] = schema
    if use_cache:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        entry = {"url": url, "schema": schema}
        with open(_cache_path(url), "w") as f:
            json.dump(entry, f)
    return schema


def list_entries() -> list[tuple[str, str]]:
    if not CACHE_DIR.exists():
        return []
    results = []
    for path in sorted(CACHE_DIR.glob("*.json")):
        entry = _read_entry(path)
        results.append((entry["url"], str(path)))
    return results


def remove_entry(url: str) -> bool:
    path = _cache_path(url)
    if path.exists():
        path.unlink()
        return True
    return False


def clear_all() -> int:
    if not CACHE_DIR.exists():
        return 0
    count = 0
    for path in CACHE_DIR.glob("*.json"):
        path.unlink()
        count += 1
    return count
