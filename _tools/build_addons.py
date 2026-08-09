# -*- coding: utf-8 -*-
"""Galerie des créations de la communauté.

Une seule page pour tous les modules, filtrée côté client. Le bouton d'une page
de module y mène en pré-filtrant : addons/?module=wood

Les données viennent de website/addons/addons.json. Vide = état d'invitation.
DEMO=1 fabrique un aperçu avec des entrées d'exemple, SANS toucher au site.
"""
import io, json, os, re, sys

SITE = "D:/Modding/Minecraft/Tactile/website"
PREV = "D:/Modding/Minecraft/Tactile/website/_tools/preview"
os.makedirs(PREV, exist_ok=True)
SVG  = "D:/Modding/Minecraft/Tactile/Documentation/Logos/svg"
DEMO = os.environ.get("DEMO") == "1"

DISCORD   = "https://discord.gg/WPdhCW4JdU"
CURSEFORGE= "https://www.curseforge.com/members/belerion/projects"
KOFI      = "https://ko-fi.com/belerion"
GITHUB    = "https://github.com/Belerion63/Tactile"
LIC       = "https://github.com/Belerion63/Tactile/blob/main/LICENSE"
X = ' target="_blank" rel="noopener"'

# Modules dotés d'un éditeur : ce sont les seuls qui peuvent recevoir des créations.
MODULES = [("wood", "Wood", "#4f9e3a")]

EMB = ('<g fill="none" stroke="#191510" stroke-width="8" stroke-linecap="round" stroke-linejoin="round">'
       '<line x1="-46" y1="-52" x2="46" y2="-52"/><line x1="0" y1="-52" x2="0" y2="58"/></g>'
       '<g fill="#191510"><circle cx="-46" cy="-52" r="9.5"/><circle cx="46" cy="-52" r="9.5"/>'
       '<circle cx="0" cy="58" r="9.5"/></g>'
       '<circle cx="0" cy="-52" r="12" fill="none" stroke="#c07f1e" stroke-width="7"/>'
       '<circle cx="0" cy="-52" r="5" fill="#c07f1e"/>')

def counts():
    """Nombre de téléchargements par fichier, lu sur les Releases GitHub À LA GÉNÉRATION.

    Aucune dépendance à l'exécution : les chiffres sont inscrits dans la page. Ils
    datent donc de la dernière régénération, ce qui est sans importance à ce rythme.
    En cas de réseau absent ou d'API muette, on renvoie un dictionnaire vide et la
    page se passe simplement du compteur."""
    try:
        import urllib.request
        url = "https://api.github.com/repos/Belerion63/Tactile/releases"
        req = urllib.request.Request(url, headers={"User-Agent": "tactile-site"})
        with urllib.request.urlopen(req, timeout=8) as r:
            rel = json.loads(r.read().decode())
        out = {}
        for rl in rel:
            for a in rl.get("assets", []):
                out[a["name"]] = a.get("download_count", 0)
        return out
    except Exception:
        return {}


def load():
    p = f"{SITE}/addons/addons.json"
    if DEMO:
        return json.loads(io.open(f"{PREV}/addons_demo.json", encoding="utf-8").read())
    if not os.path.exists(p):
        return []
    return json.loads(io.open(p, encoding="utf-8").read())

CSS = r"""
:root{--paper:#f2f1ec;--paper2:#ebe8e1;--card:#fff;--ink:#191510;--ink2:#5f594e;--line:#dcd7cd;--accent:#c07f1e}
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

.head{border-bottom:1px solid var(--line);background:var(--paper2)}
.head .wrap{padding-top:52px;padding-bottom:44px}
.head h1{margin:0;font-size:clamp(30px,4.4vw,46px);font-weight:700;letter-spacing:-.015em}
.head p{margin:14px 0 0;font-size:17.5px;line-height:1.72;color:var(--ink2);max-width:62ch}

.install{display:grid;grid-template-columns:repeat(3,1fr);gap:22px;margin:26px 0 0}
.install div{background:var(--card);border:1px solid var(--line);border-radius:4px;padding:16px 18px}
.install b{display:block;font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--accent);margin-bottom:6px}
.install span{font-size:14.5px;color:var(--ink2)}
.install code{font-family:Consolas,monospace;font-size:13.5px;color:var(--ink)}
@media(max-width:800px){.install{grid-template-columns:1fr}}

.bar{display:flex;gap:12px;align-items:center;flex-wrap:wrap;padding:26px 0 4px}
.bar input,.bar select{font:inherit;font-size:14.5px;color:var(--ink);background:var(--card);border:1px solid var(--line);border-radius:3px;padding:10px 14px}
.bar input{flex:1;min-width:220px}
.bar input:focus,.bar select:focus{outline:none;border-color:var(--ink)}
.count{margin-left:auto;font-size:13.5px;color:var(--ink2)}

.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(330px,1fr));gap:26px;padding:22px 0 70px}
.card{background:var(--card);border:1px solid var(--line);border-top:3px solid var(--c,#999);border-radius:5px;overflow:hidden;display:flex;flex-direction:column}
.shot{position:relative;aspect-ratio:16/9;background:#12141b;overflow:hidden}
.shot img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0;transition:opacity .35s}
.shot img.on{opacity:1}
.shot .nav{position:absolute;top:50%;transform:translateY(-50%);width:30px;height:44px;border:none;background:rgba(0,0,0,.34);color:#fff;font-size:17px;cursor:pointer;opacity:0;transition:opacity .2s}
.shot:hover .nav{opacity:1}
.shot .prev{left:0}.shot .next{right:0}
.dots{position:absolute;bottom:8px;left:0;right:0;display:flex;justify-content:center;gap:6px}
.dots i{width:6px;height:6px;border-radius:50%;background:rgba(255,255,255,.45)}
.dots i.on{background:#fff}
.mod{position:absolute;top:10px;left:10px;font-size:11px;letter-spacing:.1em;text-transform:uppercase;font-weight:700;color:#fff;background:var(--c,#666);padding:4px 9px;border-radius:2px}
.body{padding:18px 20px 20px;display:flex;flex-direction:column;flex:1}
.body h2{margin:0;font-size:20px;font-weight:700;letter-spacing:-.01em}
.by{margin:5px 0 0;font-size:14px;color:var(--ink2)}
.desc{margin:12px 0 0;font-size:15px;line-height:1.65;color:#3f3a31}
.meta{display:flex;flex-wrap:wrap;gap:7px;margin:15px 0 0}
.meta span{font-size:12.5px;color:var(--ink2);border:1px solid var(--line);border-radius:2px;padding:3px 9px}
.foot{display:flex;align-items:center;gap:12px;margin-top:auto;padding-top:18px}
.dl{background:var(--ink);color:var(--paper);font-weight:700;font-size:14.5px;padding:11px 20px;border-radius:2px}
.dl:hover{background:var(--accent)}
.ver{font-size:13px;color:var(--ink2)}
.dls{margin-left:auto;font-size:13px;color:var(--ink2)}

.empty{text-align:center;padding:70px 32px 90px;max-width:640px;margin:0 auto}
.empty svg{width:64px;height:64px;opacity:.3;margin-bottom:20px}
.empty h2{margin:0 0 14px;font-size:26px;font-weight:700}
.empty p{margin:0 0 12px;font-size:16.5px;line-height:1.75;color:var(--ink2)}
.empty .cta{display:inline-block;margin-top:18px;background:var(--ink);color:var(--paper);font-weight:700;font-size:15px;padding:13px 26px;border-radius:2px}
.empty .cta:hover{background:var(--accent)}

.lb{position:fixed;inset:0;background:rgba(10,7,3,.9);display:none;align-items:center;justify-content:center;z-index:50;padding:32px}
.lb.on{display:flex}
.lb img{max-width:100%;max-height:100%;object-fit:contain}
.lb button{position:absolute;top:18px;right:22px;background:none;border:none;color:#fff;font-size:30px;cursor:pointer}

footer{border-top:1px solid var(--line);padding:34px 0;font-size:13px;color:var(--ink2)}
footer .row{display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:16px}
footer .links{display:flex;gap:10px;flex-wrap:wrap}
footer .links a{border:1px solid var(--line);border-radius:2px;padding:8px 15px}
footer .links a:hover{border-color:var(--ink);color:var(--ink)}
"""

def esc(s): return (s or "").replace('"', "&quot;")

def card(a):
    col = dict((m[0], m[2]) for m in MODULES).get(a["module"], "#888")
    name = dict((m[0], m[1]) for m in MODULES).get(a["module"], a["module"])
    imgs = a.get("images") or []
    shots = "".join(f'<img src="{im}" alt="" class="{"on" if i==0 else ""}" loading="lazy">'
                    for i, im in enumerate(imgs))
    dots = "".join(f'<i class="{"on" if i==0 else ""}"></i>' for i in range(len(imgs))) if len(imgs) > 1 else ""
    nav = ('<button class="nav prev" aria-label="prev">&#8249;</button>'
           '<button class="nav next" aria-label="next">&#8250;</button>') if len(imgs) > 1 else ""
    bits = []
    if a.get("species"): bits.append(f'<span>{a["species"]} <span data-fr="espèces" data-en="species">species</span></span>')
    if a.get("models"):  bits.append(f'<span>{a["models"]} <span data-fr="modèles" data-en="models">models</span></span>')
    if a.get("leaves"):  bits.append(f'<span>{a["leaves"]} <span data-fr="feuillages" data-en="foliages">foliages</span></span>')
    for r in a.get("requires", []):
        bits.append(f'<span>+ {r}</span>')
    search = " ".join(str(a.get(k, "")) for k in ("name", "author", "description")).lower()
    return (f'<article class="card" style="--c:{col}" data-module="{a["module"]}" data-name="{esc(a["name"]).lower()}" '
            f'data-search="{esc(search)}" data-date="{a.get("updated","")}" data-dl="{a.get("downloads",0)}">'
            f'<div class="shot">{shots}<span class="mod">{name}</span>{nav}<div class="dots">{dots}</div></div>'
            f'<div class="body"><h2>{a["name"]}</h2>'
            f'<p class="by"><span data-fr="par" data-en="by">by</span> {a["author"]}</p>'
            f'<p class="desc">{a.get("description","")}</p>'
            f'<div class="meta">{"".join(bits)}</div>'
            f'<div class="foot"><a class="dl" href="{a["download"]}"{X} '
            f'data-fr="Télécharger" data-en="Download">Download</a>'
            f'<span class="ver">v{a.get("version",1)} · {a.get("updated","")}</span>'
            + (f'<span class="dls">{a["downloads"]} <span data-fr="téléchargements" data-en="downloads">downloads</span></span>'
               if a.get("downloads") is not None else "")
            + '</div>'
            f'</div></article>')

def build():
    data = load()
    dl = counts()
    for a in data:
        if "downloads" not in a:
            n = (a.get("download") or "").rsplit("/", 1)[-1]
            if n in dl:
                a["downloads"] = dl[n]
    opts = "".join(f'<option value="{m[0]}">{m[1]}</option>' for m in MODULES)
    cards = "\n".join(card(a) for a in data)

    empty = (f'<div class="empty" id="empty"><svg viewBox="-75 -75 150 150">{EMB}</svg>'
             f'<h2 data-fr="Rien encore, et c\'est une invitation" data-en="Nothing yet, and that is an invitation">'
             f'Nothing yet, and that is an invitation</h2>'
             f'<p data-fr="L\'atelier est livré avec le mod. On y sculpte une espèce entière, on règle son feuillage, '
             f'et on l\'envoie en un clic depuis le jeu." '
             f'data-en="The workshop ships with the mod. You sculpt a whole species there, tune its foliage, '
             f'and send it in one click from the game.">'
             f'The workshop ships with the mod. You sculpt a whole species there, tune its foliage, and send it in one click from the game.</p>'
             f'<p data-fr="La première création publiée ici sera la vôtre." '
             f'data-en="The first creation published here will be yours.">The first creation published here will be yours.</p>'
             f'<a class="cta" href="{DISCORD}"{X} data-fr="Rejoindre le Discord" data-en="Join the Discord">Join the Discord</a>'
             f'</div>')

    body = f"""<style>{CSS}</style>
<svg width="0" height="0" style="position:absolute"><defs><g id="emb">{EMB}</g></defs></svg>
<div class="top"><a class="back" href="../index.html"><svg viewBox="-64 -72 128 144"><use href="#emb"/></svg>
<span data-fr="Tous les modules" data-en="All modules">All modules</span></a>
<div class="r"><span class="langsw"><button class="lang on" data-lang="fr">FR</button><button class="lang" data-lang="en">EN</button></span>
<a href="{DISCORD}"{X}>Discord</a><a href="{KOFI}"{X}>Ko-fi</a><a class="pri" href="{CURSEFORGE}"{X}>CurseForge</a></div></div>

<section class="head"><div class="wrap">
  <h1 data-fr="Créations de la communauté" data-en="Community creations">Community creations</h1>
  <p data-fr="Ce que les joueurs ont façonné dans les ateliers de la suite, partagé et libre à installer. Chaque création reste la propriété de son auteur."
     data-en="What players have shaped in the suite's workshops, shared and free to install. Every creation remains the property of its author.">What players have shaped in the suite's workshops, shared and free to install. Every creation remains the property of its author.</p>
  <div class="install">
    <div><b data-fr="1. Télécharger" data-en="1. Download">1. Download</b><span data-fr="Récupérez l'archive de la création." data-en="Grab the creation's archive.">Grab the creation's archive.</span></div>
    <div><b data-fr="2. Déposer" data-en="2. Drop">2. Drop</b><span data-fr="Décompressez le dossier dans " data-en="Unzip the folder into ">Unzip the folder into </span><code>Tactile/Wood/Addons</code></div>
    <div><b data-fr="3. Actualiser" data-en="3. Refresh">3. Refresh</b><span data-fr="La création apparaît dans le panneau Add-ons." data-en="The creation shows up in the Add-ons panel.">The creation shows up in the Add-ons panel.</span></div>
  </div>
</div></section>

<div class="wrap">
  <div class="bar">
    <input id="q" type="search" placeholder="Rechercher" data-ph-fr="Rechercher une création, un auteur…" data-ph-en="Search a creation, an author…">
    <select id="mod"><option value="" data-fr="Tous les modules" data-en="All modules">All modules</option>{opts}</select>
    <select id="sort"><option value="date" data-fr="Plus récentes" data-en="Most recent">Most recent</option><option value="dl" data-fr="Plus téléchargées" data-en="Most downloaded">Most downloaded</option><option value="name" data-fr="Alphabétique" data-en="Alphabetical">Alphabetical</option></select>
    <span class="count" id="count"></span>
  </div>
  <div class="grid" id="grid">{cards}</div>
  {empty}
</div>

<div class="lb" id="lb"><button aria-label="close">&times;</button><img src="" alt=""></div>

<footer><div class="wrap"><div class="row">
<span data-fr="Tactile · suite de mods Minecraft" data-en="Tactile · a Minecraft mod suite">Tactile · a Minecraft mod suite</span>
<div class="links"><a href="{LIC}"{X} data-fr="© 2026 belerion · Tous droits réservés" data-en="© 2026 belerion · All rights reserved">© 2026 belerion · All rights reserved</a><a href="{GITHUB}"{X}>GitHub</a></div>
</div></div></footer>
{SCRIPT}"""
    return body

SCRIPT = """<script>
(function(){
  // ---- langue, partagée avec le reste du site
  function set(l){
    document.querySelectorAll('[data-fr]').forEach(function(e){var v=e.getAttribute('data-'+l);if(v!==null)e.textContent=v;});
    document.querySelectorAll('[data-ph-fr]').forEach(function(e){e.placeholder=e.getAttribute('data-ph-'+l);});
    document.documentElement.setAttribute('lang',l);
    try{localStorage.setItem('tactile_lang',l);}catch(e){}
    document.querySelectorAll('.lang').forEach(function(b){b.classList.toggle('on',b.getAttribute('data-lang')===l);});
  }
  var s='en';try{s=localStorage.getItem('tactile_lang')||'en';}catch(e){}
  document.querySelectorAll('.lang').forEach(function(b){b.addEventListener('click',function(){set(b.getAttribute('data-lang'));});});
  set(s);

  // ---- diaporama de chaque carte
  document.querySelectorAll('.shot').forEach(function(sh){
    var imgs=sh.querySelectorAll('img'), dots=sh.querySelectorAll('.dots i'), i=0;
    if(!imgs.length) return;
    function go(n){ imgs[i].classList.remove('on'); if(dots[i])dots[i].classList.remove('on');
      i=(n+imgs.length)%imgs.length; imgs[i].classList.add('on'); if(dots[i])dots[i].classList.add('on'); }
    var p=sh.querySelector('.prev'), n=sh.querySelector('.next');
    if(p) p.addEventListener('click',function(e){e.preventDefault();go(i-1);});
    if(n) n.addEventListener('click',function(e){e.preventDefault();go(i+1);});
    sh.addEventListener('click',function(e){ if(e.target.classList.contains('nav'))return;
      var lb=document.getElementById('lb'); lb.querySelector('img').src=imgs[i].src; lb.classList.add('on'); });
  });
  var lb=document.getElementById('lb');
  lb.addEventListener('click',function(){lb.classList.remove('on');});

  // ---- filtre, recherche, tri
  var grid=document.getElementById('grid'), q=document.getElementById('q'),
      mod=document.getElementById('mod'), sort=document.getElementById('sort'),
      count=document.getElementById('count'), empty=document.getElementById('empty');
  var all=[].slice.call(grid.children);

  var params=new URLSearchParams(location.search);
  if(params.get('module')) mod.value=params.get('module');

  function apply(){
    var t=(q.value||'').toLowerCase().trim(), m=mod.value, shown=0;
    all.forEach(function(c){
      var ok=(!m||c.dataset.module===m)&&(!t||c.dataset.search.indexOf(t)>=0);
      c.style.display=ok?'':'none'; if(ok)shown++;
    });
    var arr=all.slice().sort(function(a,b){
      if(sort.value==='name') return a.dataset.name.localeCompare(b.dataset.name);
      if(sort.value==='dl')   return (+b.dataset.dl||0)-(+a.dataset.dl||0);
      return (b.dataset.date||'').localeCompare(a.dataset.date||''); });
    arr.forEach(function(c){grid.appendChild(c);});
    count.textContent=shown+' / '+all.length;
    if(all.length===0){ count.textContent=''; }
    else { empty.style.display=shown?'none':'block'; }
  }
  if(all.length===0){ grid.style.display='none'; document.querySelector('.bar').style.display='none'; }
  else { empty.style.display='none'; [q,mod,sort].forEach(function(e){e.addEventListener('input',apply);}); apply(); }
})();
</script>"""

def wrap(inner, title_fr, title_en):
    i = inner.index("</style>") + len("</style>")
    head, rest = inner[:i], inner[i:]
    return ('<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            '<link rel="icon" type="image/png" href="../assets/favicon.png">\n'
            '<meta name="description" content="Species, biomes and worlds shaped by players in the Tactile workshops, free to download.">\n'
            '<meta property="og:type" content="website">\n'
            '<meta property="og:site_name" content="Tactile">\n'
            '<meta property="og:title" content="Community creations, Tactile">\n'
            '<meta property="og:description" content="Species, biomes and worlds shaped by players in the Tactile workshops, free to download.">\n'
            '<meta property="og:url" content="https://belerion63.github.io/Tactile/addons/">\n'
            '<meta property="og:image" content="https://belerion63.github.io/Tactile/assets/og.jpg">\n'
            '<meta name="twitter:card" content="summary_large_image">\n'
            f'<title data-fr="{title_fr}" data-en="{title_en}">{title_en}</title>\n'
            + head + "\n</head>\n<body>\n" + rest + "\n</body>\n</html>\n")

html = wrap(build(), "Créations de la communauté, Tactile", "Community creations, Tactile")

if DEMO:
    io.open(f"{PREV}/addons_demo.html", "w", encoding="utf-8").write(html)
    print("aperçu DEMO :", len(html)//1024, "Ko")
else:
    os.makedirs(f"{SITE}/addons", exist_ok=True)
    p = f"{SITE}/addons/addons.json"
    if not os.path.exists(p):
        io.open(p, "w", encoding="utf-8").write("[]\n")
    io.open(f"{SITE}/addons/index.html", "w", encoding="utf-8").write(html)
    print("website/addons/index.html :", len(html)//1024, "Ko,", len(load()), "création(s)")
