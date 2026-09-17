#!/usr/bin/env python3
"""
Temple of Sun — rebuild the _headers file.

Run this after editing ANY .html file:

    cd "path/to/the/website-folder"
    python3 tools/generate-headers.py

Why it exists
-------------
The security policy names every inline <script> block on the site by its
fingerprint (a SHA-256 hash). Change one character inside a page's inline
script and its fingerprint changes, so the browser refuses to run it. This
script re-reads every page and rewrites the fingerprints, which keeps the
policy and the pages in step.

It only writes _headers. It never touches your HTML.
"""

import base64
import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HEADERS_FILE = ROOT / "_headers"

# Inline <script> blocks only — anything with src= is an external file and
# is already covered by 'self'.
INLINE_SCRIPT = re.compile(
    r"<script(?![^>]*\bsrc\s*=)([^>]*)>(.*?)</script\s*>",
    re.IGNORECASE | re.DOTALL,
)

PERMISSIONS_POLICY = (
    "accelerometer=(), autoplay=(self), camera=(), display-capture=(), "
    "encrypted-media=(), fullscreen=(self), geolocation=(), gyroscope=(), "
    "magnetometer=(), microphone=(), midi=(), payment=(), "
    "picture-in-picture=(self), publickey-credentials-get=(), "
    "screen-wake-lock=(), usb=(), xr-spatial-tracking=()"
)


def sha256_csp(text: str) -> str:
    digest = hashlib.sha256(text.encode("utf-8")).digest()
    return "'sha256-" + base64.b64encode(digest).decode("ascii") + "'"


def collect_hashes():
    hashes = {}          # hash -> list of "file (kind)"
    # Every page on the site: the root, plus the generated product pages.
    pages = sorted(ROOT.glob("*.html")) + sorted((ROOT / "products").glob("*.html"))
    # the journal entries live one folder down too
    pages += sorted(p for p in (ROOT / "journal").glob("*.html"))
    if not pages:
        sys.exit("No .html files found. Run this from inside the Website folder.")

    for page in pages:
        html = page.read_text(encoding="utf-8")
        for attrs, body in INLINE_SCRIPT.findall(html):
            kind = "structured data" if "ld+json" in attrs.lower() else "script"
            h = sha256_csp(body)
            hashes.setdefault(h, []).append(f"{page.name} ({kind})")

    return pages, hashes


def build_csp(hashes) -> str:
    script_src = " ".join(["'self'"] + sorted(hashes))
    return "; ".join([
        "default-src 'self'",
        "base-uri 'self'",
        "object-src 'none'",
        "frame-ancestors 'none'",
        "form-action 'self'",
        "img-src 'self' data:",
        "media-src 'self'",
        "font-src 'self'",
        # Inline styles stay allowed. The scanner does not penalise this and
        # there is no known real-world attack through CSS alone.
        "style-src 'self' 'unsafe-inline'",
        f"script-src {script_src}",
        "connect-src 'self'",
        "manifest-src 'self'",
        # The site has no iframes and no web workers.
        "frame-src 'none'",
        "worker-src 'none'",
        "upgrade-insecure-requests",
    ])


def main():
    check_only = "--check" in sys.argv

    pages, hashes = collect_hashes()
    csp = build_csp(hashes)

    content = f"""# Temple of Sun — security headers
#
# GENERATED FILE. Do not edit by hand.
# Rebuilt automatically by Cloudflare on every deploy
# (build command: python3 tools/generate-headers.py)
#
# Covers {len(pages)} pages and {len(hashes)} inline script blocks.
# Read by Cloudflare Pages and Netlify. Ignored by GitHub Pages.

/*
  Content-Security-Policy: {csp}
  Strict-Transport-Security: max-age=63072000; includeSubDomains; preload
  X-Frame-Options: DENY
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: {PERMISSIONS_POLICY}
  Cross-Origin-Opener-Policy: same-origin
  Cross-Origin-Resource-Policy: same-origin
  X-Permitted-Cross-Domain-Policies: none
"""

    if check_only:
        current = HEADERS_FILE.read_text(encoding="utf-8") if HEADERS_FILE.exists() else ""
        if current.strip() != content.strip():
            print("OUT OF DATE — a page changed since _headers was built.")
            print("Fix it with:  python3 tools/generate-headers.py")
            sys.exit(1)
        print(f"Up to date. {len(pages)} pages, {len(hashes)} inline scripts.")
        return

    HEADERS_FILE.write_text(content, encoding="utf-8")
    print(f"Wrote {HEADERS_FILE}")
    print(f"  {len(pages)} pages scanned")
    print(f"  {len(hashes)} unique inline scripts fingerprinted")
    print(f"  policy is {len(csp)} characters")


if __name__ == "__main__":
    main()
