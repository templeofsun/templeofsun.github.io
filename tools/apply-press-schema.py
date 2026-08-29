#!/usr/bin/env python3
"""
Temple of Sun — put Péter's press credits into every page's structured data.

Add a credit once to `tools/press-credits.json`, run this, and it appears in the
invisible data Google and AI assistants read on every page of the site. There is
nothing to copy by hand.

Why every page and not just bio.html: search engines and AI crawlers do not
always reach the bio. Whichever page they land on, they should be able to see
that this person is an invited speaker and a named expert. The credits sit
*inside* the Person entity, so they read as facts about Péter — not as a claim
that the page itself is about the event.

Run directly, or let `tools/prepare-for-upload.py` run it for you:

    python3 tools/apply-press-schema.py
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CREDITS = ROOT / "tools" / "press-credits.json"
PERSON_ID = "https://templeofsun.com/#peter"


def load_credits() -> dict:
    if not CREDITS.exists():
        sys.exit(f"ERROR: {CREDITS.name} is missing.")
    data = json.loads(CREDITS.read_text(encoding="utf-8"))
    return {k: v for k, v in data.items() if not k.startswith("_")}


def main() -> None:
    credits = load_credits()
    pages = sorted(ROOT.glob("*.html")) + sorted((ROOT / "products").glob("*.html"))

    touched = 0
    skipped = []

    for page in pages:
        text = page.read_text(encoding="utf-8")
        changed = False

        def patch(match):
            nonlocal changed
            try:
                data = json.loads(match.group(1))
            except json.JSONDecodeError:
                return match.group(0)
            graph = data.get("@graph", [data])
            for node in graph:
                if node.get("@type") == "Person" and node.get("@id") == PERSON_ID:
                    for key, value in credits.items():
                        node[key] = value
                    changed = True
            if not changed:
                return match.group(0)
            out = data if "@graph" in data else graph[0]
            return ('<script type="application/ld+json">'
                    + json.dumps(out, ensure_ascii=False, separators=(", ", ": "))
                    + "</script>")

        new_text = re.sub(
            r'<script type="application/ld\+json">(.*?)</script>', patch, text, flags=re.S
        )

        if changed:
            if new_text != text:
                page.write_text(new_text, encoding="utf-8")
            touched += 1
        else:
            skipped.append(page.name)

    total = sum(len(v) for v in credits.values())
    print(f"press credits: {total} applied to {touched} pages")
    if skipped:
        print(f"  no Person entity on: {', '.join(skipped)}")


if __name__ == "__main__":
    main()
