# -*- coding: utf-8 -*-
"""Publie une création reçue dans la galerie du site.

Prend l'archive envoyée par un auteur, en lit les métadonnées, prépare les
images et écrit l'entrée dans addons/addons.json. Une mise à jour remplace
l'entrée existante au lieu d'en créer une seconde.

    python publish_addon.py <archive.zip | dossier> --images <dossier|fichiers…>

Tout ce qui manque est demandé à l'écran. Ce qui peut être lu dans pack.json
n'est jamais redemandé : nom d'auteur, version, nombre d'espèces, de modèles,
de feuillages, mods requis.

Options utiles :
    --name "Conifères du Nord"    nom affiché (par défaut : celui du dossier)
    --desc "…"                    description affichée
    --download "https://…"        lien de l'archive (Release GitHub)
    --module wood                 module concerné (défaut : wood)
    --dry                         montre ce qui serait écrit, sans rien écrire
"""
import argparse, io, json, os, re, shutil, sys, zipfile
from datetime import date

try:
    from PIL import Image
except ImportError:
    sys.exit("Pillow est nécessaire :  pip install pillow")

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ADDONS = os.path.join(SITE, "addons")
IMGDIR = os.path.join(ADDONS, "img")
DB = os.path.join(ADDONS, "addons.json")

IMG_W, IMG_H, IMG_Q, IMG_MAX = 1280, 720, 82, 6


def slug(s):
    s = re.sub(r"[^a-z0-9]+", "-", (s or "").lower()).strip("-")
    return s or "creation"


def read_pack(src):
    """Lit pack.json, que la source soit une archive ou un dossier."""
    if os.path.isdir(src):
        p = os.path.join(src, "pack.json")
        if not os.path.exists(p):
            sys.exit(f"pack.json introuvable dans {src}")
        return json.loads(io.open(p, encoding="utf-8").read())
    with zipfile.ZipFile(src) as z:
        names = [n for n in z.namelist() if n.endswith("pack.json")]
        if not names:
            sys.exit("pack.json introuvable dans l'archive")
        # le moins profond : celui du pack, pas celui d'un sous-dossier
        names.sort(key=lambda n: n.count("/"))
        return json.loads(z.read(names[0]).decode("utf-8"))


def gather_images(args_images):
    out = []
    for a in args_images:
        if os.path.isdir(a):
            out += [os.path.join(a, f) for f in sorted(os.listdir(a))
                    if f.lower().endswith((".png", ".jpg", ".jpeg", ".webp"))]
        elif os.path.exists(a):
            out.append(a)
    return out[:IMG_MAX]


def cover(im, w, h):
    sr, ir = w / h, im.width / im.height
    if ir > sr:
        nw = int(im.height * sr); x = (im.width - nw) // 2
        im = im.crop((x, 0, x + nw, im.height))
    else:
        nh = int(im.width / sr); y = (im.height - nh) // 2
        im = im.crop((0, y, im.width, y + nh))
    return im.resize((w, h), Image.LANCZOS)


def ask(label, default=""):
    v = input(f"{label}{f' [{default}]' if default else ''} : ").strip()
    return v or default


def main():
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("source", help="archive .zip ou dossier du pack")
    ap.add_argument("--images", nargs="*", default=[])
    ap.add_argument("--name"); ap.add_argument("--desc")
    ap.add_argument("--download"); ap.add_argument("--module", default="wood")
    ap.add_argument("--dry", action="store_true")
    a = ap.parse_args()

    if not os.path.exists(a.source):
        sys.exit(f"introuvable : {a.source}")

    pack = read_pack(a.source)
    folder = os.path.basename(os.path.abspath(a.source)).replace(".zip", "")

    name = a.name or ask("Nom affiché", folder)
    author = pack.get("author") or ask("Auteur")
    desc = a.desc or ask("Description")
    dl = a.download or ask("Lien de l'archive (Release GitHub)")

    # L'identité : celle du pack si elle existe, sinon dérivée du nom et de l'auteur.
    ident = pack.get("id") or f"{slug(author)}-{slug(name)}"
    if not pack.get("id"):
        print("  ! ce pack n'a pas d'identifiant : identité dérivée du nom et de l'auteur.")
        print("    une mise à jour ne sera reconnue que si les deux restent identiques.")

    db = json.loads(io.open(DB, encoding="utf-8").read()) if os.path.exists(DB) else []
    old = next((e for e in db if e.get("id") == ident), None)

    # Images : recadrées en 16:9 et réencodées pour le web.
    imgs, srcs = [], gather_images(a.images)
    if not srcs and not old:
        print("  ! aucune image : la carte s'affichera sans diaporama.")
    for i, s in enumerate(srcs, 1):
        rel = f"img/{slug(name)}-{i}.jpg"
        if not a.dry:
            os.makedirs(IMGDIR, exist_ok=True)
            im = cover(Image.open(s).convert("RGB"), IMG_W, IMG_H)
            im.save(os.path.join(ADDONS, rel), "JPEG", quality=IMG_Q, optimize=True, progressive=True)
        imgs.append(rel)
    if not imgs and old:
        imgs = old.get("images", [])

    entry = {
        "id": ident,
        "module": a.module,
        "name": name,
        "author": author,
        "description": desc,
        "version": pack.get("version", 1),
        "updated": date.today().isoformat(),
        "format_version": pack.get("format_version"),
        "species": pack.get("species"), "models": pack.get("models"), "leaves": pack.get("leaves"),
        "requires": pack.get("requires", []),
        "images": imgs,
        "download": dl,
    }
    entry = {k: v for k, v in entry.items() if v not in (None, [], "")}

    if old:
        print(f"\n  MISE À JOUR de « {old['name'] }» : v{old.get('version','?')} -> v{entry['version']}")
        db[db.index(old)] = entry
    else:
        print(f"\n  NOUVELLE CRÉATION : « {name} » de {author}")
        db.append(entry)

    print(json.dumps(entry, ensure_ascii=False, indent=1))
    if a.dry:
        print("\n  --dry : rien n'a été écrit.")
        return
    io.open(DB, "w", encoding="utf-8").write(json.dumps(db, ensure_ascii=False, indent=1) + "\n")
    print(f"\n  écrit dans addons/addons.json ({len(db)} création(s))")
    print("  reste à faire :  python build_addons.py")


if __name__ == "__main__":
    main()
