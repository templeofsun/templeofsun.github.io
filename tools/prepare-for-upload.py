#!/usr/bin/env python3
"""
Temple of Sun — get the folder ready to upload to GitHub.

Run this after ANY change to the site, then upload the folder as usual:

    cd "path/to/the/website-folder"
    python3 tools/prepare-for-upload.py            # while the site is private
    python3 tools/prepare-for-upload.py --live     # on launch day and after

It does four things:

1. Rebuilds the 23 blend pages from the DATA in the two collection pages,
   and relinks them from the collections and the sitemap.
2. Syncs Péter's press credits (tools/press-credits.json) into the structured
   data on every page.
3. Writes the right robots.txt.
   default  -> blocks every crawler, so the unfinished site stays private
   --live   -> the real one: search engines welcome, AI training refused
4. Rebuilds _headers so the security policy matches the pages.

Step 4 is the one that matters most. The policy carries a fingerprint of the
code inside each page. Edit a page without rerunning this, and that page's
scripts stop working once it is live.

There is no build step on Cloudflare. Whatever sits in this folder is exactly
what gets served.
"""

import re
import sys
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent.parent

LIVE_SOURCE = ROOT / "robots-live.txt"
ROBOTS = ROOT / "robots.txt"

PRIVATE_ROBOTS = """# SITE NOT PUBLIC YET.
# Every crawler is blocked so unfinished pages never reach search results.
#
# On launch day, run:  python3 tools/prepare-for-upload.py --live
# That replaces this file with robots-live.txt, which welcomes search engines
# and refuses AI training.

User-agent: *
Disallow: /
"""


def check_live_robots(text: str) -> None:
    """
    Refuse to launch with a robots.txt that hides the site.

    The live file blocks AI training crawlers on purpose, so a bare search for
    'Disallow: /' would trip on those and mean nothing. What matters is the one
    group that everybody else falls into: 'User-agent: *'. If that group says
    Disallow: /, the entire site disappears from Google and nobody notices for
    weeks. So this reads the file the way a crawler does — user-agent lines
    group together until a rule line appears — and inspects only that group.
    """
    agents: list[str] = []
    star_rules: list[tuple[str, str]] = []
    collecting = False

    for raw in text.splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line or ":" not in line:
            continue
        field, _, value = line.partition(":")
        field, value = field.strip().lower(), value.strip()
        if field == "user-agent":
            if collecting:          # a new group begins
                agents, collecting = [], False
            agents.append(value)
        elif field in ("allow", "disallow"):
            collecting = True
            if "*" in agents:
                star_rules.append((field, value))

    if not star_rules:
        sys.exit("ERROR: robots-live.txt has no rules for 'User-agent: *'. "
                 "Search engines would have nothing to follow.")
    for field, value in star_rules:
        if field == "disallow" and value == "/":
            sys.exit("ERROR: robots-live.txt blocks every crawler — 'User-agent: *' "
                     "has 'Disallow: /'.\nThe whole site would vanish from Google. "
                     "Fix that line before launching.")
    if not any(f == "allow" and v == "/" for f, v in star_rules):
        print("  ! note: 'User-agent: *' has no 'Allow: /'. That is legal, but check "
              "it is what you meant.")
    if not re.search(r"(?im)^\s*sitemap:\s*http", text):
        sys.exit("ERROR: robots-live.txt has no Sitemap line. Add it before launching.")


def write_robots(live: bool) -> str:
    if live:
        if not LIVE_SOURCE.exists():
            sys.exit(
                f"ERROR: {LIVE_SOURCE.name} is missing — cannot write the live robots.txt."
            )
        text = LIVE_SOURCE.read_text(encoding="utf-8")
        check_live_robots(text)
        ROBOTS.write_text(text, encoding="utf-8")
        return "LIVE — search engines welcome, AI training refused"
    ROBOTS.write_text(PRIVATE_ROBOTS, encoding="utf-8")
    return "PRIVATE — every crawler blocked"


def run(script: str, label: str) -> None:
    result = subprocess.run([sys.executable, str(ROOT / "tools" / script)], cwd=str(ROOT))
    if result.returncode != 0:
        sys.exit(f"ERROR: {label} failed — fix this before uploading.")


def main() -> None:
    live = "--live" in sys.argv

    # Content first — the headers are fingerprinted from the finished pages,
    # so anything that rewrites a page has to run before them.
    run("generate-product-pages.py", "product pages")
    run("generate-session-pages.py", "online session pages")
    run("build-poem-page.py", "the poem page")
    run("sync-journal.py", "the journal list")
    run("sitemap-images.py", "the photo lists in the sitemap")
    run("stamp-shell.py", "menu and footer")
    run("apply-press-schema.py", "press credits")
    run("generate-reviews-schema.py", "guest reviews")
    run("generate-faq-schema.py", "the FAQ data")
    run("generate-llms.py", "the AI map")
    run("generate-redirects.py", "redirects from the old site")
    run("generate-headers.py", "header generation")

    mode = write_robots(live)
    print(f"robots.txt: {mode}")

    print("\nFolder is ready to upload.")
    if live:
        print("\n" + "=" * 62)
        print("LAUNCH DAY — do not skip this")
        print("=" * 62)
        print("robots.txt now says search engines are welcome. That only counts")
        print("once it is actually on the server. AFTER uploading, check it:")
        print()
        print("    curl -s https://templeofsun.com/robots.txt")
        print()
        print("You should see 'Allow: /'. If you see 'Disallow: /', the upload")
        print("did not take and the whole site is invisible to Google.")
        print("=" * 62)
    else:
        print("Reminder: on launch day run this again with --live.")


if __name__ == "__main__":
    main()
