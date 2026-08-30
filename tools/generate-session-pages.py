#!/usr/bin/env python3
"""
Temple of Sun — build the three online session pages.

Péter offers three different things online. Each one now has its own page:

    health-consultation.html
    spiritual-mentoring.html
    meditation-guidance.html

All three are BUILT, not written by hand. The words live in
tools/session-pages.json. Change the words there, run this, and the pages
rebuild. Anything you type directly into the three .html files is lost on the
next run.

online-sessions.html stays as the front door: a short page that introduces the
three and links to them. This script also keeps the three cards on that page,
and the three links in the menu, in step with the JSON.

Run directly, or let tools/prepare-for-upload.py run it for you:

    python3 tools/generate-session-pages.py
"""

import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "tools" / "session-pages.json"
TEMPLATE = ROOT / "online-sessions.html"
SITE_JS = ROOT / "js" / "site.js"
SITEMAP = ROOT / "sitemap.xml"
BASE = "https://templeofsun.com/"

# The site's small drawn symbols, lifted from the pages that already use them.
ICONS = {
    "speech": ("sage", '<path d="M4.5 5.5h15v9.5h-8.5l-4 3.5v-3.5h-2.5z"/>'
                       '<path d="M8.5 10.5h7M8.5 8h7" opacity=".5"/>'),
    "rings": ("ether", '<circle cx="12" cy="12" r="2.4"/>'
                       '<circle cx="12" cy="12" r="7" opacity=".45"/>'),
    "drop": ("amber", '<path d="M12 4.5c2.8 3.2 4.4 5.6 4.4 7.9a4.4 4.4 0 1 1-8.8 0c0-2.3 1.6-4.7 4.4-7.9z"/>'
                      '<path d="M10.3 12.6a1.9 1.9 0 0 0 1.4 1.8" opacity=".55"/>'),
    "heart": ("rose", '<path d="M12 19.2S5.5 15 5.5 10.6A3.5 3.5 0 0 1 12 8.9a3.5 3.5 0 0 1 6.5 1.7C18.5 15 12 19.2 12 19.2z"/>'),
    "spiral": ("amber", '<path d="M12 12a1.6 1.6 0 0 0 3.2 0 3.2 3.2 0 0 0-6.4 0 4.8 4.8 0 0 0 9.6 0 6.4 6.4 0 0 0-12.8 0"/>'),
    "bottles": ("amber", '<path d="M8.3 4.5c1 2.4-1 4.6 0 7s-1 4.6 0 7.5M12 4.5c1 2.4-1 4.6 0 7s-1 4.6 0 7.5'
                         'M15.7 4.5c1 2.4-1 4.6 0 7s-1 4.6 0 7.5"/>'),
    "lotus": ("sage", '<circle cx="12" cy="6" r="1.4"/><circle cx="17.2" cy="9" r="1.4"/>'
                      '<circle cx="17.2" cy="15" r="1.4"/><circle cx="12" cy="18" r="1.4"/>'
                      '<circle cx="6.8" cy="15" r="1.4"/><circle cx="6.8" cy="9" r="1.4"/>'),
    "sparkle": ("amber", '<path d="M12 4.5c.6 3.6 2.9 5.9 6.5 6.5-3.6.6-5.9 2.9-6.5 6.5-.6-3.6-2.9-5.9-6.5-6.5 3.6-.6 5.9-2.9 6.5-6.5z"/>'
                         '<circle cx="18" cy="6" r=".7" fill="currentColor" stroke="none" opacity=".6"/>'),
    "sun": ("amber", '<circle cx="12" cy="12" r="4"/>'
                     '<path d="M12 3.5v2M12 18.5v2M3.5 12h2M18.5 12h2M6 6l1.4 1.4M16.6 16.6L18 18M6 18l1.4-1.4M16.6 7.4L18 6"/>'),
    "breath": ("air", '<path d="M8 16.5c0-1.9 1.5-2.4 1.5-3.9S8 10.1 8 8.2M12 17.5c0-1.9 1.5-2.4 1.5-3.9S12 11.1 12 9.2'
                      'M16 16.5c0-1.9 1.5-2.4 1.5-3.9S16 10.1 16 8.2"/>'),
    "waves": ("water", '<path d="M12 5.5c1.7 2.3 1.7 4.6 0 6.9-1.7-2.3-1.7-4.6 0-6.9z"/>'
                       '<path d="M5.8 10.8c1.9-.2 4.1.8 6.2 2.9M18.2 10.8c-1.9-.2-4.1.8-6.2 2.9" opacity=".6"/>'
                       '<path d="M6.2 15.5a6.5 6.5 0 0 0 11.6 0" opacity=".5"/>'),
}

SVG_OPEN = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" '
            'stroke-linecap="round" stroke-linejoin="round">')


def plain(text: str) -> str:
    """Entity-encoded copy back to plain text, for use inside JSON and meta tags."""
    return html.unescape(text)


def icon(name: str, small: bool = False) -> str:
    tone, paths = ICONS[name]
    cls = "scent scent-sm scent-" + tone if small else "scent scent-" + tone
    return f'<div class="{cls}" aria-hidden="true">{SVG_OPEN}{paths}</svg></div>'


# ---------------------------------------------------------------- page blocks

def block_duo(b: dict) -> str:
    tone = b.get("tone", "")
    cls = " class=\"section-%s\"" % tone if tone else ""
    body = ""
    if b.get("lead"):
        body += f'\n          <p class="lead">{b["lead"]}</p>'
    for p in b.get("paras", []):
        body += f"\n          <p>{p}</p>"
    if b.get("pull"):
        body += f'\n          <p class="pull">&ldquo;{b["pull"]}&rdquo;</p>'
    return f"""
  <section{cls}>
    <div class="wrap">
      <div class="duo">
        <div class="duo-head reveal">
          <span class="label">{b["label"]}</span>
          <h2>{b["h2"]}</h2>
        </div>
        <div class="duo-body reveal" style="--d:.1s">{body}
        </div>
      </div>
    </div>
  </section>
"""


def block_rites(b: dict) -> str:
    tone = b.get("tone", "")
    cls = " class=\"section-%s center\"" % tone if tone else " class=\"center\""
    items = ""
    for i, it in enumerate(b["items"]):
        delay = f' style="--d:.{i*7:02d}s"' if i else ""
        items += (f'\n        <div class="rite reveal"{delay}>\n'
                  f'          {icon(it["icon"], small=True)}\n'
                  f'          <h3 class="serif">{it["title"]}</h3>\n'
                  f'          <p>{it["line"]}</p>\n'
                  f'        </div>')
    return f"""
  <section{cls}>
    <div class="wrap">
      <div class="reveal">
        <span class="label">{b["label"]}</span>
        <h2 class="serif" style="margin-top:12px">{b["h2"]}</h2>
      </div>
      <div class="rite-grid" style="margin-top:44px">{items}
      </div>
    </div>
  </section>
"""


def block_quote(b: dict) -> str:
    cite = f'\n      <cite>{b["cite"]}</cite>' if b.get("cite") else ""
    return f"""
  <section class="quote-band">
    <div class="wrap reveal">
      <blockquote>&ldquo;{b["text"]}&rdquo;</blockquote>{cite}
    </div>
  </section>
"""


BUILDERS = {"duo": block_duo, "rites": block_rites, "quote": block_quote}


def sibling_cards(pages: list, current: str, heading: str) -> str:
    """The other two sessions, at the foot of each page."""
    cards = ""
    shown = 0
    for p in pages:
        if p["slug"] == current:
            continue
        delay = ' style="--d:.12s"' if shown else ""
        shown += 1
        cards += f"""
        <a class="card"{delay} href="{p["slug"]}.html">
          <div class="frame ratio-45"><img loading="lazy" decoding="async" data-onerr="remote" src="assets/img/{p["hero"]["img"]}" alt="{p["hero"]["alt"]}" width="{p["hero"]["w"]}" height="{p["hero"]["h"]}"></div>
          <div class="card-body">
            <span class="k">{p["kicker"]}</span>
            <h3>{p["title"]}</h3>
            <p>{p["cardLine"]}</p>
            <span class="lnk">Read more<span class="arr">&rarr;</span></span>
          </div>
        </a>"""
    return f"""
  <section>
    <div class="wrap">
      <div class="center reveal"><h2 class="serif">{heading}</h2></div>
      <div class="grid-3" style="margin-top:48px;max-width:760px;margin-left:auto;margin-right:auto;grid-template-columns:repeat(auto-fit,minmax(240px,1fr))">{cards}
      </div>
    </div>
  </section>
"""


DISCOVERY = """
  <section class="section-sand center">
    <div class="wrap-text reveal">
      <span class="label">Begin softly</span>
      <h2 class="serif">Start with a free discovery call</h2>
      <p style="margin:20px auto 34px;max-width:54ch">If this awakened your interest, please feel free to schedule a discovery call with me; it would be my pleasure to get to know you!</p>
      <a class="btn btn-solid" href="contact.html?topic=online">Request a discovery call</a>
      <p style="margin:26px auto 0;font-size:15px;color:var(--sage)">Would you rather be in the room? See the <a href="treatments.html">in-person treatments</a>.</p>
    </div>
  </section>
"""


def build_main(page: dict, pages: list) -> str:
    h = page["hero"]
    out = f"""<main>

  <section class="subhero subhero-light" style="padding:0">
    <div class="frame"><img fetchpriority="high" decoding="async" data-onerr="remote" src="assets/img/{h["img"]}" alt="{h["alt"]}" width="{h["w"]}" height="{h["h"]}"></div>
    <div class="subhero-scrim"></div>
    <div class="subhero-content">
      <span class="label"><a href="online-sessions.html">Online Sessions</a> &middot; {page["kicker"]}</span>
      <h1>{page["title"]}</h1>
      <p class="italic">{page["tagline"]}</p>
    </div>
  </section>
"""
    for b in page["blocks"]:
        out += BUILDERS[b["type"]](b)
    out += DISCOVERY
    out += sibling_cards(pages, page["slug"], "The other two ways to work together")
    out += "\n</main>"
    return out


# ------------------------------------------------------------------ page head

def stamp_head(shell: str, page: dict) -> str:
    url = BASE + page["slug"] + ".html"
    title = plain(page["title"])
    desc = page["metaDescription"]
    img = BASE + "assets/img/" + page["hero"]["img"]
    full_title = f'{page["title"]} &middot; Temple of Sun | Aromatherapy &amp; Healing Retreats'

    def sub(pattern, repl, text, label):
        new, n = re.subn(pattern, repl.replace("\\", "\\\\"), text, count=1)
        if n != 1:
            sys.exit(f"ERROR: could not stamp {label} for {page['slug']} — the template changed.")
        return new

    s = shell
    s = sub(r"<title>.*?</title>", f"<title>{full_title}</title>", s, "title")
    s = sub(r'<meta name="description" content=".*?">',
            f'<meta name="description" content="{desc}">', s, "description")
    s = sub(r'<link rel="canonical" href=".*?">',
            f'<link rel="canonical" href="{url}">', s, "canonical")
    s = sub(r'<meta property="og:title" content=".*?">',
            f'<meta property="og:title" content="{page["title"]} &middot; Temple of Sun">', s, "og:title")
    s = sub(r'<meta property="og:description" content=".*?">',
            f'<meta property="og:description" content="{desc}">', s, "og:description")
    s = sub(r'<meta property="og:url" content=".*?">',
            f'<meta property="og:url" content="{url}">', s, "og:url")
    s = sub(r'<meta property="og:image" content=".*?">',
            f'<meta property="og:image" content="{img}">', s, "og:image")
    s = sub(r'<meta name="twitter:title" content=".*?">',
            f'<meta name="twitter:title" content="{page["title"]} &middot; Temple of Sun">', s, "twitter:title")
    s = sub(r'<meta name="twitter:description" content=".*?">',
            f'<meta name="twitter:description" content="{desc}">', s, "twitter:description")
    s = sub(r'<meta name="twitter:image" content=".*?">',
            f'<meta name="twitter:image" content="{img}">', s, "twitter:image")
    s = sub(r'<link rel="preload" as="image" href=".*?">',
            f'<link rel="preload" as="image" href="assets/img/{page["hero"]["img"]}">', s, "preload")

    crumbs = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE},
            {"@type": "ListItem", "position": 2, "name": "Online Sessions",
             "item": BASE + "online-sessions.html"},
            {"@type": "ListItem", "position": 3, "name": title, "item": url},
        ],
    }
    service = {
        "@context": "https://schema.org",
        "@type": "Service",
        "@id": url + "#service",
        "name": title,
        "serviceType": page["serviceType"],
        "url": url,
        "description": plain(desc),
        "provider": {"@id": BASE + "#organization"},
        "areaServed": [{"@type": "Place", "name": "Worldwide"}],
        "audience": {"@type": "Audience", "audienceType": "Adults seeking holistic wellbeing support"},
        "availableChannel": {
            "@type": "ServiceChannel",
            "serviceUrl": url,
            "availableLanguage": ["en", "hu", "de"],
        },
        "isRelatedTo": [
            {"@type": "Service", "name": plain(p["title"]), "url": BASE + p["slug"] + ".html"}
            for p in PAGES if p["slug"] != page["slug"]
        ],
    }
    def dump(obj):
        return ('<script type="application/ld+json">'
                + json.dumps(obj, ensure_ascii=False, separators=(", ", ": "))
                + "</script>")

    s = sub(r'<script type="application/ld\+json">\{"@context": "https://schema\.org", "@type": "BreadcrumbList".*?</script>',
            dump(crumbs), s, "breadcrumbs")
    s = sub(r'<script type="application/ld\+json">\{"@context": "https://schema\.org", "@type": "Service".*?</script>',
            dump(service), s, "service")
    return s


# --------------------------------------------------------------- front door

def front_door(pages: list) -> str:
    """The three cards that replace the long programme sections on online-sessions.html."""
    cards = ""
    for i, p in enumerate(pages):
        delay = f' style="--d:.{i*12:02d}s"' if i else ""
        cards += f"""
        <a class="card reveal"{delay} href="{p["slug"]}.html">
          <div class="frame ratio-45"><img loading="lazy" decoding="async" data-onerr="remote" src="assets/img/{p["hero"]["img"]}" alt="{p["hero"]["alt"]}" width="{p["hero"]["w"]}" height="{p["hero"]["h"]}"></div>
          <div class="card-body">
            <span class="k">{p["kicker"]}</span>
            <h3>{p["title"]}</h3>
            <p>{p["cardLine"]}</p>
            <span class="lnk">Read more<span class="arr">&rarr;</span></span>
          </div>
        </a>"""
    return f"""      <div class="grid-3" style="margin-top:56px">{cards}
      </div>
"""


def update_front_door(pages: list) -> bool:
    page = TEMPLATE.read_text(encoding="utf-8")
    start = "<!-- session-cards start -->"
    end = "<!-- session-cards end -->"
    if start not in page:
        return False
    new = re.sub(re.escape(start) + r".*?" + re.escape(end),
                 start + "\n" + front_door(pages) + "      " + end,
                 page, flags=re.S)
    if new != page:
        TEMPLATE.write_text(new, encoding="utf-8")
    return True


def update_menu(pages: list) -> None:
    """Keep the three links in the shared menu in step with the JSON."""
    js = SITE_JS.read_text(encoding="utf-8")
    links = "".join(
        '<a href="%s.html">%s</a>' % (p["slug"], plain(p["navLabel"])) for p in pages
    )
    js2 = js
    for marker in ("session-links-desktop", "session-links-mobile"):
        pattern = r"(/\* " + marker + r" \*/')(.*?)(')"
        js2, n = re.subn(pattern, lambda m: m.group(1) + links + m.group(3), js2, count=1, flags=re.S)
        if n != 1:
            sys.exit(f"ERROR: the {marker} marker is missing from js/site.js.")
    if js2 != js:
        SITE_JS.write_text(js2, encoding="utf-8")
    print("  menu: three links in step")


def update_sitemap(pages: list) -> None:
    if not SITEMAP.exists():
        return
    xml = SITEMAP.read_text(encoding="utf-8")
    anchor = BASE + "online-sessions.html"
    m = re.search(r"<url>\s*<loc>" + re.escape(anchor) + r"</loc>.*?</url>", xml, re.S)
    if not m:
        print("  ! online-sessions.html not found in the sitemap; skipped")
        return
    block = m.group(0)
    added = []
    for p in pages:
        loc = BASE + p["slug"] + ".html"
        if loc in xml:
            continue
        added.append(block.replace(anchor, loc))
    if added:
        xml = xml.replace(block, block + "\n" + "\n".join(added))
        SITEMAP.write_text(xml, encoding="utf-8")
    print(f"  sitemap: {len(added)} added, {len(pages)-len(added)} already there")


# ---------------------------------------------------------------------- main

PAGES: list = []


def main() -> None:
    global PAGES
    if not CONTENT.exists():
        sys.exit(f"ERROR: {CONTENT.name} is missing.")
    if not TEMPLATE.exists():
        sys.exit("ERROR: online-sessions.html is missing — it is the template.")

    data = json.loads(CONTENT.read_text(encoding="utf-8"))
    PAGES = data["pages"]

    shell = TEMPLATE.read_text(encoding="utf-8")
    if "<!-- session-cards start -->" in shell:
        # Never inherit the front door's own card list into a child page.
        shell = re.sub(r"<main>.*?</main>", "<main></main>", shell, flags=re.S)

    written = 0
    for page in PAGES:
        out = stamp_head(shell, page)
        body = build_main(page, PAGES)
        out, n = re.subn(r"<main>.*?</main>", lambda _m: body, out, count=1, flags=re.S)
        if n != 1:
            sys.exit(f"ERROR: could not place the content for {page['slug']}.")
        target = ROOT / f"{page['slug']}.html"
        if not target.exists() or target.read_text(encoding="utf-8") != out:
            target.write_text(out, encoding="utf-8")
        written += 1

    print(f"session pages: {written} built")
    if update_front_door(PAGES):
        print("  online-sessions.html: three cards refreshed")
    update_menu(PAGES)
    update_sitemap(PAGES)


if __name__ == "__main__":
    main()
