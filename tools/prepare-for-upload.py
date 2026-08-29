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


def write_robots(live: bool) -> str:
    if live:
        if not LIVE_SOURCE.exists():
            sys.exit(
                f"ERROR: {LIVE_SOURCE.name} is missing — cannot write the live robots.txt."
            )
        ROBOTS.write_text(LIVE_SOURCE.read_text(encoding="utf-8"), encoding="utf-8")
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
    run("stamp-shell.py", "menu and footer")
    run("apply-press-schema.py", "press credits")
    run("generate-headers.py", "header generation")

    mode = write_robots(live)
    print(f"robots.txt: {mode}")

    print("\nFolder is ready to upload.")
    if not live:
        print("Reminder: on launch day run this again with --live.")


if __name__ == "__main__":
    main()
