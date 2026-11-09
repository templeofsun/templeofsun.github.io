#!/usr/bin/env python3
"""
Temple of Sun — keep the photo lists in sitemap.xml true to the pages.

Each page in the sitemap carries a list of the photos on it, so Google Images
can find them. Those lists used to be written by hand and went stale: when the
retreat gallery changed, the sitemap still pointed at the old photos, and new
journal entries were given the Philosophy page's photos.

This reads every page (not the product pages, which generate-product-pages.py
handles) and rewrites its photo list from what is actually inside <main>:
images, gallery links and inline backgrounds under assets/img/, plus
the page's share picture (og:image). Logos, the
site logo and video posters are left out, since they are not photos of the
work. Journal entries also get their real publication date as lastmod.

It changes nothing else in the sitemap.

    python3 tools/sitemap-images.py           # rewrite
    python3 tools/sitemap-images.py --check   # report only
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITEMAP = ROOT / "sitemap.xml"
BASE = "https://templeofsun.com/"
SKIP = ("assets/img/logos/", "assets/img/posters/", "assets/img/logo")
IMG = re.compile(r"""(?:src|href)="((?:\.\./)?assets/img/[^"#?]+\.(?:webp|jpe?g|png))"|url\(['"]?((?:\.\./)?assets/img/[^'")]+)""")


def photos(page: Path) -> list:
    html = page.read_text(encoding="utf-8")
    m = re.search(r"<main\b.*?</main>", html, re.S)
    body = m.group(0) if m else html
    seen = []
    og = re.search(r'<meta property="og:image" content="' + re.escape(BASE) + r'(assets/img/[^"]+)"', html)
    if og and not og.group(1).startswith(SKIP) and (ROOT / og.group(1)).exists():
        seen.append(og.group(1))       # the picture the page is shared with
    for a, b in IMG.findall(body):
        p = (a or b).replace("../", "")
        if p.startswith(SKIP) or p in seen:
            continue
        if (ROOT / p).exists():
            seen.append(p)
    return seen


def main() -> None:
    check = "--check" in sys.argv
    xml = SITEMAP.read_text(encoding="utf-8")
    changed = []

    def fix(u):
        block, loc = u.group(0), u.group(1)
        rel = loc.replace(BASE, "") or "index.html"
        page = ROOT / rel
        if rel.startswith("products/") or not page.exists():
            return block
        imgs = photos(page)
        head = re.sub(r"\s*<image:image>.*?</image:image>", "", block, flags=re.S)
        head = head.replace("</url>", "").rstrip()
        if rel == "journal.html":       # the list is as new as its newest entry
            dates = sorted(re.findall(r'<time datetime="(\d{4}-\d{2}-\d{2})"', "".join(
                f.read_text(encoding="utf-8") for f in (ROOT / "journal").glob("*.html")
                if 'noindex' not in f.read_text(encoding="utf-8"))))
            if dates:
                head = re.sub(r"<lastmod>[^<]*</lastmod>", f"<lastmod>{dates[-1]}</lastmod>", head)
        if rel.startswith("journal/"):
            d = re.search(r'<time datetime="(\d{4}-\d{2}-\d{2})"', page.read_text(encoding="utf-8"))
            if d:
                head = re.sub(r"<lastmod>[^<]*</lastmod>", f"<lastmod>{d.group(1)}</lastmod>", head)
        lines = [f"    <image:image><image:loc>{BASE}{p}</image:loc></image:image>" for p in imgs]
        new = head + ("\n" + "\n".join(lines) if lines else "") + "\n  </url>"
        if new != block:
            changed.append(f"{rel} ({len(imgs)} photos)")
        return new

    out = re.sub(r"<url>\s*<loc>([^<]+)</loc>.*?</url>", fix, xml, flags=re.S)
    if changed:
        print("sitemap photos: " + ("would update " if check else "updated ") + ", ".join(changed))
        if not check:
            SITEMAP.write_text(out, encoding="utf-8")
    else:
        print("sitemap photos: every page's list already matches")


if __name__ == "__main__":
    main()
