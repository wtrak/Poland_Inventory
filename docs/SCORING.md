# Opportunity scoring

Score listings out of 100.

## Price gate before scoring

First compare the listing's asking price with the category walk-away ceiling.

- **At or below walk-away max:** score normally.
- **Above max but generally within ~50%:** it may enter `OFFER ONLY` if the marketplace supports negotiation and the comps justify trying.
- **Far above max:** normally PASS rather than spending time negotiating.

For an `OFFER ONLY` listing, the displayed score is **score if the suggested offer is accepted**, not a score at the current asking price. Every offer candidate must show a suggested offer and a hard walk-away max. See `docs/OFFER_RULES.md`.

## 1. U.S. resale evidence — 30 points
- 30: 3+ recent sold comps in the target band with consistent pricing
- 20: 2 recent sold comps or wider variance
- 10: only active asking prices / weak comps
- 0: no reliable evidence

## 2. Source price spread — 25 points
Use conservative U.S. resale value, not the highest comp. For offer-only candidates, calculate this section using the **proposed accepted offer**, then verify again using the true all-in source cost before purchase.

- 25: source unit cost <= 10% of conservative U.S. resale
- 20: <= 15%
- 15: <= 20%
- 5: <= 30%
- 0: > 30%

## 3. Shipping efficiency — 20 points
- 20: <100 g, compact/non-fragile
- 16: 100-200 g
- 10: 200-500 g or modest fragility
- 5: 500 g-1 kg / bulky / fragile
- 0: poor fit for consolidation

## 4. Repeatability — 15 points
- 15: deep supply / frequent lots
- 10: recurring but selective
- 5: rare one-off opportunity

## 5. Reseller simplicity — 10 points
- 10: obvious keywords/model/brand; easy photos and listing
- 5: requires expertise
- 0: hard to authenticate, explain or comp

## Interpretation
- 90-100: STRONG BUY
- 80-89: BUY
- 65-79: WATCH
- 50-64: RESEARCH
- <50: PASS

`OFFER ONLY` is a price status layered on top of the score, not a separate quality score.
