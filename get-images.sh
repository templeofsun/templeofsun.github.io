#!/bin/bash
# ============================================================
# TEMPLE OF SUN — pull Peter's photos into assets/img/
# Run this once from the Website folder, in Terminal:
#   cd "path/to/the/website-folder"
#   bash get-images.sh
# Downloads 25 photos (~15 MB) from templeofsun.com's own media
# library. After that the whole site works fully offline.
# ============================================================
set -e
cd "$(dirname "$0")"
mkdir -p assets/img

R="https://i0.wp.com/www.templeofsun.com/wp-content/uploads/2026/03/soulalchemyretreat-templeofsun-holistichealth-aromatherapy-massage-meditation-yoga-spirituality"
P="https://i0.wp.com/www.templeofsun.com/wp-content/uploads/2020/06"

get () {  # get <filename> <url> <width>
  if [ -s "assets/img/$1" ]; then echo "✓ $1 (already there)"; return; fi
  echo "↓ $1"
  curl -fsSL "$2?w=$3&ssl=1" -o "assets/img/$1"
}

# Hero slideshow (home)
get hero-1.jpg            "$R-gratitude-scaled.jpg"        1920
get hero-2.jpg            "$P/Templeofsun0045-scaled.jpg"  1920
get hero-3.jpg            "$R-groupmeditation-scaled.jpg"  1920
get hero-4.jpg            "$P/Templeofsun0089-1-scaled.jpg" 1920
get hero-5.jpg            "$R-joy-scaled.jpg"              1920
get hero-6.jpg            "$R-heartfelt-scaled.jpg"        1920

# Home
get portrait-peter.jpg    "$P/Templeofsun0070-1-scaled.jpg" 1200
get peter-bio.jpg         "https://i0.wp.com/www.templeofsun.com/wp-content/uploads/2023/10/bio.jpeg" 1200
get oils-ether.jpg        "https://i0.wp.com/www.templeofsun.com/wp-content/uploads/2024/03/templeofsun-5-elements-ether-aromatherapy.jpg" 1200
get peter-story.jpg       "https://i0.wp.com/www.templeofsun.com/wp-content/uploads/2023/10/mystory.jpeg" 1200
get peter-philosophy.jpg  "https://i0.wp.com/www.templeofsun.com/wp-content/uploads/2023/10/philisophy.jpeg" 1200
get meditation-1.jpg      "https://i0.wp.com/www.templeofsun.com/wp-content/uploads/2025/11/meditationreszbe.jpeg" 1200
get meditation-2.jpg      "https://i0.wp.com/www.templeofsun.com/wp-content/uploads/2025/11/meditationreszbe2.jpeg" 1200
get path-oils.jpg         "$P/Templeofsun0116-2-scaled.jpg" 1200
get path-treatments.jpg   "$P/Templeofsun0150-1-scaled.jpg" 1200
get path-retreats.jpg     "$R-grouppic-scaled.jpg"          1200

# Aromatherapy
get collections-hero.jpg  "$P/Templeofsun0104-1-scaled.jpg" 1920
get rainbow.jpg           "$P/Templeofsun0124-1-scaled.jpg" 1200
get elements.jpg          "$P/Templeofsun0132-1-scaled.jpg" 1200
get formula-hero.jpg      "$P/Templeofsun0139-1-scaled.jpg" 1920
get formula-craft.jpg     "$P/Templeofsun0147-1-scaled.jpg" 1200

# Retreats
get retreats-hero.jpg     "$R-gratitude2-scaled.jpg"        1920
get gal-1.jpg             "$R-happiness-scaled.jpg"         1200
get gal-2.jpg             "$R-innerchild-scaled.jpg"        1200
get gal-3.jpg             "$R-groupsession-scaled.jpg"      1200
get gal-4.jpg             "$R-gratitude3-scaled.jpg"        1200

# Treatments / LABs / Online / About / Philosophy / Contact
get treatments-hero.jpg   "$P/Templeofsun0142-1-scaled.jpg" 1920
get anahata.jpg           "$P/Templeofsun0085-1-scaled.jpg" 1200
get treatment-1.jpg       "https://i0.wp.com/www.templeofsun.com/wp-content/uploads/2021/10/Picture-1-2.png" 1200
get treatment-2.jpg       "https://i0.wp.com/www.templeofsun.com/wp-content/uploads/2021/10/Picture-1-4.png" 1200
get labs-hero.jpg         "$P/Templeofsun0144-1-scaled.jpg" 1920
get online-hero.jpg       "$P/Templeofsun0102-1-scaled.jpg" 1920
get philosophy-hero.jpg   "$P/Templeofsun0159-1-scaled.jpg" 1920
get contact-hero.jpg      "$P/Templeofsun0088-1-scaled.jpg" 1200

echo ""
echo "☀ Done. All photos are in assets/img/ — open index.html and enjoy."
