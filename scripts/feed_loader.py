from __future__ import annotations

import json
from pathlib import Path
from urllib.request import Request, urlopen


def _dig(value, path: str):
    cur = value
    for part in (path or "").split("."):
        if not part:
            continue
        if isinstance(cur, dict):
            cur = cur.get(part)
        else:
            return None
    return cur


def load_permitted_json_feeds(config_path: Path, fx: dict) -> tuple[list[dict], dict]:
    try:
        configs = json.loads(config_path.read_text(encoding="utf-8"))
    except Exception:
        return [], {"approved_feeds": "configuration unavailable"}

    output = []
    status = {}
    for cfg in configs:
        name = cfg.get("name", "unnamed feed")
        if not cfg.get("enabled") or not cfg.get("automation_allowed") or not cfg.get("url"):
            continue
        if cfg.get("type") != "json":
            status[name] = "skipped: only explicit JSON feeds are supported automatically"
            continue
        try:
            req = Request(cfg["url"], headers={"User-Agent": "PolandInventoryRadar/1.0"})
            with urlopen(req, timeout=20) as response:
                payload = json.loads(response.read().decode("utf-8"))
            items = _dig(payload, cfg.get("items_path", "")) if cfg.get("items_path") else payload
            if not isinstance(items, list):
                raise ValueError("items_path did not resolve to a list")
            mapping = cfg.get("field_map", {})
            currency = cfg.get("currency", "PLN").upper()
            rate = fx["rates"][currency]
            for raw in items[: int(cfg.get("max_items_per_run", 100))]:
                ask = float(_dig(raw, mapping.get("asking_price", "price")) or 0)
                if ask <= 0:
                    continue
                output.append({
                    "source_url": str(_dig(raw, mapping.get("url", "url")) or ""),
                    "source": cfg.get("marketplace", name),
                    "marketplace": cfg.get("marketplace", name),
                    "country": cfg.get("country", ""),
                    "title": str(_dig(raw, mapping.get("title", "title")) or ""),
                    "category": cfg.get("category", "Uncategorized"),
                    "asking_price_local": ask,
                    "currency": currency,
                    "asking_price_usd": round(ask * float(rate["usd_per_unit"]), 2),
                    "asking_price_pln": round(ask * float(rate["pln_per_unit"]), 2),
                    "conservative_us_resale_usd": float(cfg.get("conservative_us_resale_usd", 0)),
                    "comp_count": int(cfg.get("comp_count", 0)),
                    "weight_g": float(cfg.get("weight_g", 9999)),
                    "source_side_costs_usd": float(cfg.get("source_side_costs_usd", 0)),
                    "notes": f"Imported from approved feed: {name}",
                })
            status[name] = f"OK ({len(items)} raw item(s))"
        except Exception as exc:
            status[name] = f"failed: {exc}"
    return output, status
