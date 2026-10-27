#!/usr/bin/env python3
"""Builds the Weingoat static site from src/ into the repo root.
Run: python3 build.py   (then commit; Vercel serves the root)
One shared head/nav/footer on every page, per-page SEO meta + JSON-LD, sitemap.xml, robots.txt,
and artifact/weingoat.html (the home page with CSS inlined, for the claude.ai preview)."""
import json, os, re, datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
BASE = "https://weingoat-site.vercel.app"   # change once the custom domain lands
TODAY = datetime.date.today().isoformat()
PERSON_DESC = ("Adam Weingard, known as Weingoat, is a professional poker player who plays live cash games, "
               "online and tournaments, and teaches the decision process behind his results.")
SAME_AS = ["https://www.instagram.com/adamweingard/",
           "https://www.cardplayer.com/poker-players/453884-adam-weingard"]

def read(p): return open(os.path.join(ROOT, p), encoding="utf-8").read()
def write(p, s):
    os.makedirs(os.path.dirname(os.path.join(ROOT, p)) or ".", exist_ok=True)
    open(os.path.join(ROOT, p), "w", encoding="utf-8").write(s)

css = read("src/styles.css")
defs = read("src/defs.html")
script = read("src/script.js")

PERSON = {
    "@type": "Person", "@id": BASE + "/#adam", "name": "Adam Weingard", "alternateName": "Weingoat",
    "jobTitle": "Professional poker player", "description": PERSON_DESC, "url": BASE + "/about",
    "image": BASE + "/img/portrait-cigar.jpg", "sameAs": SAME_AS,
    "knowsAbout": ["Poker strategy", "Live cash game poker", "Preflop strategy", "Tournament poker"],
}
WEBSITE = {"@type": "WebSite", "@id": BASE + "/#website", "name": "Weingoat", "url": BASE + "/",
           "publisher": {"@id": BASE + "/#adam"}, "inLanguage": "en-US"}

def breadcrumb(items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": BASE + u} for i, (n, u) in enumerate(items)]}

PAGES = [
    dict(slug="index", path="/", title="Weingoat | Adam Weingard, Pro Poker Player & Coach",
         description="Adam Weingard (Weingoat) won $500K+ in twelve months at live cash, online and tournaments. Learn the question he asks at every decision, from $9.",
         image="/img/og-home.jpg", schema=[WEBSITE, PERSON,
            {"@type": "WebPage", "@id": BASE + "/#webpage", "url": BASE + "/", "name": "Weingoat",
             "isPartOf": {"@id": BASE + "/#website"}, "about": {"@id": BASE + "/#adam"}, "inLanguage": "en-US"}]),
    dict(slug="about", path="/about", title="About Adam Weingard, Professional Poker Player | Weingoat",
         description="Indiana to Orange County to Florida, a kitchen-table education, the $5,000 night that rebuilt his game, and the record since. The player behind Weingoat.",
         image="/img/og-home.jpg", schema=[
            {"@type": "ProfilePage", "@id": BASE + "/about#page", "url": BASE + "/about", "name": "About Adam Weingard",
             "mainEntity": {"@id": BASE + "/#adam"}, "isPartOf": {"@id": BASE + "/#website"}, "dateModified": TODAY},
            PERSON, breadcrumb([("Home", "/"), ("About", "/about")])]),
    dict(slug="products", path="/products", title="Preflop Playbook, Community & Coaching | Weingoat",
         description="Three ways to learn Adam Weingard's decision process: the $9 Preflop Playbook, the community with weekly hand reviews, and one-on-one coaching.",
         image="/img/og-home.jpg", schema=[
            {"@type": "CollectionPage", "@id": BASE + "/products#page", "url": BASE + "/products",
             "name": "Weingoat poker training", "isPartOf": {"@id": BASE + "/#website"},
             "mainEntity": {"@type": "ItemList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "item": {"@type": "Product", "name": "The Preflop Playbook",
                    "description": "Map, assess, play: the preflop process Adam Weingard uses in live games, with hand groups, 20-second player-type tells, and the quick math used at the table.",
                    "brand": {"@type": "Brand", "name": "Weingoat"}, "url": BASE + "/products#playbook",
                    "offers": {"@type": "Offer", "price": "9.00", "priceCurrency": "USD",
                               "availability": "https://schema.org/PreOrder", "url": BASE + "/products#playbook"}}},
                {"@type": "ListItem", "position": 2, "item": {"@type": "Service", "name": "The Weingoat community",
                    "description": "Monthly membership: weekly live calls, hand breakdowns, tournament game theory deep dives, and online games played together then reviewed.",
                    "provider": {"@id": BASE + "/#adam"}, "url": BASE + "/products#community"}},
                {"@type": "ListItem", "position": 3, "item": {"@type": "Service", "name": "One-on-one poker coaching",
                    "description": "A free strategy call to find where your game leaks, then private coaching by application.",
                    "provider": {"@id": BASE + "/#adam"}, "url": BASE + "/products#coaching"}}]}},
            breadcrumb([("Home", "/"), ("Products", "/products")])]),
    dict(slug="contact", path="/contact", title="Contact Adam Weingard | Weingoat",
         description="Reach Adam Weingard: Instagram DMs for the fastest reply, a strategy call for coaching, and a contact form for everything else.",
         image="/img/og-home.jpg", schema=[
            {"@type": "ContactPage", "@id": BASE + "/contact#page", "url": BASE + "/contact", "name": "Contact Adam Weingard",
             "isPartOf": {"@id": BASE + "/#website"}, "about": {"@id": BASE + "/#adam"}},
            breadcrumb([("Home", "/"), ("Contact", "/contact")])]),
    dict(slug="og", path="/og", title="Weingoat", description="Share card.", image="/img/og-home.jpg", noindex=True, schema=[], bare=True),
    dict(slug="404", path="/404", title="Page not found | Weingoat", description="That page isn't on the table.",
         image="/img/og-home.jpg", noindex=True, schema=[]),
]

NAV = [("Home", "/"), ("About", "/about"), ("Products", "/products"), ("Contact", "/contact")]

def header(page):
    links = "".join(f'<a href="{u}"{" aria-current=\"page\"" if u == page["path"] else ""}>{n}</a>' for n, u in NAV)
    dealt = "" if page["slug"] == "index" else " data-dealt=\"5\""
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="top">
  <div class="wrap">
    <a class="mark" href="/" aria-label="Weingoat, home">Wein<span>goat</span></a>
    <div class="board" aria-label="Community cards" id="board"{dealt}>
      <div class="slot" data-rank="A" data-suit="♦" data-color="red"></div>
      <div class="slot" data-rank="K" data-suit="♣" data-color="black"></div>
      <div class="slot" data-rank="7" data-suit="♠" data-color="black"></div>
      <div class="slot" data-rank="K" data-suit="♥" data-color="red"></div>
      <div class="slot" data-rank="2" data-suit="♦" data-color="red"></div>
    </div>
    <nav class="nav" aria-label="Pages">{links}</nav>
    <a class="btn btn-gold" href="/products#playbook"><span class="chip" aria-hidden="true"></span>Get the Playbook</a>
  </div>
</header>'''

FOOTER = '''<footer>
  <div class="wrap">
    <div class="fcol brand">
      <a class="mark" href="/">Wein<span>goat</span></a>
      <p class="small" style="margin-top:12px">Adam Weingard, professional poker player. Live cash, online and tournaments, and the decision process behind the results.</p>
      <p class="copy">© 2026 Adam Weingard. All rights reserved.</p>
    </div>
    <nav class="fcol" aria-label="Pages"><h4>Pages</h4><a href="/">Home</a><a href="/about">About Adam</a><a href="/products">Products</a><a href="/contact">Contact</a></nav>
    <nav class="fcol" aria-label="Learn"><h4>Learn</h4><a href="/products#playbook">The Preflop Playbook</a><a href="/products#community">The community</a><a href="/products#coaching">One-on-one coaching</a><a href="/#leaks">Where the money leaks</a><a href="/#method">The method</a></nav>
    <nav class="fcol" aria-label="Elsewhere"><h4>Elsewhere</h4><a href="https://www.instagram.com/adamweingard/" target="_blank" rel="noopener me">Instagram</a><a href="https://www.cardplayer.com/poker-players/453884-adam-weingard" target="_blank" rel="noopener">Tournament record (CardPlayer)</a></nav>
    <p class="small legal">Weingoat is poker education. Nothing on this site is a promise of results, and nothing here is gambling: no stakes change hands in the playbook, the community or coaching. The results shown are Adam's; yours will depend on your decisions, your games and variance. You must be 18 or older, or of legal age where you live.</p>
  </div>
</footer>'''

def head(page, inline_css=False):
    url = BASE + ("" if page["path"] == "/" else page["path"])
    if page["path"] == "/": url = BASE + "/"
    robots = "noindex, nofollow" if page.get("noindex") else "index, follow, max-image-preview:large"
    ld = {"@context": "https://schema.org", "@graph": page["schema"]} if page["schema"] else None
    style = f"<style>\n{css}</style>" if inline_css else '<link rel="stylesheet" href="/styles.css?v=4">'
    return f'''<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{page["title"]}</title>
<meta name="description" content="{page["description"]}">
<link rel="canonical" href="{url}">
<meta name="robots" content="{robots}">
<meta name="author" content="Adam Weingard">
<meta name="theme-color" content="#120709">
<meta property="og:type" content="{'profile' if page['slug']=='about' else 'website'}">
<meta property="og:site_name" content="Weingoat">
<meta property="og:locale" content="en_US">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{page["title"]}">
<meta property="og:description" content="{page["description"]}">
<meta property="og:image" content="{BASE}{page["image"]}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Weingoat: Adam Weingard, professional poker player">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{page["title"]}">
<meta name="twitter:description" content="{page["description"]}">
<meta name="twitter:image" content="{BASE}{page["image"]}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="sitemap" type="application/xml" href="/sitemap.xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght,SOFT,WONK@0,9..144,400..700,0..100,0..1;1,9..144,400..700,0..100,0..1&family=Instrument+Sans:ital,wght@0,400;0,500;0,600;1,400&display=swap">
{'<link rel="preload" as="image" href="/img/hero-portrait.jpg" fetchpriority="high">' if page["slug"]=="index" else ''}
{style}
{('<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False, separators=(",", ":")) + '</script>') if ld else ''}'''

def page_html(page):
    body = read(f"src/pages/{page['slug']}.html")
    if page.get("bare"):
        return f'''<!doctype html>
<html lang="en"><head>{head(page)}</head><body class="page-og">{defs}{body}</body></html>
'''
    return f'''<!doctype html>
<html lang="en">
<head>
{head(page)}
</head>
<body class="page-{page["slug"]}">
{defs}
{header(page)}
<main id="main">
{body}
</main>
{FOOTER}
<script>
{script}
</script>
</body>
</html>
'''

for page in PAGES:
    write(f"{page['slug']}.html", page_html(page))

write("styles.css", css)

# sitemap + robots
urls = [p for p in PAGES if not p.get("noindex")]

sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">']
for p in urls:
    loc = BASE + "/" if p["path"] == "/" else BASE + p["path"]
    pri = "1.0" if p["path"] == "/" else ("0.8" if p["slug"] == "products" else "0.6")
    img = f"<image:image><image:loc>{BASE}/img/portrait-cigar.jpg</image:loc><image:title>Adam Weingard</image:title></image:image>" if p["slug"] in ("index", "about") else ""
    sm.append(f"  <url><loc>{loc}</loc><lastmod>{TODAY}</lastmod><changefreq>monthly</changefreq><priority>{pri}</priority>{img}</url>")
sm.append("</urlset>\n")
write("sitemap.xml", "\n".join(sm))
write("robots.txt", f"User-agent: *\nAllow: /\nDisallow: /404\nDisallow: /og\n\nSitemap: {BASE}/sitemap.xml\n")

# artifact copy of the home page: CSS inline, no doctype/html/head/body (the claude.ai viewer wraps it)
home = PAGES[0]
art = f'''<title>Weingoat</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght,SOFT,WONK@0,9..144,400..700,0..100,0..1;1,9..144,400..700,0..100,0..1&family=Instrument+Sans:ital,wght@0,400;0,500;0,600;1,400&display=swap">
<style>
{css}</style>
{defs}
{header(home)}
<main id="main">
{read("src/pages/index.html")}
</main>
{FOOTER}
<script>
{script}
</script>
'''
# artifact is single-page: route page links back to anchors and relative images
art = art.replace('href="/products#playbook"', 'href="#learn"').replace('href="/products#community"', 'href="#learn"').replace('href="/products#coaching"', 'href="#learn"')
art = art.replace('href="/#leaks"', 'href="#leaks"').replace('href="/#method"', 'href="#method"').replace('href="/#record"', 'href="#record"')
art = art.replace('src="/img/', 'src="img/')
write("artifact/weingoat.html", art)
print("built:", [p["slug"] + ".html" for p in PAGES], "sitemap.xml robots.txt styles.css artifact/weingoat.html")
