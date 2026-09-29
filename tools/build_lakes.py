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
      angle="Desert bass hunting", tagline="Red Rock Bass Factory",
      hook="Chase largemouth bass in crystal blue water surrounded by Southern Utah red rock.",
      experience=["This is desert bass fishing with a completely different backdrop. You are casting for largemouth along red sandstone cliffs, sandy shorelines, flooded structure and clear blue water. It is the kind of place where you can spend the morning working shallow cover and then chase bass around deeper structure as the sun climbs."],
      why="Year round bass fishing, dramatic scenery, and the chance to catch numbers of largemouth while still having a legitimate shot at a big fish.",
      species=["Largemouth bass", "Bluegill"], access="Good boat and shore access."),
 dict(slug="lake-powell", name="Lake Powell", where="Southern Utah",
      angle="Canyon striper adventure", tagline="Striper Canyon",
      hook="Run the canyons, find the bait and watch the stripers explode on the surface.",
      experience=["Lake Powell feels less like fishing a lake and more like fishing an enormous canyon system. You run through narrow sandstone canyons, stop where bait is holding and cast for striped bass. When the stripers are schooling, the action can become frantic, with fish chasing bait right to the surface."],
      why="Massive water, endless canyon structure and the possibility of catching striped bass by the dozens when you find an active school.",
      species=["Striped bass", "Smallmouth bass", "Largemouth bass", "Walleye", "Crappie", "Catfish", "Bluegill"], access="Best fished by boat."),
 dict(slug="navajo-lake", name="Navajo Lake", where="Southern Utah",
      angle="High alpine trout escape", tagline="Lava Tube Trout Lake",
      hook="High alpine trout fishing on a lake where the water disappears underground.",
      experience=["Navajo is almost the opposite of Lake Powell. You are fishing at more than 9,000 feet, surrounded by spruce and pine rather than desert cliffs. The water is cold, quiet and surprisingly deep in places despite the lake\u2019s relatively small size. It feels like a remote mountain trout expedition."],
      why="Brook trout, rainbow trout and a completely different high-country fishing experience. The surrounding forest and elevation make the trip feel more like Colorado or Montana than Southern Utah.",
      species=["Rainbow trout", "Brook trout"], access="Cool, forested mountain setting."),
 dict(slug="panguitch-lake", name="Panguitch Lake", where="Southern Utah",
      angle="Trophy trout hunting", tagline="Big Fish Reboot",
      hook="Fish the lake named \u2018Big Fish\u2019 for Southern Utah\u2019s trophy trout.",
      experience=["Panguitch is built around one thing: trout. You can troll open water for cruising fish, work shorelines and structure, or target tiger trout and cutthroat with more aggressive presentations. The lake\u2019s high elevation and open basin make changing weather and conditions part of the experience."],
      why="This is where you go when the goal is not simply catching trout but looking for a genuinely large Southern Utah trout.",
      species=["Rainbow trout", "Cutthroat trout", "Tiger trout"], access="Good boat access.",
      details=["Full 8 hour guided fishing trip", "All fishing gear and equipment provided", "Lunch provided",
               "Customized start and end times to fit your schedule", "Expert instruction and local knowledge",
               "Perfect for beginners, families and experienced anglers"]),
 dict(slug="gunlock-reservoir", name="Gunlock Reservoir", where="near St. George, Southern Utah",
      angle="Intimate red rock bass fishing", tagline="Comeback Waterfall Bass",
      hook="Fish a red rock bass lake that came back from the brink.",
      experience=["Gunlock feels more intimate than Sand Hollow or Powell. You are fishing a smaller red rock reservoir where finding the right shoreline, point or piece of cover can make all the difference. It is a good lake for slowing down and actually learning where the bass are holding.",
                  "And when conditions are right, the fishing trip comes with something you cannot manufacture: Gunlock Falls spilling over the dam."],
      why="Smaller water, less overwhelming than Powell, beautiful red rock scenery and a bass fishery with an unusual comeback story.",
      species=["Largemouth bass", "Crappie", "Catfish"], access="Smaller warm water lake."),
 dict(slug="quail-creek-reservoir", name="Quail Creek Reservoir", where="near St. George, Southern Utah",
      angle="Clear water trophy bass", tagline="Record Factory",
      hook="A desert reservoir where stocked trout help grow trophy bass.",
      experience=["Quail Creek is one of those lakes that can surprise you. It does not look like a trophy fishery from the shore, but beneath the clear water is an unusual combination of warm water bass habitat and stocked trout. Largemouth can key on trout, creating opportunities to target bigger bass around deeper water and structure."],
      why="Clear water, big largemouth, aggressive smallmouth-style sight fishing opportunities and the unusual possibility of catching trout and bass in the same day.",
      species=["Largemouth bass", "Crappie", "Bluegill", "Rainbow trout"], access="Good facilities and boat ramps."),
 dict(slug="fish-lake", name="Fish Lake", where="farther north in Utah",
      angle="Deep water Mackinaw hunting", tagline="Alpine Mackinaw Lake",
      hook="Go deep for a trophy Mackinaw in the heart of Utah\u2019s high country.",
      experience=["Fish Lake is not a numbers game in the same way as some of the Southern Utah bass lakes. This is about hunting. You are working deep water for lake trout, watching electronics, finding the right depth and putting a bait or lure in front of a fish that can weigh tens of pounds.",
                  "In summer, the high-elevation setting makes the boat trip itself part of the experience. In winter, the entire lake transforms into an ice fishing destination."],
      why="Trophy lake trout, high alpine scenery and the feeling that every deep-water mark on the electronics could be the fish you came for.",
      species=["Lake trout", "Splake", "Rainbow trout", "Cutthroat trout", "Other trout"], access="Worth the longer drive."),
]
for _l in LAKES:
    _l["blurb"] = _l["hook"]

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
    exp_html = "".join(f"<p>{E(p)}</p>" for p in l["experience"])
    details_html = ""
    if l.get("details"):
        details_html = "<h3>Good to know</h3><ul class=\"know\">" + "".join(f"<li>{E(d)}</li>" for d in l["details"]) + "</ul>"
    url = f"{BASE}lakes/{l['slug']}.html"
    title = f"Guided Fishing Trips at {l['name']}, Utah | Henrie Outfitters"
    desc = f"{l['hook']} Guided fishing trips at {l['name']} with Henrie Outfitters. Call {PHONE_DISPLAY}."
    qa = faq(l)
    others = "".join(f'<li><a href="{o["slug"]}.html">{E(o["name"])}</a></li>' for o in LAKES if o["slug"] != l["slug"])
    fish = "".join(f"<li>{E(s)}</li>" for s in l["species"])
    faq_html = "".join(f"<details open><summary>{E(q)}</summary><p>{E(a)}</p></details>" for q, a in qa)
    graph = [
      {"@context": "https://schema.org", "@type": "Service", "name": f"Guided fishing trips at {l['name']}",
       "serviceType": "Guided fishing trip", "description": f"{l['tagline']}. {l['hook']} {l['experience'][0]}", "url": url,
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
<p class="kicker">{E(l["angle"])} &middot; {E(l["where"])}</p>
<h1>Guided fishing trips at {E(l["name"])}</h1>
<p class="sub">{E(l["hook"])}</p>
<a class="btn" href="{book}"><span>Book a trip at {E(l["name"])}</span><i>&rarr;</i></a>
</div></section>
<section><div class="wrap two">
<div><p class="eyebrow">The experience</p><h2>{E(l["tagline"])}</h2>
{exp_html}
<h3>Why fish {E(l["name"])}</h3><p>{E(l["why"])}</p>
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

def cards_html():
    out = []
    for n, l in enumerate(LAKES, 1):
        tags = "".join(f"<li>{E(s)}</li>" for s in l["species"])
        out.append(f'''    <article class="lakeitem reveal">
      <span class="num">{n:02d}</span>
      <div><span class="angle">{E(l["angle"])}</span><h3><a href="lakes/{l["slug"]}.html">{E(l["name"])}</a></h3><p class="hook">{E(l["hook"])}</p><ul class="fish">{tags}</ul><a class="more" href="lakes/{l["slug"]}.html">Lake details &rarr;</a><a class="btn" href="#contact" data-lake="{E(l["name"])}"><span>Book a trip here</span><i>&rarr;</i></a></div>
    </article>
''')
    return "".join(out)

def patch_index():
    p = ROOT / "index.html"
    s = p.read_text(encoding="utf-8")
    a, z = "<!-- LAKES:START -->", "<!-- LAKES:END -->"
    if a in s:
        head, rest = s.split(a, 1); _, tail = rest.split(z, 1)
        s = head + a + "\n" + cards_html() + "  " + z + tail
        p.write_text(s, encoding="utf-8")

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
        lines.append(f"- [{l['name']}]({BASE}lakes/{l['slug']}.html): {l['tagline']}, {l['angle'].lower()}. {l['hook']}")
    lines += ["", "## Main site", "", f"- [Henrie Outfitters home]({BASE}): trips, lakes, guide, booking", f"- [Instagram]({INSTAGRAM})", ""]
    (ROOT / "llms.txt").write_text("\n".join(lines))
    patch_index()
    print("built", len(LAKES), "lake pages")

if __name__ == "__main__":
    main()
