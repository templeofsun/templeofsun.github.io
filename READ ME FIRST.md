# How to upload

This is the whole website, split into folders small enough for GitHub.
GitHub refuses more than 100 files at a time. Nothing here is over 40.

Upload them **one folder at a time**, in any order. Folder 13 goes into a
`journal` folder — if it does not exist yet on GitHub, type `journal/` at the
start of the file name when uploading and GitHub creates it.

For each one:

1. Open the folder on GitHub named on the right below
2. Click **Add file → Upload files**
3. Drag in **the files** from the matching folder here — not the folder itself
4. Click **Commit changes**

Then do the next one.

| Folder here | Goes into, on GitHub |
|---|---|
| 1 - ROOT | the top level (where `index.html` lives) |
| 2 - css | `css` |
| 3 - js | `js` |
| 4 - products | `products` |
| 5 - tools | `tools` |
| 6 - assets | `assets` |
| 7 - assets_fonts | `assets` → `fonts` |
| 8 - assets_img | `assets` → `img` |
| 9 - assets_img_logos | `assets` → `img` → `logos` |
| 10 - assets_img_posters | `assets` → `img` → `posters` |
| 11 - assets_img_products | `assets` → `img` → `products` |
| 12 - assets_video | `assets` → `video` |
| 13 - journal | `journal` |

### You can probably skip folders 6 to 12

Those seven are pictures, fonts and video. **Nothing in them has changed since
August**, so if you have uploaded them to GitHub before, skip them and save
yourself about 100 files.

That leaves six: **1 - ROOT, 2 - css, 3 - js, 4 - products, 5 - tools,
13 - journal.** Upload only those and the site is current.

Upload all thirteen only if this is a brand-new repository.

Uploading a file that is already there just replaces it. That is fine and expected.

---

## Two things to know

**The site is still private.** `robots.txt` tells every search engine to stay
away, so nothing can appear in Google yet. That is on purpose.

**On launch day**, before uploading, run this once:

```
cd "path/to/the/website-folder"
python3 tools/prepare-for-upload.py --live
```

That swaps `robots.txt` to the public one, which welcomes search engines and
refuses AI training. Then upload the changed files as usual.

---

## Nothing has to be deleted

Uploading a file replaces the one already there, so the whole site refreshes
itself. Four old files stay behind on GitHub, and none of them do any harm:

| File | Why it is harmless |
|---|---|
| `about.html` | a redirect now sends anyone who finds it to `bio.html` |
| `assets/img/logos/vale-de-moses.webp` | an image no page uses |
| `get-images.sh` | an old helper script |
| `assets/fonts/.keep` | an empty placeholder |

Delete them one day if you want a tidy repository. The site does not need it.

---

## What changed this time

- Three new pages: **Health Consultation**, **Spiritual Mentoring**,
  **Meditation Guidance** — each one of Péter's online offerings, on its own
  page, in his own words. **Online Sessions** in the menu is now a drop-down
  holding those three.
- The **Healing** box on the home page now opens the online booking.
- **Links across the whole site** no longer show as browser blue.
- **Everything about Vale de Moses removed** — logo, text and hidden data.
- **A new page**: *The essence of you*, the poem written for Péter on retreat.
- **My Story and Bio are one page**, called My Story, at `bio.html`.
- **The six unfinished FAQ answers are written.** All 35 are live.
- The **23 blend pages** now carry the menu, the footer and the medical
  disclaimer, like every other page.
- **80 redirects** from the old WordPress addresses, so nothing that Google
  already knows becomes a dead end on launch day.
- **The 28 guest reviews** are marked up so search engines can read them.
- **A new Journal section**, with one Latin placeholder entry in it.
- Pages now show properly with JavaScript switched off, and for people who
  have asked their computer to reduce motion.

**The journal has one placeholder entry**, written in Latin. It is there so the
page can be seen with something in it. Replace it with Péter's first real entry
before launch day, or search engines will index the Latin.

Because `css/site.css` and the shared menu changed, nearly every page is newer
than what is on GitHub. That is why the whole site is in this upload.
