# Translations (not started yet)

This folder is ready for the Portuguese, Hungarian and German versions of the site.
Nothing in here is live. No translated pages exist yet, and the English site is unchanged.

## Order

1. Finish the phone version.
2. Launch in English.
3. Wait until the English text is mostly settled (translating early means paying twice).
4. Portuguese first (`pt/`), then Hungarian (`hu/`), then German (`de/`).

## How it will work

- **English is the source.** Only the English pages are ever edited by hand.
- **One file per page per language**, for example `pt/retreats.json`. Each sentence is stored
  next to a fingerprint of the English it was translated from.
- **When the English changes**, the build tool lists which sentences are out of date in each
  language (for example: "retreats: 3 sentences out of date in pt, hu, de"). Only those get
  re-translated.
- **Nothing breaks while a translation is behind.** A missing or outdated sentence shows in
  English until it is updated.
- **The translated pages are built automatically** into `/pt/`, `/hu/` and `/de/` on the site,
  with the tags that tell Google which page matches which.
- **A language switcher** goes in the menu once the first language is ready.

## What gets translated

- 25 main pages and 23 blend pages (48 pages).
- Menu, footer, buttons, contact form, find-your-blend quiz.
- Page titles, Google descriptions, image descriptions.

## What stays as it is

- Journal posts stay in the language Péter wrote them in. The journal list page is translated,
  and each post shows a small "in English" label.
- Péter's name, the "templeofsun" logo text, place names.
- To decide with Péter later: blend names, Sanskrit words, prices.

## Who translates

First drafts by Claude. Péter, or a native speaker he trusts, reads each language before it
goes live. Most care with the health and safety wording on the oils.

## Not used

- Google Translate button: poor quality, and Google does not list those pages.
- Paid services like Weglot: monthly fee forever; the build tool does the same job for free.
