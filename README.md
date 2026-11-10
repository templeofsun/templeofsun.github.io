# Temple of Sun website

The website of Péter Frák (templeofsun, alchemy of souls). Plain HTML, CSS and JavaScript, no framework.
This folder is the one copy to edit; GitHub gets an exact copy of it.

- Test site: https://templeofsun.github.io/
- GitHub repo: `templeofsun/templeofsun.github.io` (organisation `templeofsun`)
- Real domain templeofsun.com is still on HostGator. Moving to Cloudflare (notes kept outside this repo).

## Before every publish

```bash
cd path/to/the/website-folder
python3 tools/prepare-for-upload.py
```

It rebuilds the generated pages, the menu and footer on every page, the sitemap, the AI map
(llms.txt), the redirects and the security headers. Skip it and some page scripts stop working.
On launch day run it with `--live` (see `START-HERE-CLOUDFLARE.md`).

Then publish: clone the repo, copy this folder into it, commit, push to `main`. GitHub rebuilds the
test site in about a minute.

## What is where

| Folder / file | What it is |
|---|---|
| `*.html` (root) | The 25 main pages |
| `products/` | 23 blend pages, built from `tools/blend-pages.json` |
| `journal/` | Journal posts (Péter's own words) |
| `css/site.css` | All styling. Colours at the top (`:root`), dark mode at the bottom |
| `js/site.js` | Menu, footer, slideshow, gallery, lightbox, forms, light/dark button |
| `js/img-fallback.js` | Loaded first on every page: picks light/dark, handles broken images |
| `assets/` | Photos (`img/`), guest videos (`video/`), fonts, icons |
| `tools/` | Build scripts and their data files (see below) |
| `translations/` | Ready for PT, HU, DE. Not started, see `translations/README.md` |
| `robots.txt` / `robots-live.txt` | Private now (blocks search engines). Live version for launch day |
| `_headers`, `_redirects` | Security headers and old-address redirects, for Cloudflare |
| `c59f5...txt` | IndexNow key. Keep at the root, never rename |

## Pages that are built, not edited by hand

| Edit this | To change |
|---|---|
| `tools/blend-pages.json` | The 23 blend pages |
| `tools/session-pages.json` | Health Consultation, Spiritual Mentoring, Meditation Guidance |
| `js/site.js` (HEADER / MOBILE / FOOTER) | The menu and footer on every page |
| `tools/redirects.json` | Old HostGator addresses that forward to new pages |
| `tools/press-credits.json` | Press credits |

## Rules for edits

- Facts only from Péter: prices, dates, names, oil safety. Nothing invented.
- His voice is warm, devotional, first person. Don't polish it.
- Photos: WebP, compressed, descriptive file names.
- Light mode is the default. Dark only when a visitor picks it with the sun/moon button.
- Anything loaded from another website (YouTube, booking widget, analytics) is blocked until its
  address is added to `tools/generate-headers.py`.

## Still to do before launch

- Phone version.
- Contact form and newsletter (they only look like they work for now).
- Domain move to Cloudflare, then `prepare-for-upload.py --live`.
- Shop: waiting on Péter's tax details.
