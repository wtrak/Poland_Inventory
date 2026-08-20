# Offer Opportunity Rules

Some source marketplaces allow buyers to negotiate. Listings that are too expensive at the asking price can still be worth tracking if a realistic lower offer would bring them inside the buy model.

## Core statuses

- **BUY / WATCH** — asking price is already at or below the category walk-away ceiling.
- **OFFER ONLY** — asking price is above the ceiling, but close enough that a lower offer could make the item worth buying.
- **PASS** — even a realistic offer is unlikely to reach a worthwhile acquisition cost.

## Required numbers for every offer candidate

1. Asking price — Local / USD / PLN
2. Suggested offer — Local / USD / PLN
3. Walk-away max — Local / USD / PLN
4. Percentage discount requested from asking price
5. Offer method / marketplace
6. Date and FX date
7. Source-side cost note

## Pricing logic

The **walk-away max** is the highest item price we should accept without weakening the category economics.

The **suggested offer** should be below the walk-away max so there is room for one seller counter. As a default, start around 80-90% of the walk-away max, rounded to a normal marketplace amount. Never raise a counter above the walk-away max just because the seller responds.

### Candidate range

As a default, keep a listing in the Offer Opportunities lane when:

- its asking price is above the normal walk-away ceiling, and
- the asking price is generally no more than about 50% above that ceiling, or there is unusually strong resale evidence that justifies trying a deeper offer.

Listings far above the ceiling should normally be ignored rather than wasting negotiation time.

## Source-side fees matter

For Vinted and similar marketplaces, the real acquisition cost can include:

- accepted item price,
- buyer-protection/platform charge,
- shipping to the Poland consolidation point,
- any payment or handling cost.

If those costs are known, subtract them from the category's all-in acquisition budget before determining the item-price walk-away max. If they are not yet known, the opportunity must carry a note that an all-in check is required before purchase.

Bundling multiple items from one seller can materially lower source-side shipping cost per item, so a borderline item may become attractive as part of a seller bundle even when it is poor as a one-item order.

## Negotiation discipline

- Do not offer just because a seller accepts offers; the item must already have strong comp evidence.
- Do not chase counters past the walk-away max.
- Do not let an accepted offer override condition/authenticity concerns.
- After an offer is accepted, record the accepted price and recalculate the actual source-cost spread.
- Rejected offers stay in the feed only if a future price drop could make them viable.
