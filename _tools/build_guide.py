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

Un corps est une LISTE DE BLOCS, et les versions française et anglaise doivent
avoir les mêmes blocs dans le même ordre (le contrôle est fait au montage). Les
blocs disponibles :

    ("p",     "un paragraphe")
    ("h",     "un sous-titre", "its english title")   les DEUX langues, il sert d'ancre
    ("steps", ["première étape", "deuxième étape"])
    ("list",  ["un point", "un autre"])
    ("keys",  [("clic milieu", "orbiter"), ...])     touche + ce qu'elle fait
    ("img",   "../img/g1.jpg", "légende")            la légende est facultative
    ("svg",   SVG_TIRAGE, "légende")                 un schéma, dessiné dans guide_wood
    ("fold",  "Le titre du dépliant", [blocs...])    replié par défaut
    ("link",  "https://…", "le libellé")
    ("note",  "un encart")

Le texte traduisible voyage dans des attributs data-fr/data-en, lus par le
sélecteur de langue : il est échappé au montage, et il ne peut donc contenir
aucune balise. C'est la raison d'être des blocs — une liste ou une touche
mise en avant se déclare, elle ne s'écrit pas en HTML dans la phrase.
"""
import html, io, os, re, sys

import guide_wood

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_URL = "https://belerion63.github.io/Tactile"

DISCORD = "https://discord.com/invite/WPdhCW4JdU"
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
# Le CONTENU vit dans un fichier par module de la suite (guide_wood.py pour le
# bois) : le generateur est commun, les textes ne le sont pas, et un guide de
# cinq modules noierait tout le reste de ce fichier.
GUIDES = {
 "wood": {
  "name": "Wood", "color": "#4f9e3a",
  "title": ("L'atelier d'espèces", "The species workshop"),
  "lead": ("Tout ce qu'il faut savoir pour sculpter une espèce et la partager. "
           "Chaque module se lit seul, dans l'ordre que l'on veut.",
           "Everything needed to sculpt a species and share it. "
           "Each section stands alone, read them in any order."),
  "chapters": guide_wood.CHAPTERS,
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
.body img{display:block;max-width:100%;height:auto;margin:0;border:1px solid rgba(25,18,10,.10);border-radius:6px;box-shadow:0 14px 30px rgba(25,18,10,.15)}
.body{padding-top:34px}
.body h2{margin:46px 0 0;font-size:22.5px;font-weight:700;letter-spacing:-.015em}
.body h2:first-child{margin-top:0}
.body figure{margin:30px 0 0}
.body figcaption{margin-top:9px;font-size:13.5px;line-height:1.55;color:var(--ink2);max-width:66ch}
.body ol{margin:22px 0 0;padding:0;list-style:none;counter-reset:s}
.body ol li{counter-increment:s;position:relative;padding-left:40px;margin-top:13px;font-size:16.5px;line-height:1.72;color:#3f3a31;max-width:64ch}
.body ol li::before{content:counter(s);position:absolute;left:0;top:2px;width:25px;height:25px;border-radius:50%;background:var(--c);color:#fff;font-size:13px;font-weight:700;line-height:25px;text-align:center}
.keys{margin:24px 0 0;border:1px solid var(--line);border-radius:4px;background:var(--card);overflow:hidden;max-width:66ch}
.keys>div{display:flex;gap:18px;padding:10px 16px;border-top:1px solid var(--line)}
.keys>div:first-child{border-top:none}
.keys b{flex:0 0 190px;font-family:ui-monospace,"Cascadia Mono",Consolas,monospace;font-size:13px;font-weight:600;color:var(--ink);line-height:1.5}
.keys span{font-size:15.5px;line-height:1.5;color:var(--ink2)}
.note{margin:28px 0 0;padding:15px 20px;background:var(--card);border:1px solid var(--line);border-left:3px solid var(--accent);border-radius:0 4px 4px 0;font-size:15.5px;line-height:1.7;color:var(--ink2);max-width:66ch}
.body ul{margin:20px 0 0;padding:0;list-style:none;max-width:66ch}
.body ul li{position:relative;padding-left:010px;margin-top:11px;font-size:16.5px;line-height:1.72;color:#3f3a31;padding-left:20px}
.body ul li::before{content:"";position:absolute;left:2px;top:11px;width:6px;height:6px;border-radius:50%;background:var(--c)}
.sch{overflow-x:auto}
.sch svg{display:block;width:100%;height:auto;max-width:640px;margin:0 auto}
details{margin:26px 0 0;border:1px solid var(--line);border-radius:4px;background:var(--card);max-width:66ch}
details summary{cursor:pointer;padding:13px 18px;font-size:15.5px;font-weight:700;list-style:none;display:flex;align-items:center;gap:10px}
details summary::-webkit-details-marker{display:none}
details summary::before{content:"+";color:var(--accent);font-weight:700;font-size:17px;line-height:1}
details[open] summary::before{content:"–"}
details .fold{padding:0 18px 16px}
details .fold>*:first-child{margin-top:4px}
p.go{margin:26px 0 0}
p.go a{display:inline-block;border:1px solid var(--line);border-radius:2px;padding:11px 20px;font-size:14.5px;background:var(--card)}
p.go a:hover{border-color:var(--ink);color:var(--ink)}
.toc{margin:0 0 6px;padding:16px 20px;background:var(--paper2);border:1px solid var(--line);border-radius:4px;max-width:66ch}
.toc b{display:block;font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--ink2);margin-bottom:9px}
.toc a{display:block;padding:4px 0;font-size:15px;color:var(--ink2);border-bottom:1px solid transparent}
.toc a:hover{color:var(--ink)}
@media(max-width:640px){.keys>div{display:block}.keys b{display:block;margin-bottom:3px}}

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

SCRIPT = """<script>(function(){function set(l){document.querySelectorAll('[data-fr]').forEach(function(e){var v=e.getAttribute('data-'+l);if(v===null)return;if(e.classList.contains('rich')){e.innerHTML=v;}else{e.textContent=v;}});document.documentElement.setAttribute('lang',l);try{localStorage.setItem('tactile_lang',l);}catch(e){}document.querySelectorAll('.lang').forEach(function(b){b.classList.toggle('on',b.getAttribute('data-lang')===l);});}var s='en';try{s=localStorage.getItem('tactile_lang')||'en';}catch(e){}document.querySelectorAll('.lang').forEach(function(b){b.addEventListener('click',function(){set(b.getAttribute('data-lang'));});});set(s);})();</script>"""

TODO = ('<div class="todo"><b data-fr="À écrire" data-en="To be written">À écrire</b>'
        "<span data-fr=\"Ce module sera rédigé quand l'atelier sera figé.\""
        " data-en=\"This section will be written once the workshop is settled.\">"
        "Ce module sera rédigé quand l'atelier sera figé.</span></div>")


def slug(s):
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return s or "module"


def esc(s):
    """Tout texte d'auteur passe par ici : il finit dans un attribut, guillemets et esperluettes compris."""
    return html.escape(str(s), quote=True)


SLUGS = set()   # les modules du guide en cours de construction, pour refuser un lien vers le vide
LINK = re.compile(r"\{([a-z0-9-]+)(#[a-z0-9-]+)?\|([^}]+)\}")


def links(text):
    """Transforme les {module|libellé} du texte d'auteur en vrais liens. Rend (html, y_a_t_il_un_lien)."""
    found = [False]

    def one(m):
        target, anchor, label = m.group(1), m.group(2) or "", m.group(3)
        if SLUGS and target not in SLUGS:
            raise SystemExit(f"lien vers un module inconnu : « {target} »")
        found[0] = True
        return f'<a href="{target}.html{anchor}">{label}</a>'

    return LINK.sub(one, text), found[0]


def t(fr, en, tag="span", cls=""):
    """Un noeud traduisible. Le français est écrit dans le corps, en_first() y mettra l'anglais au montage.

    <p>UN MOT PEUT RENVOYER À UN AUTRE MODULE, avec {module|libellé} dans le texte. Le texte traduit voyage dans un
    attribut et se pose par {@code textContent} : il ne peut donc pas contenir de balise. Le noeud qui en porte une
    est marqué {@code rich}, et le sélecteur de langue le pose par {@code innerHTML} — c'est la seule différence, et
    elle ne concerne que les phrases qui en ont besoin. Le contenu vient d'ici, jamais d'un lecteur.
    """
    fh, a = links(esc(fr))
    eh, b = links(esc(en))
    if not (a or b):
        c = f' class="{cls}"' if cls else ""
        return f'<{tag}{c} data-fr="{esc(fr)}" data-en="{esc(en)}">{esc(fr)}</{tag}>'
    # L'ANGLAIS EST POSÉ DIRECTEMENT : en_first() ne sait pas réécrire un noeud qui contient déjà des balises,
    # et il n'a pas à le savoir — on lui livre la page dans l'état qu'il produit ailleurs.
    c = " ".join(x for x in (cls, "rich") if x)
    return f'<{tag} class="{c}" data-fr="{attr(fh)}" data-en="{attr(eh)}">{eh}</{tag}>'


def attr(h):
    """Range un fragment HTML DÉJÀ échappé dans une valeur d'attribut.

    ⚠ Surtout pas {@code esc()} ici : il ré-échapperait les entités que le texte porte déjà, et une apostrophe
    française finirait affichée « &#x27; » en toutes lettres. Seuls les caractères qui casseraient l'attribut
    partent ; les entités existantes sont laissées telles quelles, le navigateur les rendra au getAttribute.
    """
    return h.replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")


def blocks_html(bfr, ben):
    """Le corps d'un module. Les deux langues portent les mêmes blocs, sinon on refuse de construire."""
    if len(bfr) != len(ben):
        raise SystemExit(f"corps FR ({len(bfr)} blocs) et EN ({len(ben)} blocs) de longueurs différentes")
    out = []
    for a, b in zip(bfr, ben):
        kind = a[0]
        if kind != b[0]:
            raise SystemExit(f"blocs désalignés : « {kind} » en français, « {b[0]} » en anglais")
        if kind == "h":
            # UN SOUS-TITRE PORTE SES DEUX LANGUES DANS LE MÊME BLOC : ("h", titre_fr, titre_en). C'est le seul bloc
            # dans ce cas, et pour une raison — son texte sert aussi d'ANCRE, et une ancre doit être la même des deux
            # côtés. Les tenir dans deux listes séparées, c'était accepter qu'elles divergent en silence et que le
            # sommaire pointe à côté.
            out.append(f'<h2 id="{slug(a[2])}" data-fr="{esc(a[1])}" data-en="{esc(a[2])}">{esc(a[1])}</h2>')
        elif kind in ("p", "note"):
            out.append(t(a[1], b[1], "p", "note" if kind == "note" else ""))
        elif kind == "steps":
            if len(a[1]) != len(b[1]):
                raise SystemExit("étapes en nombre différent entre les deux langues")
            out.append("<ol>" + "".join(t(x, y, "li") for x, y in zip(a[1], b[1])) + "</ol>")
        elif kind == "keys":
            if len(a[1]) != len(b[1]):
                raise SystemExit("raccourcis en nombre différent entre les deux langues")
            # La touche ne se traduit pas — « Shift » est « Shift » partout ; seul ce qu'elle fait change de langue.
            rows = "".join(f"<div><b>{esc(x[0])}</b>{t(x[1], y[1])}</div>" for x, y in zip(a[1], b[1]))
            out.append(f'<div class="keys">{rows}</div>')
        elif kind == "list":
            if len(a[1]) != len(b[1]):
                raise SystemExit("puces en nombre différent entre les deux langues")
            out.append("<ul>" + "".join(t(x, y, "li") for x, y in zip(a[1], b[1])) + "</ul>")
        elif kind == "img":
            # DIFFÉRÉES : une page de guide porte jusqu'à neuf captures, et on n'en voit qu'une à la fois.
            fig = f'<img src="{esc(a[1])}" alt="" loading="lazy" decoding="async">'
            if len(a) > 2 and a[2]:
                fig += t(a[2], b[2], "figcaption")
            out.append(f"<figure>{fig}</figure>")
        elif kind == "svg":
            # LE DESSIN N'EST PAS TRADUIT, sa légende oui. Un schéma dont les étiquettes changent de langue demanderait
            # deux dessins à tenir ; ceux-ci n'écrivent donc que des mots qui ne se traduisent pas (des chiffres, des
            # noms de boutons) ou rien du tout.
            fig = f'<div class="sch">{a[1]}</div>'
            if len(a) > 2 and a[2]:
                fig += t(a[2], b[2], "figcaption")
            out.append(f"<figure>{fig}</figure>")
        elif kind == "fold":
            # DÉPLIANT : ce qui mérite d'être écrit mais pas d'être traversé. Ouvert, il se lit comme le reste ; fermé,
            # il ne coupe pas le fil de la page.
            out.append("<details><summary>" + t(a[1], b[1], "span") + "</summary>"
                       + f'<div class="fold">{blocks_html(a[2], b[2])}</div></details>')
        elif kind == "link":
            out.append(f'<p class="go"><a href="{esc(a[1])}"{X}>' + t(a[2], b[2], "span") + "</a></p>")
        else:
            raise SystemExit(f"bloc inconnu : « {kind} »")
    return "".join(out)


def toc_html(bfr, ben):
    """Le sommaire d'un module, tiré de ses sous-titres. Rien à tenir à jour : il suit le texte."""
    items = []
    for a in bfr:
        if a[0] == "h":
            items.append(f'<a href="#{slug(a[2])}">' + t(a[1], a[2], "span") + "</a>")
    if len(items) < 3:
        return ""  # deux entrées ne sont pas un sommaire, juste du bruit en haut de page
    return ('<nav class="toc">'
            '<b data-fr="Sur cette page" data-en="On this page">Sur cette page</b>'
            + "".join(items) + "</nav>")


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
    desc = esc(g["lead"][1])
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
    doc = ('<!DOCTYPE html>\n<html lang="fr">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            f'<link rel="icon" type="image/png" href="{fav}">\n'
            f'<meta name="description" content="{desc}">\n'
            '<meta property="og:type" content="website">\n'
            '<meta property="og:site_name" content="Tactile">\n'
            f'<meta property="og:title" content="{title_en}">\n'
            f'<meta property="og:description" content="{desc}">\n'
            f'<meta property="og:image" content="{BASE_URL}/assets/og.jpg">\n'
            '<meta name="twitter:card" content="summary_large_image">\n'
            f'<title data-fr="{esc(title_fr)}" data-en="{esc(title_en)}">{esc(title_en)}</title>\n'
            f'<style>{css}</style>\n</head>\n<body>\n'
            f'<svg width="0" height="0" style="position:absolute"><defs><g id="emb">{EMB}</g></defs></svg>\n'
            + head_html + body_html + end + foot + SCRIPT + "\n</body>\n</html>\n")
    return en_first(doc)


def build_index(g):
    cards = []
    for c in g["chapters"]:
        fr, en, rfr, ren = c[0], c[1], c[2], c[3]
        cards.append(f'<a class="ch" href="{slug(en)}.html">' + t(fr, en, "b") + t(rfr, ren) + "</a>")
    head = (chrome(g, "../index.html", f"Retour à Tactile:{g['name']}", f"Back to Tactile:{g['name']}")
            + f'<section class="gh"><div class="wrap"><span class="mod">Tactile:{g["name"]}</span>'
            + t(g["title"][0], g["title"][1], "h1") + t(g["lead"][0], g["lead"][1], "p") + '</div></section>')
    body = f'<div class="doc"><div class="chs">{"".join(cards)}</div></div>'
    return page(g, f'{g["title"][0]}, Tactile:{g["name"]}', f'{g["title"][1]}, Tactile:{g["name"]}', head, body)


def build_chapter(g, i):
    fr, en, rfr, ren, img, bfr, ben = g["chapters"][i]
    corps = (toc_html(bfr, ben) + blocks_html(bfr, ben)) if bfr else TODO
    # L'IMAGE EN TÊTE, plus en pied : sur un module rédigé, elle montre de quoi on parle avant qu'on en parle.
    # En pied, elle n'était plus qu'une décoration qu'on découvrait après avoir tout lu.
    pic = f'<img src="{esc(img)}" alt="">' if img else ""

    nav = []
    if i > 0:
        p = g["chapters"][i - 1]
        nav.append(f'<a class="prev" href="{slug(p[1])}.html">'
                   f'<i data-fr="Module précédent" data-en="Previous section">Module précédent</i>'
                   + t(p[0], p[1]) + "</a>")
    if i < len(g["chapters"]) - 1:
        n = g["chapters"][i + 1]
        nav.append(f'<a class="next" href="{slug(n[1])}.html">'
                   f'<i data-fr="Module suivant" data-en="Next section">Module suivant</i>'
                   + t(n[0], n[1]) + "</a>")

    crumb = (f'<p class="crumb"><a href="../index.html">Tactile:{g["name"]}</a> · '
             f'<a href="index.html" data-fr="{esc(g["title"][0])}" data-en="{esc(g["title"][1])}">'
             f'{esc(g["title"][0])}</a></p>')
    head = (chrome(g, "index.html", "Retour au sommaire", "Back to contents")
            + f'<section class="gh"><div class="wrap">{crumb}'
            + t(fr, en, "h1") + t(rfr, ren, "p") + '</div></section>')
    body = f'<div class="doc"><div class="body">{pic}{corps}</div><nav class="nav">{"".join(nav)}</nav></div>'
    return page(g, f'{fr}, {g["title"][0]}', f'{en}, {g["title"][1]}')  if False else \
           page(g, f'{fr}, Tactile:{g["name"]}', f'{en}, Tactile:{g["name"]}', head, body)


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else None
    for mod, g in GUIDES.items():
        if only and mod != only:
            continue
        d = os.path.join(SITE, mod, "workshop")
        os.makedirs(d, exist_ok=True)
        # LES MODULES DU GUIDE, connus AVANT de construire quoi que ce soit : un lien vers un module qui n'existe
        # pas doit arrêter la construction, pas produire une page qui mène à une 404.
        SLUGS.clear()
        SLUGS.update(slug(c[1]) for c in g["chapters"])
        io.open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(build_index(g))
        for i, c in enumerate(g["chapters"]):
            io.open(os.path.join(d, slug(c[1]) + ".html"), "w", encoding="utf-8").write(build_chapter(g, i))
        todo = sum(1 for c in g["chapters"] if c[5] is None)
        print(f"{mod}/workshop/ : 1 sommaire + {len(g['chapters'])} pages, {todo} à écrire")
        for c in g["chapters"]:
            print(f"    {slug(c[1])}.html")
        # LES PAGES ORPHELINES SE SIGNALENT. Renommer un module change son adresse, et l'ancienne page reste en
        # ligne : elle continue d'être servie, indexée et partagée alors que plus rien n'y mène.
        kept = {"index.html"} | {slug(c[1]) + ".html" for c in g["chapters"]}
        stale = sorted(f for f in os.listdir(d) if f.endswith(".html") and f not in kept)
        for f in stale:
            # Sans accent ni pictogramme : la console Windows est en cp1252, elle lève sur le reste.
            print(f"    (!) orpheline, a supprimer a la main : {f}")


if __name__ == "__main__":
    main()
