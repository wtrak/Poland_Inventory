# ChatGPT subscription workflow — no paid API

This repository's intended architecture is deliberately split into two layers:

1. **Free dashboard / automation layer**
   - GitHub Actions
   - ECB FX refresh
   - rule-based scoring and offer math
   - saved marketplace searches
   - candidate intake and opportunity tracking

2. **Interactive intelligence layer**
   - the user's normal ChatGPT subscription
   - image understanding
   - web search
   - current-market research
   - nuanced valuation and buy/offer/pass decisions

The dashboard does **not** need an OpenAI API key for this workflow and should not make paid model or web-search API calls.

## One-time ChatGPT setup

Create a ChatGPT Project, for example **Poland Inventory Scout**.

In ChatGPT, open the project's settings and paste the contents of:

`docs/chatgpt-project-instructions.txt`

Projects keep project instructions, chats and files together, and normal ChatGPT web search can be used inside project conversations subject to the user's ChatGPT plan limits.

Then copy the URL of that ChatGPT Project and paste it into the dashboard under **ChatGPT Analysis → ChatGPT Project URL**. The dashboard saves that URL only in browser `localStorage`.

## Per-listing workflow

1. Open **ChatGPT Analysis** in the dashboard.
2. Enter the listing title, asking price, quantity, shipping/weight if known, URL and seller notes.
3. Click **Build + Copy Packet**.
4. Click **Open ChatGPT**.
5. Attach the listing photos in ChatGPT.
6. Paste the prepared packet and send.

For listings already stored in Live Opportunities or Offer Opportunities, use the **Analyze with ChatGPT** button on that row to preload the analysis form.

## What is and is not automated

The dashboard can automatically calculate acquisition ratios, auction economics, FX conversions, thresholds and other deterministic math.

It intentionally does **not** attempt to silently route external website traffic through a ChatGPT subscription. A ChatGPT subscription is used interactively inside ChatGPT; unattended programmatic model access is API territory and would be separately billed.

This design keeps the paid API cost at **$0** while still using the user's existing ChatGPT plan for the expensive reasoning, image analysis and web research.
