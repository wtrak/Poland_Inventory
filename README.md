# Poland Inventory Radar

Sourcing-intelligence workspace for finding low-cost inventory in Central/Eastern Europe that can be consolidated in Poland and sold into U.S. reseller auctions.

## Core idea

The model is not traditional retail arbitrage. The priority is merchandise that:

1. can be bought extremely cheaply in Europe,
2. has believable recent U.S. resale comps,
3. is compact/light enough to preserve shipping margin,
4. is easy for an auction buyer to identify and relist,
5. has enough source-market supply to repeat.

## ChatGPT subscription workflow

The dashboard now includes **ChatGPT Analysis**, designed to use the user's existing ChatGPT subscription instead of the separately billed OpenAI API.

- No OpenAI API key is required.
- The dashboard prepares and copies a structured listing-analysis packet.
- **Open ChatGPT** opens ChatGPT or a saved ChatGPT Project URL.
- Listing photos are attached directly in ChatGPT so normal ChatGPT vision, web search and reasoning can be used subject to the user's plan limits.
- Live/Offer Opportunity rows can be preloaded into the ChatGPT Analysis form.
- Project instructions are stored in `docs/chatgpt-project-instructions.txt`.

See `docs/CHATGPT_PLUS_WORKFLOW.md` for setup and usage.

## Hourly radar

The repository includes a GitHub Actions workflow scheduled for **17 minutes past every hour** plus a manual `workflow_dispatch` Run button.

Each run refreshes FX, consumes new GitHub Issue intake candidates, consumes any explicitly permitted JSON feeds, scores/deduplicates listings, calculates negotiated offer ceilings, archives stale opportunities, updates scan statistics, and commits only generated data files.

Vinted is intentionally handled through its native saved-search workflow plus the repo's **Add Candidate** intake form; this project does not deploy a Vinted crawler.

See `docs/AUTOMATION.md` for details.

## Repository sections

- `data/buy-list.json` — permanent category-level buy criteria.
- `data/opportunities.json` — current/recent online listings worth checking at the asking price.
- `data/offer-opportunities.json` — listings that are too expensive at ask but worth pursuing at a specific lower offer.
- `data/vinted-searches.json` — saved-search terms across the regional Vinted storefronts.
- `data/sources.json` — marketplaces and search terms by country.
- `data/settings.json` — automated source-cost and offer thresholds.
- `data/scan-state.json` — most recent automated-run status and counts.
- `data/archive/` — stale opportunity history.
- `data/feeds.json` — explicitly permitted automated JSON source configuration.
- `docs/SCORING.md` — how opportunities are scored.
- `docs/RESEARCH_METHOD.md` — rules for evidence and comp quality.
- `docs/OFFER_RULES.md` — offer price, walk-away ceiling, source-side cost and counteroffer discipline.
- `docs/AUTOMATION.md` — hourly workflow architecture and source-policy rules.
- `index.html` — dashboard for browsing and submitting candidates.

## Default buying thresholds

A category is strongest when it meets most of these:

- U.S. believable sold value: **$20+**
- Preferred U.S. sold band: **$25–$40**
- Recent sold evidence: **3+ comps preferred**
- Acquisition cost: **under $1–$2 per unit**, preferably below $1
- Effective packed weight: **under 200 g preferred**
- Easy to photograph, identify, title and relist
- Repeatable source-market supply

Automated offer math currently targets roughly **10% all-in source cost** and uses roughly **15% as the hard walk-away ceiling**, both measured against conservative U.S. resale. Source-side costs such as buyer protection and inbound shipping to Poland are deducted before the item-price ceiling is calculated.

## Status definitions

- `STRONG BUY` — source price is inside the target range and resale evidence is strong.
- `BUY` — attractive but requires a normal condition/authenticity check.
- `OFFER ONLY` — asking price is too high, but a specific lower offer would make the item viable. Use the suggested offer and never exceed the listed walk-away max.
- `WATCH` — price or comp evidence needs one more check.
- `RESEARCH` — interesting lead, not enough evidence to buy yet.
- `PASS` — spread is too small or shipping/operational risk is too high.

## Currency rule

All source prices retain the original local currency and also show USD and PLN equivalents with an FX date. The hourly workflow refreshes reference FX from the European Central Bank.

## Important

Listings expire quickly. Opportunity files record the date checked and should be treated as radar, not a guarantee that an item remains available.

For negotiated purchases, buyer protection, inbound shipping to Poland and other unavoidable source-side costs must be included before final purchase. Bundling multiple items from the same seller can improve the economics substantially.

**Privacy:** live sourcing opportunities and offer ceilings are commercially sensitive. This repository should be private if you do not want those data exposed publicly.
