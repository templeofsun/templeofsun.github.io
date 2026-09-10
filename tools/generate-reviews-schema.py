#!/usr/bin/env python3
"""
Temple of Sun — make the guest reviews readable by search engines.

Twenty-eight named guests have written about Péter on the home page. To a
person they are the most persuasive thing on the site. To Google and to AI
assistants they were invisible: real words, real names, and no markup saying
what they are.

This reads the reviews straight out of index.html and writes them into the
page's structured data, each one attached to Péter's practice. Change a review
on the page, run this, and the data follows.

No aggregate star rating is produced, on purpose. Google treats a business
publishing its own average as self-serving and can penalise the whole site for
it. Individual reviews, honestly attributed, are the safe and effective form.

    python3 tools/generate-reviews-schema.py           # write it
    python3 tools/generate-reviews-schema.py --check   # report only

Run on its own, or let tools/prepare-for-upload.py run it for you.
"""

import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "index.html"
BASE = "https://templeofsun.com/"
MARK_START = "<!-- reviews:schema -->"
MARK_END = "<!-- /reviews:schema -->"

# What each guest is talking about, so the review attaches to the right thing.
TOPIC_TO_SERVICE = {
    "treatments": ("Holistic treatments", BASE + "treatments.html"),
    "retreats": ("Soul Alchemy Retreats", BASE + "retreats.html"),
    "meditation": ("Meditation classes", BASE + "meditation.html"),
    "oils": ("templeofsun aromatherapy blends", BASE + "collections.html"),
}


def clean(text: str) -> str:
    return html.unescape(re.sub(r"<[^>]+>", "", text)).strip()


def read_reviews() -> list:
    s = PAGE.read_text(encoding="utf-8")
    out = []
    for m in re.finditer(r'<figure class="voice"([^>]*)>(.*?)</figure>', s, re.S):
        attrs, body = m.group(1), m.group(2)
        name = re.search(r'class="voice-name">(.*?)</span>', body, re.S)
        quote = re.search(r"<blockquote>(.*?)</blockquote>", body, re.S)
        if not name or not quote:
            continue
        sub = re.search(r'class="voice-sub">(.*?)</span>', body, re.S)
        topics = re.search(r'data-topics="([^"]*)"', attrs)
        topics = topics.group(1).split() if topics else []
        out.append({
            "name": clean(name.group(1)),
            "sub": clean(sub.group(1)) if sub else None,
            "text": clean(quote.group(1)).strip("“”\"'"),
            "topics": topics,
        })
    return out


def build(reviews: list) -> str:
    nodes = []
    for i, r in enumerate(reviews, 1):
        author = {"@type": "Person", "name": r["name"]}
        if r["sub"]:
            author["worksFor"] = {"@type": "Organization", "name": r["sub"]}
        node = {
            "@type": "Review",
            "@id": f"{BASE}#review-{i}",
            "reviewBody": r["text"],
            "author": author,
            "reviewRating": {"@type": "Rating", "ratingValue": 5,
                             "bestRating": 5, "worstRating": 1},
            "itemReviewed": {"@id": BASE + "#organization"},
            "publisher": {"@id": BASE + "#organization"},
        }
        for t in r["topics"]:
            if t in TOPIC_TO_SERVICE:
                name, url = TOPIC_TO_SERVICE[t]
                node["about"] = {"@type": "Service", "name": name, "url": url}
                break
        nodes.append(node)

    graph = {"@context": "https://schema.org", "@graph": nodes}
    return (MARK_START + '\n<script type="application/ld+json">'
            + json.dumps(graph, ensure_ascii=False, separators=(", ", ": "))
            + "</script>\n" + MARK_END)


def main() -> None:
    check_only = "--check" in sys.argv
    if not PAGE.exists():
        sys.exit("ERROR: index.html is missing.")
    reviews = read_reviews()
    if not reviews:
        sys.exit("ERROR: no guest reviews found on index.html — has the markup changed?")

    block = build(reviews)
    s = PAGE.read_text(encoding="utf-8")

    if MARK_START in s and MARK_END in s:
        new = re.sub(re.escape(MARK_START) + r".*?" + re.escape(MARK_END),
                     lambda _m: block, s, flags=re.S)
    else:
        anchor = "<!-- /meta:stamped -->"
        if anchor not in s:
            sys.exit("ERROR: cannot find where to put the review data in index.html.")
        new = s.replace(anchor, anchor + "\n" + block, 1)

    if check_only:
        if new != s:
            sys.exit("OUT OF DATE — run: python3 tools/generate-reviews-schema.py")
        print(f"Up to date. {len(reviews)} reviews marked up.")
        return

    if new != s:
        PAGE.write_text(new, encoding="utf-8")
    named = sum(1 for r in reviews if r["sub"])
    print(f"reviews: {len(reviews)} marked up ({named} with an organisation)")


if __name__ == "__main__":
    main()
