# Temple of Sun — Website

Static site for Peter (Péter Frák) — Temple of Sun, alchemy of souls.
Pure HTML / CSS / JS. No frameworks, no build step. Open `index.html` in a browser and it works.

## Photos: work immediately, go local when you want

Every image tries the local file in `assets/img/` first; if it's missing, it
loads the same photo straight from templeofsun.com (needs internet). So the
site looks right out of the box.

To make it fully local/offline, pull the 26 photos once:

```bash
cd "path/to/the/website-folder"
bash get-images.sh
```

After that, no internet needed for images. `_IMAGES.html` is a visual
checklist of every photo if you'd rather save any by hand.

## Files

| File | What it is |
|---|---|
| `index.html` | Home — hero slideshow, welcome, 3 paths, quote, testimonials, newsletter |
| `aromatherapy.html` | Aromatherapy introduction — what it is, history, how it works, safety |
| `collections.html` | Aromatherapy — the shop: Rainbow + 5 Elements collections |
| `create-your-own-formula.html` | Bespoke signature scents |
| `retreats.html` | Soul Alchemy Retreats — no upcoming edition; subscribe block |
| `treatments.html` | Anahata + Marma-Abhyanga (no prices — enquire) |
| `mindfulness-labs.html` | The four LABs + venue class menu |
| `meditation.html` | Weekly community practice + 28-day challenge |
| `online-sessions.html` | Three online programs + discovery call |
| `about.html` | My story, timeline, credentials |
| `philosophy.html` | The five beliefs |
| `contact.html` | Form (visual only) + direct channels |
| `css/site.css` | Everything visual. Design tokens at the top. |
| `js/site.js` | Header/footer injection, nav, slideshow, reveals, lightbox, forms |
| `get-images.sh` | Downloads the 25 photos into `assets/img/` |
| `_PLAN.html` | The approved plan (design system + blueprints) |
| `_IMAGES.html` | Visual checklist of all photos |

## Conventions (for future edits)

- **Design tokens** live at the top of `css/site.css` (`:root`). Colours: lighter mix approved Aug 2026 — porcelain `#FAF6EF` ~70%, oat `#F4EDE1`, sand `#E7DAC5`, clay `#C08B5C` for buttons, umber `#4E3E2C` for text (lightened from the report's `#3A2E24`), sage + gold as rare accents. Footer is light (oat), not dark. Fonts: Cormorant Garamond (headlines) + Inter (body), loaded from Google Fonts.
- **Header/footer/menu are edited once** — in the `HEADER` / `MOBILE` / `FOOTER` strings inside `js/site.js`. Every page just has `<header data-site-header>` etc.
- **New page:** copy any inner page, change `<title>`, description and content. Pages with a photo hero use `body class="has-hero"` (transparent nav over the image).
- **Motion:** one easing `cubic-bezier(.22,1,.36,1)`. Add `class="reveal"` (+ optional `style="--d:.12s"` stagger) to anything that should fade up on scroll.
- **Voice:** warm, devotional, first-person. "May help you feel…", never medical claims. Sign-offs: *with love, Peter aka templeofsun*.
- **Facts only from the vault** — prices, dates, names. Nothing invented.

## Wired later (currently visual-only)

- **Newsletter + contact form + ebook signup** (aromatherapy.html) — front-end only; submitting shows a soft thank-you. To connect: Formspree (form `action`), Mailchimp/Buttondown embed for newsletter. The ebook itself doesn't exist yet — Peter provides the PDF, then the form delivers it.
- **Shop** — product cards say "Shop coming soon". When the shop exists, each card's footer gets a real link.
- **Retreat block** — when the next edition is confirmed: dates, venue, price + "Request your spot" button on `retreats.html`.
- **Fonts offline** — currently from Google Fonts CDN; can be self-hosted into `assets/fonts/` for a fully offline site.
