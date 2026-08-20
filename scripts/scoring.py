from __future__ import annotations


def _clamp(value, low, high):
    return max(low, min(high, value))


def evidence_points(comp_count: int) -> int:
    if comp_count >= 3:
        return 30
    if comp_count == 2:
        return 20
    if comp_count == 1:
        return 10
    return 0


def spread_points(total_source_usd: float, conservative_resale_usd: float) -> int:
    if conservative_resale_usd <= 0:
        return 0
    ratio = total_source_usd / conservative_resale_usd
    if ratio <= 0.10:
        return 25
    if ratio <= 0.15:
        return 20
    if ratio <= 0.20:
        return 15
    if ratio <= 0.30:
        return 5
    return 0


def shipping_points(weight_g: float) -> int:
    if weight_g < 100:
        return 20
    if weight_g <= 200:
        return 16
    if weight_g <= 500:
        return 10
    if weight_g <= 1000:
        return 5
    return 0


def score_candidate(candidate: dict, settings: dict) -> int:
    ask = float(candidate.get("asking_price_usd", 0) or 0)
    source_costs = float(candidate.get("source_side_costs_usd", 0) or 0)
    resale = float(candidate.get("conservative_us_resale_usd", 0) or 0)
    comps = int(candidate.get("comp_count", 0) or 0)
    weight = float(candidate.get("weight_g", 9999) or 9999)
    repeatability = int(candidate.get("repeatability_points", settings.get("default_repeatability_points", 10)) or 0)
    simplicity = int(candidate.get("simplicity_points", settings.get("default_reseller_simplicity_points", 5)) or 0)
    return int(
        evidence_points(comps)
        + spread_points(ask + source_costs, resale)
        + shipping_points(weight)
        + _clamp(repeatability, 0, 15)
        + _clamp(simplicity, 0, 10)
    )


def score_label(score: int) -> str:
    if score >= 90:
        return "STRONG BUY"
    if score >= 80:
        return "BUY"
    if score >= 65:
        return "WATCH"
    if score >= 50:
        return "RESEARCH"
    return "PASS"


def offer_math(candidate: dict, settings: dict) -> dict:
    ask = float(candidate.get("asking_price_usd", 0) or 0)
    resale = float(candidate.get("conservative_us_resale_usd", 0) or 0)
    source_costs = float(candidate.get("source_side_costs_usd", 0) or 0)
    target_pct = float(settings.get("target_source_cost_pct", 0.10))
    walk_pct = float(settings.get("walk_away_source_cost_pct", 0.15))
    proximity = float(settings.get("offer_proximity_multiplier", 1.50))

    target_item = max(0.0, resale * target_pct - source_costs)
    walk_item = max(0.0, resale * walk_pct - source_costs)

    if ask <= target_item:
        lane = "BUY_NOW"
    elif ask <= walk_item:
        lane = "BUY_AT_ASK"
    elif walk_item > 0 and ask <= walk_item * proximity:
        lane = "OFFER_ONLY"
    else:
        lane = "TOO_EXPENSIVE"

    suggested = min(ask, target_item)
    return {
        "lane": lane,
        "suggested_offer_usd": round(suggested, 2),
        "walk_away_max_usd": round(walk_item, 2),
        "target_all_in_usd": round(resale * target_pct, 2),
        "walk_away_all_in_usd": round(resale * walk_pct, 2),
    }
