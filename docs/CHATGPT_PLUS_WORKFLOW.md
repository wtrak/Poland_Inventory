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

## Photos

The dashboard includes a local photo workspace. Photos are **not uploaded by the dashboard** and do not use an API.

- Drop image files onto the photo area, click to choose them, or paste screenshots with Ctrl/Cmd+V.
- The dashboard renders local previews.
- In Chrome, right-click a preview (or long-press on Android) and choose **Search with Google Lens** for a free consumer visual search.
- **Open Google Lens** opens Google's normal Lens interface for manual upload/search.
- **Copy Contact Sheet** combines the selected photos locally in the browser and places one PNG on the clipboard. Paste that image directly into ChatGPT. For tiny labels, serials, or dense detail, attach the original full-resolution photos in ChatGPT as well.

A website cannot safely inject local image files into another website's upload control. That browser security boundary is why the final photo attachment to ChatGPT or Google Lens remains an interactive user action.

Google Lens is used here as its free consumer product, not as an automated backend. The free Lens interface is useful for identification and visual matches, but it is not an official free programmatic API for arbitrary bulk image evaluation.

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
