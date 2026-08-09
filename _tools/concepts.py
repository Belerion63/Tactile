# -*- coding: utf-8 -*-
"""Contenu des 10 modules CONCEPTUELS de la vitrine Tactile.

Structure : CONC = [(id, nom, couleur, (pitch_fr, pitch_en), [sections]), ...]
  section = (titre_fr, titre_en, [(para_fr, para_en), ...], cle_figure|None)
FIGS[cle] = (svg, legende_fr, legende_en)

Regles de forme : voix impersonnelle (jamais << tu >>), aucun tiret cadratin,
aucun guillemet double dans les textes (ils partent dans des attributs HTML).
Les <text> des schemas portent data-fr/data-en : ils sont traduits par le meme script.
"""

# --------------------------------------------------------------------------
# Helpers de schema
# --------------------------------------------------------------------------
def _t(x, y, fr, en, size=13.5, anchor="middle", fill="var(--ink)", weight="400"):
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" data-fr="{fr}" data-en="{en}">{fr}</text>')

def _box(x, y, w, h, fr, en, fill="var(--card)", stroke="var(--line)", size=13.5, weight="600"):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="{fill}" stroke="{stroke}"/>'
            + _t(x + w / 2, y + h / 2 + 5, fr, en, size=size, weight=weight))

def _har(x1, x2, y, color="var(--c)"):
    return (f'<line x1="{x1}" y1="{y}" x2="{x2 - 8}" y2="{y}" stroke="{color}" stroke-width="2"/>'
            f'<polygon points="{x2},{y} {x2 - 9},{y - 4.5} {x2 - 9},{y + 4.5}" fill="{color}"/>')

def _var(x, y1, y2, color="var(--c)"):
    return (f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2 - 8}" stroke="{color}" stroke-width="2"/>'
            f'<polygon points="{x},{y2} {x - 4.5},{y2 - 9} {x + 4.5},{y2 - 9}" fill="{color}"/>')

def _svg(vb, inner):
    return f'<svg viewBox="{vb}" xmlns="http://www.w3.org/2000/svg" role="img">{inner}</svg>'


HOT, TEMP, COLD = "#c8702f", "#7f9e57", "#6d93bd"

FIGS = {}

# --- Season : les anneaux climatiques -------------------------------------
_rings = (
    f'<circle cx="215" cy="150" r="140" fill="{HOT}" fill-opacity=".16"/>'
    f'<circle cx="215" cy="150" r="140" fill="none" stroke="{HOT}" stroke-opacity=".45"/>'
    f'<circle cx="215" cy="150" r="108" fill="{TEMP}" fill-opacity=".20"/>'
    f'<circle cx="215" cy="150" r="108" fill="none" stroke="{TEMP}" stroke-opacity=".5"/>'
    f'<circle cx="215" cy="150" r="74" fill="{COLD}" fill-opacity=".22"/>'
    f'<circle cx="215" cy="150" r="74" fill="none" stroke="{COLD}" stroke-opacity=".5"/>'
    f'<circle cx="215" cy="150" r="38" fill="{TEMP}" fill-opacity=".20"/>'
    f'<circle cx="215" cy="150" r="38" fill="none" stroke="{TEMP}" stroke-opacity=".5"/>'
    f'<circle cx="215" cy="150" r="5" fill="var(--ink)"/>'
    + _t(215, 174, "Point d'apparition", "Spawn point", size=12, fill="var(--ink2)")
    + f'<circle cx="415" cy="82" r="8" fill="{HOT}" fill-opacity=".55" stroke="{HOT}"/>'
    + _t(434, 87, "Chaud et sec, jamais de neige", "Hot and dry, never any snow", anchor="start", fill="var(--ink2)")
    + f'<circle cx="415" cy="122" r="8" fill="{TEMP}" fill-opacity=".55" stroke="{TEMP}"/>'
    + _t(434, 127, "Tempéré, le plus arrosé", "Temperate, the wettest", anchor="start", fill="var(--ink2)")
    + f'<circle cx="415" cy="162" r="8" fill="{COLD}" fill-opacity=".55" stroke="{COLD}"/>'
    + _t(434, 167, "Froid, neige et pluie", "Cold, snow and rain", anchor="start", fill="var(--ink2)")
    + '<line x1="415" y1="196" x2="672" y2="196" stroke="var(--line)"/>'
    + _t(415, 224, "Les anneaux se répètent en s'éloignant.", "The rings repeat as you move away.", anchor="start", size=12.5, fill="var(--ink2)")
    + _t(415, 244, "Aucun nord, aucun sud : la latitude est une distance.", "No north, no south: latitude is a distance.", anchor="start", size=12.5, fill="var(--ink2)")
)
FIGS["season_rings"] = (_svg("0 0 700 300", _rings),
    "Le climat s'organise en cercles autour du point d'apparition.",
    "Climate is organized in circles around the spawn point.")

# --- Season : ce qui oscille ----------------------------------------------
def _wave(amp, yc, color, label_fr, label_en):
    import math
    pts = []
    for i in range(0, 81):
        x = 150 + i * 6.3
        y = yc - amp * math.sin(i / 80 * 2 * math.pi * 2)
        pts.append(f"{x:.0f},{y:.1f}")
    return (f'<polyline points="{" ".join(pts)}" fill="none" stroke="{color}" stroke-width="2.4"/>'
            + _t(140, yc + 4, label_fr, label_en, anchor="end", size=12.5, fill="var(--ink2)"))

_swing = (
    ''.join(f'<line x1="{150 + i * 126}" y1="26" x2="{150 + i * 126}" y2="196" stroke="var(--line)"/>' for i in range(5))
    + _t(213, 216, "Printemps", "Spring", size=12, fill="var(--ink2)")
    + _t(339, 216, "Été", "Summer", size=12, fill="var(--ink2)")
    + _t(465, 216, "Automne", "Autumn", size=12, fill="var(--ink2)")
    + _t(591, 216, "Hiver", "Winter", size=12, fill="var(--ink2)")
    + _wave(8, 58, HOT, "Anneau chaud", "Hot ring")
    + _wave(46, 112, TEMP, "Anneau tempéré", "Temperate ring")
    + _wave(8, 172, COLD, "Anneau froid", "Cold ring")
)
FIGS["season_swing"] = (_svg("0 0 700 240", _swing),
    "Les extrêmes bougent à peine. Ce sont les zones tempérées qui vivent vraiment les saisons.",
    "The extremes barely move. It is the temperate zones that truly live the seasons.")

# --- Weather : la cascade --------------------------------------------------
_casc = (
    _box(14, 40, 116, 52, "Température", "Temperature")
    + _har(134, 168, 66)
    + _box(172, 40, 116, 52, "Pression", "Pressure")
    + _har(292, 326, 66)
    + _box(330, 40, 116, 52, "Vent", "Wind")
    + _har(450, 484, 66)
    + _box(488, 40, 116, 52, "Nuages", "Clouds")
    + _var(546, 96, 132)
    + _box(456, 136, 180, 52, "Pluie, neige, orage", "Rain, snow, storm",
           fill="color-mix(in srgb, var(--c) 14%, var(--card))", stroke="var(--c)")
    + _t(546, 210, "quand la cumulation dépasse son seuil", "when accumulation passes its threshold", size=12, fill="var(--ink2)")
    + _var(230, 96, 132)
    + _box(140, 136, 180, 52, "Tempête, tornade", "Storm, tornado",
           fill="color-mix(in srgb, var(--c) 14%, var(--card))", stroke="var(--c)")
    + _t(230, 210, "quand la pression chute d'un coup", "when pressure drops suddenly", size=12, fill="var(--ink2)")
    + _t(14, 22, "Une seule variable maîtresse, tout le reste en découle.", "One master variable, everything else follows.", anchor="start", size=12.5, fill="var(--ink2)")
)
FIGS["weather_cascade"] = (_svg("0 0 700 230", _casc),
    "La météo n'est pas tirée au sort : elle se déduit, maillon par maillon.",
    "Weather is not rolled at random: it is derived, link by link.")

# --- Water : la coupe ------------------------------------------------------
_water = (
    '<rect x="0" y="0" width="700" height="112" fill="#dbe6f0"/>'
    '<path d="M0,112 L700,112 L700,320 L0,320 Z" fill="#cdbfa4"/>'
    '<path d="M0,196 L700,196 L700,320 L0,320 Z" fill="#b7ab92"/>'
    '<g fill="#fff" stroke="#c3d2e0"><ellipse cx="150" cy="44" rx="46" ry="22"/><ellipse cx="192" cy="50" rx="34" ry="17"/><ellipse cx="112" cy="52" rx="30" ry="15"/></g>'
    + ''.join(f'<line x1="{118 + i * 18}" y1="70" x2="{113 + i * 18}" y2="98" stroke="#6d93bd" stroke-width="2"/>' for i in range(6))
    + '<path d="M300,112 Q360,124 420,112 L420,132 Q360,144 300,132 Z" fill="#6d93bd" fill-opacity=".75"/>'
    + _t(360, 104, "Rivière", "River", size=12, fill="var(--ink2)")
    + ''.join(_var(150 + i * 26, 116, 176, "#6d93bd") for i in range(3))
    + _t(200, 152, "Infiltration", "Seepage", anchor="start", size=12.5, fill="var(--ink)")
    + '<line x1="0" y1="196" x2="700" y2="196" stroke="#3f7ba6" stroke-width="2.5" stroke-dasharray="7 5"/>'
    + _t(690, 188, "Nappe phréatique", "Water table", anchor="end", size=12.5, fill="#2f6a92")
    + '<rect x="536" y="104" width="30" height="94" fill="#8e846f"/><rect x="542" y="168" width="18" height="30" fill="#6d93bd"/>'
    + '<rect x="530" y="96" width="42" height="10" fill="var(--ink)" fill-opacity=".55"/>'
    + _t(551, 88, "Puits", "Well", size=12, fill="var(--ink2)")
    + '<path d="M120,222 Q170,204 232,222 Q252,262 200,278 Q140,282 116,258 Z" fill="#5d5546"/>'
    + '<path d="M124,252 Q170,242 240,250 Q248,266 200,278 Q140,282 118,260 Z" fill="#6d93bd" fill-opacity=".85"/>'
    + _t(178, 302, "Sous-sol noyé", "Flooded cellar", size=12.5, fill="var(--ink2)")
    + '<path d="M430,214 Q490,206 548,216 Q560,240 500,248 Q446,244 430,226 Z" fill="#a3906f" fill-opacity=".8"/>'
    + _t(492, 274, "Point d'eau qui monte et s'assèche", "Water body that rises and dries up", size=12.5, fill="var(--ink2)")
)
FIGS["water_section"] = (_svg("0 0 700 320", _water),
    "L'eau gagne une verticale : elle tombe, court, s'infiltre, remplit, et parfois noie.",
    "Water gains a vertical axis: it falls, runs, seeps, fills, and sometimes drowns.")

# --- Biome : l'ecotone -----------------------------------------------------
def _tree(x, y, s, color):
    return (f'<line x1="{x}" y1="{y}" x2="{x}" y2="{y - s * .5}" stroke="#8a6a44" stroke-width="{s * .13:.1f}"/>'
            f'<circle cx="{x}" cy="{y - s * .78}" r="{s * .42:.1f}" fill="{color}" fill-opacity=".85"/>')

def _cact(x, y, s):
    return (f'<rect x="{x - s * .09:.1f}" y="{y - s * .72:.1f}" width="{s * .18:.1f}" height="{s * .72:.1f}" rx="{s * .09:.1f}" fill="#7d9b5e"/>'
            f'<rect x="{x + s * .09:.1f}" y="{y - s * .58:.1f}" width="{s * .22:.1f}" height="{s * .12:.1f}" rx="{s * .06:.1f}" fill="#7d9b5e"/>')

_eco = (
    '<defs><linearGradient id="ecog" x1="0" x2="1"><stop offset="0" stop-color="#6f9e55" stop-opacity=".26"/>'
    '<stop offset="1" stop-color="#c8a24a" stop-opacity=".26"/></linearGradient></defs>'
    '<rect x="0" y="0" width="700" height="152" fill="url(#ecog)"/>'
    '<line x1="0" y1="152" x2="700" y2="152" stroke="var(--line)"/>'
    + ''.join(_tree(24 + i * 30, 152, 74, "#4f8a3f") for i in range(7))
    + _tree(240, 152, 66, "#4f8a3f") + _tree(292, 152, 58, "#5d8f45")
    + _cact(268, 152, 52) + _tree(340, 152, 48, "#74954a") + _cact(320, 152, 44) + _cact(372, 152, 56)
    + ''.join(_cact(420 + i * 42, 152, 54) for i in range(7))
    + _t(120, 178, "Forêt dense", "Dense forest", size=12.5, fill="var(--ink2)")
    + _t(316, 178, "Lisière", "Edge", size=12.5, fill="var(--c)", weight="700")
    + _t(556, 178, "Savane", "Savanna", size=12.5, fill="var(--ink2)")
    + '<line x1="248" y1="162" x2="248" y2="152" stroke="var(--c)" stroke-dasharray="3 3"/>'
    + '<line x1="392" y1="162" x2="392" y2="152" stroke="var(--c)" stroke-dasharray="3 3"/>'
)
FIGS["biome_ecotone"] = (_svg("0 0 700 194", _eco),
    "Deux biomes voisins ne se touchent plus par une ligne, mais se mélangent sur une bande.",
    "Two neighboring biomes no longer meet on a line, but blend across a band.")

# --- Monsters : le cycle du nid -------------------------------------------
def _nest(cx, cy, r, halo, n_mobs, seed):
    import math
    out = (f'<circle cx="{cx}" cy="{cy}" r="{halo}" fill="var(--c)" fill-opacity=".08" stroke="var(--c)" '
           f'stroke-opacity=".45" stroke-dasharray="5 5"/>'
           f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="var(--c)" fill-opacity=".55" stroke="var(--c)"/>')
    for i in range(n_mobs):
        a = (seed + i) * 2.399
        d = halo * .72
        out += f'<circle cx="{cx + math.cos(a) * d:.1f}" cy="{cy + math.sin(a) * d * .62:.1f}" r="4" fill="var(--ink)" fill-opacity=".65"/>'
    return out

_nests = (
    _nest(112, 108, 11, 40, 2, 1)
    + _t(112, 178, "Jeune", "Young", size=13, weight="700")
    + _t(112, 198, "un nid, quelques rôdeurs", "one nest, a few prowlers", size=12, fill="var(--ink2)")
    + _har(168, 236, 108)
    + _nest(322, 108, 17, 64, 5, 4)
    + _t(322, 178, "Mature", "Mature", size=13, weight="700")
    + _t(322, 198, "il produit plus vite qu'on ne nettoie", "it breeds faster than you clear", size=12, fill="var(--ink2)")
    + _har(400, 468, 108)
    + _nest(566, 108, 23, 88, 9, 7)
    + '<circle cx="566" cy="108" r="34" fill="none" stroke="var(--ink)" stroke-width="2"/>'
    + _t(566, 178, "Essaimant, avec matriarche", "Swarming, with a matriarch", size=13, weight="700")
    + _t(566, 198, "il contamine les nids voisins", "it seeds the neighboring nests", size=12, fill="var(--ink2)")
    + _t(14, 24, "Le temps joue contre le joueur : un nid ignoré devient une région perdue.", "Time works against the player: an ignored nest becomes a lost region.", anchor="start", size=12.5, fill="var(--ink2)")
)
FIGS["monsters_nest"] = (_svg("0 0 700 214", _nests),
    "Les monstres n'apparaissent plus de nulle part : ils sortent d'un nid qui vieillit.",
    "Monsters no longer appear from nowhere: they come out of a nest that ages.")

# --- Smith : la decomposition ---------------------------------------------
_smith = (
    '<g transform="translate(96,104)"><polygon points="-10,-58 10,-58 10,26 0,40 -10,26" fill="#cdd2d8" stroke="#9aa3ad"/></g>'
    + _t(96, 168, "Lame", "Blade", size=13, weight="700")
    + _t(96, 188, "forgée au marteau", "hammer forged", size=12, fill="var(--ink2)")
    + _t(186, 112, "+", "+", size=22, fill="var(--ink2)")
    + '<g transform="translate(276,104)"><rect x="-40" y="-8" width="80" height="16" rx="3" fill="#c2a05a" stroke="#9b7f42"/></g>'
    + _t(276, 168, "Garde", "Guard", size=13, weight="700")
    + _t(276, 188, "craft simple", "simple craft", size=12, fill="var(--ink2)")
    + _t(366, 112, "+", "+", size=22, fill="var(--ink2)")
    + '<g transform="translate(456,104)"><rect x="-8" y="-34" width="16" height="68" rx="5" fill="#8a6a44" stroke="#6d5335"/></g>'
    + _t(456, 168, "Manche", "Handle", size=13, weight="700")
    + _t(456, 188, "craft simple", "simple craft", size=12, fill="var(--ink2)")
    + _har(516, 566, 104)
    + '<g transform="translate(624,104)"><polygon points="-9,-62 9,-62 9,4 0,16 -9,4" fill="#cdd2d8" stroke="#9aa3ad"/>'
      '<rect x="-26" y="10" width="52" height="11" rx="3" fill="#c2a05a" stroke="#9b7f42"/>'
      '<rect x="-6" y="20" width="12" height="42" rx="4" fill="#8a6a44" stroke="#6d5335"/></g>'
    + _t(624, 180, "Assemblage à l'établi", "Assembly at the bench", size=13, weight="700")
    + _t(14, 26, "L'objet visé est lu, puis décomposé : la forge se déduit de l'objet, pas d'une liste écrite.", "The target item is read, then broken down: the forge is derived from the item, not from a written list.", anchor="start", size=12.5, fill="var(--ink2)")
)
FIGS["smith_parts"] = (_svg("0 0 700 206", _smith),
    "Une épée n'est plus une recette : c'est trois pièces, dont une se mérite au marteau.",
    "A sword is no longer a recipe: it is three pieces, one of which is earned at the hammer.")

# --- Farms : le champ ------------------------------------------------------
def _cell(x, y, state):
    fills = {"ok": "#7f9e57", "sick": "#b8543f", "risk": "#c8a24a", "comp": "#4f8a8a"}
    return (f'<rect x="{x}" y="{y}" width="46" height="46" rx="3" fill="{fills[state]}" fill-opacity=".55" '
            f'stroke="{fills[state]}"/>')

_layout = [
    ["ok", "ok", "sick", "risk", "ok", "ok", "comp", "ok"],
    ["ok", "risk", "sick", "sick", "risk", "ok", "comp", "ok"],
    ["ok", "ok", "risk", "sick", "ok", "ok", "comp", "ok"],
]
_grid = "".join(_cell(30 + c * 54, 40 + r * 54, st)
                for r, row in enumerate(_layout) for c, st in enumerate(row))
_farms = (
    _grid
    + '<rect x="356" y="34" width="58" height="166" rx="4" fill="none" stroke="#4f8a8a" stroke-dasharray="5 4"/>'
    + _t(30, 26, "Un champ n'est plus une rangée de cases identiques.", "A field is no longer a row of identical tiles.", anchor="start", size=12.5, fill="var(--ink2)")
    + '<rect x="470" y="46" width="14" height="14" rx="2" fill="#b8543f" fill-opacity=".55" stroke="#b8543f"/>'
    + _t(494, 58, "Malade, contamine ses voisines", "Diseased, infects its neighbors", anchor="start", fill="var(--ink2)")
    + '<rect x="470" y="86" width="14" height="14" rx="2" fill="#c8a24a" fill-opacity=".55" stroke="#c8a24a"/>'
    + _t(494, 98, "Exposée, ou trop mûre", "Exposed, or overripe", anchor="start", fill="var(--ink2)")
    + '<rect x="470" y="126" width="14" height="14" rx="2" fill="#4f8a8a" fill-opacity=".55" stroke="#4f8a8a"/>'
    + _t(494, 138, "Compagne, protège sa rangée", "Companion, shields its row", anchor="start", fill="var(--ink2)")
    + '<rect x="470" y="166" width="14" height="14" rx="2" fill="#7f9e57" fill-opacity=".55" stroke="#7f9e57"/>'
    + _t(494, 178, "Saine", "Healthy", anchor="start", fill="var(--ink2)")
)
FIGS["farms_grid"] = (_svg("0 0 700 216", _farms),
    "Espacer, alterner, intercaler : l'agencement du champ devient une décision.",
    "Spacing, alternating, interleaving: the field layout becomes a decision.")

# --- Combat : les zones ----------------------------------------------------
_combat = (
    '<g transform="translate(150,0)" fill="#b9b2a4" stroke="#8f887a">'
    '<circle cx="0" cy="46" r="26"/>'
    '<rect x="-30" y="78" width="60" height="86" rx="10"/>'
    '<rect x="-54" y="82" width="20" height="76" rx="9"/><rect x="34" y="82" width="20" height="76" rx="9"/>'
    '<rect x="-26" y="168" width="22" height="70" rx="9"/><rect x="4" y="168" width="22" height="70" rx="9"/>'
    '</g>'
    + '<circle cx="150" cy="46" r="30" fill="none" stroke="var(--c)" stroke-dasharray="4 4"/>'
    + '<rect x="112" y="74" width="76" height="94" rx="10" fill="none" stroke="var(--c)" stroke-dasharray="4 4"/>'
    + '<rect x="90" y="78" width="26" height="84" rx="9" fill="none" stroke="var(--c)" stroke-dasharray="4 4"/>'
    + '<rect x="120" y="164" width="60" height="78" rx="9" fill="none" stroke="var(--c)" stroke-dasharray="4 4"/>'
    + _har(200, 268, 46) + _t(280, 51, "Tête : étourdissement", "Head: stagger", anchor="start", weight="600")
    + _har(200, 268, 120) + _t(280, 125, "Torse : recul, souffle coupé", "Torso: knockback, winded", anchor="start", weight="600")
    + _har(200, 268, 176) + _t(280, 181, "Bras : l'arme peut lâcher", "Arm: the weapon may drop", anchor="start", weight="600")
    + _har(200, 268, 226) + _t(280, 231, "Jambes : titubement, chute", "Legs: stumble, fall", anchor="start", weight="600")
    + _t(280, 76, "Une hitbox par membre, pas une boîte unique.", "One hitbox per limb, not a single box.", anchor="start", size=12.5, fill="var(--ink2)")
    + _t(280, 150, "La réaction dépend de la zone et des dégâts.", "The reaction depends on the zone and the damage.", anchor="start", size=12.5, fill="var(--ink2)")
    + _t(280, 206, "Le geste dépend du poids de l'arme.", "The gesture depends on the weapon weight.", anchor="start", size=12.5, fill="var(--ink2)")
    + _t(280, 256, "Ces réactions arrivent par paliers, du sûr au risqué.", "These reactions land in stages, from safe to risky.", anchor="start", size=12.5, fill="var(--ink2)")
)
FIGS["combat_zones"] = (_svg("0 0 700 268", _combat),
    "Frapper cesse d'être un jet de dés contre une boîte : la zone touchée raconte le coup.",
    "Striking stops being a dice roll against a box: the zone hit tells the story of the blow.")

# --- Animals : la chaine ---------------------------------------------------
_chain = (
    _box(14, 44, 116, 50, "Flore", "Flora")
    + _har(134, 168, 69)
    + _box(172, 44, 130, 50, "Herbivores", "Herbivores")
    + _har(306, 340, 69)
    + _box(344, 44, 130, 50, "Prédateurs", "Predators")
    + _har(478, 512, 69)
    + _box(516, 44, 170, 50, "Charognards", "Scavengers")
    + '<path d="M601,98 L601,140 L72,140 L72,102" fill="none" stroke="var(--c)" stroke-width="2" stroke-dasharray="6 4"/>'
    + '<polygon points="72,94 67.5,103 76.5,103" fill="var(--c)"/>'
    + _t(350, 162, "la carcasse retourne au sol, et la boucle se referme", "the carcass returns to the soil, and the loop closes", size=12.5, fill="var(--ink2)")
    + _t(14, 26, "Chaque maillon se régule tout seul. Le joueur n'est qu'un prédateur de plus.", "Each link regulates itself. The player is just one more predator.", anchor="start", size=12.5, fill="var(--ink2)")
)
FIGS["animals_chain"] = (_svg("0 0 700 180", _chain),
    "Surchasser un maillon vide la zone : l'écosystème répond, il ne se recharge pas.",
    "Overhunting one link empties the area: the ecosystem answers back, it does not respawn.")


# --------------------------------------------------------------------------
# Contenu des modules
# --------------------------------------------------------------------------
CONC = [

# ============================== SEASON ====================================
("seasons", "Season", "#c8912f",
 ("Le climat de fond, et la source à laquelle tous les autres modules puisent.",
  "The background climate, and the source every other module draws from."),
 [
  ("Le climat comme fondation", "Climate as a foundation", [
    ("Season ne cherche pas à décorer l'année : il installe sous le monde un climat de fond que tout le reste consultera. Un calendrier paramétrable rythme le cycle, une saison durant deux semaines de jeu par défaut, et fournit les variables climatiques de base, la température en premier.",
     "Season is not out to decorate the year: it installs a background climate beneath the world that everything else will consult. A configurable calendar paces the cycle, a season lasting two in-game weeks by default, and provides the base climate variables, temperature first."),
    ("Ces variables ne sont pas décoratives non plus. Elles décident de la pluie et de la neige, de ce qui pousse, de ce qui migre, de ce qui mord à l'hameçon. Season est la source de vérité du climat pour toute la suite.",
     "Those variables are not decorative either. They decide rain and snow, what grows, what migrates, what bites the hook. Season is the suite's source of truth for climate."),
  ], None),
  ("Une carte en anneaux", "A map of rings", [
    ("Le climat ne suit pas un dégradé nord-sud, qui obligerait à marcher toujours dans la même direction pour changer d'air. Il s'organise en anomalies concentriques autour du point d'apparition : des cercles chauds, tempérés et froids qui se répètent à mesure que l'on s'éloigne.",
     "Climate does not follow a north-south gradient, which would force you to always walk the same way to change airs. It is organized as concentric anomalies around the spawn point: hot, temperate and cold circles repeating as you move away."),
    ("Des règles d'interdépendance tiennent l'ensemble crédible : les zones chaudes restent sèches et ignorent la neige, les zones froides cumulent neige et pluie, et ce sont les zones tempérées intermédiaires qui reçoivent le plus de précipitations.",
     "Interdependence rules keep the whole thing believable: hot zones stay dry and never see snow, cold zones stack snow and rain, and the intermediate temperate zones get the most rainfall."),
  ], "season_rings"),
  ("Ce qui bouge, ce qui reste", "What moves, what stays", [
    ("Un désert ne devient pas polaire en hiver. Les extrêmes ne bougent quasiment pas d'une saison à l'autre : ce sont les zones tempérées qui oscillent réellement entre chaud et froid, et ce sont donc elles qui vivent les saisons au sens où on l'entend.",
     "A desert does not turn polar in winter. The extremes barely move from season to season: it is the temperate zones that truly swing between hot and cold, and so they are the ones that live the seasons as we mean them."),
    ("Le passage d'une saison à l'autre se fait par glissement continu, en interpolant jour après jour entre les profils, plutôt que par une bascule brutale. La température glisse au lieu de sauter, dans le même esprit que le fondu d'une journée.",
     "The move from one season to the next happens by continuous drift, interpolating day after day between profiles, rather than by an abrupt switch. Temperature slides instead of jumping, in the same spirit as a day's fade."),
  ], "season_swing"),
  ("Des saisons qui voyagent", "Traveling seasons", [
    ("Puisque le climat est concentrique, la phase des saisons peut être décalée selon la distance au point d'apparition : l'anneau tempéré vit son été pendant que l'anneau voisin entre en automne. Les saisons se déplacent alors dans le monde au lieu de tomber partout en même temps.",
     "Since the climate is concentric, the phase of the seasons can be offset by distance to the spawn point: the temperate ring lives its summer while the neighboring ring enters autumn. Seasons then travel through the world instead of landing everywhere at once."),
    ("Cela donne une vraie raison de bouger, et fournit au passage un moteur naturel aux migrations animales : le troupeau ne suit pas un scénario, il suit le climat.",
     "That gives a real reason to move, and incidentally provides a natural engine for animal migrations: the herd does not follow a script, it follows the climate."),
  ], None),
  ("Lire l'année sans interface", "Reading the year without an interface", [
    ("Aucune barre de saison ne s'affiche à l'écran. La saison se lit dans le monde, et si un objet doit la dire, il est fabricable et tenu en main : un almanach qui indique la saison en cours et celle qui vient.",
     "No season bar shows on screen. The season is read from the world, and if an object must state it, that object is craftable and held in hand: an almanac showing the current season and the next."),
    ("L'année peut aussi réserver ses exceptions. Une canicule ou un grand gel, rares, annoncés à l'avance, mettent sous tension tous les modules qui dépendent du climat. Un pic que l'on peut anticiper vaut mieux qu'une moyenne toujours tiède.",
     "The year can also hold its exceptions. A heat wave or a deep freeze, rare and telegraphed in advance, put every climate-dependent module under strain. A spike you can plan for beats a forever-lukewarm average."),
  ], None),
  ("Le pivot de la suite", "The suite's pivot", [
    ("Season publie, les autres réagissent. Weather en tire sa simulation, Water le devenir de la pluie, Biome la densité de sa flore, Farms le rendement de ses cultures, Animals ses migrations, Fishing ce qui mord. Le climat cesse d'être un décor pour devenir le premier moteur du monde.",
     "Season publishes, the others react. Weather derives its simulation from it, Water the fate of the rain, Biome the density of its flora, Farms the yield of its crops, Animals its migrations, Fishing what bites. Climate stops being scenery and becomes the world's prime mover."),
  ], None),
 ]),

# ============================== WEATHER ===================================
("weather", "Weather", "#5a90c4",
 ("Une simulation atmosphérique complète, déduite maillon par maillon depuis la température.",
  "A full atmospheric simulation, derived link by link from temperature."),
 [
  ("Une simulation, pas un réglage", "A simulation, not a setting", [
    ("La pluie vanilla est un interrupteur : il pleut, ou il ne pleut pas. Weather remplace cet interrupteur par une chaîne de causes. La température est la variable maîtresse ; un écart de température crée un écart de pression, la carte de pression détermine le vent, et le vent déplace la carte météo, qui fixe à son tour l'emplacement des nuages.",
     "Vanilla rain is a switch: it rains, or it does not. Weather replaces that switch with a chain of causes. Temperature is the master variable; a temperature gap creates a pressure gap, the pressure map determines wind, and wind moves the weather map, which in turn sets where the clouds are."),
    ("Rien n'est tiré au sort au moment où l'on regarde le ciel. Tout a été décidé en amont, par des grandeurs qui ont un sens, et c'est ce qui rend le ciel lisible.",
     "Nothing is rolled at the moment you look up. Everything was decided upstream, by quantities that mean something, and that is what makes the sky readable."),
  ], "weather_cascade"),
  ("La vie d'un nuage", "The life of a cloud", [
    ("Les nuages naissent surtout au-dessus des mers et se laissent porter par les vents. Chacun possède une cumulation, qui augmente quand deux nuages fusionnent. Au-delà d'un seuil, le nuage déclenche un événement d'humidité, pluie, neige ou orage selon la température locale, jusqu'à ce que sa cumulation retombe.",
     "Clouds are born mostly over the seas and let the winds carry them. Each holds an accumulation, which rises when two clouds merge. Past a threshold, the cloud triggers a humidity event, rain, snow or storm depending on local temperature, until its accumulation falls back."),
    ("Un changement brusque de pression, lui, ne donne pas de la pluie mais du vent : bourrasque, tempête, tornade. Deux causes distinctes, deux familles d'événements, et un ciel dont on peut apprendre la grammaire.",
     "A sudden pressure change, on the other hand, yields not rain but wind: gusts, storms, tornadoes. Two distinct causes, two families of events, and a sky whose grammar can be learned."),
  ], None),
  ("Lire le ciel", "Reading the sky", [
    ("Puisque la simulation est causale, elle est prévisible, et cette prévision revient au joueur plutôt qu'à une interface. Des instruments fabricables la donnent dans le monde : un baromètre dont l'aiguille monte ou descend, une girouette qui trahit la tournure du vent.",
     "Since the simulation is causal, it is predictable, and that forecast belongs to the player rather than to an interface. Craftable instruments deliver it in the world: a barometer whose needle rises or falls, a weather vane that betrays the turn of the wind."),
    ("Une tendance vaut mieux qu'une certitude. Elle laisse le choix de rentrer les récoltes, de partir malgré tout, ou de parier sur une accalmie.",
     "A trend beats a certainty. It leaves room to bring the harvest in, to set out anyway, or to bet on a lull."),
  ], None),
  ("Le relief fabrique ses climats", "Terrain makes its own climates", [
    ("Les montagnes bloquent les nuages : le versant au vent reçoit la pluie, le versant sous le vent reste sec. L'altitude, elle, refroidit. Des microclimats émergent ainsi du terrain lui-même, sans qu'aucune donnée supplémentaire ait à être écrite.",
     "Mountains block clouds: the windward slope takes the rain, the leeward slope stays dry. Altitude, for its part, cools. Microclimates emerge from the terrain itself, with no extra data to write."),
  ], None),
  ("Des tempêtes qui laissent une trace", "Storms that leave a mark", [
    ("Un événement météo agit sur le monde au lieu de le repeindre. Une tempête réduit la visibilité et disperse les nuages ; la foudre peut allumer un feu dans la flore ou dans un champ, ou être captée par qui s'y prépare. Certains phénomènes deviennent plus probables à certaines saisons, ce qui ancre la météo dans le cycle de l'année.",
     "A weather event acts on the world instead of repainting it. A storm cuts visibility and scatters the clouds; lightning can set fire to flora or to a field, or be captured by whoever prepares for it. Some phenomena grow likelier in certain seasons, anchoring weather in the year's cycle."),
  ], None),
  ("Tenir la performance", "Holding performance", [
    ("Une simulation globale ne peut pas se payer à la résolution du bloc. Elle tourne donc sur une grille grossière à l'échelle du monde, et le détail n'émerge que dans la distance de rendu, là où le joueur peut le voir.",
     "A global simulation cannot be paid for at block resolution. It therefore runs on a coarse grid at world scale, and detail emerges only within render distance, where the player can actually see it."),
    ("Deux cartes cohabitent : l'une procédurale pour les régions jamais visitées, l'autre nourrie par les données de biome pour les zones explorées. Leur interaction fait dériver l'ensemble dans le temps, et la couture entre les deux est lissée par un fondu étalé sur une journée complète.",
     "Two maps coexist: a procedural one for never-visited regions, another fed by biome data for explored areas. Their interaction makes the whole drift over time, and the seam between them is smoothed by a fade spread across a full day."),
  ], None),
 ]),

# =============================== WATER ====================================
("water", "Water", "#2f8fbd",
 ("Ce que la pluie devient une fois au sol. Le morceau le plus lourd de la suite.",
  "What rain becomes once it hits the ground. The heaviest piece of the suite."),
 [
  ("La pluie a une suite", "Rain has a sequel", [
    ("Weather s'arrête quand la goutte touche le sol. Water commence exactement là. La pluie sature la terre, percole, gonfle les rivières, remplit les creux, et peut finir par noyer une grotte ou une cave. L'eau gagne une verticale qu'elle n'avait pas.",
     "Weather stops when the drop lands. Water starts exactly there. Rain saturates the ground, percolates, swells the rivers, fills the hollows, and can end up drowning a cave or a cellar. Water gains a vertical axis it never had."),
    ("Le module vise un vrai moteur aquatique : un courant plus ou moins fort, du débordement, de l'assèchement, des points d'eau qui ne sont plus des sources infinies, et une dynamique de rivières.",
     "The module targets a real water engine: current of varying strength, overflow, drying, water bodies that are no longer infinite sources, and river dynamics."),
  ], "water_section"),
  ("La frontière honnête", "The honest boundary", [
    ("Water est jugé théoriquement viable mais mécaniquement difficile, et une ligne nette se dégage. L'érosion, c'est-à-dire un terrain qui se transforme dans le temps, est le vrai mur, peut-être infranchissable dans un jeu où le sol est un tableau de blocs.",
     "Water is judged theoretically viable but mechanically hard, and a clear line emerges. Erosion, meaning terrain that transforms over time, is the real wall, perhaps impassable in a game where the ground is an array of blocks."),
    ("Tout le reste, simulé sur terrain fixe, est bien plus accessible, presque plus simple que la météo. La feuille de route en tient compte : d'abord une eau complète et jouable sur terrain fixe, ensuite seulement, et séparément, la question de l'érosion.",
     "Everything else, simulated on fixed terrain, is far more reachable, almost simpler than weather. The roadmap reflects that: first a complete, playable water on fixed terrain, and only then, separately, the question of erosion."),
  ], None),
  ("Une eau qui a un état", "Water with a state", [
    ("Toute l'eau ne se vaut plus. Une eau courante et une eau stagnante ne se boivent pas de la même façon, n'abritent pas les mêmes espèces et n'irriguent pas un champ avec le même résultat. La différence se voit avant de se subir.",
     "Not all water is equal anymore. Running water and standing water are not drunk the same way, do not shelter the same species and do not irrigate a field to the same effect. The difference is visible before it is suffered."),
    ("En hiver, les points d'eau gèlent puis dégèlent. Une rivière prise devient un chemin, un lac gelé devient un plafond sous lequel on peut encore pêcher, et le paysage change sans qu'aucun bloc de terrain n'ait bougé.",
     "In winter, water bodies freeze then thaw. A frozen river becomes a road, a frozen lake becomes a ceiling you can still fish under, and the landscape changes without a single terrain block moving."),
  ], None),
  ("Creuser, détourner, retenir", "Digging, diverting, holding", [
    ("Sous le sol, une nappe alimentée par l'infiltration monte et descend avec les saisons et la météo. Creuser un puits cesse d'être décoratif : c'est atteindre une ressource dynamique, qui peut manquer.",
     "Below ground, a table fed by seepage rises and falls with the seasons and the weather. Digging a well stops being decorative: it means reaching a dynamic resource, one that can run short."),
    ("En surface, canaux, digues, drainage et irrigation permettent de conduire l'eau sur un terrain qui, lui, ne bouge pas. De quoi arroser un champ, assécher un fond, ou remplir une douve devant un nid de monstres.",
     "On the surface, canals, dikes, drainage and irrigation let water be led across terrain that itself does not move. Enough to water a field, drain a hollow, or fill a moat in front of a monster nest."),
  ], None),
 ]),

# =============================== BIOME ====================================
("biome", "Biome", "#7d8590",
 ("Reposer la flore et la faune du monde existant, et ouvrir l'éditeur aux joueurs.",
  "Re-placing the flora and fauna of the existing world, and opening the editor to players."),
 [
  ("Repeupler plutôt que régénérer", "Repopulating rather than regenerating", [
    ("Biome ne refait pas le terrain : il repose ce qui pousse et ce qui vit dessus. La végétation et les animaux sont distribués par un semis procédural, à partir des données du biome et de celles de Season, avec une densité et une rareté calibrées puis réajustées au fil de l'année.",
     "Biome does not remake the terrain: it re-places what grows and what lives on it. Vegetation and animals are distributed by procedural scattering, from the biome's data and Season's, with density and rarity calibrated then readjusted through the year."),
    ("Un même sous-bois n'a donc pas la même allure en avril et en novembre, sans qu'aucun contenu saisonnier n'ait été écrit à la main.",
     "The same undergrowth therefore does not look alike in April and November, with no seasonal content written by hand."),
  ], None),
  ("Des lisières, pas des frontières", "Edges, not borders", [
    ("Dans le monde vanilla, deux biomes se touchent le long d'une ligne, et le changement est net au pas près. Biome génère de vraies zones de transition : une bande où les deux flores se mêlent en dégradé, la densité de l'une s'effaçant à mesure que l'autre s'installe.",
     "In the vanilla world, two biomes meet along a line, and the change is sharp to the step. Biome generates real transition zones: a band where both floras blend in a gradient, one thinning out as the other settles in."),
    ("C'est un des changements les plus rentables du module : le monde gagne énormément en organicité pour un coût modéré.",
     "It is one of the module's best returns: the world gains a great deal of organic feel for a moderate cost."),
  ], "biome_ecotone"),
  ("Donner un climat aux biomes moddés", "Giving modded biomes a climate", [
    ("L'ambition est d'assigner à chaque biome un profil climatique par défaut, une température et une humidité : savane chaude et humide, neige froide et très humide, forêt de chênes tempérée et modérée. Le problème est que Minecraft n'expose pas ces profils pour les biomes ajoutés par les mods.",
     "The ambition is to assign each biome a default climate profile, a temperature and a humidity: savanna hot and humid, snow cold and very humid, oak forest temperate and moderate. The problem is that Minecraft does not expose those profiles for mod-added biomes."),
    ("Deux voies cohabitent plutôt que de s'exclure. Un tag climatique peut être déclaré dans l'éditeur, et à défaut le profil est déduit du contenu du biome : sable et buissons morts pour du chaud et sec, neige et glace pour du froid, eau et lianes pour de l'humide. La déduction est mise en cache dès le premier scan, expose son niveau de confiance, et le tag déclaré sert d'arbitrage propre quand elle hésite.",
     "Two paths coexist rather than exclude each other. A climate tag can be declared in the editor, and failing that the profile is inferred from the biome's contents: sand and dead bushes for hot and dry, snow and ice for cold, water and vines for humid. The inference is cached from the first scan, exposes its confidence level, and the declared tag serves as a clean override when it hesitates."),
  ], None),
  ("Récompenser le détour", "Rewarding the detour", [
    ("De petites anomalies sont semées à faible probabilité : une clairière, une oasis, un bosquet qui n'existe nulle part ailleurs, avec la flore ou la faune rare qui va avec. Explorer redevient une façon de trouver, pas seulement de traverser.",
     "Small anomalies are seeded at low probability: a clearing, an oasis, a grove that exists nowhere else, with the rare flora or fauna that comes with it. Exploring becomes a way of finding again, not merely of crossing."),
    ("L'oreille est servie comme l'oeil. Une ambiance sonore procédurale peut se dériver du profil climatique et de la faune présente, insectes dans la chaleur humide, vent dans le froid : l'ASMR étendu au son.",
     "The ear is served like the eye. A procedural soundscape can be derived from the climate profile and the fauna present, insects in humid heat, wind in the cold: the ASMR extended to sound."),
  ], None),
  ("Un éditeur de biomes", "A biome editor", [
    ("Comme ailleurs dans la suite, les règles ne restent pas enfermées dans le code. Un éditeur permet de composer ses propres biomes, leur flore, leur faune, leurs règles de semis, et d'y intégrer directement les arbres façonnés dans Tactile:Wood.",
     "As elsewhere in the suite, the rules do not stay locked in code. An editor allows composing your own biomes, their flora, their fauna, their scattering rules, and dropping in the trees shaped in Tactile:Wood."),
  ], None),
 ]),

# ============================== ANIMALS ===================================
("animals", "Animals", "#b4894f",
 ("Un écosystème qui tourne sans le joueur, un élevage qui se mérite, une chasse entièrement gestuelle.",
  "An ecosystem that runs without the player, husbandry that is earned, hunting done entirely by hand."),
 [
  ("Un monde animal qui ne l'attend pas", "An animal world that is not waiting", [
    ("Les animaux vanilla existent pour être trouvés. Ici, ils existent d'abord entre eux : interactions inter-espèces, territoires, reproduction, chasse, et une régulation des populations qui se fait toute seule. Le joueur n'est qu'un prédateur de plus dans le tableau.",
     "Vanilla animals exist to be found. Here, they exist among themselves first: cross-species interactions, territories, breeding, hunting, and population regulation that happens on its own. The player is just one more predator in the picture."),
    ("Une carcasse abandonnée attire des charognards, ce qui rend la chaîne alimentaire visible et referme la boucle : ce qui meurt nourrit, puis retourne au sol.",
     "An abandoned carcass draws scavengers, which makes the food chain visible and closes the loop: what dies feeds, then returns to the soil."),
  ], "animals_chain"),
  ("Des comportements crédibles", "Believable behavior", [
    ("Chaque espèce occupe la place qui lui ressemble : le loup tient un territoire en montagne et en forêt, les moutons vont en troupeaux dans les plaines. Une carte de migration reliée à Season et Weather déplace ces populations au fil de l'année, plutôt que de les figer là où elles sont nées.",
     "Each species holds the place that suits it: the wolf keeps a territory in mountains and forests, sheep move in flocks across the plains. A migration map tied to Season and Weather shifts those populations through the year, rather than freezing them where they were born."),
    ("Une zone surchassée se vide temporairement, et ne se remplit qu'au rythme où la population se refait. Le gibier devient une ressource, pas un distributeur.",
     "An overhunted area empties temporarily, and refills only as fast as the population recovers. Game becomes a resource, not a dispenser."),
  ], None),
  ("L'élevage se mérite", "Husbandry is earned", [
    ("Les animaux ont peur du joueur par défaut. Il n'y a plus de vache qui suit un épi de blé après deux secondes : l'apprivoisement passe par la laisse, ou par une présence régulière jusqu'à l'habituation. Un troupeau se construit dans la durée.",
     "Animals fear the player by default. No more cow following a stalk of wheat after two seconds: taming goes through the leash, or through regular presence until the animal grows used to you. A herd is built over time."),
    ("La bête se souvient. Un animal apprivoisé reconnaît son éleveur, et un troupeau qui a été surchassé devient plus farouche et fuit de plus loin. Le comportement répond à l'histoire du joueur.",
     "The animal remembers. A tamed beast recognizes its keeper, and a herd that has been overhunted grows warier and flees from further away. Behavior answers the player's history."),
    ("Sur plusieurs générations, les traits se transmettent procéduralement, la taille, le tempérament, la robe. Sélectionner devient un objectif de long terme, et un troupeau finit par ressembler à celui qui l'a élevé.",
     "Across generations, traits pass down procedurally, size, temperament, coat. Selective breeding becomes a long-term goal, and a herd ends up resembling whoever raised it."),
  ], None),
  ("La chasse est une suite de gestes", "Hunting is a sequence of gestures", [
    ("Abattre une bête ne fait rien tomber au sol. Il faut la dépecer, découper la viande, tanner le cuir, récupérer les os : chaque ressource est une étape, avec son geste, et non une ligne de butin.",
     "Killing a beast drops nothing on the ground. It must be skinned, the meat cut, the hide tanned, the bones recovered: each resource is a step, with its own gesture, not a loot line."),
    ("Avant l'abattage, il y a la traque. Les animaux laissent des traces, empreintes, poils, indices, que le chasseur apprend à lire. Chasser, c'est d'abord lire le monde.",
     "Before the kill comes the track. Animals leave signs, prints, hair, clues, that the hunter learns to read. To hunt is first to read the world."),
  ], None),
  ("Ouvert au contenu moddé", "Open to modded content", [
    ("La prise en charge des animaux ajoutés par les mods se fait par tags de famille et de comportement, sans liste écrite espèce par espèce. Des animaux maison peuvent s'ajouter par la même porte.",
     "Support for mod-added animals goes through family and behavior tags, with no list written species by species. Custom animals come in through the same door."),
  ], None),
 ]),

# ============================== MONSTERS ==================================
("monsters", "Monsters", "#9161bd",
 ("Le pendant hostile d'Animals : plus de spawn aléatoire, mais des nids qui essaiment.",
  "The hostile counterpart to Animals: no random spawns, but nests that swarm."),
 [
  ("Les monstres viennent de quelque part", "Monsters come from somewhere", [
    ("Le spawn aléatoire est remplacé par une distribution logique, qui suit Biome et Season et ancre chaque monstre à un élément proche : l'araignée et sa toile, le zombie et une structure voisine, le creeper et les forêts.",
     "Random spawning is replaced by a logical distribution, following Biome and Season and anchoring each monster to something nearby: the spider and its web, the zombie and a neighboring structure, the creeper and the forests."),
    ("Au coeur du module, les monstres ne se matérialisent plus du tout. Seuls des nids apparaissent, et chaque nid diffuse peu à peu ses monstres autour de lui. Plus il perdure, plus il en produit ; détruire le nid tarit la source.",
     "At the module's core, monsters no longer materialize at all. Only nests appear, and each nest slowly seeds its monsters around it. The longer it lasts, the more it produces; destroying the nest dries up the source."),
  ], "monsters_nest"),
  ("Un nid se reconnaît de loin", "A nest is recognizable from afar", [
    ("Un nid est visuellement composé de morceaux de l'entité qu'il abrite et de son butin, ce qui le rend identifiable au premier regard, sans notification ni marqueur.",
     "A nest is visually built from pieces of the entity it shelters and of its loot, which makes it identifiable at a glance, with no notification and no marker."),
    ("Son âge se lit aussi sur lui. Des phases visibles, jeune, mature, essaimant, télégraphient sa maturité, ce qui permet de choisir lequel nettoyer en premier au lieu de tous les traiter pareil.",
     "Its age can be read on it too. Visible phases, young, mature, swarming, telegraph its maturity, which allows choosing which one to clear first instead of treating them all alike."),
  ], None),
  ("La matriarche", "The matriarch", [
    ("Chaque nid abrite une matriarche, version renforcée du monstre qui gagne en puissance avec l'âge. Elle n'est pas dessinée à la main : elle est générée procéduralement depuis l'entité de base, attributs, échelle, son, textures, voire déformation du squelette, ce qui la rend disponible pour n'importe quel monstre, vanilla ou moddé.",
     "Each nest shelters a matriarch, a reinforced version of the monster that grows stronger with age. She is not hand-drawn: she is generated procedurally from the base entity, attributes, scale, sound, textures, even skeleton deformation, which makes her available for any monster, vanilla or modded."),
    ("Sa présentation compte autant que ses statistiques : un cri long et intense, un léger tremblement de caméra, des déplacements ralentis, des pas lourds. On sait qu'elle est là avant de la voir.",
     "Her presentation matters as much as her stats: a long, intense cry, a slight camera shake, slowed movement, heavy steps. You know she is there before you see her."),
    ("Ce qu'elle laisse en mourant dépend de son âge et de son espèce, ce qui rend la récompense proportionnelle au risque pris, et donne de la matière à forger.",
     "What she leaves behind on death depends on her age and species, which makes the reward proportional to the risk taken, and gives material worth forging."),
  ], None),
  ("Des territoires, et des rivalités", "Territories, and rivalries", [
    ("Une carte de territoire définie au chunk décide quel monstre peuple quelle zone, et les nids adjacents se diffusent mutuellement. Deux territoires voisins d'espèces différentes peuvent entrer en conflit et s'affaiblir : il devient possible d'exploiter une rivalité plutôt que de tout affronter.",
     "A chunk-level territory map decides which monster populates which area, and adjacent nests seed each other. Two neighboring territories of different species can come into conflict and weaken each other: it becomes possible to exploit a rivalry instead of fighting everything."),
  ], None),
  ("La cicatrice au sol", "The scar on the ground", [
    ("Un nid ancien marque le terrain autour de lui, toiles, brûlure, ronces. Tuer la source ne suffit pas : il reste à nettoyer ce qu'elle a laissé. L'éradication devient un acte en deux temps, et le paysage raconte l'infestation longtemps après.",
     "An old nest marks the ground around it, webs, scorch, brambles. Killing the source is not enough: what it left behind still has to be cleared. Eradication becomes a two-part act, and the landscape tells the story of the infestation long afterwards."),
  ], None),
 ]),

# =============================== FARMS ====================================
("farms", "Farms", "#c69a2b",
 ("Une agriculture qui demande de l'attention : maladie, péremption, agencement, fauchage.",
  "Agriculture that asks for attention: disease, spoilage, layout, scything."),
 [
  ("Un champ n'est plus une rangée de cases", "A field is no longer a row of tiles", [
    ("Le rendu est repris pour un champ dense et foisonnant, enrichi procéduralement plutôt que répété à l'identique. Sous le visuel, la culture repose sur de vraies données, l'arrosage, la température, la luminosité, auxquelles s'ajoute le cycle des saisons.",
     "The rendering is reworked for a dense, abundant field, procedurally enriched rather than repeated identically. Under the visuals, the crop relies on real data, watering, temperature, light, on top of the seasonal cycle."),
    ("Un champ cesse d'être un compte à rebours et redevient un lieu où l'on passe.",
     "A field stops being a countdown and becomes a place you tend again."),
  ], "farms_grid"),
  ("Deux tensions", "Two tensions", [
    ("La maladie peut tuer une récolte, et se propage aux plantes adjacentes : planter tout serré et tout pareil devient un risque assumé. La péremption fait le reste, une récolte laissée trop mûre ne donne presque plus rien.",
     "Disease can kill a harvest, and spreads to adjacent plants: planting everything tight and identical becomes a knowing risk. Spoilage does the rest, a harvest left overripe yields almost nothing."),
    ("Ces deux pressions transforment le champ en décision, alors qu'il n'était qu'une attente.",
     "Those two pressures turn the field into a decision, where it was only a wait."),
  ], None),
  ("Ce qui récompense le soin", "What rewards care", [
    ("À la propagation des maladies répond le compagnonnage : certaines cultures protègent leurs voisines ou augmentent leur rendement. L'agencement du champ devient un petit puzzle, qui récompense la diversité au lieu de la punir.",
     "Answering disease spread is companion planting: some crops shield their neighbors or raise their yield. The field layout becomes a small puzzle, rewarding diversity instead of punishing it."),
    ("Cultiver toujours la même plante au même endroit appauvrit le sol ; la rotation ou la jachère le régénèrent. Et là où les abeilles et les insectes vivent, près des ruches et des fleurs sauvages, le rendement monte, ce qui relie directement le champ à Biome et Animals.",
     "Always growing the same plant in the same spot depletes the soil; rotation or fallow restore it. And where bees and insects live, near hives and wildflowers, yield rises, tying the field directly to Biome and Animals."),
  ], None),
  ("Le fauchage", "The scything", [
    ("La récolte est un geste et non une collecte. Le fauchage fait chuter les épis au sol, où ils persistent, en tas, à la vue de tous, jusqu'à ce qu'on vienne les ramasser.",
     "Harvesting is a gesture, not a pickup. Scything drops the ears to the ground, where they linger, in heaps, in plain sight, until someone comes to gather them."),
    ("La tension se prolonge jusqu'au stockage : laissées dehors, les récoltes se dégradent avec le temps et l'humidité, que la météo fournit. Rentrer la moisson devient un geste qui compte.",
     "The tension carries on to storage: left outside, harvests degrade with time and humidity, which the weather provides. Bringing the crop in becomes a gesture that counts."),
  ], None),
 ]),

# =============================== SMITH ====================================
("smith", "Smith", "#cf7a2f",
 ("La forge remplace la grille de craft : décomposer, chauffer, marteler, assembler.",
  "The forge replaces the crafting grid: break down, heat, hammer, assemble."),
 [
  ("L'objet dicte la forge", "The item dictates the forge", [
    ("Un objet n'est plus une recette en trois par trois, mais un assemblage de parties : un manche, une garde, une lame, une tête d'outil. Chacune se fabrique séparément, puis l'ensemble se monte à l'établi.",
     "An item is no longer a three-by-three recipe, but an assembly of parts: a handle, a guard, a blade, a tool head. Each is made separately, then the whole is put together at the bench."),
    ("Le point important est le sens de lecture. Ce sont les objets existants, vanilla comme moddés, qui déterminent la forge : le mod prend l'objet visé comme résultat voulu, le décompose, et en dérive ce qu'il faut forger. La compatibilité avec tout l'arsenal vient donc gratuitement, sans qu'aucune recette n'ait été écrite à la main. C'est exactement la logique de Tactile:Wood avec les arbres.",
     "The important thing is the reading direction. Existing items, vanilla or modded, determine the forge: the mod takes the target item as the desired result, breaks it down, and derives what must be forged. Compatibility with the whole arsenal therefore comes for free, with no recipe written by hand. It is exactly the logic of Tactile:Wood with trees."),
  ], "smith_parts"),
  ("Forger une lame", "Forging a blade", [
    ("Le manche et la garde relèvent d'un craft simple. La lame, elle, se mérite. Il faut deux lingots, allumer la forge, et chauffer jusqu'à ce que le métal rougisse : une ébauche procédurale de lame brute apparaît alors.",
     "The handle and guard come from a simple craft. The blade is earned. It takes two ingots, lighting the forge, and heating until the metal glows red: a procedural rough blade then appears."),
    ("Chaque coup de marteau rapproche visuellement la pièce du résultat attendu. La forme sert de jauge : il n'y a pas de barre de progression, on regarde la lame devenir la lame. L'assemblage final se fait au maillet de bois.",
     "Each hammer blow visually brings the piece closer to the expected result. The shape is the gauge: there is no progress bar, you watch the blade become the blade. Final assembly is done with a wooden mallet."),
    ("La gestion de la chaleur est obligatoire, pas optionnelle. Une pièce qui refroidit ne se travaille plus, et il faut la remettre au feu.",
     "Heat management is mandatory, not optional. A cooling piece stops working, and must go back into the fire."),
  ], None),
  ("La main du forgeron reste dessus", "The smith's hand stays on it", [
    ("De subtiles marques procédurales issues du martelage peuvent être conservées sur l'objet fini. L'équipement forgé à la main devient alors unique, reconnaissable, sans le moindre impact sur l'équilibre : une récompense purement esthétique, et c'est très bien ainsi.",
     "Subtle procedural marks from the hammering can be kept on the finished item. Hand-forged gear then becomes unique, recognizable, with no impact whatsoever on balance: a purely aesthetic reward, and that is exactly right."),
    ("Autour de cette base, il y a de la place pour de la métallurgie : une étape de trempe à l'eau ou à l'huile, et la possibilité de mêler des matériaux dans une même lame, ce qui se voit sur la pièce.",
     "Around that base there is room for metallurgy: a quench step in water or oil, and the possibility of mixing materials in a single blade, which shows on the piece."),
  ], None),
  ("User, puis réparer", "Wear, then repair", [
    ("Les armes montrent procéduralement leur usure au fil des combats, ébréchures, patine, et ne se contentent plus d'une barre qui descend. Une arme émoussée se répare par re-martelage à la forge, ce qui restaure aussi son apparence.",
     "Weapons show their wear procedurally through combats, chips, patina, rather than settling for a bar going down. A blunted weapon is repaired by re-hammering at the forge, which restores its look as well."),
    ("La forge cesse d'être une étape de début de partie pour devenir un lieu où l'on revient.",
     "The forge stops being an early-game step and becomes a place you return to."),
  ], None),
  ("Les stations de forge y ont leur place", "The forge stations belong here", [
    ("L'enclume, la meule et la table de forge sont littéralement des stations de forge. Leur place logique est dans Smith, qui gère déjà la chaleur, le martelage et l'assemblage. Les y réunir renforcerait le module au lieu de disperser la suite, et éviterait d'entretenir deux systèmes de forge en parallèle.",
     "The anvil, the grindstone and the smithing table are literally forge stations. Their logical home is Smith, which already handles heat, hammering and assembly. Bringing them together there would strengthen the module instead of scattering the suite, and would avoid maintaining two parallel forge systems."),
    ("Aujourd'hui, elles vivent dans Tactile:Blocks et n'en bougent pas. Ce regroupement est une piste documentée pour plus tard, qui ne se fera pas sans transition annoncée, et jamais au prix des mondes déjà joués.",
     "Today they live in Tactile:Blocks and are not moving. This regrouping is a documented track for later, which will not happen without an announced transition, and never at the cost of worlds already played."),
  ], None),
 ]),

# ============================= ALCHEMY ====================================
("alchemy", "Alchemy", "#a1508f",
 ("L'alambic, sans doute l'interface la plus opaque du jeu, devient un vrai procédé visible.",
  "The brewing stand, arguably the game's most opaque interface, becomes a real visible process."),
 [
  ("Pourquoi un module à part", "Why a module of its own", [
    ("L'alambic est sans doute l'interface la plus opaque du jeu vanilla : trois fioles, un ingrédient, une barre qui descend, et aucun moyen de comprendre ce qui se passe. C'est exactement le genre de station qu'un module généraliste ne peut traiter qu'en surface.",
     "The brewing stand is arguably the most opaque interface in vanilla: three bottles, one ingredient, a bar going down, and no way to understand what is happening. It is exactly the kind of station a general-purpose module can only handle on the surface."),
    ("Un module dédié permettrait la profondeur que l'alchimie mérite. Aujourd'hui, le brassage reste dans Tactile:Blocks et rien n'en est retiré : ce qui suit est une piste, pas une annonce.",
     "A dedicated module would allow the depth alchemy deserves. Today, brewing stays in Tactile:Blocks and nothing is being taken out of it: what follows is a track, not an announcement."),
  ], None),
  ("Un procédé, pas un menu", "A process, not a menu", [
    ("Le geste remplacerait l'écran de bout en bout : broyer les ingrédients, les jeter dans un chaudron qui bout, voir la couleur virer et la préparation évoluer sous les yeux. Tout se lit dans le liquide, sans la moindre interface.",
     "The gesture would replace the screen from end to end: grinding the ingredients, dropping them into a boiling cauldron, watching the color turn and the mixture evolve before your eyes. Everything is read in the liquid, with no interface at all."),
    ("La chaleur du chaudron réutiliserait l'infrastructure de la forge plutôt que de la dupliquer : une même brique technique au service de deux modules.",
     "The cauldron's heat would reuse the forge's infrastructure rather than duplicate it: a single technical brick serving two modules."),
  ], None),
  ("Des recettes qui émergent", "Recipes that emerge", [
    ("Plutôt qu'une liste fixe d'associations, les effets d'une préparation pourraient se dériver procéduralement de ses ingrédients et de sa conduite, la température et la durée. L'expérimentation deviendrait alors le coeur du module, et non un tableau à consulter ailleurs.",
     "Rather than a fixed list of pairings, a mixture's effects could be derived procedurally from its ingredients and its handling, temperature and duration. Experimentation would then become the module's core, not a table to look up elsewhere."),
    ("Les composants eux-mêmes seraient vivants : la flore de Biome et le cycle de Season conditionneraient leur disponibilité et leur puissance, ce qui relierait l'alchimie à l'écosystème au lieu de l'en isoler.",
     "The components themselves would be alive: Biome's flora and Season's cycle would condition their availability and potency, tying alchemy to the ecosystem instead of isolating it from it."),
  ], None),
 ]),

# =========================== ENCHANTMENT ==================================
("enchantment", "Enchantment", "#4b52a8",
 ("La table d'enchantement devient un rituel physique, plutôt qu'un tirage derrière un menu.",
  "The enchanting table becomes a physical ritual, rather than a roll behind a menu."),
 [
  ("Approfondir, plutôt que simplifier", "Deepening, rather than simplifying", [
    ("C'est le cas typique où Tactile approfondit au lieu de simplifier. Enchanter ne devrait pas être un menu et un jet de dés, mais un rituel : disposer des éléments, préparer, et laisser la chose se dérouler dans le monde.",
     "This is the typical case where Tactile deepens instead of simplifying. Enchanting should not be a menu and a dice roll, but a ritual: laying out elements, preparing, and letting the thing unfold in the world."),
    ("Comme pour l'alchimie, rien n'est retiré de Tactile:Blocks aujourd'hui. L'enchantement y reste, et cette fiche décrit ce qu'un module dédié pourrait en faire.",
     "As with alchemy, nothing is being removed from Tactile:Blocks today. Enchanting stays there, and this page describes what a dedicated module could make of it."),
  ], None),
  ("Un rituel spatial", "A spatial ritual", [
    ("Ce que l'on dispose autour de la table, et la façon dont on l'agence, orienterait le résultat. L'agencement prendrait la place du hasard, dans le même esprit que le compagnonnage des cultures dans Farms : une décision de placement, pas une relance.",
     "What is laid out around the table, and how it is arranged, would steer the result. Layout would take the place of chance, in the same spirit as companion planting in Farms: a placement decision, not a reroll."),
  ], None),
  ("Rendre l'aléa lisible", "Making chance readable", [
    ("Des indices visuels annonceraient la tendance de l'enchantement avant validation. Le monde informe, pas une interface : on voit vers quoi le rituel penche, et l'on choisit d'aller au bout ou de reprendre la préparation.",
     "Visual cues would announce the enchantment's leaning before confirmation. The world informs, not an interface: you see where the ritual is heading, and choose to see it through or to rework the preparation."),
    ("Un enchantement puissant demanderait une préparation plus longue et plus exigeante. Le coût cesse d'être une simple soustraction de niveaux pour devenir du temps et du geste, ce qui donne du poids à chaque tentative.",
     "A powerful enchantment would demand a longer, more demanding preparation. The cost stops being a simple subtraction of levels and becomes time and gesture, which gives weight to every attempt."),
  ], None),
 ]),

# ============================== FISHING ===================================
("fishing", "Fishing", "#2fa79e",
 ("Approfondir un geste déjà à demi physique, au lieu d'ajouter une station de plus.",
  "Deepening a gesture that is already half physical, instead of adding one more station."),
 [
  ("Pas une station de plus", "Not one more station", [
    ("Peu de modules ont autant à gagner à ne rien ajouter. La canne existe déjà, le geste existe déjà : Fishing les approfondit plutôt que de les remplacer par une interface. Il réutilise au passage les fondations d'Animals, l'écosystème et le découpage, et le même procédural que le reste de la suite.",
     "Few modules gain as much from adding nothing. The rod already exists, the gesture already exists: Fishing deepens them instead of replacing them with an interface. It reuses Animals' foundations along the way, the ecosystem and the butchering, and the same procedural approach as the rest of the suite."),
  ], None),
  ("Aucun poisson identique", "No two fish alike", [
    ("La variété de poissons devient illimitée, chaque prise ayant sa taille et son poids propres, et son apport nutritif indexé sur ce poids. Une prise se regarde, se compare, et vaut d'être montrée : un gros poisson est un événement, pas une ligne d'inventaire.",
     "Fish variety becomes unlimited, each catch having its own length and weight, and its nutrition indexed on that weight. A catch is looked at, compared, and worth showing: a big fish is an event, not an inventory line."),
  ], None),
  ("Sortir la prise", "Landing the catch", [
    ("Le moment où le poisson mord devient un vrai bras de fer interactif, dont la difficulté suit le poids et l'espèce de la prise. Ferrer trop tôt ou tirer trop fort se paie, et sortir une grosse pièce se raconte.",
     "The moment the fish bites becomes a real interactive tug-of-war, its difficulty following the catch's weight and species. Striking too early or pulling too hard costs you, and landing a big one is a story."),
  ], None),
  ("Pêcher devient un choix", "Fishing becomes a choice", [
    ("L'appât, la profondeur, l'heure et la température, fournies par Season et Weather, orientent les espèces et les tailles susceptibles de mordre. Pêcher cesse d'être un tirage au sort pour devenir une décision : le bon appât, au bon endroit, au bon moment.",
     "Bait, depth, time of day and temperature, provided by Season and Weather, steer the species and sizes likely to bite. Fishing stops being a lottery and becomes a decision: the right bait, in the right place, at the right time."),
    ("Des bancs procéduraux se déplacent selon les courants fournis par Water et selon les saisons, et se repèrent à la surface avant même de lancer. La pêche commence par l'observation.",
     "Procedural shoals move with the currents provided by Water and with the seasons, and can be spotted at the surface before even casting. Fishing starts with observation."),
  ], None),
  ("Le matériel, et le reste de l'eau", "Gear, and the rest of the water", [
    ("Cannes, lignes et hameçons ont des propriétés distinctes, résistance, portée, formant un petit arbre d'équipement cohérent avec Smith. Selon le lieu, on remonte aussi des crustacés, des algues ou des débris.",
     "Rods, lines and hooks have distinct properties, strength, range, forming a small gear tree consistent with Smith. Depending on the spot, you also bring up crustaceans, algae or debris."),
    ("Et l'eau se souvient : surpêcher un plan d'eau le vide temporairement, exactement comme la surchasse vide une zone sur la terre ferme.",
     "And the water remembers: overfishing a body of water empties it temporarily, exactly as overhunting empties an area on land."),
  ], None),
 ]),

# =============================== COMBAT ===================================
("combat", "Combat", "#7688aa",
 ("Le module le plus délicat de la suite, parce qu'il touche à la physique même du jeu.",
  "The suite's most delicate module, because it touches the game's very physics."),
 [
  ("Frapper quelque part, pas frapper une boîte", "Hitting somewhere, not hitting a box", [
    ("Une entité Minecraft est une boîte : on la touche, ou on ne la touche pas. Combat remplace cela par des hitbox procédurales localisées par partie du corps, avec des animations de coup et d'impact générées plutôt que jouées à l'identique.",
     "A Minecraft entity is a box: you hit it, or you do not. Combat replaces that with procedural hitboxes localized per body part, with strike and impact animations generated rather than replayed identically."),
    ("Le geste dépend alors des statistiques de l'arme et de la présence d'un bouclier, et la réaction de la cible varie selon la zone touchée et les dégâts subis, du simple recul au titubement et à la chute.",
     "The gesture then depends on the weapon's stats and on whether a shield is carried, and the target's reaction varies with the zone hit and the damage taken, from a simple stagger to stumbling and falling."),
  ], "combat_zones"),
  ("Une hiérarchie du risque assumée", "An acknowledged hierarchy of risk", [
    ("Le module se découpe honnêtement en deux moitiés inégales. La partie sûre est le geste côté joueur, l'équilibre du poids, l'animation procédurale, les dégâts ciblés : elle porte sur une entité entièrement maîtrisée.",
     "The module honestly splits into two unequal halves. The safe part is the player-side gesture, weight balance, procedural animation, targeted damage: it operates on an entity fully under control."),
    ("La partie incertaine est le ressenti ennemi, car il suppose de lire et de piloter le squelette d'une cible arbitraire, potentiellement ajoutée par un mod. C'est là que le module peut casser, et c'est donc là qu'il avance prudemment.",
     "The uncertain part is the enemy's feedback, because it means reading and driving the skeleton of an arbitrary target, potentially added by a mod. That is where the module can break, and so that is where it moves carefully."),
    ("D'où une livraison par paliers : d'abord des réactions génériques qui ne dépendent d'aucun squelette, recul, flash, son, et qui fonctionnent sur n'importe quel monstre ; ensuite seulement le titubement et la chute par zone, sur les squelettes que l'on sait lire.",
     "Hence a staged delivery: first generic reactions that depend on no skeleton, knockback, flash, sound, which work on any monster; only then per-zone stumbling and falling, on skeletons that can be read."),
  ], None),
  ("L'arme décide du style", "The weapon decides the style", [
    ("Le poids et l'équilibre d'une arme forgée dans Smith déterminent une posture, qui change les zones atteignables et la vitesse de récupération. Choisir ou forger une arme, c'est choisir une façon de se battre, et cela reste entièrement du côté sûr du module.",
     "The weight and balance of a weapon forged in Smith determine a stance, which changes the reachable zones and the recovery speed. Choosing or forging a weapon means choosing a way to fight, and that stays entirely on the module's safe side."),
    ("Enchaîner des coups lourds essouffle et impose un rythme, parer, esquiver, frapper, plutôt que le matraquage. La profondeur vient du geste, sans toucher aux dégâts.",
     "Chaining heavy blows winds you and imposes a rhythm, parry, dodge, strike, rather than mashing. Depth comes from the gesture, without touching damage numbers."),
  ], None),
  ("Cohabiter avec l'existant", "Coexisting with what exists", [
    ("De grands mods de combat existent déjà, et se battre contre eux ne servirait personne. Combat sait les détecter et s'effacer proprement quand ils sont là, ou s'assumer comme l'option unique en leur absence : le même principe d'automatisme avec repli que le reste de la suite.",
     "Large combat mods already exist, and fighting them would serve no one. Combat can detect them and bow out cleanly when they are present, or stand as the only option in their absence: the same automatic-with-fallback principle as the rest of the suite."),
  ], None),
 ]),
]
