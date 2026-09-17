#!/usr/bin/env python3
"""
Temple of Sun — build the-essence-of-you.html

A guest, the author and curator Diana Murray Watts, wrote a piece about Péter
during a retreat in Mora, Portugal, in May 2026. It is not a review, so it is
not shown as one. It gets a page of its own, with nothing else on it.

Her words are held here, once. Run this and the page is rebuilt from them.
Do not edit the-essence-of-you.html by hand; it is overwritten every run.

    python3 tools/build-poem-page.py

Run on its own, or let tools/prepare-for-upload.py run it for you.

NOTE ON PERMISSION
------------------
She wrote this privately, as a gift. Before the page goes public she needs to
say yes, and to say how she wants her name to appear. Until then, keep the
site private (the default robots.txt already blocks every crawler).
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "philosophy.html"      # same head shape, calm page
TARGET = ROOT / "the-essence-of-you.html"
BASE = "https://templeofsun.com/"
SLUG = "the-essence-of-you.html"

TITLE = "The essence of you"
AUTHOR = "Diana Murray Watts"
AUTHOR_ROLE = "author and curator"

# Her own website or profile. Ask her which link she wants, then paste it here
# and rerun. While it is empty her name is plain text, which is the safe default:
# never link a person's name to a page they did not choose.
AUTHOR_URL = ""

PLACE = "Mora, Portugal"
WRITTEN = "2026-05-01"
WRITTEN_HUMAN = "1 May 2026"

DESCRIPTION = ("A piece written for Péter Frák by the author and curator Diana Murray Watts, "
               "during a Soul Alchemy Retreat in Mora, Portugal, in May 2026. She tries to "
               "distil him into an essential oil, a hydrolat and a carrier oil, and finds "
               "that none of them hold him.")

# Her words, exactly as she wrote them.
PARAS = [
    "Peter, I tried. Your energy and your knowledge are so special that I tried to bring them into aromatherapy. Scents inspired by you.",
    "First I tried to extract the essence of the calming water in your eyes. I imagined it would become a powerful essential oil featuring fresh, floral notes able to give a comforting, warming sensation. You have a special gift and, through your words and treatments, know how to honour and enhance the feminine power in us.",
    "I could not, however, capture the scent required to make this essential oil, so I decided to move on and try to distill you into a hydrolat. How would you turn out to be in this form?",
    "As a hydrolat, I imagined that you would be floral and feminine, like a happy dance; and also sweet and understanding. You would be a hydrolat that would also inspire assertiveness and creativity. These are all strong qualities in you, and they make me think of the bright bouquet of tattoos that you carry!",
    "What resulted from this hydrolat experiment did not honour you entirely, and so I moved onto my last recourse: transforming your energy into a carrier oil.",
    "You already have a similar effect upon us, members of your cosmic family, for you always take time to help us find our own true essence just as you envelop us with your beautiful oil base. Indeed, you are a carrier of stability that inspires our will to discover and enhance what is best in each one of us.",
    "The carrier oil that I concocted, however, was not up to par with you, and so I let it go.",
    "Thank you, Peter, for the incredible alchemic voyage that you led us into this week. You are simply too special of a being to be translated into aromatherapy!",
]

# The three lines she wrote in Hungarian, with her own English underneath.
# Left exactly as she typed them, accents and all. Do not "correct" these.
HUNGARIAN = [
    ("Kerlek tanits minket tovabb", "Please keep teaching us."),
    ("Szeretunk", "We love you."),
    ("Aldott legyel mindig", "Bless you, always."),
]

CLOSING = "Namaste."

# Two quiet doors at the foot. No more than two — the page should stay still.
DOORS = [
    ("find-your-blend.html", "Find your blend"),
    ("retreats.html", "Soul Alchemy Retreats"),
]
DOORS_LINE = "The retreat she wrote this on happens once a year. The blends are made the same way: slowly, one at a time."


def body() -> str:
    paras = "\n".join(f"          <p>{p}</p>" for p in PARAS)
    hu = "\n".join(
        f"            <p><b>{a}</b><span>{b}</span></p>" for a, b in HUNGARIAN
    )
    doors = "\n".join(
        f'          <a class="btn" href="{href}">{label}</a>'
        for href, label in DOORS
    )
    name = (f'<a href="{AUTHOR_URL}" target="_blank" rel="noopener">{AUTHOR}</a>'
            if AUTHOR_URL else AUTHOR)
    return f"""

  <section class="poem-page">
    <div class="poem">

      <header class="poem-head reveal">
        <h1>{TITLE}</h1>
        <p class="poem-by">by {name}<br>{AUTHOR_ROLE}</p>
      </header>

      <div class="poem-body reveal" style="--d:.1s">
{paras}

        <div class="poem-hu">
{hu}
        </div>

        <p class="poem-close">{CLOSING}</p>
        <p class="poem-where">{PLACE}<br><time datetime="{WRITTEN}">{WRITTEN_HUMAN}</time></p>
      </div>

      <div class="poem-after reveal">
        <p>{DOORS_LINE}</p>
        <div class="poem-doors">
{doors}
        </div>
      </div>

    </div>
  </section>
"""


def stamp_head(shell: str) -> str:
    url = BASE + SLUG
    full_title = f"{TITLE} &middot; Temple of Sun"
    img = BASE + "assets/img/philosophy-hero.webp"

    def sub(pattern, repl, text, label):
        new, n = re.subn(pattern, lambda _m: repl, text, count=1, flags=re.S)
        if n != 1:
            sys.exit(f"ERROR: could not stamp {label} — philosophy.html changed shape.")
        return new

    s = shell
    s = sub(r"<title>.*?</title>", f"<title>{full_title}</title>", s, "title")
    s = sub(r'<meta name="description" content=".*?">',
            f'<meta name="description" content="{DESCRIPTION}">', s, "description")
    s = sub(r'<link rel="canonical" href=".*?">',
            f'<link rel="canonical" href="{url}">', s, "canonical")
    s = sub(r'<meta property="og:title" content=".*?">',
            f'<meta property="og:title" content="{TITLE} &middot; Temple of Sun">', s, "og:title")
    s = sub(r'<meta property="og:description" content=".*?">',
            f'<meta property="og:description" content="{DESCRIPTION}">', s, "og:description")
    s = sub(r'<meta property="og:url" content=".*?">',
            f'<meta property="og:url" content="{url}">', s, "og:url")
    s = sub(r'<meta property="og:image" content=".*?">',
            f'<meta property="og:image" content="{img}">', s, "og:image")
    s = sub(r'<meta name="twitter:title" content=".*?">',
            f'<meta name="twitter:title" content="{TITLE} &middot; Temple of Sun">', s, "twitter:title")
    s = sub(r'<meta name="twitter:description" content=".*?">',
            f'<meta name="twitter:description" content="{DESCRIPTION}">', s, "twitter:description")
    s = sub(r'<meta name="twitter:image" content=".*?">',
            f'<meta name="twitter:image" content="{img}">', s, "twitter:image")
    # no hero photograph on this page, so nothing to preload
    s = re.sub(r'\n<link rel="preload" as="image" href=".*?">', "", s, count=1)

    import json
    crumbs = {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE},
            {"@type": "ListItem", "position": 2, "name": TITLE, "item": url},
        ],
    }
    work = {
        "@context": "https://schema.org",
        "@type": "CreativeWork",
        "@id": url + "#work",
        "name": TITLE,
        "url": url,
        "genre": "Prose poem",
        "inLanguage": ["en", "hu"],
        "dateCreated": WRITTEN,
        "datePublished": WRITTEN,
        "description": DESCRIPTION,
        "author": dict({"@type": "Person", "name": AUTHOR,
                        "jobTitle": AUTHOR_ROLE.title()},
                       **({"url": AUTHOR_URL, "sameAs": AUTHOR_URL} if AUTHOR_URL else {})),
        "about": {"@id": BASE + "#peter"},
        "locationCreated": {"@type": "Place", "name": PLACE,
                            "address": {"@type": "PostalAddress",
                                        "addressLocality": "Mora",
                                        "addressCountry": "PT"}},
        "isPartOf": {"@id": BASE + "#website"},
        "copyrightHolder": {"@type": "Person", "name": AUTHOR},
        "publisher": {"@id": BASE + "#organization"},
    }

    def dump(o):
        return ('<script type="application/ld+json">'
                + json.dumps(o, ensure_ascii=False, separators=(", ", ": ")) + "</script>")

    s = sub(r'<script type="application/ld\+json">\{"@context": "https://schema\.org", "@type": "BreadcrumbList".*?</script>',
            dump(crumbs), s, "breadcrumbs")
    # philosophy.html carries an extra block after the crumbs; replace the last one
    s, n = re.subn(r'<script type="application/ld\+json">\{"@context": "https://schema\.org", "@type": "(?!BreadcrumbList)(?!.*?"@graph").*?</script>',
                   lambda _m: dump(work), s, count=1, flags=re.S)
    if n != 1:
        # philosophy had no third block: put ours right after the crumbs
        s = s.replace(dump(crumbs), dump(crumbs) + "\n" + dump(work), 1)
    return s


def main() -> None:
    if not TEMPLATE.exists():
        sys.exit("ERROR: philosophy.html is missing — it is the template.")
    shell = TEMPLATE.read_text(encoding="utf-8")
    shell = re.sub(r"<main>.*?</main>", "<main>@@BODY@@</main>", shell, flags=re.S)
    out = stamp_head(shell).replace("@@BODY@@", body())
    if not TARGET.exists() or TARGET.read_text(encoding="utf-8") != out:
        TARGET.write_text(out, encoding="utf-8")
    print(f"poem page: {TARGET.name} built ({len(PARAS)} paragraphs, {len(HUNGARIAN)} Hungarian lines)")


if __name__ == "__main__":
    main()
