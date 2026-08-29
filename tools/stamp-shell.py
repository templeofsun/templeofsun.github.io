#!/usr/bin/env python3
"""
Temple of Sun — copy the menu and footer from js/site.js into every page.

Why this exists
---------------
The menu is written once, in js/site.js. But every page in the root folder also
carries a copy of that menu inside its own HTML, so the page shows a full menu
the instant it loads, before any JavaScript runs. Search engines and anyone with
JavaScript switched off see it too.

That means the same menu lives in 45 places. Change js/site.js and those copies
go stale: the site.js code only fills a host that is empty, so an existing copy
is left exactly as it was.

This script is what keeps them honest. It reads the real menu out of
js/site.js and writes it into every page that carries a copy.

The blend pages in products/ are left alone on purpose: their hosts are empty,
so site.js fills them at load time and rewrites the links with ../ in front.

Run directly, or let tools/prepare-for-upload.py run it for you:

    python3 tools/stamp-shell.py
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE_JS = ROOT / "js" / "site.js"

# Which JavaScript variable fills which host in the page.
HOSTS = [
    ("HEADER", "header", "data-site-header", "site-header"),
    ("MOBILE", "div", "data-site-mobile", "mobile-menu"),
    ("FOOTER", "footer", "data-site-footer", "site-footer"),
]


def strip_comments(js: str) -> str:
    return re.sub(r"/\*.*?\*/", "", js, flags=re.S)


def read_icons(js: str) -> dict:
    """The IC object: a name for each small social symbol."""
    m = re.search(r"var IC = \{(.*?)\n  \};", js, re.S)
    if not m:
        sys.exit("ERROR: could not find the IC icon list in js/site.js.")
    icons = {}
    for key, val in re.findall(r"(\w+):\s*'((?:[^'\\]|\\.)*)'", m.group(1)):
        icons[key] = val.replace("\\'", "'")
    return icons


def read_var(js: str, name: str, icons: dict) -> str:
    """Rebuild one of the big HTML strings out of its pieces."""
    m = re.search(r"var " + name + r" =\s*(.*?);\n", js, re.S)
    if not m:
        sys.exit(f"ERROR: could not find {name} in js/site.js.")
    body = strip_comments(m.group(1))
    out = []
    for token in re.finditer(r"'((?:[^'\\]|\\.)*)'|IC\.(\w+)", body):
        if token.group(1) is not None:
            out.append(token.group(1).replace("\\'", "'"))
        else:
            key = token.group(2)
            if key not in icons:
                sys.exit(f"ERROR: {name} uses IC.{key}, which does not exist.")
            out.append(icons[key])
    if not out:
        sys.exit(f"ERROR: {name} came out empty — the shape of js/site.js changed.")
    return "".join(out)


def find_host(text: str, tag: str, attr: str):
    """
    Locate one host element and the exact span of what sits inside it.

    A plain search for the next closing tag is not safe here: the mobile menu is
    a <div> full of other <div>s, so the first </div> belongs to a child, not to
    the host. This walks forward counting opening and closing tags of the same
    name until the count returns to zero.

    Returns (inner_start, inner_end, element_end) or None.
    """
    opening = re.search(r"<" + tag + r"\s+" + attr + r"[^>]*>", text)
    if not opening:
        return None
    depth = 1
    pos = opening.end()
    token = re.compile(r"<(/?)" + tag + r"(?=[\s/>])", re.I)
    while depth:
        m = token.search(text, pos)
        if not m:
            return None                    # unbalanced markup: leave it alone
        depth += -1 if m.group(1) else 1
        pos = m.end()
    close = text.index(">", pos) + 1
    return opening.end(), close - len(f"</{tag}>"), close


def main() -> None:
    if not SITE_JS.exists():
        sys.exit("ERROR: js/site.js is missing.")
    js = SITE_JS.read_text(encoding="utf-8")
    icons = read_icons(js)
    markup = {name: read_var(js, name, icons) for name, _, _, _ in HOSTS}

    pages = sorted(ROOT.glob("*.html"))
    changed, empty_hosts = [], 0

    for page in pages:
        text = page.read_text(encoding="utf-8")
        before = text
        for name, tag, attr, css in HOSTS:
            found = find_host(text, tag, attr)
            if not found:
                continue
            inner_start, inner_end, _ = found
            if not text[inner_start:inner_end].strip():
                empty_hosts += 1          # site.js will fill this one at load
                continue
            text = text[:inner_start] + markup[name] + text[inner_end:]
        if text != before:
            page.write_text(text, encoding="utf-8")
            changed.append(page.name)

    print(f"shell: {len(pages)} pages checked, {len(changed)} updated")
    if changed:
        preview = ", ".join(changed[:6])
        more = f" and {len(changed)-6} more" if len(changed) > 6 else ""
        print(f"  {preview}{more}")
    if empty_hosts:
        print(f"  {empty_hosts} empty hosts left for site.js to fill")


if __name__ == "__main__":
    main()
