#!/usr/bin/env python3
"""
Temple of Sun — keep the FAQ page and its search data saying the same thing.

The FAQ exists twice: once as the page a person reads, and once as a hidden
copy that Google and AI assistants read. Google can print those answers straight
into search results.

Keeping two copies in step by hand does not work. Six answers were written on
the page and never reached the hidden copy, and it took an outside audit to
notice. So the hidden copy is now built from the page itself, every time.

One rule worth keeping: an answer still marked "faq-todo" is left out. Better
that Google shows nothing for a question than shows "Peter is writing this
answer" under the site's own name.

    python3 tools/generate-faq-schema.py           # write it
    python3 tools/generate-faq-schema.py --check   # report only

Run on its own, or let tools/prepare-for-upload.py run it for you.
"""

import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "faq.html"
BASE = "https://templeofsun.com/"


def text_of(fragment: str) -> str:
    """Readable text from a chunk of markup, links flattened to their words."""
    t = re.sub(r"<br\s*/?>", " ", fragment)
    t = re.sub(r"</p>\s*<p[^>]*>", " ", t)
    t = re.sub(r"<[^>]+>", "", t)
    return re.sub(r"\s+", " ", html.unescape(t)).strip()


def read_questions() -> tuple[list, list]:
    s = PAGE.read_text(encoding="utf-8")
    body = re.sub(r"<script.*?</script>", "", s, flags=re.S)
    ready, waiting = [], []
    pattern = (r'<details class="faq-q"(?:\s+id="([^"]*)")?>\s*'
               r"<summary>(.*?)</summary>\s*"
               r'<div class="faq-a[^"]*">(.*?)</div>\s*</details>')
    for m in re.finditer(pattern, body, re.S):
        qid, q, a = m.group(1) or "", m.group(2), m.group(3)
        question, answer = text_of(q), text_of(a)
        if not question or not answer:
            continue
        if "faq-todo" in a:
            waiting.append(question)
            continue
        ready.append({"id": qid, "q": question, "a": answer})
    return ready, waiting


def build(items: list) -> str:
    faq = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "@id": BASE + "faq.html#faq",
        "mainEntity": [
            {"@type": "Question",
             "name": it["q"],
             "acceptedAnswer": {"@type": "Answer", "text": it["a"]}}
            for it in items
        ],
        "speakable": {"@type": "SpeakableSpecification",
                      "cssSelector": [".faq-a-ready"]},
    }
    return ('<script type="application/ld+json">'
            + json.dumps(faq, ensure_ascii=False, separators=(", ", ": "))
            + "</script>")


def main() -> None:
    check_only = "--check" in sys.argv
    if not PAGE.exists():
        sys.exit("ERROR: faq.html is missing.")
    ready, waiting = read_questions()
    if not ready:
        sys.exit("ERROR: no finished questions found on faq.html — has the markup changed?")

    s = PAGE.read_text(encoding="utf-8")
    block = build(ready)
    new, n = re.subn(
        r'<script type="application/ld\+json">\{"@context": "https://schema\.org", "@type": "FAQPage".*?</script>',
        lambda _m: block, s, count=1, flags=re.S)
    if n != 1:
        sys.exit("ERROR: could not find the FAQ data block in faq.html.")

    if check_only:
        if new != s:
            sys.exit("OUT OF DATE — run: python3 tools/generate-faq-schema.py")
        print(f"Up to date. {len(ready)} questions published.")
        return

    if new != s:
        PAGE.write_text(new, encoding="utf-8")
    print(f"faq: {len(ready)} questions in the search data")
    if waiting:
        print(f"  {len(waiting)} still unanswered, kept out on purpose:")
        for q in waiting:
            print(f"    · {q}")


if __name__ == "__main__":
    main()
