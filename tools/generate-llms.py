#!/usr/bin/env python3
"""
Temple of Sun — keep llms.txt honest.

llms.txt is the map ChatGPT, Claude, Perplexity and Google's AI read to work out
what is on this site. A page missing from it is a page they may never quote.

The 23 blend pages carry the best writing on the site — around thirteen thousand
words of Péter's own descriptions — and were the only pages not listed. This
builds that section straight from the pages themselves, so it can never fall
behind again, and then checks that every single page on the site is mentioned
somewhere in the file.

The hand-written parts of llms.txt are left alone. Only the block between

    <!-- blends start -->  ...  <!-- blends end -->

is rewritten.

    python3 tools/generate-llms.py           # write it
    python3 tools/generate-llms.py --check   # report only, change nothing

Run on its own, or let tools/prepare-for-upload.py run it for you.
"""

import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LLMS = ROOT / "llms.txt"
BASE = "https://templeofsun.com/"
START = "<!-- blends start -->"
END = "<!-- blends end -->"


def blend_facts(path: Path) -> dict | None:
    """Pull name, price and one honest line out of a blend page."""
    s = path.read_text(encoding="utf-8")
    product = None
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try:
            d = json.loads(m.group(1))
        except json.JSONDecodeError:
            continue
        for node in (d["@graph"] if "@graph" in d else [d]):
            if node.get("@type") == "Product":
                product = node
    if not product:
        return None

    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", s, re.S)
    name = html.unescape(re.sub(r"<[^>]+>", "", h1.group(1))).strip() if h1 else product["name"]

    # which collection does it belong to
    crumb = re.search(r'"name": "(The Rainbow Collection|The 5 Elements)"', s)
    collection = crumb.group(1) if crumb else (
        "The 5 Elements" if "5 Elements" in s[:4000] else "The Rainbow Collection")

    price = product.get("offers", {}).get("price")
    return {
        "slug": path.stem,
        "name": name,
        "line": html.unescape(product.get("description", "")).split(" Hand-blended")[0].strip().rstrip("."),
        "collection": collection,
        "price": price,
    }


def build_block() -> tuple[str, int]:
    pages = sorted((ROOT / "products").glob("*.html"))
    rows = [f for f in (blend_facts(p) for p in pages) if f]
    rainbow = [r for r in rows if r["collection"] == "The Rainbow Collection"]
    elements = [r for r in rows if r["collection"] == "The 5 Elements"]

    out = [START, "",
           f"## The {len(rows)} blends",
           "",
           "Every blend has its own page, with the plants inside it, how to use it, "
           "who it is not for, and what it was made for. Prices are in euros.",
           ""]
    for title, group in (("The Rainbow Collection", rainbow), ("The 5 Elements", elements)):
        if not group:
            continue
        out.append(f"### {title}")
        out.append("")
        for r in group:
            price = f" · €{r['price']}" if r["price"] else ""
            out.append(f"- [{r['name']}]({BASE}products/{r['slug']}.html): {r['line']}{price}")
        out.append("")
    out.append(END)
    return "\n".join(out), len(rows)


def coverage() -> list:
    """Every page on the site should appear somewhere in llms.txt."""
    text = LLMS.read_text(encoding="utf-8")
    missing = []
    for p in sorted(ROOT.glob("*.html")) + sorted((ROOT / "products").glob("*.html")):
        if p.name == "404.html":
            continue
        rel = p.name if p.parent == ROOT else f"products/{p.name}"
        if rel == "index.html":
            rel_url = BASE
        else:
            rel_url = BASE + rel
        if rel_url not in text:
            missing.append(rel)
    return missing


def main() -> None:
    check_only = "--check" in sys.argv
    if not LLMS.exists():
        sys.exit("ERROR: llms.txt is missing.")
    text = LLMS.read_text(encoding="utf-8")
    block, n = build_block()

    if START in text and END in text:
        new = re.sub(re.escape(START) + r".*?" + re.escape(END), lambda _m: block, text, flags=re.S)
    else:
        # first run: slot the blends in just before the Press section
        anchor = "\n## Press & appearances"
        if anchor not in text:
            sys.exit("ERROR: cannot find where to put the blends in llms.txt.")
        new = text.replace(anchor, "\n" + block + "\n" + anchor, 1)

    if check_only:
        if new != text:
            sys.exit("OUT OF DATE — run: python3 tools/generate-llms.py")
    elif new != text:
        LLMS.write_text(new, encoding="utf-8")

    missing = coverage()
    print(f"llms.txt: {n} blends listed")
    if missing:
        print(f"  ! {len(missing)} page(s) still not mentioned anywhere: {', '.join(missing)}")
    else:
        print("  every page on the site is listed")


if __name__ == "__main__":
    main()
