# -*- coding: utf-8 -*-
"""Les bords du site : page d'erreur, plan de site, robots.

    python build_meta.py

Écrit 404.html, sitemap.xml et robots.txt à la racine. Le plan de site est
construit en parcourant les pages réellement présentes : il ne peut pas
mentir sur ce qui existe.
"""
import io, os, re, time

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://belerion63.github.io/Tactile"
DISCORD = "https://discord.com/invite/WPdhCW4JdU"
CURSEFORGE = "https://www.curseforge.com/members/belerion/projects"

# Les robots d'entraînement des IA. Les autoriser, c'est accepter que ton texte
# nourrisse des modèles ; les bloquer, c'est risquer que les assistants ignorent
# l'existence de tes mods quand on leur demande « quel mod fait ceci ».
# Aucun de ces jetons n'influence le classement dans la recherche Google :
# Google-Extended ne concerne QUE l'entraînement de Gemini.
AI_BOTS = ["Google-Extended", "GPTBot", "OAI-SearchBot", "ClaudeBot", "anthropic-ai",
           "PerplexityBot", "CCBot", "Applebot-Extended", "Bytespider", "meta-externalagent"]
ALLOW_AI = True   # passer à False pour les bloquer tous


def pages():
    out = []
    for root, dirs, files in os.walk(SITE):
        dirs[:] = [d for d in dirs if d not in (".git", "_tools", "img", "assets")]
        for f in files:
            if f.endswith(".html") and f != "404.html":
                rel = os.path.relpath(os.path.join(root, f), SITE).replace("\\", "/")
                out.append(rel)
    return sorted(out)


def sitemap(ps):
    now = time.strftime("%Y-%m-%d")
    urls = []
    for p in ps:
        loc = f"{BASE}/" + (p[:-len("index.html")] if p.endswith("index.html") else p)
        prio = "1.0" if p == "index.html" else ("0.8" if p.count("/") <= 1 else "0.6")
        urls.append(f"  <url><loc>{loc}</loc><lastmod>{now}</lastmod><priority>{prio}</priority></url>")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + "\n".join(urls) + "\n</urlset>\n")


def robots():
    lines = ["# Tactile", "User-agent: *", "Allow: /", "Disallow: /_tools/", ""]
    lines.append("# Robots d'entraînement des IA" if ALLOW_AI else "# Robots d'entraînement des IA : refusés")
    for b in AI_BOTS:
        lines += [f"User-agent: {b}", "Allow: /" if ALLOW_AI else "Disallow: /", ""]
    lines.append(f"Sitemap: {BASE}/sitemap.xml")
    return "\n".join(lines) + "\n"


CSS404 = """
:root{--paper:#f2f1ec;--card:#fff;--ink:#191510;--ink2:#5f594e;--line:#dcd7cd;--accent:#c07f1e}
*{box-sizing:border-box}html,body{height:100%}
body{margin:0;background:var(--paper);color:var(--ink);font-family:"Segoe UI",system-ui,-apple-system,Arial,sans-serif;
 display:flex;align-items:center;justify-content:center;line-height:1.6;padding:32px}
a{color:inherit;text-decoration:none}
.box{max-width:620px;text-align:center}
.box svg{width:70px;height:70px;opacity:.32}
.box h1{margin:22px 0 0;font-size:clamp(30px,5vw,46px);font-weight:700;letter-spacing:-.02em}
.box p{margin:16px 0 0;font-size:17px;color:var(--ink2)}
.links{display:flex;gap:12px;justify-content:center;flex-wrap:wrap;margin-top:30px}
.links a{border:1px solid var(--line);border-radius:2px;padding:12px 22px;font-size:15px;background:var(--card)}
.links a:hover{border-color:var(--ink)}
.links a.pri{background:var(--ink);color:var(--paper);border-color:var(--ink)}
.links a.pri:hover{background:var(--accent)}
"""

EMB = ('<g fill="none" stroke="#191510" stroke-width="8" stroke-linecap="round" stroke-linejoin="round">'
       '<line x1="-46" y1="-52" x2="46" y2="-52"/><line x1="0" y1="-52" x2="0" y2="58"/></g>'
       '<g fill="#191510"><circle cx="-46" cy="-52" r="9.5"/><circle cx="46" cy="-52" r="9.5"/>'
       '<circle cx="0" cy="58" r="9.5"/></g>'
       '<circle cx="0" cy="-52" r="12" fill="none" stroke="#c07f1e" stroke-width="7"/>'
       '<circle cx="0" cy="-52" r="5" fill="#c07f1e"/>')


def page404():
    # Chemins ABSOLUS : cette page s'affiche depuis n'importe quelle profondeur.
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<link rel="icon" type="image/png" href="/Tactile/assets/favicon.png">
<title>Page not found, Tactile</title>
<style>{CSS404}</style>
</head>
<body>
<div class="box">
  <svg viewBox="-64 -72 128 144">{EMB}</svg>
  <h1 data-fr="Cette page n'existe pas" data-en="This page does not exist">This page does not exist</h1>
  <p data-fr="Le lien est peut-être ancien, ou l'adresse mal recopiée. Le reste du site est intact."
     data-en="The link may be old, or the address mistyped. The rest of the site is fine.">The link may be old, or the address mistyped. The rest of the site is fine.</p>
  <div class="links">
    <a class="pri" href="/Tactile/" data-fr="Retour à l'accueil" data-en="Back to the homepage">Back to the homepage</a>
    <a href="/Tactile/wood/index.html">Tactile:Wood</a>
    <a href="/Tactile/ore/index.html">Tactile:Ore</a>
    <a href="/Tactile/blocks/index.html">Tactile:Blocks</a>
    <a href="{DISCORD}" target="_blank" rel="noopener">Discord</a>
  </div>
</div>
<script>(function(){{var l='en';try{{l=localStorage.getItem('tactile_lang')||'en';}}catch(e){{}}
document.querySelectorAll('[data-fr]').forEach(function(e){{var v=e.getAttribute('data-'+l);if(v!==null)e.textContent=v;}});
document.documentElement.setAttribute('lang',l);}})();</script>
</body>
</html>
"""


def main():
    ps = pages()
    io.open(os.path.join(SITE, "sitemap.xml"), "w", encoding="utf-8").write(sitemap(ps))
    io.open(os.path.join(SITE, "robots.txt"), "w", encoding="utf-8").write(robots())
    io.open(os.path.join(SITE, "404.html"), "w", encoding="utf-8").write(page404())
    print(f"sitemap.xml : {len(ps)} pages")
    print(f"robots.txt  : IA {'autorisées' if ALLOW_AI else 'bloquées'} ({len(AI_BOTS)} robots déclarés)")
    print("404.html    : écrite")


if __name__ == "__main__":
    main()
