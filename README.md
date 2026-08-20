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
- `data/opportunities.json` — current/recent online listings worth checking at the asking price.
- `data/offer-opportunities.json` — listings that are too expensive at ask but worth pursuing at a specific lower offer.
- `data/sources.json` — marketplaces and search terms by country.
- `docs/SCORING.md` — how opportunities are scored.
- `docs/RESEARCH_METHOD.md` — rules for evidence and comp quality.
- `docs/OFFER_RULES.md` — offer price, walk-away ceiling, source-side cost and counteroffer discipline.
- `index.html` — lightweight dashboard for browsing the datasets.

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
- `OFFER ONLY` — asking price is too high, but a specific lower offer would make the item viable. Use the suggested offer and never exceed the listed walk-away max.
- `WATCH` — price or comp evidence needs one more check.
- `RESEARCH` — interesting lead, not enough evidence to buy yet.
- `PASS` — spread is too small or shipping/operational risk is too high.

## Currency rule

All source prices should retain the original local currency and also show USD and PLN equivalents with an FX date.

## Important

Listings expire quickly. Opportunity files record the date checked and should be treated as radar, not a guarantee that an item remains available.

For negotiated purchases, buyer protection, inbound shipping to Poland and other unavoidable source-side costs must be included before final purchase. Bundling multiple items from the same seller can improve the economics substantially.
