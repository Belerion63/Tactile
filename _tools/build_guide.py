# -*- coding: utf-8 -*-
"""Guides d'atelier : un guide par module de la suite, un module de guide par page.

    python build_guide.py            construit tous les guides déclarés
    python build_guide.py wood       n'en construit qu'un

Arborescence produite :

    website/<mod>/workshop/index.html        le sommaire
    website/<mod>/workshop/<slug>.html       un module du guide, une page

Chaque module se lit seul et porte son adresse : on peut l'envoyer sur Discord
ou le citer depuis l'atelier. Un module dont le corps vaut None affiche un
emplacement en attente, visible et impossible à publier par mégarde.
"""
import io, os, re, sys

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_URL = "https://belerion63.github.io/Tactile"

DISCORD = "https://discord.gg/WPdhCW4JdU"
CURSEFORGE = "https://www.curseforge.com/members/belerion/projects"
KOFI = "https://ko-fi.com/belerion"
GITHUB = "https://github.com/Belerion63/Tactile"
LIC = "https://github.com/Belerion63/Tactile/blob/main/LICENSE"
X = ' target="_blank" rel="noopener"'

EMB = ('<g fill="none" stroke="#191510" stroke-width="8" stroke-linecap="round" stroke-linejoin="round">'
       '<line x1="-46" y1="-52" x2="46" y2="-52"/><line x1="0" y1="-52" x2="0" y2="58"/></g>'
       '<g fill="#191510"><circle cx="-46" cy="-52" r="9.5"/><circle cx="46" cy="-52" r="9.5"/>'
       '<circle cx="0" cy="58" r="9.5"/></g>'
       '<circle cx="0" cy="-52" r="12" fill="none" stroke="#c07f1e" stroke-width="7"/>'
       '<circle cx="0" cy="-52" r="5" fill="#c07f1e"/>')

# ---------------------------------------------------------------- les guides
# module = (titre_fr, titre_en, resume_fr, resume_en, image|None, corps_fr|None, corps_en|None)
# Le corps accepte plusieurs paragraphes : une liste de chaînes.
GUIDES = {
 "wood": {
  "name": "Wood", "color": "#4f9e3a",
  "title": ("L'atelier d'espèces", "The species workshop"),
  "lead": ("Tout ce qu'il faut savoir pour sculpter une espèce et la partager. "
           "Chaque module se lit seul, dans l'ordre que l'on veut.",
           "Everything needed to sculpt a species and share it. "
           "Each section stands alone, read them in any order."),
  "chapters": [
    ("Entrer dans l'éditeur", "Entering the editor",
     "Ouvrir l'atelier, créer un pack, comprendre ce que l'on voit.",
     "Opening the workshop, creating a pack, reading what is on screen.",
     None, None, None),
    ("La forme", "Shape",
     "Le squelette : tronc, branches, et les règles qui les gouvernent.",
     "The skeleton: trunk, branches, and the rules that govern them.",
     "../img/g1.jpg", None, None),
    ("Le feuillage", "Foliage",
     "La masse, sa densité, ses creux, ses ombres.",
     "The mass, its density, its hollows, its shadows.",
     "../img/g2.jpg", None, None),
    ("La texture", "Texture",
     "Dessiner la feuille et la fleur à partir des textures du jeu.",
     "Drawing the leaf and the flower from the game's own textures.",
     "../img/g3.jpg", None, None),
    ("Les paramètres procéduraux", "Procedural parameters",
     "Ce qui fait qu'un arbre n'est jamais deux fois le même.",
     "What makes a tree never twice the same.",
     None, None, None),
    ("Exporter et partager", "Exporting and sharing",
     "Enregistrer l'espèce, l'emporter, l'envoyer à la galerie.",
     "Saving the species, taking it with you, sending it to the gallery.",
     "../img/g4.jpg", None, None),
  ],
 },
}

CSS = r"""
:root{--paper:#f2f1ec;--paper2:#ebe8e1;--card:#fff;--ink:#191510;--ink2:#5f594e;--line:#dcd7cd;--accent:#c07f1e;--c:CCC}
*{box-sizing:border-box}html{background:var(--paper)}
body{margin:0;background:var(--paper);color:var(--ink);font-family:"Segoe UI",system-ui,-apple-system,Arial,sans-serif;-webkit-font-smoothing:antialiased;line-height:1.6}
a{color:inherit;text-decoration:none}
.wrap{max-width:1240px;margin:0 auto;padding:0 32px}
.top{display:flex;justify-content:space-between;align-items:center;gap:10px;padding:14px 32px;max-width:1240px;margin:0 auto}
.back{display:flex;align-items:center;gap:11px;color:var(--ink2);font-size:14px}.back svg{width:20px;height:24px}.back:hover{color:var(--ink)}
.top .r{display:flex;gap:10px;align-items:center}
.top .r a{font-size:13px;color:var(--ink2);border:1px solid var(--line);border-radius:2px;padding:8px 15px}
.top .r a:hover{border-color:var(--ink);color:var(--ink)}
.top .r a.pri{background:var(--ink);color:var(--paper);border-color:var(--ink)}
.langsw{display:inline-flex;border:1px solid var(--line);border-radius:2px;overflow:hidden}
.langsw .lang{background:var(--card);border:none;color:var(--ink2);font-size:12px;font-weight:700;letter-spacing:.06em;padding:8px 11px;cursor:pointer}
.langsw .lang.on{background:var(--ink);color:var(--paper)}

.gh{background:var(--paper2);border-bottom:1px solid var(--line);border-top:3px solid var(--c)}
.gh .wrap{padding:48px 32px 42px;max-width:900px}
.gh .crumb{font-size:13px;color:var(--ink2)}
.gh .crumb a:hover{color:var(--ink)}
.gh .mod{display:inline-block;font-size:11px;letter-spacing:.14em;text-transform:uppercase;font-weight:700;color:#fff;background:var(--c);padding:4px 10px;border-radius:2px}
.gh h1{margin:14px 0 0;font-size:clamp(28px,4vw,42px);font-weight:700;letter-spacing:-.015em}
.gh p{margin:14px 0 0;font-size:17.5px;line-height:1.72;color:var(--ink2);max-width:60ch}

.doc{max-width:900px;margin:0 auto;padding:0 32px 60px}
.chs{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:14px;padding:34px 0 8px}
.ch{display:block;background:var(--card);border:1px solid var(--line);border-left:3px solid var(--c);border-radius:4px;padding:16px 18px}
.ch:hover{border-color:var(--ink);border-left-color:var(--c)}
.ch b{display:block;font-size:16px;font-weight:700;letter-spacing:-.01em}
.ch span{display:block;margin-top:6px;font-size:14px;line-height:1.55;color:var(--ink2)}

.body p{margin:22px 0 0;font-size:17px;line-height:1.78;color:#3f3a31;max-width:66ch}
.body img{display:block;width:100%;height:auto;margin:28px 0 0;border:1px solid rgba(25,18,10,.10);border-radius:6px;box-shadow:0 14px 30px rgba(25,18,10,.15)}
.body{padding-top:34px}

.todo{margin:26px 0 0;padding:18px 20px;border:1px dashed var(--line);border-radius:4px;background:var(--card)}
.todo b{display:block;font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--accent);margin-bottom:6px}
.todo span{font-size:15px;color:var(--ink2)}

.nav{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;margin-top:52px;padding-top:26px;border-top:1px solid var(--line)}
.nav a{max-width:46%;font-size:14.5px;color:var(--ink2);border:1px solid var(--line);border-radius:3px;padding:12px 16px;background:var(--card)}
.nav a:hover{border-color:var(--ink);color:var(--ink)}
.nav a i{display:block;font-style:normal;font-size:11.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--ink2);margin-bottom:3px}
.nav a.next{margin-left:auto;text-align:right}

.end{background:var(--paper2);border-top:1px solid var(--line)}
.end .wrap{padding:46px 32px;max-width:900px;text-align:center}
.end h2{margin:0 0 12px;font-size:24px;font-weight:700}
.end p{margin:0 0 20px;font-size:16.5px;color:var(--ink2)}
.end a{display:inline-block;background:var(--ink);color:var(--paper);font-weight:700;font-size:15px;padding:13px 26px;border-radius:2px}
.end a:hover{background:var(--accent)}

footer{border-top:1px solid var(--line);padding:34px 0;font-size:13px;color:var(--ink2)}
footer .row{display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:16px}
footer .links{display:flex;gap:10px;flex-wrap:wrap}
footer .links a{border:1px solid var(--line);border-radius:2px;padding:8px 15px}
footer .links a:hover{border-color:var(--ink);color:var(--ink)}
"""

SCRIPT = """<script>(function(){function set(l){document.querySelectorAll('[data-fr]').forEach(function(e){var v=e.getAttribute('data-'+l);if(v!==null)e.textContent=v;});document.documentElement.setAttribute('lang',l);try{localStorage.setItem('tactile_lang',l);}catch(e){}document.querySelectorAll('.lang').forEach(function(b){b.classList.toggle('on',b.getAttribute('data-lang')===l);});}var s='en';try{s=localStorage.getItem('tactile_lang')||'en';}catch(e){}document.querySelectorAll('.lang').forEach(function(b){b.addEventListener('click',function(){set(b.getAttribute('data-lang'));});});set(s);})();</script>"""

TODO = ('<div class="todo"><b data-fr="À écrire" data-en="To be written">À écrire</b>'
        "<span data-fr=\"Ce module sera rédigé quand l'atelier sera figé.\""
        " data-en=\"This section will be written once the workshop is settled.\">"
        "Ce module sera rédigé quand l'atelier sera figé.</span></div>")


def slug(s):
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return s or "module"


def en_first(h):
    h = re.sub(r'(data-fr="([^"]*)"\s+data-en="([^"]*)"([^>]*)>)([^<]*)(</)',
               lambda m: m.group(1) + m.group(3) + m.group(6), h)
    return h.replace('<html lang="fr">', '<html lang="en">')


def chrome(g, back_href, back_fr, back_en):
    return (f'<div class="top"><a class="back" href="{back_href}">'
            f'<svg viewBox="-64 -72 128 144"><use href="#emb"/></svg>'
            f'<span data-fr="{back_fr}" data-en="{back_en}">{back_fr}</span></a>'
            f'<div class="r"><span class="langsw"><button class="lang on" data-lang="fr">FR</button>'
            f'<button class="lang" data-lang="en">EN</button></span>'
            f'<a href="{DISCORD}"{X}>Discord</a><a href="{KOFI}"{X}>Ko-fi</a>'
            f'<a class="pri" href="{CURSEFORGE}"{X}>CurseForge</a></div></div>')


def page(g, title_fr, title_en, head_html, body_html, up=2):
    fav = "../" * up + "assets/favicon.png"
    desc = g["lead"][1].replace(chr(34), "&quot;")
    css = CSS.replace("CCC", g["color"])
    end = (f'<section class="end"><div class="wrap">'
           f'<h2 data-fr="Une question, un blocage ?" data-en="A question, a wall?">Une question, un blocage ?</h2>'
           f'<p data-fr="Le salon d\'entraide est là pour ça, et les créations des autres sont souvent la meilleure réponse."'
           f' data-en="The help channel is there for that, and other people\'s creations are often the best answer.">'
           f'Le salon d\'entraide est là pour ça, et les créations des autres sont souvent la meilleure réponse.</p>'
           f'<a href="{DISCORD}"{X} data-fr="Rejoindre le Discord" data-en="Join the Discord">Rejoindre le Discord</a>'
           f'</div></section>')
    foot = (f'<footer><div class="wrap"><div class="row">'
            f'<span data-fr="Tactile · suite de mods Minecraft" data-en="Tactile · a Minecraft mod suite">Tactile · suite de mods Minecraft</span>'
            f'<div class="links"><a href="{LIC}"{X} data-fr="© 2026 belerion · Tous droits réservés"'
            f' data-en="© 2026 belerion · All rights reserved">© 2026 belerion · Tous droits réservés</a>'
            f'<a href="{GITHUB}"{X}>GitHub</a></div></div></div></footer>')
    html = ('<!DOCTYPE html>\n<html lang="fr">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            f'<link rel="icon" type="image/png" href="{fav}">\n'
            f'<meta name="description" content="{desc}">\n'
            '<meta property="og:type" content="website">\n'
            '<meta property="og:site_name" content="Tactile">\n'
            f'<meta property="og:title" content="{title_en}">\n'
            f'<meta property="og:description" content="{desc}">\n'
            f'<meta property="og:image" content="{BASE_URL}/assets/og.jpg">\n'
            '<meta name="twitter:card" content="summary_large_image">\n'
            f'<title data-fr="{title_fr}" data-en="{title_en}">{title_en}</title>\n'
            f'<style>{css}</style>\n</head>\n<body>\n'
            f'<svg width="0" height="0" style="position:absolute"><defs><g id="emb">{EMB}</g></defs></svg>\n'
            + head_html + body_html + end + foot + SCRIPT + "\n</body>\n</html>\n")
    return en_first(html)


def build_index(g):
    cards = []
    for c in g["chapters"]:
        fr, en, rfr, ren = c[0], c[1], c[2], c[3]
        cards.append(f'<a class="ch" href="{slug(en)}.html">'
                     f'<b data-fr="{fr}" data-en="{en}">{fr}</b>'
                     f'<span data-fr="{rfr}" data-en="{ren}">{rfr}</span></a>')
    head = (chrome(g, "../index.html", f"Retour à Tactile:{g['name']}", f"Back to Tactile:{g['name']}")
            + f'<section class="gh"><div class="wrap"><span class="mod">Tactile:{g["name"]}</span>'
              f'<h1 data-fr="{g["title"][0]}" data-en="{g["title"][1]}">{g["title"][0]}</h1>'
              f'<p data-fr="{g["lead"][0]}" data-en="{g["lead"][1]}">{g["lead"][0]}</p></div></section>')
    body = f'<div class="doc"><div class="chs">{"".join(cards)}</div></div>'
    return page(g, f'{g["title"][0]}, Tactile:{g["name"]}', f'{g["title"][1]}, Tactile:{g["name"]}', head, body)


def build_chapter(g, i):
    fr, en, rfr, ren, img, bfr, ben = g["chapters"][i]
    if bfr:
        paras = bfr if isinstance(bfr, list) else [bfr]
        parae = ben if isinstance(ben, list) else [ben]
        corps = "".join(f'<p data-fr="{a}" data-en="{b}">{a}</p>' for a, b in zip(paras, parae))
    else:
        corps = TODO
    pic = f'<img src="{img}" alt="">' if img else ""

    nav = []
    if i > 0:
        p = g["chapters"][i - 1]
        nav.append(f'<a class="prev" href="{slug(p[1])}.html">'
                   f'<i data-fr="Module précédent" data-en="Previous section">Module précédent</i>'
                   f'<span data-fr="{p[0]}" data-en="{p[1]}">{p[0]}</span></a>')
    if i < len(g["chapters"]) - 1:
        n = g["chapters"][i + 1]
        nav.append(f'<a class="next" href="{slug(n[1])}.html">'
                   f'<i data-fr="Module suivant" data-en="Next section">Module suivant</i>'
                   f'<span data-fr="{n[0]}" data-en="{n[1]}">{n[0]}</span></a>')

    crumb = (f'<p class="crumb"><a href="../index.html">Tactile:{g["name"]}</a> · '
             f'<a href="index.html" data-fr="{g["title"][0]}" data-en="{g["title"][1]}">{g["title"][0]}</a></p>')
    head = (chrome(g, "index.html", "Retour au sommaire", "Back to contents")
            + f'<section class="gh"><div class="wrap">{crumb}'
              f'<h1 data-fr="{fr}" data-en="{en}">{fr}</h1>'
              f'<p data-fr="{rfr}" data-en="{ren}">{rfr}</p></div></section>')
    body = f'<div class="doc"><div class="body">{corps}{pic}</div><nav class="nav">{"".join(nav)}</nav></div>'
    return page(g, f'{fr}, {g["title"][0]}', f'{en}, {g["title"][1]}')  if False else \
           page(g, f'{fr}, Tactile:{g["name"]}', f'{en}, Tactile:{g["name"]}', head, body)


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else None
    for mod, g in GUIDES.items():
        if only and mod != only:
            continue
        d = os.path.join(SITE, mod, "workshop")
        os.makedirs(d, exist_ok=True)
        io.open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(build_index(g))
        for i, c in enumerate(g["chapters"]):
            io.open(os.path.join(d, slug(c[1]) + ".html"), "w", encoding="utf-8").write(build_chapter(g, i))
        todo = sum(1 for c in g["chapters"] if c[5] is None)
        print(f"{mod}/workshop/ : 1 sommaire + {len(g['chapters'])} pages, {todo} à écrire")
        for c in g["chapters"]:
            print(f"    {slug(c[1])}.html")


if __name__ == "__main__":
    main()
