# Hourly automation

## Schedule

`.github/workflows/hourly-inventory-radar.yml` runs at minute 17 of every hour and can also be started manually with **Run workflow** in GitHub Actions.

The workflow:

1. refreshes ECB currency reference rates,
2. reads new `[INBOX]` GitHub Issue submissions,
3. reads any explicitly permitted JSON feeds enabled in `data/feeds.json`,
4. normalizes asking prices into local currency, USD and PLN,
5. scores candidates using `docs/SCORING.md`,
6. calculates offer and walk-away prices from `data/settings.json`,
7. deduplicates marketplace listings,
8. moves stale records to `data/archive/`,
9. updates `data/scan-state.json`,
10. commits only radar-generated data files.

## Vinted

Vinted is deliberately **not crawled or scraped** by this repository. Use the country-specific terms in `data/vinted-searches.json` with Vinted's own saved searches, then submit interesting listings through **Add Candidate** on the dashboard.

The GitHub Issue intake form asks for the minimum data needed to score a listing without crawling the marketplace page. The next hourly run processes the issue, posts the decision back to the issue, and closes it.

## Offer math

Default settings are in `data/settings.json`:

- target all-in source cost: ~10% of conservative U.S. resale,
- hard walk-away all-in source cost: ~15%,
- listings up to 1.5x the walk-away item-price ceiling may be surfaced as `OFFER ONLY`.

Buyer protection and inbound shipping allocation to Poland belong in `source_side_costs_usd`; the offer calculator subtracts those costs before computing the item-price ceiling.

## Permitted automated feeds

`data/feeds.json` supports JSON endpoints only when `automation_allowed` is explicitly `true`. Each enabled entry needs a URL, currency, field mapping and category economics. Do not add a marketplace endpoint unless its API/feed terms allow automated retrieval.

The generic adapter intentionally does not HTML-scrape shopping sites.

## GitHub permissions

The workflow requests:

- `contents: write` to save refreshed data,
- `issues: write` to comment on and close processed inbox issues.

No external API secrets are required for the baseline system. The ECB FX feed and GitHub-provided `GITHUB_TOKEN` are sufficient.

## Public repository warning

A public repository exposes sourcing thresholds, live opportunities and offer ceilings. This project should be private if the data is commercially sensitive.
