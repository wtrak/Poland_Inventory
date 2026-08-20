from __future__ import annotations

import re
from urllib.parse import urlsplit, urlunsplit

VINTED_ID = re.compile(r"/items/(\d+)")


def normalized_url(url: str) -> str:
    try:
        parts = urlsplit(url.strip())
        return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), parts.path.rstrip("/"), "", ""))
    except Exception:
        return (url or "").strip()


def listing_key(item: dict) -> str:
    url = normalized_url(str(item.get("source_url") or item.get("listing_url") or ""))
    marketplace = str(item.get("source") or item.get("marketplace") or "unknown").lower().strip()
    match = VINTED_ID.search(url)
    if match:
        return f"vinted:{match.group(1)}"
    explicit = item.get("listing_id")
    if explicit:
        return f"{marketplace}:{explicit}"
    return f"{marketplace}:{url}"


def dedupe(items: list[dict]) -> list[dict]:
    output = {}
    for item in items:
        key = listing_key(item)
        current = output.get(key)
        if current is None:
            output[key] = item
            continue
        current_score = int(current.get("score", current.get("score_if_accepted", 0)) or 0)
        new_score = int(item.get("score", item.get("score_if_accepted", 0)) or 0)
        if new_score >= current_score:
            output[key] = item
    return list(output.values())
