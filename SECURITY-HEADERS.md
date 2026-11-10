# Security headers — A+

The site scores **D** today because GitHub Pages cannot send security headers at
all. On Cloudflare it scores **A+**.

There is **no build step** — you upload the folder and Cloudflare serves it
as-is. So the folder has to be correct before it leaves your computer.

---

## The rule

**Edit any page → run this → then upload.**

```bash
cd path/to/the/website-folder
python3 tools/prepare-for-upload.py --live
```

Why: the policy names every inline script by a fingerprint of its code. Change
one character in a page and its fingerprint no longer matches, so the browser
refuses to run that page's scripts. The command re-reads every page and fixes
the fingerprints.

To check without changing anything:

```bash
python3 tools/generate-headers.py --check
```

If Claude makes the change for you, this is already done.

---

## What the policy blocks

Anything the site does not use: outside scripts, injected scripts, plugins,
framing by another site, forms posting elsewhere. Tested — a rogue inline script
and an outside jQuery load were both refused.

**So anything you add later from another domain gets blocked** — YouTube embeds,
Google Analytics, a booking widget, Google Fonts. That is the policy doing its
job. Tell me what you added and I'll allow that one domain.

---

## What changed inside the site

| Before | Now |
|---|---|
| 116 inline `onerror="..."` on images | `data-onerr="..."`, handled by `js/img-fallback.js` |
| 66 inline `<script>` blocks | unchanged, now fingerprinted automatically |
| 425 inline `style="..."` | unchanged — inline styles are still allowed |

Image fallback modes: `hide`, `swap` (show next element), `remote` (retry
`data-remote` once), `parent` (adds `t-fallback` class), `text` (replace with
`data-onerr-text`).

---

## One warning about HSTS preload

`preload` tells browsers "never load this domain over plain http, ever", and it
is hard to undo. Only keep it once templeofsun.com and every subdomain work
properly over https. If unsure, remove the word `preload` from
`tools/generate-headers.py` before launch and add it back a week later.

---

## After launch

Scan at https://securityheaders.com — expect **A+**.

---

## How this was tested

All 21 pages were loaded in a real headless browser twice: once as the original
site with no policy, once with the exact headers applied. Result: **0 policy
violations, and no difference at all** — same header, footer, navigation,
structured data, images and page text on every page. Product modals, FAQ search,
the blend quiz and image fallbacks all still work.

The site as it was before these edits is kept at
a backup copy kept outside this repo.
