# ⚠️ READ THIS ON LAUNCH DAY

Whenever that day comes — next week, next year.

**How this site deploys:** you upload the folder to GitHub by hand, and
Cloudflare copies it as-is. There is **no build step**. Whatever sits in the
folder is exactly what the world sees. So the folder has to be correct
*before* it leaves your computer.

---

## 1. Before you upload — one command

```bash
cd "path/to/the/website-folder"
python3 tools/prepare-for-upload.py --live
```

The `--live` matters. It publishes the real `robots.txt`. Without it the site
stays blocked from every search engine.

That single command:

1. Publishes the real robots.txt — search engines welcome, AI training refused
2. Refreshes the readable version of the Find Your Blend quiz
3. Rebuilds the security headers, which is what scores **A+**

Then upload the folder as normal.

Easier option: just ask Claude to "prepare the site files for launch" and it
runs the same thing.

---

## 2. Cloudflare Pages settings

| Field | What to put |
|---|---|
| Framework preset | None |
| Build command | **leave empty** |
| Build output directory | `/` |

Then Custom domains → add `templeofsun.com`.

No CNAME file. That is a GitHub Pages thing; Cloudflare attaches the domain in
the dashboard.

---

## 3. The rule that applies forever after

**Edit any page → run `prepare-for-upload.py --live` → then upload.**

If you skip it, the security policy no longer matches the page you changed, and
that page's scripts stop running once live. To check without changing anything:

```bash
python3 tools/generate-headers.py --check
```

It answers "Up to date" or "OUT OF DATE". Nothing else.

If Claude makes the change for you, this is already done — the folder comes back
ready.

---

## 4. Files that must stay exactly where they are

| File | What it does | Do not |
|---|---|---|
| `c59f5cc5a8bdcc9d632453126db078c0.txt` | IndexNow key — tells Bing/Yandex instantly when pages change | rename, move or delete |
| `sitemap.xml` | Lists all 45 pages for search engines | move out of the root |
| `llms.txt` / `llms-full.txt` | What AI assistants read to learn who you are | move out of the root |
| `robots-live.txt` | The real robots.txt, copied into place by `--live` | delete or rename |
| `_headers` | The security policy | edit by hand — it is regenerated |
| `js/img-fallback.js` | Handles images that fail to load | delete |
| `tools/` | The scripts that keep everything in step | delete |
| `products/` | The 23 blend pages — generated, one per formula | edit by hand; they are rebuilt |

All of these sit at the **top level** of the site. Their addresses are baked
into the sitemap and into search-engine settings.

---

## 5. HSTS preload — think before keeping it

The security file contains the word `preload`. It tells browsers "never load
this domain over plain http, ever", and it is hard to undo.

Only keep it once templeofsun.com and every subdomain work properly over https.
If unsure at launch, remove the word `preload` from
`tools/generate-headers.py`, rerun the prepare command, and add it back a week
later once the site is proven healthy.

---

## After it is live — 4 checks

1. Visit `templeofsun.com/robots.txt`. It must **not** say `Disallow: /`.
   If it does, you forgot `--live`.
2. Open the site, press F12 → Console. Any red "Refused to load…" line means
   something needs allowing in the policy. There were none in testing.
3. Scan at https://securityheaders.com — expect **A+**.
4. Submit `templeofsun.com/sitemap.xml` in Google Search Console.

---

## One thing to remember afterwards

Anything you add later that loads from another domain **will be blocked** —
YouTube embed, Google Analytics, a booking widget, Google Fonts. That is the
security policy doing its job, not a bug. Tell Claude what you added and it will
allow that one domain.

---

Full detail: `SECURITY-HEADERS.md` in this folder.
Site as it was before this work: `../Website-backup-before-csp/`
