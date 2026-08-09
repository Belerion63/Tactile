# -*- coding: utf-8 -*-
import re, os, io, base64
from PIL import Image
import re as _re
def en_first(h):
    """L'anglais devient la langue affichee par defaut (voir build_all)."""
    h=_re.sub(r'(data-fr="([^"]*)"\s+data-en="([^"]*)"([^>]*)>)([^<]*)(</)',
              lambda m: m.group(1)+m.group(3)+m.group(6), h)
    return h.replace('<html lang="fr">','<html lang="en">')

SVG = "D:/Modding/Minecraft/Tactile/Documentation/Logos/svg"
SRC = "D:/Modding/Minecraft/Tactile/website/_tools/src"
SITE = "D:/Modding/Minecraft/Tactile/website"
PREV = "D:/Modding/Minecraft/Tactile/website/_tools/preview"
os.makedirs(SITE+"/assets/img", exist_ok=True)
os.makedirs(PREV, exist_ok=True)

def raw(m):
    t = open(f"{SVG}/tactile-{m}.svg", encoding="utf-8").read().splitlines()
    return "\n".join(t[1:-1])
def white(s):
    s = re.sub(r"#[0-9a-fA-F]{6}", "#ffffff", s)
    s = re.sub(r'fill-opacity="[0-9.]+"', 'fill-opacity="0.42"', s)
    s = re.sub(r'stroke-width="([0-9.]+)"', lambda m: 'stroke-width="%.1f"' % (float(m.group(1))*1.55), s)
    return s
MODS = ["wood","ore","blocks","seasons","biome","weather","water","animals","monsters","farms","smith","fishing","combat","alchemy","enchantment"]
defs = "\n".join(f'<g id="i-{m}">{raw(m)}</g>' for m in MODS)
defs += "\n" + "\n".join(f'<g id="w-{m}">{white(raw(m))}</g>' for m in MODS)

URI = {}
def cover(src, w, h, cb=0.0):
    im = Image.open(src).convert("RGB")
    if cb: im = im.crop((0,0,im.width,int(im.height*(1-cb))))
    sr=w/h; ir=im.width/im.height
    if ir>sr:
        nw=int(im.height*sr); x=(im.width-nw)//2; im=im.crop((x,0,x+nw,im.height))
    else:
        nh=int(im.width/sr); y=(im.height-nh)//2; im=im.crop((0,y,im.width,y+nh))
    return im.resize((w,h), Image.LANCZOS)
def make(key, src, w, h, cb=0.0, q=80):
    # RÈGLE : une image déjà présente appartient à Jordan. On ne l'écrase JAMAIS.
    # (Le générateur ne sert qu'à amorcer les images manquantes.)
    dst=f"{SITE}/assets/img/{key}.jpg"
    im = cover(dst if os.path.exists(dst) else src, w, h, 0.0 if os.path.exists(dst) else cb)
    if not os.path.exists(dst):
        im.save(dst,"JPEG",quality=q)
    buf=io.BytesIO(); im.save(buf,"JPEG",quality=q)
    URI[key]="data:image/jpeg;base64,"+base64.b64encode(buf.getvalue()).decode()
make("banner", f"{SRC}/wood_a.jpg", 1600, 440)
make("feat-wood", f"{SRC}/wood_b.jpg", 760, 470)
make("feat-ore", f"{SRC}/ore.png", 760, 470, cb=0.10)
make("feat-blocks", f"{SRC}/blocks.png", 760, 470, cb=0.10)
make("trailer-wood", f"{SRC}/wood_c.jpg", 1280, 520)

D = {
 "blocks":("Blocks","#7d8794","live"),"ore":("Ore","#b83c4a","live"),"wood":("Wood","#4f9e3a","dev"),
 "seasons":("Season","#c8912f","vision"),"weather":("Weather","#5a90c4","vision"),"farms":("Farms","#c69a2b","vision"),
 "biome":("Biome","#7d8590","vision"),"animals":("Animals","#b4894f","vision"),"monsters":("Monsters","#9161bd","vision"),
 "fishing":("Fishing","#2fa79e","vision"),"smith":("Smith","#cf7a2f","vision"),"combat":("Combat","#7688aa","vision"),
 "water":("Water","#2f8fbd","vision"),
 "alchemy":("Alchemy","#a1508f","piste"),"enchantment":("Enchantment","#4b52a8","piste"),
}
REAL=["blocks","ore","wood"]
VISION=["seasons","weather","farms","biome","animals","monsters","fishing","smith","combat","water"]
PISTES=["alchemy","enchantment"]
BADGE={"live":("Disponible","Available"),"dev":("Bientôt","Soon")}

def feat(m):
    name,col,st=D[m]; bfr,ben=BADGE[st]
    return f'''<a class="feat" style="--c:{col}" href="{m}/index.html">
      <div class="feat-img" style="background-image:url(@@IMG:feat-{m}@@)"></div>
      <div class="feat-scrim"></div>
      <span class="feat-badge {st}" data-fr="{bfr}" data-en="{ben}">{bfr}</span>
      <div class="feat-foot">
        <svg class="feat-ic" viewBox="-75 -75 150 150"><use href="#w-{m}"/></svg>
        <span class="feat-name">Tactile<i>:</i>{name}</span>
        <span class="feat-go" data-fr="Découvrir →" data-en="Discover →">Découvrir →</span>
      </div>
    </a>'''
def vt(m,piste=False):
    name,col,st=D[m]
    cls="vt piste" if piste else "vt"
    return f'<a class="{cls}" style="--c:{col}" href="{m}/index.html"><svg viewBox="-75 -75 150 150"><use href="#w-{m}"/></svg><span>{name}</span></a>'
featured="\n".join(feat(m) for m in REAL)
visionwall="\n".join(vt(m) for m in VISION)
pisteswall="\n".join(vt(m,piste=True) for m in PISTES)

BASE="https://belerion63.github.io/Tactile"
DISCORD="https://discord.gg/WPdhCW4JdU"
CURSEFORGE="https://www.curseforge.com/members/belerion/projects"
KOFI="https://ko-fi.com/belerion"
GITHUB="https://github.com/Belerion63/Tactile"
X=' target="_blank" rel="noopener"'

EMBLEM='<g fill="none" stroke="#f4efe4" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"><line x1="-46" y1="-52" x2="46" y2="-52"/><line x1="0" y1="-52" x2="0" y2="58"/></g><g fill="#f4efe4"><circle cx="-46" cy="-52" r="9.5"/><circle cx="46" cy="-52" r="9.5"/><circle cx="0" cy="58" r="9.5"/></g><circle cx="0" cy="-52" r="12" fill="none" stroke="#d9a441" stroke-width="7"/><circle cx="0" cy="-52" r="5" fill="#d9a441"/>'

CSS = """
:root{--paper:#f2f1ec;--card:#fff;--ink:#191510;--ink2:#655e52;--line:#dcd7cd;--accent:#c07f1e;--dark:#171208}
*{box-sizing:border-box}
html{background:var(--paper);scroll-behavior:smooth}
body{margin:0;background:var(--paper);color:var(--ink);font-family:"Segoe UI",system-ui,-apple-system,Arial,sans-serif;-webkit-font-smoothing:antialiased}
a{color:inherit;text-decoration:none}
.wrap{max-width:1200px;margin:0 auto;padding:0 24px}
.top{display:flex;justify-content:flex-end;align-items:center;gap:10px;padding:16px 24px;max-width:1200px;margin:0 auto}
.top a{font-size:13px;color:var(--ink2);border:1px solid var(--line);border-radius:2px;padding:8px 15px}
.top a:hover{border-color:var(--ink);color:var(--ink)}
.top a.pri{background:var(--ink);color:var(--paper);border-color:var(--ink)}
.langsw{display:inline-flex;border:1px solid var(--line);border-radius:2px;overflow:hidden;margin-right:4px}
.langsw .lang{background:var(--card);border:none;color:var(--ink2);font-size:12px;font-weight:700;letter-spacing:.06em;padding:8px 11px;cursor:pointer}
.langsw .lang.on{background:var(--ink);color:var(--paper)}

.banner{position:relative;height:min(46vw,430px);min-height:280px;overflow:hidden;display:flex;align-items:center}
.banner .bg{position:absolute;inset:0;background:url(@@IMG:banner@@) center/cover;transform:scale(1.03)}
.banner .scrim{position:absolute;inset:0;background:linear-gradient(90deg,rgba(10,7,3,.82) 0%,rgba(10,7,3,.5) 42%,rgba(10,7,3,.05) 78%)}
.banner .in{position:relative;max-width:1200px;margin:0 auto;padding:0 44px;width:100%;color:#f4efe4}
.banner .wordmark{display:flex;align-items:center;margin:0;font-weight:200;text-transform:uppercase;font-size:clamp(34px,6.6vw,66px);line-height:1}
.banner .lettert{height:.84em;width:auto;margin-right:.14em;flex:0 0 auto}
.banner .wordmark span{letter-spacing:.42em;padding-left:.42em;margin-left:-.16em}
.banner p{margin:16px 0 0;color:#d7cfbf;font-size:clamp(15px,1.9vw,19px)}
.banner .bcta{display:inline-block;margin-top:22px;border:1px solid rgba(244,239,228,.6);color:#f4efe4;font-weight:600;font-size:15px;padding:12px 24px;border-radius:2px;transition:background .2s}
.banner .bcta:hover{background:rgba(244,239,228,.14)}
.banner .wm{position:absolute;right:26px;bottom:20px;display:flex;align-items:center;gap:9px;opacity:.42}
.banner .wm svg{width:19px;height:23px}
.banner .wm b{font-weight:300;letter-spacing:.3em;text-transform:uppercase;font-size:12px;color:#f4efe4}

.statusbar{display:flex;gap:28px;justify-content:center;flex-wrap:wrap;padding:15px;border-bottom:1px solid var(--line);background:#efece5;font-size:13px;color:var(--ink2)}
.statusbar>span{display:inline-flex;align-items:center;gap:8px}
.dot{width:9px;height:9px;border-radius:50%}
.dot.live{background:#4f9e3a}.dot.dev{background:var(--accent)}.dot.vis{background:#b9b3a6}

.sec{padding:52px 0}
.lab{display:flex;align-items:baseline;gap:14px;margin:0 0 20px}
.lab h2{font-size:14px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;margin:0;white-space:nowrap}
.lab .rule{height:1px;background:var(--line);flex:1;align-self:center}
.lab .n{font-size:13px;color:var(--ink2)}

.feats{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
@media(max-width:820px){.feats{grid-template-columns:1fr}}
.feat{position:relative;height:250px;border-radius:4px;overflow:hidden;display:block;border:1px solid var(--line)}
.feat-img{position:absolute;inset:0;background-size:cover;background-position:center;transition:transform .5s ease}
.feat:hover .feat-img{transform:scale(1.06)}
.feat-scrim{position:absolute;inset:0;background:linear-gradient(180deg,rgba(10,8,4,.05) 30%,color-mix(in srgb,var(--c) 55%,#0a0804) 100%)}
.feat-badge{position:absolute;top:14px;left:14px;font-size:10px;letter-spacing:.1em;text-transform:uppercase;font-weight:700;color:#fff;padding:4px 10px;border-radius:2px}
.feat-badge.live{background:#4f9e3a}.feat-badge.dev{background:var(--accent)}
.feat-foot{position:absolute;left:16px;right:16px;bottom:14px;display:flex;align-items:center;gap:12px;color:#fff}
.feat-ic{width:40px;height:40px;flex:0 0 auto;filter:drop-shadow(0 1px 3px rgba(0,0,0,.5))}
.feat-name{font-size:21px;font-weight:600}
.feat-name i{opacity:.6;font-style:normal;margin:0 1px}
.feat-go{margin-left:auto;font-size:13px;font-weight:600;opacity:0;transform:translateX(-6px);transition:.25s;white-space:nowrap}
.feat:hover .feat-go{opacity:.95;transform:none}

.vwall{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:12px}
.pistes-sec{padding-top:0}
.pistes-note{margin:-6px 0 20px;font-size:14.5px;color:var(--ink2);max-width:62ch}
.pwall{grid-template-columns:repeat(auto-fill,minmax(150px,1fr))}
.pwall>.vt{max-width:calc((1240px - 32px*2 - 12px*6)/7)}
.vt.piste{filter:saturate(.6) brightness(.98)}
.vt.piste::after{content:'';position:absolute;inset:5px;border:1.5px dashed rgba(255,255,255,.5);border-radius:3px;pointer-events:none}
.vt{position:relative;aspect-ratio:1/1;border-radius:4px;overflow:hidden;background:linear-gradient(155deg,var(--c),color-mix(in srgb,var(--c) 72%,#000));display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px;color:#fff;filter:saturate(.82);transition:transform .22s,filter .22s}
.vt:hover{transform:translateY(-4px);filter:saturate(1)}
.vt svg{width:46%;height:46%}
.vt span{font-size:13.5px;font-weight:600;letter-spacing:.02em}

.trailers{background:var(--dark)}
.tr-title{text-align:center;color:#cfc7b6;font-size:12px;letter-spacing:.2em;text-transform:uppercase;padding:22px 0 0}
.tr-stage{position:relative;height:min(42vw,440px);min-height:240px}
.tr-slide{position:absolute;inset:0;background-size:cover;background-position:center;display:flex;align-items:center;justify-content:center;flex-direction:column;gap:16px}
.tr-slide::after{content:"";position:absolute;inset:0;background:rgba(12,9,4,.42)}
.tr-play{position:relative;z-index:1;width:76px;height:76px;border-radius:50%;border:2px solid rgba(255,255,255,.85);background:rgba(0,0,0,.25);color:#fff;font-size:24px;cursor:pointer;display:flex;align-items:center;justify-content:center;padding-left:5px;transition:.2s}
.tr-play:hover{background:var(--accent);border-color:var(--accent)}
.tr-cap{position:relative;z-index:1;color:#f4efe4;font-size:15px;letter-spacing:.06em}
.tr-nav{position:absolute;top:50%;transform:translateY(-50%);z-index:2;width:44px;height:44px;border:none;background:rgba(0,0,0,.3);color:#fff;font-size:26px;cursor:pointer}
.tr-nav:hover{background:rgba(0,0,0,.55)}
.tr-prev{left:14px}.tr-next{right:14px}

footer{border-top:1px solid var(--line);padding:34px 0;font-size:13px;color:var(--ink2)}
footer .row{display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:16px}
footer .links{display:flex;gap:10px;flex-wrap:wrap}
footer .links a{border:1px solid var(--line);border-radius:2px;padding:8px 15px}
footer .links a:hover{border-color:var(--ink);color:var(--ink)}
footer .wip{font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--accent);border:1px dashed var(--line);border-radius:2px;padding:4px 12px}
@media(prefers-reduced-motion:reduce){*{transition:none!important}}
"""

TEMPLATE = """<title data-fr="Tactile, la vitrine" data-en="Tactile, the showcase">Tactile, la vitrine</title>
<style>@@CSS@@</style>
<svg width="0" height="0" style="position:absolute"><defs>@@DEFS@@</defs></svg>

<div class="top">
  <span class="langsw"><button class="lang on" data-lang="fr">FR</button><button class="lang" data-lang="en">EN</button></span>
  <a href="@@DISCORD@@" target="_blank" rel="noopener">Discord</a>
  <a href="@@KOFI@@" target="_blank" rel="noopener">Ko-fi</a>
  <a class="pri" href="@@CURSEFORGE@@" target="_blank" rel="noopener">CurseForge</a>
</div>

<section class="banner">
  <div class="bg"></div><div class="scrim"></div>
  <div class="in">
    <h1 class="wordmark"><svg class="lettert" viewBox="-64 -72 128 144">@@EMBLEM@@</svg><span>actile</span></h1>
    <p data-fr="Un monde transformé en profondeur. Le geste en est la note finale." data-en="A world transformed in depth. The gesture is its final note.">Un monde transformé en profondeur. Le geste en est la note finale.</p>
    <a class="bcta" href="addons/index.html" data-fr="Créations de la communauté" data-en="Community creations">Créations de la communauté</a>
  </div>
  <div class="wm"><svg viewBox="-64 -72 128 144">@@EMBLEM@@</svg><b>Tactile</b></div>
</section>

<div class="statusbar">
  <span><i class="dot live"></i><span data-fr="2 jouables" data-en="2 playable">2 jouables</span></span>
  <span><i class="dot dev"></i><span data-fr="1 en développement" data-en="1 in development">1 en développement</span></span>
  <span><i class="dot vis"></i><span data-fr="10 à venir" data-en="10 upcoming">10 à venir</span></span>
</div>

<section class="sec" id="feats"><div class="wrap">
  <div class="lab"><h2 data-fr="Jouables &amp; imminents" data-en="Playable &amp; imminent">Jouables &amp; imminents</h2><span class="rule"></span><span class="n" data-fr="les modules réels" data-en="the real modules">les modules réels</span></div>
  <div class="feats">@@FEATURED@@</div>
</div></section>

<!-- BANDEAU TRAILERS : reactiver quand une video existe
<section class="trailers">
  <div class="tr-title">Trailers</div>
  <div class="tr-stage">
    <div class="tr-slide" style="background-image:url(@@IMG:trailer-wood@@)">
      <button class="tr-play" aria-label="Play">&#9654;</button>
      <div class="tr-cap" data-fr="Tactile:Wood — premier trailer" data-en="Tactile:Wood — first trailer">Tactile:Wood — premier trailer</div>
    </div>
    <button class="tr-nav tr-prev" aria-label="Prev">&#8249;</button>
    <button class="tr-nav tr-next" aria-label="Next">&#8250;</button>
  </div>
</section>
-->

<section class="sec"><div class="wrap">
  <div class="lab"><h2 data-fr="La vision" data-en="The vision">La vision</h2><span class="rule"></span><span class="n" data-fr="dix modules à venir" data-en="ten upcoming modules">dix modules à venir</span></div>
  <div class="vwall">@@VISION@@</div>
</div></section>

<section class="sec pistes-sec"><div class="wrap">
  <div class="lab"><h2 data-fr="Pistes" data-en="Tracks">Pistes</h2><span class="rule"></span><span class="n" data-fr="explorées, pas décidées" data-en="explored, not decided">explorées, pas décidées</span></div>
  <p class="pistes-note" data-fr="Deux stations de Tactile:Blocks mériteraient un module à elles seules. Rien n'en est retiré à ce jour." data-en="Two Tactile:Blocks stations would deserve a module of their own. Nothing is being removed from it as of today.">Deux stations de Tactile:Blocks mériteraient un module à elles seules. Rien n'en est retiré à ce jour.</p>
  <div class="vwall pwall">@@PISTES@@</div>
</div></section>

<footer><div class="wrap"><div class="row">
  <span data-fr="Tactile · suite de mods Minecraft · treize modules et deux pistes" data-en="Tactile · a Minecraft mod suite · thirteen modules and two tracks">Tactile · suite de mods Minecraft · treize modules et deux pistes</span>
  <div class="links"><a href="@@LICENCE@@" target="_blank" rel="noopener" data-fr="© 2026 belerion · Tous droits réservés" data-en="© 2026 belerion · All rights reserved">© 2026 belerion · Tous droits réservés</a><a href="@@GITHUB@@" target="_blank" rel="noopener">GitHub</a></div>
</div></div></footer>

<script>
(function(){
  function set(l){
    document.querySelectorAll('[data-fr]').forEach(function(e){ var v=e.getAttribute('data-'+l); if(v!==null) e.textContent=v; });
    document.documentElement.setAttribute('lang', l);
    try{ localStorage.setItem('tactile_lang', l); }catch(e){}
    document.querySelectorAll('.lang').forEach(function(b){ b.classList.toggle('on', b.getAttribute('data-lang')===l); });
  }
  var saved='en'; try{ saved=localStorage.getItem('tactile_lang')||'en'; }catch(e){}
  document.querySelectorAll('.lang').forEach(function(b){ b.addEventListener('click',function(){ set(b.getAttribute('data-lang')); }); });
  set(saved);
})();
</script>"""

assembled = (TEMPLATE
  .replace("@@CSS@@", CSS).replace("@@DEFS@@", defs)
  .replace("@@EMBLEM@@", EMBLEM)
  .replace("@@DISCORD@@", DISCORD).replace("@@CURSEFORGE@@", CURSEFORGE).replace("@@GITHUB@@", GITHUB).replace("@@KOFI@@", KOFI).replace("@@LICENCE@@", "https://github.com/Belerion63/Tactile/blob/main/LICENSE")
  .replace("@@FEATURED@@", featured).replace("@@VISION@@", visionwall).replace("@@PISTES@@", pisteswall))

def resolve(html, fn):
    return re.sub(r"@@IMG:([a-z\-]+)@@", lambda m: fn(m.group(1)), html)
html_prev = resolve(assembled, lambda k: URI[k])
html_site = resolve(assembled, lambda k: f"assets/img/{k}.jpg")

open(PREV+"/landing4.html","w",encoding="utf-8").write(en_first(html_prev))
idx = html_site.index("</style>")+len("</style>")
head, body = html_site[:idx], html_site[idx:]
standalone=('<!DOCTYPE html>\n<html lang="fr">\n<head>\n<meta charset="utf-8">\n'
 '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
 '<meta name="description" content="Le minerai, les arbres, le climat, la faune : une suite de mods qui refond le monde de Minecraft en profondeur, jusqu\'au geste.">\n'
 # Carte de partage : ce que Discord, Reddit ou Twitter affichent quand on colle le lien.
 '<meta property="og:type" content="website">\n'
 '<meta property="og:site_name" content="Tactile">\n'
 '<meta property="og:title" content="Tactile, suite de mods Minecraft">\n'
 '<meta property="og:description" content="Ore, trees, climate, wildlife: a suite of Minecraft mods that reworks the world in depth, down to the gesture.">\n'
 f'<meta property="og:url" content="{BASE}/">\n'
 f'<meta property="og:image" content="{BASE}/assets/og.jpg">\n'
 '<meta property="og:image:width" content="1200">\n'
 '<meta property="og:image:height" content="630">\n'
 '<meta name="twitter:card" content="summary_large_image">\n'
 '<link rel="icon" type="image/png" href="assets/favicon.png">\n'+head+"\n</head>\n<body>\n"+body+"\n</body>\n</html>\n")
open(SITE+"/index.html","w",encoding="utf-8").write(en_first(standalone))
print("OK — apercu %d Ko + website/index.html %d Ko" % (len(html_prev)//1024, len(standalone)//1024))
