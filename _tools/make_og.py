# -*- coding: utf-8 -*-
"""Fabrique la carte de partage (og:image) en rendant la BANNIÈRE DU SITE en 1200x630.

On réutilise le vrai visuel et la vraie typographie plutôt que de redessiner :
la carte de partage est exactement ce que le visiteur verra en arrivant.
"""
import base64, os, subprocess, glob
from PIL import Image

SITE = "D:/Modding/Minecraft/Tactile/website"
TMP  = "D:/Modding/Minecraft/Tactile/website/_tools/preview"
os.makedirs(TMP, exist_ok=True)
EDGE = "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"

EMB = ('<g fill="none" stroke="#f4efe4" stroke-width="8" stroke-linecap="round" stroke-linejoin="round">'
       '<line x1="-46" y1="-52" x2="46" y2="-52"/><line x1="0" y1="-52" x2="0" y2="58"/></g>'
       '<g fill="#f4efe4"><circle cx="-46" cy="-52" r="9.5"/><circle cx="46" cy="-52" r="9.5"/>'
       '<circle cx="0" cy="58" r="9.5"/></g>'
       '<circle cx="0" cy="-52" r="12" fill="none" stroke="#d9a441" stroke-width="7"/>'
       '<circle cx="0" cy="-52" r="5" fill="#d9a441"/>')

bg = base64.b64encode(open(f"{SITE}/assets/img/banner.jpg", "rb").read()).decode()

HTML = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
*{{box-sizing:border-box;margin:0}}
body{{width:1200px;height:630px;overflow:hidden;
 font-family:"Segoe UI",system-ui,Arial,sans-serif;-webkit-font-smoothing:antialiased}}
.card{{position:relative;width:1200px;height:630px;overflow:hidden}}
.bg{{position:absolute;inset:0;background:url(data:image/jpeg;base64,{bg}) center/cover}}
.scrim{{position:absolute;inset:0;
 background:linear-gradient(90deg,rgba(10,7,3,.86) 0%,rgba(10,7,3,.55) 46%,rgba(10,7,3,.10) 82%)}}
.in{{position:absolute;left:0;right:0;top:50%;transform:translateY(-50%);padding:0 86px;color:#f4efe4}}
.wordmark{{display:flex;align-items:center;font-weight:200;text-transform:uppercase;
 font-size:96px;line-height:1}}
.lettert{{height:.84em;width:auto;margin-right:.14em;flex:0 0 auto}}
.wordmark span{{letter-spacing:.42em;padding-left:.42em;margin-left:-.16em}}
.tag{{margin-top:28px;color:#ded5c5;font-size:29px;line-height:1.5;max-width:24ch}}
.foot{{position:absolute;left:86px;bottom:52px;display:flex;gap:20px;font-size:19px;color:#bdb3a2;
 letter-spacing:.04em}}
.foot b{{color:#d9a441;font-weight:600}}
</style></head><body>
<div class="card">
  <div class="bg"></div><div class="scrim"></div>
  <div class="in">
    <h1 class="wordmark"><svg class="lettert" viewBox="-64 -72 128 144">{EMB}</svg><span>actile</span></h1>
    <p class="tag">Un monde transformé en profondeur. Le geste en est la note finale.</p>
  </div>
  <div class="foot"><span><b>3</b> mods jouables ou imminents</span><span><b>12</b> modules pensés</span></div>
</div></body></html>"""

src = f"{TMP}/og_card.html"
open(src, "w", encoding="utf-8").write(HTML)

png = f"{TMP}/og_card.png"
if os.path.exists(png):
    os.remove(png)
ud = f"{TMP}/edge_og"
subprocess.run([EDGE, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                f"--user-data-dir={ud}", "--window-size=1200,630",
                f"--screenshot={png}", f"file:///{src}"],
               capture_output=True, timeout=90)

im = Image.open(png).convert("RGB").resize((1200, 630), Image.LANCZOS)
out = f"{SITE}/assets/og.jpg"
im.save(out, "JPEG", quality=88, optimize=True, progressive=True)
print("og.jpg :", im.size, "%.0f Ko" % (os.path.getsize(out) / 1e3))
