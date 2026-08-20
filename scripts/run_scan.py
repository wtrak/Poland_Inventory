from __future__ import annotations

import json
from datetime import datetime, timezone, date
from pathlib import Path

from dedupe import dedupe
from feed_loader import load_permitted_json_feeds
from fx import refresh_fx
from github_inbox import fetch_candidates, close_processed
from scoring import score_candidate, score_label, offer_math

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def load(path: Path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def save(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def parse_day(value: str | None):
    try:
        return date.fromisoformat(str(value)[:10])
    except Exception:
        return None


def parse_dt(value: str | None):
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00")).astimezone(timezone.utc)
    except Exception:
        return None


def archive_stale(items: list[dict], archive: list[dict], days: int, today: date):
    keep, moved = [], []
    for item in items:
        checked = parse_day(item.get("checked"))
        if checked and (today - checked).days >= days:
            copy = dict(item)
            copy["archived_at"] = today.isoformat()
            copy["archive_reason"] = f"Not rechecked for {days}+ days"
            moved.append(copy)
        else:
            keep.append(item)
    return keep, dedupe(archive + moved), len(moved)


def expire_vinted(items: list[dict], archive: list[dict], ttl_hours: float, now: datetime):
    keep, moved = [], []
    for item in items:
        source = str(item.get("source", "")).lower()
        url = str(item.get("source_url", "")).lower()
        is_vinted = "vinted" in source or "vinted." in url
        if not is_vinted:
            keep.append(item)
            continue
        verified = parse_dt(item.get("availability_verified_at"))
        if not verified or (now - verified).total_seconds() / 3600.0 > ttl_hours:
            copy = dict(item)
            copy["archived_at"] = now.date().isoformat()
            copy["archive_reason"] = f"Vinted availability confirmation older than {ttl_hours:g} hours"
            moved.append(copy)
        else:
            keep.append(item)
    return keep, dedupe(archive + moved), len(moved)


def money_local(usd: float, currency: str, fx: dict) -> float:
    per_unit = float(fx["rates"][currency]["usd_per_unit"])
    return 0.0 if per_unit <= 0 else usd / per_unit


def money_pln(usd: float, fx: dict) -> float:
    return usd * float(fx["rates"]["USD"]["pln_per_unit"])


def candidate_to_buy(candidate: dict, score: int, label: str, fx: dict, today: str) -> dict:
    ask_local = candidate["asking_price_local"]
    currency = candidate["currency"]
    ask_usd = candidate["asking_price_usd"]
    ask_pln = candidate["asking_price_pln"]
    resale = candidate["conservative_us_resale_usd"]
    return {
        "status": label,
        "score": score,
        "source": candidate["source"],
        "country": candidate["country"],
        "title": candidate["title"],
        "source_price": f"{ask_local:g} {currency}",
        "source_price_usd": f"${ask_usd:.2f}",
        "source_price_pln": f"{ask_pln:.2f} PLN",
        "unit_cost": f"{ask_local:g} {currency}",
        "unit_cost_usd": f"${ask_usd:.2f}",
        "unit_cost_pln": f"{ask_pln:.2f} PLN",
        "fx_date": fx.get("as_of"),
        "category": candidate["category"],
        "expected_us_value": f"Conservative U.S. resale input: ${resale:.2f}; {candidate['comp_count']} recent sold comp(s)",
        "why": f"Automated intake score {score}/100. Asking price plus estimated source-side costs is ${ask_usd + candidate['source_side_costs_usd']:.2f} against ${resale:.2f} conservative U.S. resale.",
        "source_url": candidate["source_url"],
        "comp_urls": [],
        "checked": today,
        "notes": candidate.get("notes", ""),
        "github_issue": candidate.get("github_issue"),
        "availability_verified_at": candidate.get("availability_verified_at"),
        "automation_generated": True,
    }


def candidate_to_offer(candidate: dict, score: int, offer: dict, fx: dict, today: str) -> dict:
    currency = candidate["currency"]
    ask_usd = candidate["asking_price_usd"]
    offer_usd = offer["suggested_offer_usd"]
    walk_usd = offer["walk_away_max_usd"]
    ask_local = candidate["asking_price_local"]
    suggested_local = money_local(offer_usd, currency, fx)
    walk_local = money_local(walk_usd, currency, fx)
    ask_pln = candidate["asking_price_pln"]
    suggested_pln = money_pln(offer_usd, fx)
    walk_pln = money_pln(walk_usd, fx)
    discount = 0 if ask_usd <= 0 else round((1 - offer_usd / ask_usd) * 100)
    channel = "Vinted in-app offer" if "vinted" in candidate["source"].lower() else "Marketplace offer/message"
    return {
        "status": "OFFER ONLY",
        "score_if_accepted": score,
        "source": candidate["source"],
        "country": candidate["country"],
        "title": candidate["title"],
        "category": candidate["category"],
        "asking_price_local": f"{ask_local:g} {currency}",
        "asking_price_usd": f"${ask_usd:.2f}",
        "asking_price_pln": f"{ask_pln:.2f} PLN",
        "suggested_offer_local": f"{suggested_local:.2f} {currency}",
        "suggested_offer_usd": f"${offer_usd:.2f}",
        "suggested_offer_pln": f"{suggested_pln:.2f} PLN",
        "walk_away_max_local": f"{walk_local:.2f} {currency}",
        "walk_away_max_usd": f"${walk_usd:.2f}",
        "walk_away_max_pln": f"{walk_pln:.2f} PLN",
        "offer_discount_from_ask": f"{discount}%",
        "offer_channel": channel,
        "expected_us_value": f"Conservative U.S. resale input: ${candidate['conservative_us_resale_usd']:.2f}; {candidate['comp_count']} recent sold comp(s)",
        "why_offer": "Ask is too high for the target acquisition ratio, but it is close enough to negotiate. Suggested offer targets ~10% all-in acquisition cost; walk-away max targets ~15% after source-side costs.",
        "source_side_cost_note": f"Estimated buyer protection/inbound source costs: ${candidate['source_side_costs_usd']:.2f}. Never exceed the walk-away item price unless those costs fall.",
        "source_url": candidate["source_url"],
        "checked": today,
        "fx_date": fx.get("as_of"),
        "notes": candidate.get("notes", ""),
        "github_issue": candidate.get("github_issue"),
        "availability_verified_at": candidate.get("availability_verified_at"),
        "automation_generated": True,
    }


def main():
    now = datetime.now(timezone.utc)
    today = now.date()
    today_s = today.isoformat()
    settings = load(DATA / "settings.json", {})
    state = load(DATA / "scan-state.json", {})

    fx, fx_error = refresh_fx(DATA / "fx-rates.json")
    opportunities = load(DATA / "opportunities.json", [])
    offers = load(DATA / "offer-opportunities.json", [])
    archive = load(DATA / "archive/opportunities.json", [])
    offer_archive = load(DATA / "archive/offer-opportunities.json", [])

    vinted_ttl = float(settings.get("vinted_live_ttl_hours", 4) or 4)
    opportunities, archive, moved_v1 = expire_vinted(opportunities, archive, vinted_ttl, now)
    offers, offer_archive, moved_v2 = expire_vinted(offers, offer_archive, vinted_ttl, now)

    archive_days = int(settings.get("archive_after_days", 21))
    opportunities, archive, moved_a = archive_stale(opportunities, archive, archive_days, today)
    offers, offer_archive, moved_b = archive_stale(offers, offer_archive, archive_days, today)

    issue_candidates, processed_issues, inbox_error = fetch_candidates(fx, settings)
    feed_candidates, feed_status = load_permitted_json_feeds(DATA / "feeds.json", fx)
    candidates = dedupe(issue_candidates + feed_candidates)
    result_comments = {}
    buy_count = offer_count = watch_count = 0

    for candidate in candidates:
        score = score_candidate(candidate, settings)
        label = score_label(score)
        offer = offer_math(candidate, settings)
        issue_no = int(candidate.get("github_issue") or 0)

        if offer["lane"] in {"BUY_NOW", "BUY_AT_ASK"} and label != "PASS":
            item = candidate_to_buy(candidate, score, label, fx, today_s)
            opportunities.append(item)
            if score >= 80:
                buy_count += 1
            else:
                watch_count += 1
            if issue_no:
                result_comments[issue_no] = f"Radar result: **{label}** — score {score}/100. Ask ${candidate['asking_price_usd']:.2f} / {candidate['asking_price_pln']:.2f} PLN. Conservative U.S. resale ${candidate['conservative_us_resale_usd']:.2f}. Added to Live Opportunities."
        elif offer["lane"] == "OFFER_ONLY" and score >= 50:
            item = candidate_to_offer(candidate, score, offer, fx, today_s)
            offers.append(item)
            offer_count += 1
            if issue_no:
                result_comments[issue_no] = f"Radar result: **OFFER ONLY** — score {score}/100. Send about ${offer['suggested_offer_usd']:.2f}; hard walk-away ${offer['walk_away_max_usd']:.2f}. Added to Offer Opportunities."
        else:
            if issue_no:
                result_comments[issue_no] = f"Radar result: **PASS / RESEARCH** — score {score}/100. Ask ${candidate['asking_price_usd']:.2f}; formula walk-away ${offer['walk_away_max_usd']:.2f}. Not added to the active buying feed."

    opportunities = dedupe(opportunities)
    offers = dedupe(offers)
    save(DATA / "opportunities.json", opportunities)
    save(DATA / "offer-opportunities.json", offers)
    save(DATA / "archive/opportunities.json", archive)
    save(DATA / "archive/offer-opportunities.json", offer_archive)

    source_status = {
        "vinted": f"manual in-app verification only; live TTL {vinted_ttl:g}h; no public-web Vinted candidates",
        "fx": fx_error or f"OK ({fx.get('as_of', 'unknown')})",
        "github_inbox": inbox_error or f"OK ({len(issue_candidates)} candidate(s))",
        "approved_feeds": feed_status or {"status": "No enabled permitted feeds"},
    }
    state.update({
        "last_run_utc": now.isoformat(),
        "last_success_utc": now.isoformat(),
        "last_fx_refresh": fx.get("as_of"),
        "runs": int(state.get("runs", 0) or 0) + 1,
        "candidates_seen": len(candidates),
        "new_buy_now": buy_count,
        "new_offer_only": offer_count,
        "new_watch": watch_count,
        "archived": moved_a + moved_b + moved_v1 + moved_v2,
        "source_status": source_status,
    })
    save(DATA / "scan-state.json", state)
    close_processed(processed_issues, result_comments)


if __name__ == "__main__":
    main()
