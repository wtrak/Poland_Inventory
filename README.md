# Poland Inventory Radar

Sourcing-intelligence workspace for finding low-cost inventory in Central/Eastern Europe that can be consolidated in Poland and sold into U.S. reseller auctions.

## Core idea

The model is not traditional retail arbitrage. The priority is merchandise that:

1. can be bought extremely cheaply in Europe,
2. has believable recent U.S. resale comps,
3. is compact/light enough to preserve shipping margin,
4. is easy for an auction buyer to identify and relist,
5. has enough source-market supply to repeat.

## Repository sections

- `data/buy-list.json` — permanent category-level buy criteria.
- `data/opportunities.json` — current/recent online listings worth checking.
- `data/sources.json` — marketplaces and search terms by country.
- `docs/SCORING.md` — how opportunities are scored.
- `docs/RESEARCH_METHOD.md` — rules for evidence and comp quality.
- `index.html` — lightweight dashboard for browsing the three datasets.

## Default buying thresholds

A category is strongest when it meets most of these:

- U.S. believable sold value: **$20+**
- Preferred U.S. sold band: **$25–$40**
- Recent sold evidence: **3+ comps preferred**
- Acquisition cost: **under $1–$2 per unit**, preferably below $1
- Effective packed weight: **under 200 g preferred**
- Easy to photograph, identify, title and relist
- Repeatable source-market supply

## Status definitions

- `STRONG BUY` — source price is inside the target range and resale evidence is strong.
- `BUY` — attractive but requires a normal condition/authenticity check.
- `WATCH` — price or comp evidence needs one more check.
- `RESEARCH` — interesting lead, not enough evidence to buy yet.
- `PASS` — spread is too small or shipping/operational risk is too high.

## Important

Listings expire quickly. `opportunities.json` records the date checked and should be treated as a radar, not a guarantee that an item remains available.
