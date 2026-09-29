#!/usr/bin/env python3
"""Generate the per-lake pages, sitemap.xml, robots.txt and llms.txt.

Run from the repo root:  python3 tools/build_lakes.py
Change BASE when the site moves to a custom domain, then re-run.
"""
import json, html, datetime, pathlib

BASE = "https://firsttimemanager1-png.github.io/James/"
PHONE_DISPLAY, PHONE_TEL, EMAIL = "(435) 592-0680", "+14355920680", "henrieoutfitters@gmail.com"
INSTAGRAM = "https://www.instagram.com/henrieoutfitters/"
TODAY = datetime.date.today().isoformat()
ROOT = pathlib.Path(__file__).resolve().parent.parent

LAKES = [
 dict(slug="sand-hollow-reservoir", name="Sand Hollow Reservoir", where="near St. George, Southern Utah",
      species=["Largemouth bass", "Bluegill"],
      blurb="A top pick for bass fishing in Southern Utah. Sand Hollow Reservoir holds largemouth bass and bluegill and has good boat and shore access.",
      access="Good boat and shore access."),
 dict(slug="lake-powell", name="Lake Powell", where="Southern Utah",
      species=["Striped bass", "Smallmouth bass", "Largemouth bass", "Walleye", "Crappie", "Catfish", "Bluegill"],
      blurb="Lake Powell offers by far the biggest variety of fish in Southern Utah: striped bass, smallmouth and largemouth bass, walleye, crappie, catfish and bluegill. It is especially good if you have a boat.",
      access="Best fished by boat."),
 dict(slug="navajo-lake", name="Navajo Lake", where="Southern Utah",
      species=["Rainbow trout", "Brook trout"],
      blurb="Navajo Lake is an excellent mountain trout lake with rainbow and brook trout, in a much cooler, forested setting than the St. George area.",
      access="Cool, forested mountain setting."),
 dict(slug="panguitch-lake", name="Panguitch Lake", where="Southern Utah",
      species=["Rainbow trout", "Cutthroat trout"],
      blurb="Panguitch Lake is one of the better trout destinations in Southern Utah, with rainbow and cutthroat trout and good boat access. It is home water for Henrie Outfitters.",
      access="Good boat access.",
      details=["Full 8 hour guided fishing trip", "All fishing gear and equipment provided", "Lunch provided",
               "Customized start and end times to fit your schedule", "Expert instruction and local knowledge",
               "Perfect for beginners, families and experienced anglers"]),
 dict(slug="gunlock-reservoir", name="Gunlock Reservoir", where="near St. George, Southern Utah",
      species=["Largemouth bass", "Crappie", "Catfish"],
      blurb="Gunlock Reservoir is a smaller warm water lake near St. George with largemouth bass, crappie and catfish.",
      access="Smaller warm water lake."),
 dict(slug="quail-creek-reservoir", name="Quail Creek Reservoir", where="near St. George, Southern Utah",
      species=["Largemouth bass", "Crappie", "Bluegill", "Rainbow trout"],
      blurb="Quail Creek Reservoir is a very good option near St. George for largemouth bass, crappie, bluegill and rainbow trout. It has good facilities and boat ramps.",
      access="Good facilities and boat ramps."),
 dict(slug="fish-lake", name="Fish Lake", where="farther north in Utah",
      species=["Lake trout", "Splake", "Rainbow trout", "Cutthroat trout", "Other trout"],
      blurb="Fish Lake is a serious trout destination for anglers willing to drive farther north, with lake trout, splake, rainbow, cutthroat and other trout.",
      access="Worth the longer drive."),
]

E = html.escape
def jl(obj):  # JSON-LD script tag
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False).replace("</", "<\\/") + "</script>"

BUSINESS = {"@type": "LocalBusiness", "@id": BASE + "#business", "name": "Henrie Outfitters LLC",
            "url": BASE, "telephone": "+1-435-592-0680", "email": EMAIL}

def faq(l):
    sp = ", ".join(s.lower() for s in l["species"][:-1]) + " and " + l["species"][-1].lower() if len(l["species"]) > 1 else l["species"][0].lower()
    qa = [
     (f"Does Henrie Outfitters guide fishing trips at {l['name']}?",
      f"Yes. Henrie Outfitters LLC, owned and guided by James Henrie, runs guided fishing trips at {l['name']} and at other lakes across Southern Utah."),
     (f"What fish can I catch at {l['name']}?", f"{l['name']} has {sp}."),
     ("How do I book a guided fishing trip?",
      f"Call or text {PHONE_DISPLAY}, email {EMAIL}, or use the booking form on the Henrie Outfitters website. Customized trip packages are available."),
    ]
    if l["slug"] == "panguitch-lake":
        qa.insert(2, ("What is included on a guided fishing trip at Panguitch Lake?",
            "A full 8 hour guided fishing trip, all fishing gear and equipment, lunch, customized start and end times to fit your schedule, and expert instruction and local knowledge."))
    return qa

def sp_short(l):
    s = [x.lower() for x in l["species"][:3]]
    return ", ".join(s[:-1]) + " and " + s[-1] if len(s) > 1 else s[0]

def lake_page(l):
    # Optional per-lake facts. Add keys to a lake in LAKES to show them:
    #   details = ["Best months: ...", "Boat ramp: ...", "Typical catch: ..."]
    details_html = ""
    if l.get("details"):
        details_html = "<h3>Good to know</h3><ul class=\"know\">" + "".join(f"<li>{E(d)}</li>" for d in l["details"]) + "</ul>"
    url = f"{BASE}lakes/{l['slug']}.html"
    title = f"Guided Fishing Trips at {l['name']}, Utah | Henrie Outfitters"
    desc = f"Book a guided fishing trip at {l['name']} ({l['where']}) with Henrie Outfitters. Target {', '.join(s.lower() for s in l['species'][:4])}. Call {PHONE_DISPLAY}."
    qa = faq(l)
    others = "".join(f'<li><a href="{o["slug"]}.html">{E(o["name"])}</a></li>' for o in LAKES if o["slug"] != l["slug"])
    fish = "".join(f"<li>{E(s)}</li>" for s in l["species"])
    faq_html = "".join(f"<details open><summary>{E(q)}</summary><p>{E(a)}</p></details>" for q, a in qa)
    graph = [
      {"@context": "https://schema.org", "@type": "Service", "name": f"Guided fishing trips at {l['name']}",
       "serviceType": "Guided fishing trip", "description": l["blurb"], "url": url,
       "areaServed": {"@type": "Place", "name": f"{l['name']}, Utah"},
       "provider": {**BUSINESS, "founder": {"@type": "Person", "name": "James Henrie"}}},
      {"@context": "https://schema.org", "@type": "FAQPage",
       "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qa]},
      {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Henrie Outfitters", "item": BASE},
        {"@type": "ListItem", "position": 2, "name": "Fishing lakes", "item": BASE + "#lakes"},
        {"@type": "ListItem", "position": 3, "name": l["name"], "item": url}]},
    ]
    book = f"{BASE}?lake={l['name'].replace(' ', '%20')}#contact"
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Henrie Outfitters">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}assets/hero.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="../assets/logo.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700&family=Barlow:wght@500;600&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../assets/lake.css">
{"".join(jl(g) for g in graph)}
</head>
<body>
<header class="nav"><a class="brand" href="../"><img src="../assets/logo.png" alt="Henrie Outfitters LLC logo" width="44" height="44">Henrie Outfitters</a>
<nav><a href="../#lakes">All lakes</a><a href="tel:{PHONE_TEL}">Call {PHONE_DISPLAY}</a><a class="book" href="{book}">Book now &rarr;</a></nav></header>
<main>
<section class="hero{' photo' if l['slug']=='panguitch-lake' else ''}"><div class="wrap">
<nav class="crumbs" aria-label="Breadcrumb"><a href="../">Home</a> / <a href="../#lakes">Fishing lakes</a> / <span>{E(l["name"])}</span></nav>
<p class="kicker">{E(l["where"])}</p>
<h1>Guided fishing trips at {E(l["name"])}</h1>
<p class="sub">Guided fishing for {E(sp_short(l))} in {E(l["where"])}.</p>
<a class="btn" href="{book}"><span>Book a trip at {E(l["name"])}</span><i>&rarr;</i></a>
</div></section>
<section><div class="wrap two">
<div><h2>Fishing at {E(l["name"])}</h2>
<p>{E(l["blurb"])}</p>
{details_html}
<p class="guide">Guided by James Henrie, owner of Henrie Outfitters LLC. Call <a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a> or email <a href="mailto:{EMAIL}">{EMAIL}</a> to plan a trip.</p></div>
<div><h2>What you can catch</h2><ul class="fish">{fish}</ul>
<p class="note">{E(l["access"])}</p></div>
</div></section>
<section class="alt"><div class="wrap"><h2>Questions about {E(l["name"])}</h2>{faq_html}</div></section>
<section><div class="wrap"><h2>Other lakes we fish</h2><ul class="others">{others}</ul>
<p><a class="btn" href="{book}"><span>Book a guided trip</span><i>&rarr;</i></a></p></div></section>
</main>
<footer><div class="wrap"><p><strong>Henrie Outfitters LLC</strong> &middot; Guided fishing and hunting in Southern Utah with James Henrie</p>
<p><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a> &middot; <a href="mailto:{EMAIL}">{EMAIL}</a> &middot; <a href="{INSTAGRAM}">Instagram</a></p></div></footer>
</body>
</html>
'''

def main():
    out = ROOT / "lakes"; out.mkdir(exist_ok=True)
    for l in LAKES:
        (out / f"{l['slug']}.html").write_text(lake_page(l), encoding="utf-8")
    urls = [BASE] + [f"{BASE}lakes/{l['slug']}.html" for l in LAKES]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + \
         "".join(f"  <url><loc>{u}</loc><lastmod>{TODAY}</lastmod></url>\n" for u in urls) + "</urlset>\n"
    (ROOT / "sitemap.xml").write_text(sm)
    bots = ["*", "GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-User", "Claude-SearchBot", "PerplexityBot", "Google-Extended", "Applebot-Extended"]
    (ROOT / "robots.txt").write_text("".join(f"User-agent: {b}\nAllow: /\n\n" for b in bots) + f"Sitemap: {BASE}sitemap.xml\n")
    lines = ["# Henrie Outfitters", "",
      "> Henrie Outfitters LLC offers guided fishing and hunting trips in Southern Utah, led by owner and local expert James Henrie (25 years of outdoor experience). Home water is Panguitch Lake, and guided fishing trips are offered at six other Southern Utah lakes.", "",
      f"Book: call or text {PHONE_DISPLAY}, email {EMAIL}, or use the form at {BASE}#contact. Customized trip packages are available.", "",
      "## Guided fishing trips by lake", ""]
    for l in LAKES:
        lines.append(f"- [{l['name']}]({BASE}lakes/{l['slug']}.html): {l['blurb']}")
    lines += ["", "## Main site", "", f"- [Henrie Outfitters home]({BASE}): trips, lakes, guide, booking", f"- [Instagram]({INSTAGRAM})", ""]
    (ROOT / "llms.txt").write_text("\n".join(lines))
    print("built", len(LAKES), "lake pages")

if __name__ == "__main__":
    main()
