#!/usr/bin/env python3
"""
Temple of Sun — keep the journal list in step with the journal entries.

HOW THE JOURNAL WORKS

Every entry in journal/ is an ordinary page. Open one and edit it, the same as
any other page on the site. Nothing rewrites what you wrote.

To add a new entry, copy an existing one:

    cp journal/placeholder-example.html journal/my-new-entry.html

then change, inside that file:
    · the <title>
    · the description (it appears three times: description, og, twitter)
    · the canonical link, the og:url, and the two links in the data at the foot
    · the heading, the date and the writing itself

Then run tools/prepare-for-upload.py. This script finds it and adds it to:
    · journal.html   the list of entries, newest first, and the blog data in
                     its head that tells Google this is a blog section
    · sitemap.xml    so Google knows it exists
    · llms.txt       so AI assistants know it exists

Keep the <title> under about 60 characters and the description under about
160, or Google cuts the end off in the search result.

It also corrects the "N min read" line from the real word count, so that stays
honest even after you edit the writing.

TO KEEP AN ENTRY PRIVATE
Put this in the page's head and it is built and viewable, but kept out of the
list, out of the sitemap and out of llms.txt, and search engines are told to
ignore it:

    <meta name="robots" content="noindex, follow">

Change it back to the normal line to publish:

    <meta name="robots" content="max-snippet:-1, max-image-preview:large">

    python3 tools/sync-journal.py           # sync
    python3 tools/sync-journal.py --check   # report only, change nothing
"""

import html as html_mod
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JOURNAL = ROOT / "journal"
INDEX = ROOT / "journal.html"
SITEMAP = ROOT / "sitemap.xml"
LLMS = ROOT / "llms.txt"
BASE = "https://templeofsun.com/"

MONTHS = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]

LIST_START = "<!-- journal:list start -->"
LIST_END = "<!-- journal:list end -->"
LLMS_START = "<!-- journal start -->"
LLMS_END = "<!-- journal end -->"
BLOG_START = "<!-- journal:schema start -->"
BLOG_END = "<!-- journal:schema end -->"


def human(d: str) -> str:
    return f"{int(d[8:10])} {MONTHS[int(d[5:7]) - 1]} {d[:4]}"


def esc(s: str) -> str:
    return re.sub(r"&(?!amp;|lt;|gt;|quot;|#)", "&amp;", s)


def plain(s: str) -> str:
    return re.sub(r"\s+", " ", html_mod.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


def read_entries() -> list:
    """Everything the list needs, read out of the finished pages themselves."""
    entries, problems = [], []
    for f in sorted(JOURNAL.glob("*.html")):
        s = f.read_text(encoding="utf-8")

        h1 = re.search(r"<h1[^>]*>(.*?)</h1>", s, re.S)
        desc = re.search(r'<meta name="description" content="(.*?)">', s, re.S)
        cat = re.search(r'<span class="label">(.*?)</span>', s, re.S)
        when = re.search(r'<time datetime="(\d{4}-\d{2}-\d{2})"', s)
        robots = re.search(r'<meta name="robots" content="(.*?)"', s)

        missing = [n for n, v in (("a heading", h1), ("a description", desc),
                                  ("a date", when)) if not v]
        if missing:
            problems.append(f"journal/{f.name} has no {', no '.join(missing)}")
            continue

        # exactly one Article, and it must belong to this page
        articles = []
        for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
            try:
                d = json.loads(m.group(1))
            except json.JSONDecodeError:
                problems.append(f"journal/{f.name}: the data at the foot is not valid")
                continue
            if d.get("@type") == "Article":
                articles.append(d)
        if len(articles) != 1:
            problems.append(f"journal/{f.name}: found {len(articles)} Article blocks, expected 1")
        elif not articles[0].get("@id", "").startswith(f"{BASE}journal/{f.stem}"):
            problems.append(f"journal/{f.name}: its Article data points at another page")

        body = re.search(r'<div class="jr-body[^"]*"[^>]*>(.*)</div>\s*<aside', s, re.S)
        words = len(plain(body.group(1)).split()) if body else 0

        img = re.search(r'<figure class="jr-featured[^"]*">.*?src="\.\./([^"]+)"'
                        r'.*?alt="([^"]*)"', s, re.S)

        entries.append({
            "slug": f.stem,
            "file": f,
            "title": plain(h1.group(1)),
            "desc": html_mod.unescape(desc.group(1)),
            "cat": plain(cat.group(1)) if cat else "Journal",
            "date": when.group(1),
            "draft": "noindex" in (robots.group(1) if robots else ""),
            "words": words,
            "read": max(1, round(words / 200)) if words else 1,
            "img": img.group(1) if img else "",
            "alt": img.group(2) if img else "",
        })
    entries.sort(key=lambda e: e["date"], reverse=True)
    return entries, problems


def fix_read_time(e: dict) -> bool:
    """Keep 'N min read' true to what is actually written."""
    s = e["file"].read_text(encoding="utf-8")
    new = re.sub(r"\b\d+ min read", f"{e['read']} min read", s)
    if new != s:
        e["file"].write_text(new, encoding="utf-8")
        return True
    return False


def replace_block(path: Path, start: str, end: str, body: str, label: str) -> None:
    s = path.read_text(encoding="utf-8")
    i, j = s.find(start), s.find(end)
    if i == -1 or j == -1 or j < i:
        sys.exit(f"ERROR: {label}: the markers {start} / {end} are missing.")
    new = s[:i + len(start)] + "\n" + body + "\n" + s[j:]
    if new != s:
        path.write_text(new, encoding="utf-8")


def update_index(entries: list) -> None:
    live = [e for e in entries if not e["draft"]]
    if not live:
        rows = ('      <p class="jr-empty">The first entry is being written. '
                '<a href="contact.html">Write to me</a> in the meantime.</p>')
    else:
        rows = ""
        for e in live:
            thumb = ""
            if e["img"]:
                thumb = (f'<div class="jr-thumb"><div class="frame ratio-45">'
                         f'<img src="{e["img"]}" alt="{esc(e["alt"])}" width="1264" height="848" '
                         f'loading="lazy" decoding="async" data-onerr="hide"></div></div>')
            rows += (f'\n      <a class="jr-item reveal" href="journal/{e["slug"]}.html">\n'
                     f'        <div class="jr-item-body">\n'
                     f'          <span class="label">{esc(e["cat"])} &middot; {human(e["date"])}</span>\n'
                     f'          <h2>{esc(e["title"])}</h2>\n'
                     f'          <p>{esc(e["desc"])}</p>\n'
                     f'          <span class="lnk">Read<span class="arr">&rarr;</span></span>\n'
                     f'        </div>\n        {thumb}\n      </a>')
    replace_block(INDEX, LIST_START, LIST_END, rows.strip("\n"), "journal.html")
    s = INDEX.read_text(encoding="utf-8")
    count = (f'{len(live)} entr{"y" if len(live) == 1 else "ies"}'
             + (f' &middot; last written {human(live[0]["date"])}' if live else ""))
    s2 = re.sub(r'(<p class="jr-count">)[^<]*(</p>)', r"\g<1>" + count + r"\2", s, count=1)
    if s2 != s:
        INDEX.write_text(s2, encoding="utf-8")


def update_blog_schema(entries: list) -> None:
    """
    Tell search engines that journal.html is a blog, and which entries are in it.

    Without this the list page is just a page with links on it. With it, Google
    can see it is a blog section, whose it is, and what is inside. Every entry
    points back at the Article block on its own page, so nothing is said twice.

    Private entries are left out, the same as everywhere else.
    """
    live = [e for e in entries if not e["draft"]]
    blog = {
        "@context": "https://schema.org",
        "@type": "Blog",
        "@id": f"{BASE}journal.html#blog",
        "name": "The Temple of Sun Journal",
        "description": "Péter Frák's longer writing on aromatherapy, the blends and the practice.",
        "url": f"{BASE}journal.html",
        "inLanguage": "en",
        "author": {"@id": f"{BASE}#peter"},
        "publisher": {"@id": f"{BASE}#organization"},
        "isPartOf": {"@id": f"{BASE}#website"},
        "blogPost": [
            {
                "@type": "BlogPosting",
                "@id": f"{BASE}journal/{e['slug']}.html#article",
                "headline": e["title"],
                "description": plain(e["desc"]),
                "url": f"{BASE}journal/{e['slug']}.html",
                "datePublished": e["date"],
                "author": {"@id": f"{BASE}#peter"},
            }
            for e in live
        ],
    }
    if not live:                       # an empty list would be a lie
        blog.pop("blogPost")

    block = (BLOG_START + '\n<script type="application/ld+json">'
             + json.dumps(blog, ensure_ascii=False) + "</script>\n" + BLOG_END)

    s = INDEX.read_text(encoding="utf-8")
    if BLOG_START in s and BLOG_END in s:
        i, j = s.find(BLOG_START), s.find(BLOG_END) + len(BLOG_END)
        new = s[:i] + block + s[j:]
    else:
        anchor = "<!-- /meta:stamped -->"
        if anchor not in s:
            print("  ! journal.html has no <!-- /meta:stamped --> marker; blog data not added")
            return
        new = s.replace(anchor, block + "\n" + anchor, 1)
    if new != s:
        INDEX.write_text(new, encoding="utf-8")


def update_sitemap(entries: list) -> None:
    if not SITEMAP.exists():
        return
    live = [e for e in entries if not e["draft"]]
    xml = SITEMAP.read_text(encoding="utf-8")
    anchor = BASE + "philosophy.html"
    m = re.search(r"<url>\s*<loc>" + re.escape(anchor) + r"</loc>.*?</url>", xml, re.S)
    if not m:
        print("  ! could not find where to put the journal in the sitemap")
        return
    block = m.group(0)
    xml = re.sub(r"\s*<url>\s*<loc>" + re.escape(BASE) + r"journal[^<]*</loc>.*?</url>", "", xml, flags=re.S)
    added = [block.replace(anchor, BASE + "journal.html")]
    for e in live:
        added.append(block.replace(anchor, f"{BASE}journal/{e['slug']}.html"))
    m = re.search(r"<url>\s*<loc>" + re.escape(anchor) + r"</loc>.*?</url>", xml, re.S)
    SITEMAP.write_text(xml.replace(m.group(0), m.group(0) + "\n" + "\n".join(added)), encoding="utf-8")


def update_llms(entries: list) -> None:
    if not LLMS.exists():
        return
    live = [e for e in entries if not e["draft"]]
    lines = [f"- [The Journal]({BASE}journal.html): Péter's longer writing on aromatherapy, "
             "the blends and the practice"]
    for e in live:
        lines.append(f'- [{e["title"]}]({BASE}journal/{e["slug"]}.html): {plain(e["desc"])}')
    body = "\n".join(lines)
    s = LLMS.read_text(encoding="utf-8")
    if LLMS_START in s and LLMS_END in s:
        replace_block(LLMS, LLMS_START, LLMS_END, body, "llms.txt")
    else:
        anchor = "\n## Press & appearances"
        if anchor in s:
            LLMS.write_text(s.replace(anchor, "\n" + LLMS_START + "\n" + body + "\n" + LLMS_END + "\n" + anchor, 1),
                            encoding="utf-8")


def main() -> None:
    check_only = "--check" in sys.argv
    if not JOURNAL.exists():
        sys.exit("ERROR: there is no journal folder.")

    entries, problems = read_entries()
    if problems:
        print("journal: something is wrong with these entries —")
        for p in problems:
            print("    " + p)
        sys.exit("Fix them before uploading.")

    if not check_only:
        fixed = [e["slug"] for e in entries if fix_read_time(e)]
        update_index(entries)
        update_blog_schema(entries)
        update_sitemap(entries)
        update_llms(entries)
        if fixed:
            print(f"  reading time corrected on: {', '.join(fixed)}")

    live = [e for e in entries if not e["draft"]]
    print(f"journal: {len(entries)} entr{'y' if len(entries) == 1 else 'ies'}, "
          f"{len(live)} published, {len(entries) - len(live)} private")
    for e in entries:
        mark = "[private] " if e["draft"] else ""
        print(f"    {mark}journal/{e['slug']}.html — {e['read']} min, {e['words']} words")


if __name__ == "__main__":
    main()
