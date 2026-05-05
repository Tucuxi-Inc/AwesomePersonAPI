# Demo walkthrough

A 21-slide Playwright-captured walkthrough of the Simple Mode end-to-end flow,
from admin login → AI requirement extraction → magic-link invite → candidate
interview → results page with PDF export.

## View it

Open [`deck.html`](deck.html) in any browser. Arrow keys navigate, `O` opens
the thumbnail overview, `F` toggles fullscreen.

## Re-run it

`demo.js` is a self-contained Playwright script. From a clean checkout with
the stack running (`docker-compose up -d`), set up Playwright once:

```bash
mkdir -p /tmp/apapi-demo-runner && cd /tmp/apapi-demo-runner
npm init -y >/dev/null && npm install playwright
npx playwright install chromium
```

Then run from the repo root:

```bash
node docs/demo/demo.js
```

The script will overwrite `screenshots/` and regenerate `captions.json` and
`captions.js`. Total runtime ~3-5 minutes (LLM-bound).

## Customizing

The script is intentionally short and editable — change the role
(`JOB_TITLE` / `JOB_DESCRIPTION`), candidate (`CANDIDATE_NAME`), or trait
selection (`desiredTraits`) at the top of the file. Captions are written from
the `cap()` calls inline; edit there.
