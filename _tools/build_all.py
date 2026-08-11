# -*- coding: utf-8 -*-
import re, os, io, base64
from PIL import Image
from concepts import CONC, FIGS
SVG="D:/Modding/Minecraft/Tactile/Documentation/Logos/svg"
# Images d'origine : utiles seulement pour AMORCER une image absente du site.
SRC="D:/Modding/Minecraft/Tactile/website/_tools/src"
SITE="D:/Modding/Minecraft/Tactile/website"
WSH="D:/Modding/Minecraft/Tactile/tactile-wood 26.1/run/screenshots"
PREV="D:/Modding/Minecraft/Tactile/website/_tools/preview"
os.makedirs(PREV, exist_ok=True)
os.makedirs(SITE+"/assets/img",exist_ok=True)

def raw(m):
    t=open(f"{SVG}/tactile-{m}.svg",encoding="utf-8").read().splitlines(); return "\n".join(t[1:-1])
def white(s):
    s=re.sub(r"#[0-9a-fA-F]{6}","#ffffff",s)
    s=re.sub(r'fill-opacity="[0-9.]+"','fill-opacity="0.42"',s)
    s=re.sub(r'stroke-width="([0-9.]+)"',lambda m:'stroke-width="%.1f"'%(float(m.group(1))*1.55),s); return s
URI={}
def cover(src,w,h,cb=0.0,ct=0.0):
    im=Image.open(src).convert("RGB")
    if ct: im=im.crop((0,int(im.height*ct),im.width,im.height))
    if cb: im=im.crop((0,0,im.width,int(im.height*(1-cb))))
    sr=w/h; ir=im.width/im.height
    if ir>sr:
        nw=int(im.height*sr); x=(im.width-nw)//2; im=im.crop((x,0,x+nw,im.height))
    else:
        nh=int(im.width/sr); y=(im.height-nh)//2; im=im.crop((0,y,im.width,y+nh))
    return im.resize((w,h),Image.LANCZOS)
def keep(m,key,w,h,q=80,fit=False):
    """Image fournie par Jordan : on ne réécrit PAS le fichier du site.
    On n'en fabrique qu'une version allégée en mémoire, pour l'aperçu artifact.
    fit=True : image montrée entière (pas de recadrage)."""
    p=f"{SITE}/{m}/img/{key}.jpg"
    if fit:
        im=Image.open(p).convert("RGB"); im.thumbnail((w,h),Image.LANCZOS)
    else:
        im=cover(p,w,h)
    b=io.BytesIO(); im.save(b,"JPEG",quality=q)
    URI[key]="data:image/jpeg;base64,"+base64.b64encode(b.getvalue()).decode()

def make(m,key,src,w,h,cb=0.0,ct=0.0,q=80):
    os.makedirs(f"{SITE}/{m}/img",exist_ok=True)
    # RÈGLE : une image déjà présente appartient à Jordan. On ne l'écrase JAMAIS.
    # (Le générateur ne sert qu'à amorcer les images manquantes.)
    if os.path.exists(f"{SITE}/{m}/img/{key}.jpg"):
        keep(m,key,w,h,q); return
    im=cover(src,w,h,cb,ct); im.save(f"{SITE}/{m}/img/{key}.jpg","JPEG",quality=q)
    b=io.BytesIO(); im.save(b,"JPEG",quality=q); URI[key]="data:image/jpeg;base64,"+base64.b64encode(b.getvalue()).decode()

BASE="https://belerion63.github.io/Tactile"
DISCORD="https://discord.com/invite/WPdhCW4JdU"
CURSEFORGE="https://www.curseforge.com/members/belerion/projects"
KOFI="https://ko-fi.com/belerion"
GITHUB="https://github.com/Belerion63/Tactile"
X=' target="_blank" rel="noopener"'

SP=[("Chargeur","Loader","NeoForge 26.1","NeoForge 26.1"),("Version","Version","Minecraft 26.1","Minecraft 26.1"),("Côté","Side","Client + serveur","Client + server")]
def spU(fr,en): return SP+[("Désinstallation","Uninstall",fr,en)]

M={
 "blocks":{"t":"full","name":"Blocks","c":"#7d8794","st":("Disponible","Available"),
   "pitch":("Les stations à interface deviennent des gestes : four, enclume, alambic, table d'enchantement — sans jamais ouvrir de menu.",
            "Interface stations become gestures — furnace, anvil, brewing stand, enchanting table — without ever opening a menu."),
   "hero":(f"{SRC}/blocks_hero.png",0.10,0.0),
   "features":[
     (f"{SRC}/blocks_1.png",("Poser, pas cliquer","Place, don't click"),("On dépose les objets directement sur la station, et le travail se déroule dans le monde, à vue.","You drop items straight onto the station, and the work unfolds in the world, in plain sight.")),
     (f"{SRC}/blocks_2.png",("Chaque station, son geste","Each station, its gesture"),("Le four cuit ce qu'on y pose, l'enclume répare au marteau, l'alambic distille sous tes yeux.","The furnace cooks what you place, the anvil repairs by hammer, the still distills before your eyes.")),
     (f"{SRC}/blocks_3.png",("Rien de neuf sous le capot","Nothing new under the hood"),("Ce sont les recettes vanilla qui pilotent tout : compatibilité totale, zéro interface.","Vanilla recipes drive everything — full compatibility, zero interface.")),
   ],
   "spec":spU("Propre, sans perte","Clean, no loss"),
   "deep":{"how":("Comment ça marche","How it works",
     ["Chaque station est rendue et manipulée dans le monde ; l'écran de la GUI vanilla est remplacé par des emplacements physiques.","Les recettes d'origine tournent en arrière-plan, sans interface : ce que tu poses détermine ce qui sort."],
     ["Each station is rendered and handled in the world; the vanilla GUI screen is replaced by physical slots.","The original recipes run in the background, screenless: what you place determines what comes out."]),
     "commands":[],
     "modding":("Compatibilité","Compatibility",
     ["Toute recette, vanilla ou moddée, fonctionne telle quelle — aucune liste à écrire."],
     ["Any recipe, vanilla or modded, works as-is — no list to maintain."])}},
 "wood":{"t":"full","name":"Wood","c":"#4f9e3a","st":("Bientôt","Soon"),
   "pitch":("Chaque arbre est façonné procéduralement, unique. L'abattre est un vrai geste.","Every tree is procedurally shaped, unique. Felling it is a real gesture."),
   "hero":(f"{SRC}/wood_hero.jpg",0.0,0.0),
   "features":[
     (f"{SRC}/wood_1.jpg",("Aucun arbre pareil","No two trees alike"),("Forme, inclinaison, couleurs : tout est dérivé de l'arbre lui-même. Vanilla comme moddé.","Shape, lean, colors — all derived from the tree itself. Vanilla or modded.")),
     (f"{WSH}/2026-08-06_23.54.15.png",("Un feuillage qui a du volume","Foliage with volume"),("Les feuilles ne sont plus un damier de cubes, mais des touffes de plans habillées de textures dérivées du jeu, avec leurs propres ombres.","Leaves are no longer a grid of cubes, but tufts of planes dressed in textures derived from the game, with shadows of their own.")),
     (f"{SRC}/wood_2.jpg",("L'abattage est un geste","Felling is a gesture"),("La hache mord, la cime bascule, on débite les bûches au sol, une par une.","The axe bites, the crown topples, you cut the logs on the ground, one by one.")),
     (f"{WSH}/2026-08-07_00.07.02.png",("Des forêts, pas des arbres alignés","Forests, not rows of trees"),("Chaque arbre étant façonné à part, une forêt cesse d'être un motif répété. Les silhouettes se répondent, se croisent et se recouvrent.","Since each tree is shaped on its own, a forest stops being a repeated pattern. The silhouettes answer, cross and overlap one another.")),
     (f"{SRC}/wood_3.jpg",("Beau, et réversible","Beautiful, and reversible"),("Le rendu se fait côté client, sur des blocs vanilla : le monde peut retrouver sa forme d'origine à tout moment.","Rendering is client-side, over vanilla blocks: the world can return to its original shape at any time.")),
   ],
   "addons":True,
   "guide":True,
   "gallery":{
     "t":("L'éditeur d'espèces","The species editor"),
     "lead":("Les règles de forme ne restent pas dans le code. Un atelier en jeu permet de sculpter une espèce entière, de régler son feuillage, et de composer sa propre bibliothèque d'arbres.",
             "The shape rules do not stay in the code. An in-game workshop lets you sculpt a whole species, tune its foliage, and build your own library of trees."),
     "shots":[
       (None,
        "La forme d'abord. On pose le squelette, le tronc puis les branches, en réglant leurs règles de départ, de longueur, d'effilement et de tortuosité.",
        "Shape first. The skeleton is laid down, trunk then branches, by tuning their rules for starts, length, taper and gnarl."),
       (None,
        "Vient ensuite la masse du feuillage : densité, creux de la couronne, irrégularité, dégradé. Les touffes, la lumière et les ombres portées se règlent au même endroit.",
        "Then comes the foliage mass: density, canopy hollow, irregularity, gradient. Tufts, light and cast shadows are tuned in the same place."),
       (None,
        "La feuille et la fleur se dessinent élément par élément, à partir d'une texture du jeu : répétition, teinte, motif, finition.",
        "The leaf and the flower are drawn element by element, from one of the game's textures: repetition, hue, pattern, finish."),
       (None,
        "L'espèce obtenue est enregistrée, et les arbres sauvages la rejouent ensuite, chacun avec sa propre variation.",
        "The resulting species is saved, and wild trees then replay it, each with its own variation.", "fit"),
     ]},
   "keep":{"1","3","4","g1","g2","g3","g4"},
   "deep":[
     ("Comment ça marche","How it works",[
       ("Le mod ne devine pas les arbres : il les identifie par un marquage fiable, vanilla comme moddés, sans faux positif.","The mod doesn't guess trees: it identifies them by a reliable tag, vanilla or modded, with no false positives."),
       ("À partir des blocs qui le composent, il reconstruit la hiérarchie de l'arbre : le tronc, puis les branches qu'il porte.","From the blocks that make it up, it rebuilds the tree's hierarchy: the trunk, then the branches it carries."),
       ("Chaque segment est alors redessiné en volume, à partir de boîtes (box shapes) pour le bois et de touffes pour le feuillage. Forme, inclinaison et teintes dérivent de l'arbre lui-même, si bien que deux arbres ne se ressemblent jamais.","Each segment is then redrawn as volume, from box shapes for the wood and tufts for the foliage. Shape, lean and hues derive from the tree itself, so no two trees ever look alike."),
       ("Tout se joue côté client, sur des blocs vanilla : les bûches et les feuilles restent standard, seul l'affichage change. Le serveur ne voit que du vanilla, ce qui garde le rendu réversible et sans incidence sur le reste.","It all happens client-side, over vanilla blocks: logs and leaves stay standard, only the display changes. The server sees only vanilla, which keeps the rendering reversible and harmless to the rest."),
     ]),
     ("Le feuillage","The foliage",[
       ("Le feuillage n'est plus un cube texturé, mais une touffe de plans, habillée de textures procédurales calquées directement sur les feuilles vanilla. Il s'applique à tout le jeu, feuilles vanilla comprises.","Foliage is no longer a textured cube, but a tuft of planes, dressed in procedural textures traced directly from the vanilla leaves. It applies to the whole game, vanilla leaves included."),
       ("Des jeux d'ombre et de lumière y sont créés pour lui donner du volume, loin du damier de cubes habituel. Le tout reste purement visuel : les blocs de feuilles, eux, ne changent pas.","Shadow and light are built into it to give it volume, far from the usual grid of cubes. It all stays purely visual: the leaf blocks themselves don't change."),
     ]),
     ("L'éditeur d'espèces","The species editor",[
       ("Un éditeur en jeu permet de sculpter une espèce d'arbre de zéro et d'en régler les paramètres procéduraux. Les arbres sauvages rejouent ensuite l'archétype obtenu.","An in-game editor allows a tree species to be sculpted from scratch and its procedural parameters tuned. Wild trees then replay the resulting archetype."),
       ("Sur chaque espèce, plusieurs modèles d'auteur peuvent cohabiter, le tirage vanilla restant toujours présent. L'outil continue de s'enrichir, sans rien retirer à la stabilité du mod.","For each species, several authored models can coexist, with the vanilla draw always kept. The tool keeps growing, without taking anything away from the mod's stability."),
     ]),
     ("Une brique de la suite Tactile","A piece of the Tactile suite",[
       ("Le rendu procédural n'est pas figé : il est fait pour réagir au reste de la suite Tactile.","Procedural rendering isn't fixed: it's built to react to the rest of the Tactile suite."),
       ("Tactile:Season en est l'exemple le plus net : au fil du calendrier, le feuillage pourra virer de teinte, se dégarnir puis repousser, sans que le monde change de blocs.","Tactile:Season is the clearest example: as the calendar turns, foliage will be able to shift hue, thin out then grow back, without the world ever changing blocks."),
     ]),
   ],
  },
}
M["ore"]={"t":"full","name":"Ore","c":"#b83c4a","st":("Disponible","Available"),
  "dl":"https://www.curseforge.com/minecraft/mc-mods/tactile-ore",
  "pitch":("Les minerais ne sont plus de simples cubes, mais de vrais gisements incrustés, indépendants de la roche.","Ores are no longer plain cubes, but real deposits embedded in the rock, independent from it."),
  "hero":(f"{SRC}/ore_1.png",0.0,0.12),
  "features":[
    (f"{SRC}/ore_hero.png",("Un vrai volume","Real volume"),("Les gisements existent dans l'espace 3D. Une grappe de fragments incrustés dans la roche, chacun unique, façonné par le type de minerai.","Deposits exist in 3D space. A cluster of fragments embedded in the rock, each one unique, shaped by the ore type.")),
    (f"{SRC}/ore_2.png",("Mine, ou creuse","Mine, or dig"),("Le fragment se mine directement. Ou l'on dégage la roche pour l'atteindre. Mais attention à la chute.","The fragment can be mined directly. Or the rock cleared to reach it. But mind the fall.")),
    (f"{SRC}/ore_3.png",("Compatible à 100 %","100% compatible"),("Il agit comme une surcouche du monde existant. Il interprète les données des chunks et se fixe par-dessus, sans jamais toucher à la rareté.","It acts as an overlay on the existing world. It reads the chunk data and sits on top, never touching ore rarity.")),
  ],
  "deep":[
    ("Comment ça marche","How it works",[
      ("Le mod n'ajoute aucun minerai : il relit celui qui est déjà là. À intervalle régulier, il scanne les chunks chargés autour des joueurs, section de 16×16×16 par section, et écarte d'emblée celles qui n'en contiennent aucun. Coût nul là où il n'y a rien.","The mod adds no ore: it re-reads what's already there. At a regular interval it scans the loaded chunks around players, one 16×16×16 section at a time, and immediately skips those that hold none. Zero cost where there's nothing."),
      ("Dans les sections concernées, chaque bloc de minerai, vanilla ou moddé, est remplacé par son bloc-hôte d'origine, échantillonné sur le voisinage (pierre, deepslate, netherrack, terrain moddé). Les cases voisines sont regroupées en amas : une zone de gisement.","In the sections that qualify, each ore block, vanilla or modded, is replaced by its original host block, sampled from the neighborhood (stone, deepslate, netherrack, modded terrain). Neighboring cells are grouped into clusters: a deposit zone."),
      ("Sur chaque zone, le mod bâtit alors le gisement en trois dimensions : cœurs, fusions et ramifications, façonnés par le type de minerai, chaque fragment unique. La forme est nouvelle, mais l'emplacement, la profondeur et la rareté restent exactement ceux que le monde avait déjà générés.","On each zone, the mod then builds the three-dimensional deposit: cores, fusions and ramifications, shaped by the ore type, each fragment unique. The shape is new, but the location, depth and rarity stay exactly what the world had already generated."),
      ("Le résultat est intégré à la géométrie de la section, comme n'importe quel bloc : occlusion, découpe et distance d'affichage sont gérées nativement par le moteur.","The result is baked into the section geometry, like any block: occlusion, culling and render distance are handled natively by the engine."),
    ]),
    ("La physique","The physics",[
      ("Tant qu'un fragment prend appui sur un bloc, il reste figé. Privé de ce support, il devient une entité physique : il se désolidarise de la roche et tombe, morceau par morceau.","As long as a fragment rests on a block, it stays fixed. Deprived of that support, it becomes a physical entity: it breaks loose from the rock and falls, piece by piece."),
      ("On peut donc le miner directement, ou creuser tout autour pour le faire chuter, puis ramasser au sol chaque morceau d'un clic droit.","So it can be mined directly, or dug all around to make it fall, then each piece picked up off the ground with a right click."),
      ("La surface de chaque fragment reprend la texture de l'objet obtenu en le minant : ce qui affleure est exactement ce qui sera récolté.","Each fragment's surface takes the texture of the item obtained by mining it: what surfaces is exactly what gets harvested."),
    ]),
    ("Aucune balance cassée","No balance broken",[
      ("Puisque rien n'est généré de zéro, la rareté, la hauteur et la répartition des minerais restent celles de vanilla et des mods installés. La compatibilité tient sur tous les minerais découverts, y compris dans les mondes existants, les donjons et les structures pré-générées.","Since nothing is generated from scratch, ore rarity, height and distribution stay those of vanilla and the installed mods. Compatibility holds for every ore found, including in existing worlds, dungeons and pre-generated structures."),
      ("Tout minerai est pris en charge automatiquement, sans aucune liste à écrire, et dans toutes les dimensions (Nether, End, dimensions moddées). Éprouvé sur de gros modpacks : All The Mods 11, Aether, Terralith.","Every ore is handled automatically, with no list to maintain, and across all dimensions (Nether, End, modded dimensions). Tested on large modpacks: All The Mods 11, Aether, Terralith."),
    ]),
    ("Réglages et retour en arrière","Settings and rollback",[
      ("Tout se règle dans les options du mod, y compris la régénération optionnelle des icônes 2D des objets, pour qu'elles collent à l'apparence en trois dimensions du minerai extrait.","Everything is configured in the mod options, including the optional regeneration of the items' 2D icons so they match the extracted ore's three-dimensional look."),
      ("À la conversion, le minerai d'origine est mémorisé bloc par bloc. Depuis les options, tout peut être reposé à l'identique : le monde retrouve son minerai vanilla exact, sans la moindre perte, et le mod se retire proprement.","On conversion, the original ore is remembered block by block. From the options, everything can be restored exactly: the world recovers its precise vanilla ore, without the slightest loss, and the mod removes cleanly."),
    ]),
  ]}

M["blocks"]={"t":"full","name":"Blocks","c":"#7d8794","st":("Disponible","Available"),
  "dl":"https://www.curseforge.com/minecraft/mc-mods/tactileblocks",
  "pitch":("Les blocs fonctionnels sont repensés pour être détaillés, immersifs et interactifs. Fini les menus.","Functional blocks are overhauled to be detailed, immersive and interactive. No more menus."),
  "hero":(f"{SRC}/blocks_hero.png",0.10,0.0),
  "features":[
    (f"{SRC}/blocks_1.png",("Fini les menus","No more menus"),("On interagit directement avec le bloc, dans le monde. Le four a deux compartiments, ingrédients et carburant, et s'allume au foret à main ; le fumoir cuit selon l'état de sa porte.","You interact with the block directly, in the world. The furnace has two compartments, ingredients and fuel, lit with the hand drill; the smoker cooks depending on its door.")),
    (f"{SRC}/blocks_2.png",("Quinze stations, quinze gestes","Fifteen stations, fifteen gestures"),("L'enclume répare au marteau, la meule désenchante contre de l'expérience, l'alambic distille par compartiments, le cartographe agrandit les cartes, et la table d'enchantement s'ouvre sur un grimoire nourri de livres de connaissance.","The anvil repairs by hammer, the millstone disenchants for experience, the still distills by compartment, the cartographer enlarges maps, and the enchanting table opens onto a grimoire fed by Knowledge Books.")),
    (f"{SRC}/blocks_3.png",("Il investit ton monde","It moves into your world"),("Les stations déjà posées, dans les villages comme dans tes constructions, deviennent automatiquement leurs versions Tactile, sans toucher à ton inventaire. Tu changes d'avis ? Tout revient à l'état vanilla.","Stations already placed, in villages or your own builds, automatically become their Tactile versions, without touching your inventory. Change your mind? Everything returns to vanilla.")),
  ]}

for cid,cn,cc,cp,cv in CONC:
    M[cid]={"t":"concept","name":cn,"c":cc,"st":("À venir","Upcoming"),"pitch":cp,"vision":cv}
# Pistes issues de l'annexe Blocks : statut et avertissement distincts (rien n'est retiré de Blocks).
for k in ("alchemy","enchantment"):
    M[k]["st"]=("Piste","Exploratory")
    M[k]["note"]=("Piste exploratoire, issue de Tactile:Blocks. Rien n'en est retiré à ce jour.",
                  "Exploratory track, coming out of Tactile:Blocks. Nothing is being removed from it as of today.")

EMB='<g fill="none" stroke="#191510" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"><line x1="-46" y1="-52" x2="46" y2="-52"/><line x1="0" y1="-52" x2="0" y2="58"/></g><g fill="#191510"><circle cx="-46" cy="-52" r="9.5"/><circle cx="46" cy="-52" r="9.5"/><circle cx="0" cy="58" r="9.5"/></g><circle cx="0" cy="-52" r="12" fill="none" stroke="#c07f1e" stroke-width="7"/><circle cx="0" cy="-52" r="5" fill="#c07f1e"/>'

CSS=open(PREV+"/detail_css.txt",encoding="utf-8").read() if os.path.exists(PREV+"/detail_css.txt") else ""
# CSS est injecté ci-dessous (défini en dur)
CSS=r"""
:root{--paper:#f2f1ec;--paper2:#ebe8e1;--card:#fff;--ink:#191510;--ink2:#5f594e;--line:#dcd7cd;--accent:#c07f1e;--c:CCC}
*{box-sizing:border-box}html{background:var(--paper);scroll-behavior:smooth}
body{margin:0;background:var(--paper);color:var(--ink);font-family:"Segoe UI",system-ui,-apple-system,Arial,sans-serif;-webkit-font-smoothing:antialiased;line-height:1.6}
a{color:inherit;text-decoration:none}.wrap{max-width:1240px;margin:0 auto;padding:0 32px}
.top{display:flex;justify-content:space-between;align-items:center;gap:10px;padding:14px 32px;max-width:1240px;margin:0 auto}
.back{display:flex;align-items:center;gap:11px;color:var(--ink2);font-size:14px}.back svg{width:20px;height:24px}.back:hover{color:var(--ink)}
.top .r{display:flex;gap:10px;align-items:center}.top .r a{font-size:13px;color:var(--ink2);border:1px solid var(--line);border-radius:2px;padding:8px 15px}
.top .r a:hover{border-color:var(--ink);color:var(--ink)}.top .r a.pri{background:var(--ink);color:var(--paper);border-color:var(--ink)}
.langsw{display:inline-flex;border:1px solid var(--line);border-radius:2px;overflow:hidden}
.langsw .lang{background:var(--card);border:none;color:var(--ink2);font-size:12px;font-weight:700;letter-spacing:.06em;padding:8px 11px;cursor:pointer}
.langsw .lang.on{background:var(--ink);color:var(--paper)}
.dhero{position:relative;min-height:470px;display:flex;align-items:flex-end;overflow:hidden}
.dbg{position:absolute;inset:0;background:url(HEROURL) center/cover}
.dscrim{position:absolute;inset:0;background:linear-gradient(90deg,rgba(9,6,2,.85),rgba(9,6,2,.42) 46%,rgba(9,6,2,.12) 82%),linear-gradient(0deg,color-mix(in srgb,var(--c) 52%,transparent),transparent 44%)}
.din{position:relative;max-width:1240px;width:100%;margin:0 auto;padding:0 32px 48px;color:#fff}
.dic{width:60px;height:60px;filter:drop-shadow(0 2px 6px rgba(0,0,0,.5));margin-bottom:14px}
.dbadge{display:inline-block;font-size:11px;letter-spacing:.12em;text-transform:uppercase;font-weight:700;background:rgba(255,255,255,.22);padding:4px 11px;border-radius:2px;margin-left:12px;vertical-align:middle}
.dhero h1{margin:0;font-size:clamp(36px,6vw,60px);font-weight:700;letter-spacing:-.01em;text-shadow:0 2px 14px rgba(0,0,0,.35)}.dhero h1 i{opacity:.55;font-style:normal}
.dpitch{margin:16px 0 24px;font-size:clamp(17px,2.1vw,23px);color:#f2ece0;max-width:34ch;text-shadow:0 1px 10px rgba(0,0,0,.3)}
.dl-btn{display:inline-block;background:#fff;color:var(--ink);font-weight:700;font-size:15px;padding:14px 30px;border-radius:2px}.dl-btn:hover{background:var(--accent);color:#fff}
.dl-2{display:inline-block;margin-left:12px;border:1px solid rgba(255,255,255,.62);color:#fff;font-weight:600;font-size:15px;padding:13px 26px;border-radius:2px}
.dl-2:hover{background:rgba(255,255,255,.14)}
@media(max-width:560px){.dl-2{margin-left:0;margin-top:12px}}
.dl-soon{display:inline-block;border:1px solid rgba(255,255,255,.55);color:#fff;font-weight:700;font-size:15px;padding:13px 29px;border-radius:2px;opacity:.92}
.features{max-width:1240px;margin:0 auto;padding:46px 32px 16px;display:flex;flex-direction:column;gap:46px}
.frow{display:grid;grid-template-columns:1.18fr .82fr;gap:52px;align-items:center}.frow.rev .fimg{order:2}
.fimg{aspect-ratio:16/10;border-radius:8px;background-size:cover;background-position:center;box-shadow:0 20px 44px rgba(25,18,10,.20);border:1px solid rgba(25,18,10,.10)}
.ftxt h3{margin:0 0 16px;font-size:clamp(25px,3vw,33px);font-weight:700;letter-spacing:-.015em;line-height:1.15}
.ftxt p{margin:0;color:var(--ink2);font-size:18px;line-height:1.72;max-width:42ch}
@media(max-width:800px){.frow{grid-template-columns:1fr;gap:26px}.frow.rev .fimg{order:0}}
.spec{display:grid;grid-template-columns:repeat(4,1fr);border:1px solid var(--line);border-radius:4px;margin:34px auto;max-width:1240px;background:var(--card)}
.si{padding:24px 24px;border-right:1px solid var(--line)}.si:last-child{border-right:none}
.sl{display:block;font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--ink2)}.sv{display:block;margin-top:7px;font-size:16px;font-weight:600}
@media(max-width:760px){.spec{grid-template-columns:1fr 1fr}.si{border-bottom:1px solid var(--line)}}
.gal{background:var(--paper2);border-top:1px solid var(--line);margin-top:52px}
.gal-in{max-width:1240px;margin:0 auto;padding:62px 32px 66px}
.gal h2{margin:0 0 12px;font-size:clamp(25px,3vw,33px);font-weight:700;letter-spacing:-.015em}
.gal-lead{margin:0;font-size:17.5px;line-height:1.72;color:var(--ink2);max-width:62ch}
.gal-grid{display:grid;grid-template-columns:repeat(var(--gcols,3),minmax(0,1fr));gap:30px;margin-top:36px}
.gitem{margin:0}
.gimg{aspect-ratio:16/9;border-radius:6px;background-size:cover;background-position:center;box-shadow:0 14px 30px rgba(25,18,10,.17);border:1px solid rgba(25,18,10,.10)}
.gimg.fit{background-size:contain;background-repeat:no-repeat;background-color:#12141b}
.gcap{margin-top:14px;font-size:15px;line-height:1.6;color:var(--ink2)}
@media(max-width:860px){.gal-grid{grid-template-columns:1fr;gap:30px}}
.deep{background:var(--paper2);border-top:1px solid var(--line)}.dwrap{max-width:760px;margin:0 auto;padding:66px 32px}
.deyebrow{font-size:12px;letter-spacing:.2em;text-transform:uppercase;color:var(--c);font-weight:700;margin:0 0 6px}
.deep h2{font-size:clamp(21px,2.4vw,27px);font-weight:700;letter-spacing:-.01em;margin:38px 0 14px}.deep h2:first-of-type{margin-top:10px}
.deep p{margin:0 0 14px;font-size:17px;line-height:1.75;color:#3f3a31;max-width:64ch}
.cmds{display:flex;flex-direction:column;gap:12px;margin:6px 0}.cmd{display:flex;align-items:baseline;gap:16px;flex-wrap:wrap;padding:14px 16px;background:var(--card);border:1px solid var(--line);border-left:3px solid var(--c);border-radius:3px}
.cmd code{font-family:Consolas,"Courier New",monospace;font-size:14.5px;color:var(--ink);font-weight:600;white-space:nowrap}.cmd span{color:var(--ink2);font-size:14.5px}
.chero{position:relative;overflow:hidden;min-height:400px;display:flex;align-items:flex-end;background:linear-gradient(135deg,var(--c),color-mix(in srgb,var(--c) 58%,#0a0804))}
.chero .ghost{position:absolute;right:-30px;bottom:-40px;width:360px;height:360px;opacity:.13}
.chero .din{color:#fff}
.cbadge{display:inline-block;font-size:11px;letter-spacing:.12em;text-transform:uppercase;font-weight:700;background:rgba(255,255,255,.24);padding:4px 11px;border-radius:2px;margin-left:12px;vertical-align:middle}
.vision-sec .dwrap{padding:60px 32px;max-width:820px}
.vision-sec h2{font-size:clamp(21px,2.4vw,27px);font-weight:700;letter-spacing:-.01em;margin:44px 0 14px}
.vision-sec h2:first-of-type{margin-top:8px}
.vision-sec p{margin:0 0 14px;font-size:17px;line-height:1.78;color:#3f3a31;max-width:66ch}
.fig{margin:26px 0 34px;padding:24px 22px 16px;background:var(--card);border:1px solid var(--line);border-radius:5px;overflow-x:auto}
.fig svg{display:block;width:100%;min-width:520px;height:auto}
.figcap{margin-top:16px;padding-top:13px;border-top:1px solid var(--line);font-size:13.5px;line-height:1.6;color:var(--ink2);text-align:center}
.vnote{max-width:760px;margin:0 auto 40px;padding:0 32px}
.vnote span{display:inline-block;font-size:13px;color:var(--ink2);border:1px dashed var(--line);border-radius:20px;padding:7px 16px;font-style:italic}
footer{border-top:1px solid var(--line);padding:34px 0;font-size:13px;color:var(--ink2)}
footer .row{display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:16px}
footer .links{display:flex;gap:10px;flex-wrap:wrap}footer .links a{border:1px solid var(--line);border-radius:2px;padding:8px 15px}footer .links a:hover{border-color:var(--ink);color:var(--ink)}
@media(prefers-reduced-motion:reduce){*{transition:none!important}}
"""

SCRIPT="""<script>(function(){function set(l){document.querySelectorAll('[data-fr]').forEach(function(e){var v=e.getAttribute('data-'+l);if(v!==null)e.textContent=v;});document.documentElement.setAttribute('lang',l);try{localStorage.setItem('tactile_lang',l);}catch(e){}document.querySelectorAll('.lang').forEach(function(b){b.classList.toggle('on',b.getAttribute('data-lang')===l);});}var s='en';try{s=localStorage.getItem('tactile_lang')||'en';}catch(e){}document.querySelectorAll('.lang').forEach(function(b){b.addEventListener('click',function(){set(b.getAttribute('data-lang'));});});set(s);})();</script>"""

def top(dl=None):
    # En-tête identique partout : Discord et CurseForge, quel que soit le module.
    btn=f'<a class="pri" href="{CURSEFORGE}"{X}>CurseForge</a>'
    return ('<div class="top"><a class="back" href="../index.html"><svg viewBox="-64 -72 128 144"><use href="#emb"/></svg>'
            '<span data-fr="Tous les modules" data-en="All modules">Tous les modules</span></a>'
            '<div class="r"><span class="langsw"><button class="lang on" data-lang="fr">FR</button><button class="lang" data-lang="en">EN</button></span>'
            f'<a href="{DISCORD}"{X}>Discord</a><a href="{KOFI}"{X}>Ko-fi</a>'+btn+'</div></div>')
def footer():
    return ('<footer><div class="wrap"><div class="row"><span data-fr="Tactile · suite de mods Minecraft" data-en="Tactile · a Minecraft mod suite">Tactile · suite de mods Minecraft</span>'
            f'<div class="links"><a href="https://github.com/Belerion63/Tactile/blob/main/LICENSE"{X} data-fr="© 2026 belerion · Tous droits réservés" data-en="© 2026 belerion · All rights reserved">© 2026 belerion · Tous droits réservés</a><a href="{GITHUB}"{X}>GitHub</a></div></div></div></footer>')
def defs(m):
    # Les modules sans logo dédié (pistes issues de Blocks) retombent sur l'emblème de la suite.
    icon = white(raw(m)) if os.path.exists(f"{SVG}/tactile-{m}.svg") else white(EMB)
    return f'<svg width="0" height="0" style="position:absolute"><defs><g id="w-{m}">{icon}</g><g id="emb">{EMB}</g></defs></svg>'

def build_full(m,d):
    K=d.get("keep",set())
    if "hero" in K: keep(m,"hero",1600,540)
    else: make(m,"hero", d["hero"][0], 1600, 540, cb=d["hero"][1], ct=d["hero"][2])
    fr=[]
    for i,(src,(hf,he),(tf,te)) in enumerate(d["features"],1):
        if str(i) in K: keep(m,str(i),900,620)
        else: make(m,str(i), src, 900, 620, cb=0.10)
        rev=" rev" if i%2==0 else ""
        fr.append(f'<div class="frow{rev}"><div class="fimg" style="background-image:url(@@IMG:{i}@@)"></div><div class="ftxt"><h3 data-fr="{hf}" data-en="{he}">{hf}</h3><p data-fr="{tf}" data-en="{te}">{tf}</p></div></div>')
    dl=d.get("dl")
    if dl:
        tb=' target="_blank" rel="noopener"' if dl.startswith("http") else ''
        cta=f'<a class="dl-btn" href="{dl}"{tb} data-fr="Télécharger" data-en="Download">Télécharger</a>'
    else:
        cta='<span class="dl-soon" data-fr="Bientôt disponible" data-en="Coming soon">Bientôt disponible</span>'
    # Modules dotés d'un éditeur : second bouton vers la galerie, pré-filtrée sur le module.
    if d.get("addons"):
        cta+=(f'<a class="dl-2" href="../addons/index.html?module={m}" '
              f'data-fr="Créations de la communauté" data-en="Community creations">Créations de la communauté</a>')
    # Guide de l'atelier, pour les modules qui en ont un.
    if d.get("guide"):
        cta+=("<a class=\"dl-2\" href=\"workshop/index.html\" "
              "data-fr=\"Guide de l'atelier\" data-en=\"Workshop guide\">Guide de l'atelier</a>")
    spec_html=""
    if d.get("spec"):
        specs="".join(f'<div class="si"><span class="sl" data-fr="{lf}" data-en="{le}">{lf}</span><span class="sv" data-fr="{vf}" data-en="{ve}">{vf}</span></div>' for lf,le,vf,ve in d["spec"])
        spec_html=f'<div class="wrap"><div class="spec">{specs}</div></div>'
    gal=""
    if d.get("gallery"):
        g=d["gallery"]; items=[]
        for i,shot in enumerate(g["shots"],1):
            src,cf,ce = shot[0],shot[1],shot[2]
            ft = len(shot)>3 and shot[3]=="fit"
            if f"g{i}" in K or src is None: keep(m,f"g{i}",960,540,fit=ft)
            else: make(m,f"g{i}", src, 960, 540, cb=g.get("cb",0.0))
            items.append(f'<figure class="gitem"><div class="gimg{" fit" if ft else ""}" style="background-image:url(@@IMG:g{i}@@)"></div>'
                         f'<figcaption class="gcap" data-fr="{cf}" data-en="{ce}">{cf}</figcaption></figure>')
        cols=2 if len(g["shots"])==4 else 3
        gal=(f'<section class="gal"><div class="gal-in" style="--gcols:{cols}">'
             f'<h2 data-fr="{g["t"][0]}" data-en="{g["t"][1]}">{g["t"][0]}</h2>'
             f'<p class="gal-lead" data-fr="{g["lead"][0]}" data-en="{g["lead"][1]}">{g["lead"][0]}</p>'
             f'<div class="gal-grid">{"".join(items)}</div></div></section>')
    deep=""
    if d.get("deep"):
        parts=[]
        for tf,te,paras in d["deep"]:
            parts.append(f'<h2 data-fr="{tf}" data-en="{te}">{tf}</h2>'+"".join(f'<p data-fr="{a}" data-en="{b}">{a}</p>' for a,b in paras))
        deep=f'<section class="deep"><div class="dwrap"><p class="deyebrow" data-fr="En détail" data-en="In depth">En détail</p>{"".join(parts)}</div></section>'
    css=CSS.replace("CCC",d["c"]).replace("HEROURL","@@IMG:hero@@")
    body=(f'<style>{css}</style>{defs(m)}{top(dl)}'
      f'<section class="dhero"><div class="dbg"></div><div class="dscrim"></div><div class="din">'
      f'<svg class="dic" viewBox="-75 -75 150 150"><use href="#w-{m}"/></svg>'
      f'<h1>Tactile<i>:</i>{d["name"]}<span class="dbadge" data-fr="{d["st"][0]}" data-en="{d["st"][1]}">{d["st"][0]}</span></h1>'
      f'<p class="dpitch" data-fr="{d["pitch"][0]}" data-en="{d["pitch"][1]}">{d["pitch"][0]}</p>'
      f'{cta}</div></section>'
      f'<section class="features">{"".join(fr)}</section>{spec_html}{gal}{deep}{footer()}{SCRIPT}')
    return f'<title>Tactile:{d["name"]}</title>'+body

def build_concept(m,d):
    css=CSS.replace("CCC",d["c"])
    parts=[]
    for tf,te,paras_,figk in d["vision"]:
        parts.append(f'<h2 data-fr="{tf}" data-en="{te}">{tf}</h2>')
        parts.append("".join(f'<p data-fr="{a}" data-en="{b}">{a}</p>' for a,b in paras_))
        if figk and figk in FIGS:
            sv,cf,ce=FIGS[figk]
            parts.append(f'<figure class="fig">{sv}<figcaption class="figcap" data-fr="{cf}" data-en="{ce}">{cf}</figcaption></figure>')
    paras="".join(parts)
    nf,ne=d.get("note",("Module conceptuel, pensé en détail, pas encore en développement.",
                        "Conceptual module, designed in depth, not yet in development."))
    body=(f'<style>{css}</style>{defs(m)}{top(None)}'
      f'<section class="chero"><svg class="ghost" viewBox="-75 -75 150 150"><use href="#w-{m}"/></svg><div class="din">'
      f'<svg class="dic" viewBox="-75 -75 150 150"><use href="#w-{m}"/></svg>'
      f'<h1>Tactile<i>:</i>{d["name"]}<span class="cbadge" data-fr="{d["st"][0]}" data-en="{d["st"][1]}">{d["st"][0]}</span></h1>'
      f'<p class="dpitch" data-fr="{d["pitch"][0]}" data-en="{d["pitch"][1]}">{d["pitch"][0]}</p></div></section>'
      f'<div class="vnote"><span data-fr="{nf}" data-en="{ne}">{nf}</span></div>'
      f'<section class="vision-sec"><div class="dwrap" style="background:none;padding-top:0"><p class="deyebrow" data-fr="La vision" data-en="The vision">La vision</p>'
      f'{paras}</div></section>{footer()}{SCRIPT}')
    return (f'<title data-fr="Tactile:{d["name"]}, concept" data-en="Tactile:{d["name"]}, concept">'
            f'Tactile:{d["name"]}, concept</title>')+body

def resolve(h,fn): return re.sub(r"@@IMG:([a-z0-9\-]+)@@",lambda mm:fn(mm.group(1)),h)
def wrap(site, meta=""):
    idx=site.index("</style>")+len("</style>"); head,body=site[:idx],site[idx:]
    return ('<!DOCTYPE html>\n<html lang="fr">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            '<link rel="icon" type="image/png" href="../assets/favicon.png">\n'
            + meta + head + "\n</head>\n<body>\n" + body + "\n</body>\n</html>\n")

def og(m, d):
    """Carte de partage propre à chaque page : sans elle, un lien de module
    collé sur Discord s'affiche en URL nue."""
    img = f"{BASE}/{m}/img/hero.jpg" if d["t"] == "full" else f"{BASE}/assets/og.jpg"
    desc = d["pitch"][1].replace(chr(34), "&quot;")
    t = [
        f'<meta name="description" content="{desc}">',
        '<meta property="og:type" content="website">',
        '<meta property="og:site_name" content="Tactile">',
        f'<meta property="og:title" content="Tactile:{d["name"]}">',
        f'<meta property="og:description" content="{desc}">',
        f'<meta property="og:url" content="{BASE}/{m}/">',
        f'<meta property="og:image" content="{img}">',
        '<meta name="twitter:card" content="summary_large_image">',
    ]
    return chr(10).join(t) + chr(10)

def nd(s): return s.replace(" — ", ", ").replace("—", ", ")

def en_first(h):
    """L'anglais devient la langue affichée par défaut.

    Le texte visible de chaque élément bilingue est remplacé par sa version
    anglaise ; data-fr conserve le français pour le sélecteur. Sans cela, la
    page peindrait le français avant que le script ne bascule."""
    h=re.sub(r'(data-fr="([^"]*)"\s+data-en="([^"]*)"([^>]*)>)([^<]*)(</)',
             lambda m: m.group(1)+m.group(3)+m.group(6), h)
    return h.replace('<html lang="fr">','<html lang="en">')
for m,d in M.items():
    os.makedirs(f"{SITE}/{m}",exist_ok=True)
    html = build_full(m,d) if d["t"]=="full" else build_concept(m,d)
    open(f"{SITE}/{m}/index.html","w",encoding="utf-8").write(en_first(nd(wrap(resolve(html,lambda k:f"img/{k}.jpg"), og(m,d)))))
    if True:
        open(f"{PREV}/detail_{m}.html","w",encoding="utf-8").write(en_first(nd(resolve(html,lambda k:URI.get(k,f"img/{k}.jpg")))))
print("Généré :", ", ".join(sorted(M.keys())))
