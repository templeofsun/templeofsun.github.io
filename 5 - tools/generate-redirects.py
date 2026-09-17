#!/usr/bin/env python3
"""
Temple of Sun — build the _redirects file.

The old WordPress site publishes about seventy addresses that Google has
indexed. The day templeofsun.com points at the new site, every one of them
would return "page not found" and the ranking behind it would be lost.

This turns tools/redirects.json into the _redirects file Cloudflare reads, and
checks as it goes that every destination is a page that actually exists. A typo
here is silent and expensive, so the script refuses to write a broken file.

    python3 tools/generate-redirects.py           # write it
    python3 tools/generate-redirects.py --check   # just report, change nothing

Run on its own, or let tools/prepare-for-upload.py run it for you.

Note: _redirects is read by Cloudflare Pages and Netlify. GitHub Pages ignores
it, exactly like _headers, so nothing changes until the domain moves.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "tools" / "redirects.json"
TARGET = ROOT / "_redirects"
CODE = 301  # permanent: this is what passes the old ranking to the new page


def target_exists(dest: str) -> bool:
    """Is this destination a real page in the folder?"""
    path = dest.split("#")[0].split("?")[0]
    if path in ("/", ""):
        return (ROOT / "index.html").exists()
    return (ROOT / path.lstrip("/")).exists()


def build() -> tuple[str, list, int]:
    if not SOURCE.exists():
        sys.exit(f"ERROR: {SOURCE.name} is missing.")
    data = json.loads(SOURCE.read_text(encoding="utf-8"))

    lines = [
        "# Temple of Sun — where every old address goes.",
        "#",
        "# GENERATED FILE. Do not edit by hand.",
        "# Rebuilt from tools/redirects.json by tools/prepare-for-upload.py",
        "#",
        "# Read by Cloudflare Pages and Netlify. Ignored by GitHub Pages.",
        "# Cloudflare takes the first line that matches, so the exact addresses",
        "# come first and the wildcards sit underneath as a safety net.",
        "",
    ]
    broken, count = [], 0
    width = 0
    for group in ("exact", "catchall"):
        for row in data.get(group, []):
            if row[0] != "_note":
                width = max(width, len(row[0]))
    width = min(width, 46)   # keep the file readable; one long URL should not pad them all

    for group in ("exact", "catchall"):
        rows = data.get(group, [])
        if group == "catchall" and rows:
            lines.append("")
            lines.append("# --- wildcards: anything the sitemaps did not list ---")
        for src, dest in rows:
            if src == "_note":
                lines.append("")
                lines.append(f"# {dest}")
                continue
            if "*" not in dest and not target_exists(dest):
                broken.append((src, dest))
            lines.append(f"{src.ljust(width)}  {dest}  {CODE}")
            count += 1

    lines.append("")
    return "\n".join(lines), broken, count


def main() -> None:
    check_only = "--check" in sys.argv
    text, broken, count = build()

    if broken:
        print(f"ERROR: {len(broken)} redirect(s) point at a page that does not exist:")
        for src, dest in broken:
            print(f"  {src}  ->  {dest}")
        sys.exit("Fix tools/redirects.json before deploying.")

    if check_only:
        current = TARGET.read_text(encoding="utf-8") if TARGET.exists() else ""
        if current == text:
            print(f"Up to date. {count} redirects, every destination resolves.")
        else:
            sys.exit("OUT OF DATE — run: python3 tools/generate-redirects.py")
        return

    if not TARGET.exists() or TARGET.read_text(encoding="utf-8") != text:
        TARGET.write_text(text, encoding="utf-8")
    print(f"redirects: {count} written, every destination resolves")


if __name__ == "__main__":
    main()
