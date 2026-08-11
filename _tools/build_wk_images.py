# -*- coding: utf-8 -*-
"""Prépare pour le web les captures du guide d'atelier.

    python build_wk_images.py

Lit les captures là où elles sont prises (Documentation/Tutoriel/Images pour les
numérotées, Documentation/ pour celles qu'Obsidian a nommées « Pasted image … »)
et écrit website/wood/img/wk/. Les originaux ne sont jamais touchés.

Deux formats, choisis par l'image et non par principe : un panneau d'interface
tient dans quelques centaines de couleurs, et le JPEG bave autour de son texte ;
une vue 3D en compte des milliers, et une palette de 256 y ferait des bandes
dans le feuillage. Le compte de couleurs de l'ORIGINAL tranche.

La table WK de guide_wood.py doit refléter le résultat : ce script l'imprime en
fin de course, prête à recopier.
"""
import json
import os

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.path.join(ROOT, "Documentation", "Tutoriel", "Images")
DOC = os.path.join(ROOT, "Documentation")
OUT = os.path.join(ROOT, "website", "wood", "img", "wk")

# Les captures collées gardent leur horodatage pour nom de fichier : on les renomme
# une fois ici, pour que le guide cite « pub-menu » et non un nombre de quatorze chiffres.
PASTED = {
    "20260811134056": "pub-menu",
    "20260811134508": "pub-site",
    "20260811174058": "handles",
    "20260811175249": "fruits",
    "20260811184122": "bloom",
    "20260811184545": "flower-tex",
}

MAX_W = 1500      # la colonne de texte fait 900 px : au-delà on paie des octets pour rien
UI_COLOURS = 400  # au-dessus, ce n'est plus un panneau mais une image de jeu


def main():
    os.makedirs(OUT, exist_ok=True)
    jobs = [(os.path.join(SRC, "%d.png" % i), str(i)) for i in range(1, 25)]
    jobs += [(os.path.join(DOC, "Pasted image %s.png" % k), v) for k, v in PASTED.items()]

    kept, total = {}, 0
    for path, name in jobs:
        if not os.path.isfile(path):
            print("MANQUE :", path)
            continue
        orig = Image.open(path).convert("RGB")
        ui = len(orig.getcolors(maxcolors=UI_COLOURS) or []) > 0
        im = orig
        if orig.width > MAX_W:
            im = orig.resize((MAX_W, round(orig.height * MAX_W / orig.width)), Image.LANCZOS)
        if ui:
            f = os.path.join(OUT, name + ".png")
            im.convert("P", palette=Image.ADAPTIVE, colors=256).save(f, "PNG", optimize=True)
            kept[name] = "png"
        else:
            f = os.path.join(OUT, name + ".jpg")
            im.save(f, "JPEG", quality=85, optimize=True, progressive=True)
            kept[name] = "jpg"
        # L'AUTRE FORMAT EST EFFACÉ : une capture qui change de nature d'un passage à l'autre
        # laisserait derrière elle un fichier orphelin que le site continuerait de servir.
        other = os.path.join(OUT, name + (".jpg" if kept[name] == "png" else ".png"))
        if os.path.isfile(other):
            os.remove(other)
        total += os.path.getsize(f)
        print("%-11s %-3s %5d Ko" % (name, kept[name], os.path.getsize(f) // 1024))

    print("\n%d images, %d Ko" % (len(kept), total // 1024))
    print("\nWK = " + json.dumps(kept, indent=1).replace('"', '"'))


if __name__ == "__main__":
    main()
