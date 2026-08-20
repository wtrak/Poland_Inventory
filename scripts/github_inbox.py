from __future__ import annotations

import json
import os
import re
from datetime import datetime, timezone
from urllib.request import Request, urlopen

HEADING = re.compile(r"^###\s+(.+?)\s*$", re.M)


def _request(url: str, token: str, method: str = "GET", data: dict | None = None):
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "PolandInventoryRadar/1.0",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    body = None if data is None else json.dumps(data).encode("utf-8")
    if body is not None:
        headers["Content-Type"] = "application/json"
    req = Request(url, data=body, headers=headers, method=method)
    with urlopen(req, timeout=20) as response:
        payload = response.read()
    return json.loads(payload.decode("utf-8")) if payload else None


def parse_issue_form(body: str) -> dict:
    matches = list(HEADING.finditer(body or ""))
    fields = {}
    for i, match in enumerate(matches):
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(body)
        value = body[start:end].strip()
        if value == "_No response_":
            value = ""
        fields[match.group(1).strip()] = value
    return fields


def _number(value: str, default=0.0):
    try:
        cleaned = str(value).replace(",", ".").strip()
        return float(re.findall(r"-?\d+(?:\.\d+)?", cleaned)[0])
    except Exception:
        return default


def _issue_age_hours(issue: dict) -> float:
    try:
        created = datetime.fromisoformat(str(issue.get("created_at", "")).replace("Z", "+00:00"))
        return max(0.0, (datetime.now(timezone.utc) - created).total_seconds() / 3600.0)
    except Exception:
        return 999999.0


def fetch_candidates(fx: dict, settings: dict | None = None) -> tuple[list[dict], list[dict], str | None]:
    settings = settings or {}
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    token = os.environ.get("GITHUB_TOKEN", "")
    if not repo or not token:
        return [], [], "GitHub inbox skipped: GITHUB_REPOSITORY/GITHUB_TOKEN unavailable"
    try:
        issues = _request(f"https://api.github.com/repos/{repo}/issues?state=open&per_page=100", token) or []
        candidates = []
        processed = []
        max_vinted_age = float(settings.get("vinted_max_confirmation_age_hours", 4) or 4)
        require_vinted_confirmation = bool(settings.get("vinted_manual_verification_required", True))
        for issue in issues:
            if issue.get("pull_request") or not str(issue.get("title", "")).startswith("[INBOX]"):
                continue
            fields = parse_issue_form(issue.get("body", ""))
            try:
                currency = fields.get("Currency", "").strip().upper()
                ask_local = _number(fields.get("Asking price", ""))
                rate = fx["rates"][currency]
                ask_usd = ask_local * float(rate["usd_per_unit"])
                ask_pln = ask_local * float(rate["pln_per_unit"])
                marketplace = fields.get("Marketplace", "").strip()
                source_url = fields.get("Listing URL", "").strip()
                is_vinted = "vinted" in marketplace.lower() or "vinted." in source_url.lower()
                availability_text = fields.get("Availability confirmed now", "")
                availability_confirmed = "[x]" in availability_text.lower()
                age_hours = _issue_age_hours(issue)

                # Vinted public/search-engine indexing is too stale for live buying decisions.
                # A Vinted candidate is accepted only after fresh manual in-app confirmation.
                if is_vinted and require_vinted_confirmation:
                    if not availability_confirmed or age_hours > max_vinted_age:
                        continue

                candidate = {
                    "source_url": source_url,
                    "marketplace": marketplace,
                    "source": marketplace,
                    "country": fields.get("Country", "").strip(),
                    "title": fields.get("Item title", "").strip(),
                    "category": fields.get("Category", "").strip(),
                    "asking_price_local": ask_local,
                    "currency": currency,
                    "asking_price_usd": round(ask_usd, 2),
                    "asking_price_pln": round(ask_pln, 2),
                    "conservative_us_resale_usd": _number(fields.get("Conservative U.S. resale (USD)", "")),
                    "comp_count": int(_number(fields.get("Recent sold comp count", ""))),
                    "weight_g": _number(fields.get("Estimated packed weight (g)", ""), 9999),
                    "source_side_costs_usd": _number(fields.get("Source-side costs (USD)", "")),
                    "notes": fields.get("Notes", "").strip(),
                    "github_issue": issue.get("number"),
                    "availability_confirmed": availability_confirmed,
                    "availability_verified_at": issue.get("created_at") if is_vinted else None,
                    "availability_confirmation_age_hours": round(age_hours, 2) if is_vinted else None,
                }
                if not candidate["source_url"] or not candidate["title"] or candidate["conservative_us_resale_usd"] <= 0:
                    continue
                candidates.append(candidate)
                processed.append(issue)
            except Exception:
                continue
        return candidates, processed, None
    except Exception as exc:
        return [], [], f"GitHub inbox failed: {exc}"


def close_processed(issues: list[dict], results_by_issue: dict[int, str]):
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    token = os.environ.get("GITHUB_TOKEN", "")
    if not repo or not token:
        return
    for issue in issues:
        number = int(issue["number"])
        summary = results_by_issue.get(number, "Processed by hourly inventory radar.")
        try:
            _request(f"https://api.github.com/repos/{repo}/issues/{number}/comments", token, "POST", {"body": summary})
            _request(f"https://api.github.com/repos/{repo}/issues/{number}", token, "PATCH", {"state": "closed"})
        except Exception:
            pass
