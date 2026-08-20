from __future__ import annotations

import json
from pathlib import Path
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET

ECB_URL = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml"
TRACKED = {"EUR", "USD", "PLN", "CZK", "HUF", "RON", "GBP", "BGN"}


def load_json(path: Path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def refresh_fx(path: Path) -> tuple[dict, str | None]:
    existing = load_json(path, {})
    try:
        req = Request(ECB_URL, headers={"User-Agent": "PolandInventoryRadar/1.0"})
        with urlopen(req, timeout=20) as response:
            xml = response.read()
        root = ET.fromstring(xml)
        day = None
        raw = {"EUR": 1.0}
        for node in root.iter():
            if "time" in node.attrib:
                day = node.attrib["time"]
            currency = node.attrib.get("currency")
            rate = node.attrib.get("rate")
            if currency and rate:
                raw[currency] = float(rate)
        if not day or "USD" not in raw or "PLN" not in raw:
            raise ValueError("ECB response missing required rates")

        usd_per_eur = raw["USD"]
        pln_per_eur = raw["PLN"]
        rates = {}
        for currency in sorted(TRACKED):
            if currency not in raw:
                continue
            units_per_eur = raw[currency]
            rates[currency] = {
                "usd_per_unit": round(usd_per_eur / units_per_eur, 8),
                "pln_per_unit": round(pln_per_eur / units_per_eur, 8),
            }
        data = {
            "as_of": day,
            "source": "European Central Bank daily reference rates",
            "source_url": ECB_URL,
            "base_note": "1 EUR reference rates normalized into USD and PLN. Refreshed by the hourly workflow; ECB normally publishes once per business day.",
            "rates": rates,
        }
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        return data, None
    except Exception as exc:  # retain last known rates if ECB is temporarily unavailable
        return existing, f"FX refresh failed: {exc}"


def convert(amount: float, currency: str, fx: dict) -> tuple[float, float]:
    currency = currency.upper().strip()
    rate = fx.get("rates", {}).get(currency)
    if not rate:
        raise KeyError(f"No FX rate for {currency}")
    return amount * float(rate["usd_per_unit"]), amount * float(rate["pln_per_unit"])
