# Currency display rule

Every acquisition-side price in this repository must be shown in three ways whenever a local currency is involved:

1. Original local currency — the marketplace/seller price exactly as encountered.
2. USD equivalent — for quick comparison to U.S. resale comps.
3. PLN equivalent — for Poland-based purchasing and consolidation decisions.

Each converted price must carry an `fx_date` or otherwise reference the dated FX snapshot in `data/fx-rates.json`.

## Required opportunity fields

- `source_price`
- `source_price_usd`
- `source_price_pln`
- `unit_cost`
- `unit_cost_usd`
- `unit_cost_pln`
- `fx_date`

If a unit cost cannot be calculated because the item count is unknown, say `depends on count` or `varies` rather than inventing a value.

## Buy List rule

Target and maximum buy prices should show the relevant local currency together with USD and PLN equivalents. When a threshold is intentionally defined in USD rather than a local currency, show the PLN equivalent too.

Conversions are decision aids, not accounting rates. Refresh them whenever a live opportunity is rechecked or whenever FX movement becomes material.
