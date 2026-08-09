# -*- coding: utf-8 -*-
"""Réencode pour le web les images du site trop lourdes.
Les originaux sont copiés dans Documentation/site-originaux/ avant toute écriture."""
import os, glob, shutil
from PIL import Image

SITE = "D:/Modding/Minecraft/Tactile/website"
BK   = "D:/Modding/Minecraft/Tactile/Documentation/site-originaux"
LIMIT = 400_000

os.makedirs(BK, exist_ok=True)
os.chdir(SITE)

def target_w(path):
    b = os.path.basename(path).split('.')[0]
    if b == "hero":        return 1800   # bandeau pleine largeur
    if b.startswith("g"):  return 1300   # galerie, 2 colonnes
    return 1500                          # rangées de features

total_before = total_after = 0
for f in sorted(glob.glob("*/img/*.jpg")) + sorted(glob.glob("assets/img/*.jpg")):
    f = f.replace("\\", "/")
    s = os.path.getsize(f)
    total_before += s
    if s <= LIMIT:
        total_after += s
        continue
    shutil.copy2(f, os.path.join(BK, f.replace("/", "__")))
    im = Image.open(f).convert("RGB")
    w = target_w(f)
    if im.width > w:
        im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    im.save(f, "JPEG", quality=82, optimize=True, progressive=True)
    a = os.path.getsize(f)
    total_after += a
    print("%-20s %7.2f Mo -> %6.0f Ko  (%d px)" % (f, s / 1e6, a / 1e3, im.width))

print("TOTAL SITE : %.1f Mo -> %.1f Mo" % (total_before / 1e6, total_after / 1e6))
