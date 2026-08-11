# -*- coding: utf-8 -*-
"""Le contenu du guide d'atelier de Tactile:Wood : les cinq modules, en français et en anglais.

Séparé de build_guide.py pour une raison simple : le générateur est commun à
tous les modules de la suite, ce fichier ne parle que du bois. Chacun reste
lisible de bout en bout.

Le français est la version d'auteur, l'anglais sa traduction. Les deux listes de
blocs doivent se correspondre bloc pour bloc — le générateur refuse de
construire sinon.

Les libellés de l'éditeur sont cités en ANGLAIS dans les deux langues : les
captures sont prises en anglais, et un lecteur qui joue en français a l'atelier
traduit sous les yeux. Le premier module le dit une fois, en tête.
"""

# --------------------------------------------------------------------- captures
# Les captures d'atelier, réencodées pour le web par build_wk_images.py. Le
# format retenu diffère d'une image à l'autre — palette exacte pour un panneau
# d'interface, JPEG pour une vue 3D — d'où cette table plutôt qu'une extension
# écrite en dur trente fois.

WK = {
 "1": "jpg", "2": "jpg", "3": "jpg", "4": "jpg", "5": "jpg", "6": "jpg", "7": "jpg",
 "8": "png", "9": "png", "10": "png", "11": "png", "12": "png", "13": "png", "14": "png",
 "15": "jpg", "16": "png", "17": "jpg", "18": "png", "19": "png", "20": "png", "21": "jpg",
 "22": "jpg", "23": "png", "24": "jpg",
 "pub-menu": "jpg", "pub-site": "jpg", "handles": "png", "fruits": "jpg",
 "bloom": "jpg", "flower-tex": "jpg",
}


def shot(name):
    return "../img/wk/%s.%s" % (name, WK[name])


def with_shots(fr, en, table):
    """Glisse les captures dans les deux langues À LA MÊME PLACE.

    Une capture n'appartient pas à une langue : la poser deux fois, une dans
    chaque liste, c'est accepter qu'un jour l'une des deux la perde ou la
    décale. On la pose donc une seule fois, repérée par le DÉBUT du paragraphe
    français qu'elle suit — pas par un numéro de ligne, qui se décalerait au
    premier paragraphe ajouté.
    """
    fr, en = list(fr), list(en)
    for prefix, name in table:
        hits = [i for i, b in enumerate(fr) if b[0] in ("p", "note") and b[1].startswith(prefix)]
        if len(hits) != 1:
            raise SystemExit("capture %s : %d paragraphe(s) commencent par « %s »" % (name, len(hits), prefix))
        fr.insert(hits[0] + 1, ("img", shot(name)))
        en.insert(hits[0] + 1, ("img", shot(name)))
    return fr, en


# --------------------------------------------------------------------- schémas
# Ils ne portent que des mots qui ne se traduisent pas (des chiffres, des noms
# de boutons) : leur légende, elle, est traduite comme le reste.
#
# ⚠ UN SCHÉMA NE REFAIT JAMAIS UNE CAPTURE (règle de Jordan). Ceux qui restent
# montrent ce qu'aucune capture ne peut montrer : une probabilité, un rejeu d'un
# arbre à l'autre, une valeur tirée dans une fourchette. Deux autres ont été
# retirés — un arbre aux segments coloriés et les poignées d'un pétale — parce
# que l'atelier les montre déjà, en mieux.

SVG_DRAW = '''<svg viewBox="0 0 640 210" xmlns="http://www.w3.org/2000/svg" role="img">
<g font-family="Segoe UI,system-ui,sans-serif">
<g transform="translate(20,14)">
<rect x="0" y="0" width="198" height="46" rx="3" fill="#dcd7cd"/>
<rect x="202" y="0" width="198" height="46" rx="3" fill="#4f9e3a"/>
<rect x="404" y="0" width="198" height="46" rx="3" fill="#4f9e3a"/>
<text x="99" y="29" text-anchor="middle" font-size="15" fill="#191510">vanilla</text>
<text x="301" y="29" text-anchor="middle" font-size="15" fill="#ffffff">A</text>
<text x="503" y="29" text-anchor="middle" font-size="15" fill="#ffffff">B</text>
<text x="99" y="68" text-anchor="middle" font-size="13" fill="#5f594e">1/3</text>
<text x="301" y="68" text-anchor="middle" font-size="13" fill="#5f594e">1/3</text>
<text x="503" y="68" text-anchor="middle" font-size="13" fill="#5f594e">1/3</text>
</g>
<line x1="20" y1="108" x2="620" y2="108" stroke="#dcd7cd" stroke-width="1"/>
<g transform="translate(20,130)">
<rect x="0" y="0" width="198" height="46" rx="3" fill="none" stroke="#dcd7cd" stroke-width="1" stroke-dasharray="4 4"/>
<rect x="202" y="0" width="198" height="46" rx="3" fill="#4f9e3a"/>
<rect x="404" y="0" width="198" height="46" rx="3" fill="#4f9e3a"/>
<line x1="60" y1="34" x2="138" y2="12" stroke="#b0a99c" stroke-width="1.5"/>
<text x="99" y="29" text-anchor="middle" font-size="15" fill="#b0a99c">vanilla</text>
<text x="301" y="29" text-anchor="middle" font-size="15" fill="#ffffff">A</text>
<text x="503" y="29" text-anchor="middle" font-size="15" fill="#ffffff">B</text>
<text x="301" y="68" text-anchor="middle" font-size="13" fill="#5f594e">1/2</text>
<text x="503" y="68" text-anchor="middle" font-size="13" fill="#5f594e">1/2</text>
</g>
</g></svg>'''


SVG_REPLAY = '''<svg viewBox="0 0 640 230" xmlns="http://www.w3.org/2000/svg" role="img">
<g fill="none" stroke-linecap="round">
<path d="M96 200 L96 70" stroke="#c9a227" stroke-width="11"/>
<path d="M96 96 L150 62" stroke="#8a93a0" stroke-width="7"/>
<g fill="#4f9e3a" stroke="none">
<rect x="140" y="34" width="15" height="15"/><rect x="157" y="34" width="15" height="15"/>
<rect x="140" y="51" width="15" height="15"/><rect x="157" y="51" width="15" height="15"/>
<rect x="174" y="34" width="15" height="15"/><rect x="157" y="17" width="15" height="15"/>
</g>
<path d="M258 120 L320 120" stroke="#b0a99c" stroke-width="2"/>
<path d="M310 112 L320 120 L310 128" stroke="#b0a99c" stroke-width="2"/>
<path d="M470 210 L470 60" stroke="#c9a227" stroke-width="13"/>
<path d="M470 100 L400 66" stroke="#8a93a0" stroke-width="7"/>
<path d="M470 130 L540 96" stroke="#8a93a0" stroke-width="7"/>
<path d="M470 60 L470 40" stroke="#8a93a0" stroke-width="6"/>
<g fill="#4f9e3a" stroke="none" opacity="0.92">
<rect x="366" y="30" width="13" height="13"/><rect x="381" y="30" width="13" height="13"/>
<rect x="366" y="45" width="13" height="13"/><rect x="381" y="45" width="13" height="13"/>
<rect x="396" y="38" width="13" height="13"/><rect x="381" y="15" width="13" height="13"/>
<rect x="524" y="60" width="13" height="13"/><rect x="539" y="60" width="13" height="13"/>
<rect x="524" y="75" width="13" height="13"/><rect x="539" y="75" width="13" height="13"/>
<rect x="554" y="68" width="13" height="13"/><rect x="539" y="45" width="13" height="13"/>
<rect x="447" y="8" width="13" height="13"/><rect x="462" y="8" width="13" height="13"/>
<rect x="447" y="23" width="13" height="13"/><rect x="462" y="23" width="13" height="13"/>
<rect x="477" y="16" width="13" height="13"/>
</g>
</g></svg>'''


SVG_RANGE = '''<svg viewBox="0 0 640 170" xmlns="http://www.w3.org/2000/svg" role="img">
<line x1="90" y1="120" x2="560" y2="120" stroke="#dcd7cd" stroke-width="3"/>
<g stroke="#191510" stroke-width="2">
<line x1="90" y1="104" x2="90" y2="136"/><line x1="560" y1="104" x2="560" y2="136"/>
</g>
<g font-family="Segoe UI,system-ui,sans-serif" font-size="14" fill="#5f594e">
<text x="90" y="158" text-anchor="middle">min</text>
<text x="560" y="158" text-anchor="middle">max</text>
</g>
<g fill="none" stroke="#4f9e3a" stroke-width="7" stroke-linecap="round">
<line x1="163" y1="120" x2="163" y2="86"/>
<line x1="284" y1="120" x2="284" y2="52"/>
<line x1="352" y1="120" x2="352" y2="98"/>
<line x1="441" y1="120" x2="441" y2="40"/>
<line x1="502" y1="120" x2="502" y2="74"/>
</g>
<g fill="#4f9e3a">
<circle cx="163" cy="80" r="9"/><circle cx="284" cy="46" r="13"/><circle cx="352" cy="92" r="7"/>
<circle cx="441" cy="34" r="15"/><circle cx="502" cy="68" r="11"/>
</g></svg>'''


# --------------------------------------------------------------------- module 1

M1_FR = [
 ("p", "Pour accéder à l'éditeur, il vous suffit de cliquer sur le petit T en haut à droite du menu principal. "
       "Il est conseillé de désactiver les shaders avant, ils peuvent interférer avec le rendu."),
 ("p", "L'éditeur ouvre son propre monde : vide, éclairé en permanence, et vous y êtes en spectateur. La scène est "
       "nettoyée à chaque entrée, ce que vous y posez ne survit donc pas. Votre travail, lui, vit dans des fichiers à "
       "côté du jeu, dans .minecraft\\Tactile\\Wood."),
 ("p", "À la première ouverture d'un pack, l'éditeur vous demande un pseudo. Ce pseudo sera celui utilisé pour la "
       "publication de vos packs, et il sera affiché dans le menu Add-ons des joueurs qui utilisent vos créations."),
 ("note", "Les boutons de l'atelier sont cités ici en anglais, comme sur les captures. Si vous jouez en français, "
          "l'éditeur affiche leur traduction : « Solid view » devient Modélisation, « Save the variant » devient "
          "Enregistrer la variante."),

 ("h", "Les packs", "Packs"),
 ("p", "Un pack est le dossier où vivent vos arbres. Vous travaillez toujours dans un pack, et chaque pack est géré "
       "indépendamment des autres."),
 ("p", "Au survol d'une carte de pack, deux boutons apparaissent. R renomme le pack. X le supprime : attention, une "
       "suppression est irréversible, elle emporte les arbres et les feuilles du pack, il n'y a pas de corbeille."),

 ("h", "Les add-ons", "Add-ons"),
 ("p", "Tactile:Wood est fourni avec un environnement de partage automatique, les add-ons. Un add-on est le pack d'un "
       "autre auteur, installé chez vous. Il s'intègre automatiquement à votre jeu et vous pouvez en collectionner "
       "autant que vous voulez. Un add-on ne se modifie pas."),
 ("p", "Pour en installer un, déposez son dossier dans .minecraft\\Tactile\\Wood\\Addons. Le bouton Refresh du menu "
       "évite d'avoir à relancer le jeu."),
 ("p", "Le menu Add-ons liste chaque arbre avec le nom de son auteur, en affiche l'aperçu au survol, et permet de "
       "décider lesquels seront utilisés par votre jeu : il suffit de décocher ceux que vous ne voulez pas. La "
       "décision reste chez vous, elle n'écrit rien dans le pack reçu. Un pack qui réclame un mod que vous n'avez pas "
       "est signalé et laissé de côté."),

 ("h", "Les espèces", "Species"),
 ("p", "Lorsque vous sélectionnez un pack, celui-ci s'ouvre en détail. Chaque espèce d'arbre disponible dans votre "
       "jeu apparaît, celles ajoutées par d'autres mods comprises."),
 ("p", "Chaque espèce a au minimum une sous-espèce, affichée « forms » dans l'éditeur et détectée automatiquement par "
       "le jeu, qui définit le type d'arbre mais aussi où il apparaît."),
 ("p", "Pour la création d'un nouvel arbre, vous avez trois possibilités."),
 ("p", "La première : sélectionner une sous-espèce et modifier le modèle vanilla. Cela écrase le modèle vanilla, il "
       "sort du tirage et vos arbres prennent sa place."),
 ("p", "La deuxième : sélectionner une sous-espèce et créer une nouvelle variante. Cela ajoute un modèle "
       "supplémentaire au tirage sans écraser le vanilla, qui reste donc à égalité avec le vôtre."),
 ("p", "La troisième : créer un modèle libre. Cet arbre ignore les sous-espèces et sera tiré quel que soit le biome "
       "où il se trouve. Son taux d'apparition est de 5 %."),
 ("svg", SVG_DRAW,
  "En haut, deux variantes ajoutées à côté du modèle du jeu : chacun des trois sort une fois sur trois. En bas, les "
  "mêmes variantes quand l'une d'elles remplace le modèle du jeu, qui quitte alors le tirage."),
 ("note", "Si deux packs écrasent un même modèle vanilla, ils cohabiteront en tant que variantes."),

 ("h", "Publication", "Publishing"),
 ("p", "L'écran des espèces de votre pack permet la publication de celui-ci."),
 ("p", "La liste s'ouvre avec tout coché : décochez ce qui n'est pas prêt, on ne publie pas son dossier de travail "
       "mais une sélection. Le paquet prend le nom du pack ouvert. Une ligne rouge signale avant l'envoi ce qui "
       "manque, un crédit absent ou des modèles restés au nom par défaut ; c'est un avertissement, jamais un blocage."),
 ("p", "Une description sera demandée, et elle est obligatoire : valider à vide ne fait rien. L'éditeur prépare "
       "ensuite une image par arbre, puis envoie le tout."),
 ("p", "Une fois votre pack publié, il est envoyé en vérification par un administrateur. Cela permet de garder un "
       "contenu de qualité et cohérent sur la vitrine."),
 ("p", "Une fois validé, il paraît sur le site et il est mis en avant sur le Discord, ce qui peut prendre quelques "
       "minutes."),
 ("link", "https://belerion63.github.io/Tactile/addons/index.html?module=wood", "Voir la galerie des créations"),
 ("p", "Il est tout à fait possible de partager manuellement votre pack sans passer par le site : le dossier se "
       "trouve dans .minecraft\\Tactile\\Wood\\Export. Il y est écrit avant l'envoi, renoncer à publier ne vous fait "
       "donc rien perdre."),

 ("h", "Les mises à jour", "Updates"),
 ("p", "Lorsqu'un pack déjà publié est publié à nouveau depuis la même installation, il échappe à la validation et "
       "est mis à jour directement sur le site. La mise à jour est également annoncée sur le Discord."),
 ("p", "Cette reconnaissance tient à un jeton posé dans .minecraft\\Tactile\\Wood\\author.json. Depuis une autre "
       "installation, ou pour un pack qui n'a jamais été validé, l'envoi repasse par la relecture."),
]

M1_EN = [
 ("p", "To open the editor, click the small T at the top right of the main menu. Turning shaders off beforehand is "
       "recommended, they can interfere with the rendering."),
 ("p", "The editor opens a world of its own: empty, permanently lit, and you are a spectator in it. The scene is "
       "swept clean on every entry, so nothing you leave there survives. Your work lives in files next to the game, "
       "in .minecraft\\Tactile\\Wood."),
 ("p", "The first time you open a pack, the editor asks for a name. That name is the one used when you publish your "
       "packs, and it is shown in the Add-ons menu of the players who use your creations."),
 ("note", "The workshop's buttons are quoted here in English, as on the screenshots. If you play in another "
          "language, the editor shows them translated: \"Solid view\" and \"Save the variant\" will read differently "
          "on your screen."),

 ("h", "Les packs", "Packs"),
 ("p", "A pack is the folder your trees live in. You always work inside a pack, and each pack is handled "
       "independently from the others."),
 ("p", "Hovering a pack card reveals two buttons. R renames the pack. X deletes it: be careful, deleting cannot be "
       "undone, it takes the pack's trees and leaves with it, and there is no recycle bin."),

 ("h", "Les add-ons", "Add-ons"),
 ("p", "Tactile:Wood ships with an automatic sharing environment, the add-ons. An add-on is another author's pack, "
       "installed on your side. It joins your game automatically and you can collect as many as you like. An add-on "
       "cannot be edited."),
 ("p", "To install one, drop its folder into .minecraft\\Tactile\\Wood\\Addons. The Refresh button in the menu saves "
       "you from restarting the game."),
 ("p", "The Add-ons menu lists every tree with its author's name, shows a preview on hover, and lets you decide "
       "which ones your game will use: simply untick the ones you would rather not see. The decision stays on your "
       "side, it writes nothing into the pack you received. A pack that requires a mod you do not have is flagged and "
       "left aside."),

 ("h", "Les espèces", "Species"),
 ("p", "Selecting a pack opens it in detail. Every tree species available in your game appears, including those "
       "added by other mods."),
 ("p", "Each species has at least one sub-species, shown as \"forms\" in the editor and detected automatically by "
       "the game, which defines the kind of tree and also where it grows."),
 ("p", "To create a new tree, you have three options."),
 ("p", "The first: pick a sub-species and edit the vanilla model. This overwrites the vanilla model, it leaves the "
       "draw and your trees take its place."),
 ("p", "The second: pick a sub-species and create a new variant. This adds one more model to the draw without "
       "overwriting vanilla, which therefore stays on equal terms with yours."),
 ("p", "The third: create a free model. That tree ignores sub-species and can be drawn whatever the biome it stands "
       "in. Its appearance rate is 5%."),
 ("svg", SVG_DRAW,
  "Top: two variants added next to the game's model, each of the three comes up one time in three. Bottom: the same "
  "variants once one of them replaces the game's model, which then leaves the draw."),
 ("note", "If two packs overwrite the same vanilla model, they will coexist as variants."),

 ("h", "Publication", "Publishing"),
 ("p", "The species screen of your pack is where you publish it."),
 ("p", "The list opens with everything ticked: untick what is not ready, you do not publish your working folder but "
       "a selection. The package takes the name of the open pack. A red line points out what is missing before you "
       "send, a missing credit or models still carrying their default name; it warns, it never blocks."),
 ("p", "A description is asked for, and it is required: confirming an empty one does nothing. The editor then "
       "prepares one image per tree and sends everything."),
 ("p", "Once published, your pack goes to an administrator for review. This keeps the showcase consistent and worth "
       "browsing."),
 ("p", "Once approved it appears on the site and is featured on the Discord, which can take a few minutes."),
 ("link", "https://belerion63.github.io/Tactile/addons/index.html?module=wood", "Browse the gallery"),
 ("p", "You can of course share your pack by hand, without going through the site: the folder sits in "
       ".minecraft\\Tactile\\Wood\\Export. It is written there before anything is sent, so giving up on publishing "
       "loses you nothing."),

 ("h", "Les mises à jour", "Updates"),
 ("p", "When an already published pack is published again from the same installation, it skips review and is updated "
       "directly on the site. The update is announced on the Discord too."),
 ("p", "That recognition rests on a token stored in .minecraft\\Tactile\\Wood\\author.json. From another "
       "installation, or for a pack that was never approved, the submission goes through review again."),
]


# --------------------------------------------------------------------- module 2
# Les raccourcis : la colonne de gauche ne se traduit pas, seule la colonne de
# droite change de langue. Elle est relue dans le code, pas recopiée de l'aide
# en jeu.

KEYS_FR = [
 ("Clic molette", "Orbiter autour du sujet"),
 ("Maj + clic molette", "Déplacer la vue"),
 ("Molette dans le vide", "Zoomer"),
 ("Ctrl + molette", "Zoomer même en visant un segment"),
 (".", "Recentrer sur la sélection"),
 ("Clic gauche", "Sélectionner le segment visé"),
 ("Maj + clic gauche", "Ajouter ou retirer de la sélection"),
 ("Clic gauche dans le vide", "Tout désélectionner"),
 ("Clic gauche maintenu", "Déplacer la sélection"),
 ("Clic droit maintenu", "Tirer un nouveau segment de l'articulation visée"),
 ("Molette sur un segment", "Régler son épaisseur"),
 ("Maj + molette", "Forcer son type : auto, tronc, branche, pointe"),
 ("R", "Tourner autour de l'attache"),
 ("Maj pendant R", "Aimanter l'angle sur 15 degrés"),
 ("X, Y, Z pendant un geste", "Contraindre à un axe, ré-appuyer libère"),
 ("Maj + D", "Dupliquer, puis déplacer la copie"),
 ("P", "Détacher. R oriente, clic gauche repose"),
 ("Suppr ou X", "Supprimer la sélection"),
 ("Entrée", "Valider le geste en cours"),
 ("Échap", "Annuler le geste en cours"),
 ("Ctrl + Z", "Annuler"),
 ("Ctrl + Maj + Z", "Refaire"),
]

KEYS_EN = [
 ("Clic molette", "Orbit around the subject"),
 ("Maj + clic molette", "Pan the view"),
 ("Molette dans le vide", "Zoom"),
 ("Ctrl + molette", "Zoom even while aiming at a segment"),
 (".", "Recentre on the selection"),
 ("Clic gauche", "Select the aimed segment"),
 ("Maj + clic gauche", "Add to or remove from the selection"),
 ("Clic gauche dans le vide", "Deselect everything"),
 ("Clic gauche maintenu", "Move the selection"),
 ("Clic droit maintenu", "Pull a new segment from the aimed joint"),
 ("Molette sur un segment", "Set its thickness"),
 ("Maj + molette", "Force its type: auto, trunk, branch, tip"),
 ("R", "Rotate around the attachment"),
 ("Maj pendant R", "Snap the angle to 15 degrees"),
 ("X, Y, Z pendant un geste", "Constrain to an axis, press again to release"),
 ("Maj + D", "Duplicate, then move the copy"),
 ("P", "Detach. R aims, left click drops"),
 ("Suppr ou X", "Delete the selection"),
 ("Entrée", "Confirm the gesture in progress"),
 ("Échap", "Cancel the gesture in progress"),
 ("Ctrl + Z", "Undo"),
 ("Ctrl + Maj + Z", "Redo"),
]

M2_FR = [
 ("h", "Les deux panneaux", "The two panels"),
 ("p", "Le panneau de gauche rassemble ce que vous éditez et la façon dont vous le regardez. Celui de droite tient "
       "les réglages procéduraux de votre arbre, qui font l'objet {procedural-parameters|du dernier module}."),
 ("keys", [
   ("Mode", "choisit ce que l'on édite de l'arbre, Shape dans notre cas, et détermine le contenu des deux panneaux."),
   ("Solid view", "affiche l'arbre avec son tronc, ses textures et son feuillage."),
   ("Raw", "montre le rendu brut, sans les altérations du procédural."),
   ("Procedural", "montre ce que donnera le résultat en jeu. Le bouton Draw relance le tirage."),
   ("Armature only", "retire le feuillage du rendu, surtout utile en procédural."),
   ("Stump", "détermine l'épaisseur de la souche : 1x1, 2x2, 3x3 ou 4x4."),
   ("Thickness", "apparaît dès qu'un segment est sélectionné. Spread around the trunk s'active à partir de deux "
                 "segments et les répartit en azimut, chacun tournant autour de sa propre attache."),
   ("Selection", "le nombre total de segments, le nombre sélectionné, et l'épaisseur en blocs du segment actif."),
   ("Apply to the world", "applique les changements au rendu, surtout utile pour les textures de feuilles qui ne "
                          "sont pas en temps réel."),
   ("Save the variant", "enregistre votre arbre dans le pack, réglages du panneau droit compris."),
 ]),
 ("p", "Raw, Procedural et Armature only ne s'activent qu'une fois Solid view coché, et le bouton Draw n'apparaît "
       "qu'en Procedural."),
 ("p", "La case vertical grid vous aide à juger la taille de votre arbre et son alignement. Le gizmo en bas à droite "
       "aligne la caméra sur l'un des trois axes."),

 ("h", "Les raccourcis", "Shortcuts"),
 ("p", "Le bouton ? en haut à droite les rappelle à tout moment."),
 ("keys", KEYS_FR),
 ("p", "En mode Foliage, seuls le point et Ctrl + Z restent. En mode Texture, aucun raccourci de sculpture ne "
       "répond : l'arbre n'y est plus qu'un décor, mais on continue de tourner autour et de zoomer."),

 ("h", "Se déplacer dans l'espace", "Moving around"),
 ("p", "L'éditeur est fortement inspiré de l'interface de Blender. Cela peut être déroutant pour les non-initiés, "
       "mais les habitués seront ravis."),
 ("p", "Le clic molette tourne autour de votre arbre pour l'inspecter sous tous les angles. Cela change aussi la "
       "façon dont vous interagissez avec les segments, puisque la rotation et le déplacement s'adaptent à votre vue."),
 ("p", "Maj + clic molette déplace librement la caméra, ce qui est très utile quand vous zoomez ou que vous "
       "travaillez un grand arbre. Pour revenir à la vue initiale, désélectionnez tout d'un clic dans le vide et "
       "appuyez sur le point, celui du pavé numérique comme celui du clavier : sans sélection il cadre l'arbre "
       "entier, avec une sélection il cadre le segment actif."),
 ("p", "La molette zoome, mais attention à ne pas viser un segment, au risque de modifier son épaisseur sans le "
       "vouloir. Dans ce cas, un Ctrl + Z annule. Ctrl + molette force le zoom, pratique quand l'arbre remplit "
       "l'écran et qu'il ne reste plus de vide à viser."),

 ("h", "Les types de segments", "Segment types"),
 ("p", "Le tronc, en jaune, détermine la hauteur de votre arbre. Le procédural viendra lui ajouter des protubérances "
       "et des branches supplémentaires, et pourra même l'agrandir. Il est conseillé de garder un tronc régulier, "
       "sans trop de nœuds."),
 ("p", "Les branches, en bleu, habillent votre arbre et le rendent unique. Elles sont plus permissives sur la forme "
       "et détermineront l'aspect voulu. Le procédural ajoutera toujours les siennes par-dessus, et toujours en même "
       "nombre. Il dispose pour cela d'un budget de segments fixe, qu'il partage entre ses branches et les vôtres : "
       "plus vous en sculptez, plus la part de chacune est petite, et plus les pousses ajoutées sont courtes. Votre "
       "silhouette reste donc reconnaissable sur l'arbre fini. C'est voulu et nécessaire pour garder l'identité "
       "visuelle."),
 ("p", "Les pointes, en rose, sont le dernier segment d'une branche : elles font savoir au système où une branche se "
       "termine. Elles servent surtout au feuillage, c'est principalement sur elles que l'on voudra placer les "
       "feuilles, ce qui permet au procédural de reproduire correctement la forme du houppier. {foliage|Le module suivant} y "
       "revient."),

 ("h", "Sculpter le tronc", "Sculpting the trunk"),
 ("p", "Extrudez la souche au clic droit pour donner sa forme au tronc ; Y vous permettra d'extruder parfaitement "
       "droit. Pour un résultat propre, gardez des segments de taille proche d'un bloc et évitez les angles trop "
       "aigus. N'hésitez pas à utiliser R pour les ajuster plus précisément."),
 ("p", "Votre tronc s'affine automatiquement à l'extrusion. Un tronc d'épaisseur irrégulière sera rattrapé par le "
       "procédural, mais pourrait donner des résultats étranges."),
 ("p", "Lorsque vous sélectionnez un segment, tous ceux qui le suivent s'allument avec lui et le suivront : un "
       "déplacement, une rotation ou une suppression emporte toute la descendance. Le compteur, lui, continue "
       "d'afficher un seul segment sélectionné, c'est normal."),

 ("h", "Sculpter les branches", "Sculpting the branches"),
 ("p", "Vous pouvez maintenant créer vos branches pour habiller l'arbre et lui donner une vraie identité. Il suffit "
       "d'extruder depuis l'extrémité du tronc, les branches s'affineront d'elles-mêmes. Vous pouvez ajouter des "
       "sous-branches, mais attention : un arbre trop complexe n'est pas forcément un bel arbre."),
 ("p", "Utilisez la rotation, les axes et la position de la caméra pour placer vos segments comme vous le voulez. "
       "R + Y est l'un des plus utiles."),

 ("h", "Dupliquer et détacher", "Duplicating and detaching"),
 ("p", "Pour vous simplifier la vie, utilisez votre première branche comme modèle pour les autres : Maj + D pour la "
       "dupliquer, puis P pour la détacher de son segment actuel. Utilisez ensuite la rotation axée pour la remettre "
       "correctement, R + X par exemple."),
 ("note", "Après une duplication, le bouton Spread around the trunk du panneau gauche répartit toutes les branches "
          "sélectionnées autour du tronc en un seul geste."),

 ("h", "Corriger les types de segment", "Fixing segment types"),
 ("p", "Les types de segment sont très importants, vous devez les adapter selon ce que vous voulez faire de votre "
       "arbre. Pour en modifier un, placez le curseur sur le segment voulu : Maj + molette force son type."),
 ("p", "Par exemple, pour transformer la pointe du tronc en une troisième branche, il faut passer le premier segment "
       "en branche et le second en pointe."),
 ("p", "Et voilà, vous avez terminé la première étape de votre arbre."),
]

M2_EN = [
 ("h", "Les deux panneaux", "The two panels"),
 ("p", "The left panel gathers what you are editing and how you look at it. The right one holds your tree's "
       "procedural settings, which are the subject {procedural-parameters|of the last module}."),
 ("keys", [
   ("Mode", "chooses what you edit on the tree, Shape here, and decides the contents of both panels."),
   ("Solid view", "shows the tree with its trunk, its textures and its foliage."),
   ("Raw", "shows the bare result, without anything the procedural side adds."),
   ("Procedural", "shows what the tree will look like in game. The Draw button rolls the dice again."),
   ("Armature only", "removes the foliage from the view, mostly useful in Procedural."),
   ("Stump", "sets the thickness of the stump: 1x1, 2x2, 3x3 or 4x4."),
   ("Thickness", "appears as soon as a segment is selected. Spread around the trunk becomes available from two "
                 "segments on and spreads them around, each turning about its own attachment."),
   ("Selection", "the total number of segments, how many are selected, and the active segment's thickness in blocks."),
   ("Apply to the world", "applies your changes to the rendering, mostly useful for leaf textures, which are not "
                          "live."),
   ("Save the variant", "saves your tree into the pack, right-hand settings included."),
 ]),
 ("p", "Raw, Procedural and Armature only only become available once Solid view is ticked, and the Draw button "
       "appears in Procedural only."),
 ("p", "The vertical grid checkbox helps you judge your tree's size and alignment. The gizmo at the bottom right "
       "snaps the camera to one of the three axes."),

 ("h", "Les raccourcis", "Shortcuts"),
 ("p", "The ? button at the top right brings them back at any time."),
 ("keys", KEYS_EN),
 ("p", "In Foliage mode, only the period key and Ctrl + Z remain. In Texture mode no sculpting shortcut answers at "
       "all: the tree is only scenery there, though you can still orbit and zoom."),

 ("h", "Se déplacer dans l'espace", "Moving around"),
 ("p", "The editor borrows heavily from Blender's interface. It can be disconcerting if you have never used it, and "
       "delightful if you have."),
 ("p", "Middle click orbits around your tree so you can inspect it from every angle. It also changes how you handle "
       "segments, since moving and rotating follow your point of view."),
 ("p", "Shift + middle click pans the camera freely, which helps a lot when you zoom in or work on a tall tree. To "
       "get back to the starting view, deselect everything with a click in the void and press the period key, on the "
       "numpad or on the main keyboard: with nothing selected it frames the whole tree, with a selection it frames "
       "the active segment."),
 ("p", "The wheel zooms, but be careful not to aim at a segment or you will change its thickness by accident. Ctrl + "
       "Z undoes that. Ctrl + wheel forces the zoom, which is handy when the tree fills the screen and there is no "
       "empty space left to aim at."),

 ("h", "Les types de segments", "Segment types"),
 ("p", "The trunk, in yellow, sets your tree's height. The procedural side will add burls and further branches to "
       "it, and may even make it grow. Keep the trunk regular, without too many kinks."),
 ("p", "Branches, in blue, dress your tree and make it yours. They are far more permissive in shape and they carry "
       "the look you are after. The procedural side will always add its own on top, and always the same number of "
       "them. It works from a fixed budget of segments, which it shares between its branches and yours: the more you "
       "sculpt, the smaller each share, and the shorter the growths it adds. Your silhouette therefore stays "
       "recognisable on the finished tree. This is deliberate and necessary to preserve your visual identity."),
 ("p", "Tips, in pink, are the last segment of a branch: they tell the system where a branch ends. They mostly serve "
       "the foliage, since tips are where you will want to put leaves, which is what lets the procedural side "
       "reproduce the shape of your crown. {foliage|The next module} comes back to this."),

 ("h", "Sculpter le tronc", "Sculpting the trunk"),
 ("p", "Hold right click on the stump to extrude and give the trunk its shape; Y extrudes perfectly straight. For a "
       "clean result, keep segments about one block long and avoid sharp angles. R is there to adjust them more "
       "precisely."),
 ("p", "Your trunk tapers on its own as you extrude. An irregular trunk will be caught up by the procedural side, "
       "but it may give strange results."),
 ("p", "When you select a segment, everything downstream lights up with it and will follow: moving, rotating or "
       "deleting takes the whole descent along. The counter still reads one selected segment, which is expected."),

 ("h", "Sculpter les branches", "Sculpting the branches"),
 ("p", "You can now grow branches to dress the tree and give it a real identity. Extrude from the end of the trunk, "
       "and they will taper by themselves. You can add sub-branches, but beware: an overly complex tree is not "
       "necessarily a beautiful one."),
 ("p", "Use rotation, axis constraints and the camera position to place segments exactly where you want them. R + Y "
       "is one of the most useful combinations."),

 ("h", "Dupliquer et détacher", "Duplicating and detaching"),
 ("p", "To save yourself some work, use your first branch as a model for the others: Shift + D duplicates it, then P "
       "detaches it from its current segment. Use a constrained rotation to put it back where it belongs, R + X for "
       "instance."),
 ("note", "After a duplication, the Spread around the trunk button in the left panel arranges every selected branch "
          "around the trunk in one gesture."),

 ("h", "Corriger les types de segment", "Fixing segment types"),
 ("p", "Segment types matter a great deal, and you have to set them according to what you want your tree to be. To "
       "change one, put the cursor on the segment and use Shift + wheel to force its type."),
 ("p", "For example, to turn the tip of the trunk into a third branch, set the first segment to branch and the "
       "second one to tip."),
 ("p", "And there you are, the first stage of your tree is done."),
]


# --------------------------------------------------------------------- module 3

M3_FR = [
 ("p", "Le bouton Foliage du rail de gauche ouvre le mode feuillage. Il ne s'active qu'une fois que votre arbre a "
       "autre chose qu'une souche, puisque l'on habille {shape#segment-types|des organes}."),

 ("h", "Une touffe par organe", "One tuft per organ"),
 ("p", "Lorsque vous habillez votre arbre, gardez en tête l'habillage par organe : on habille cette branche, et "
       "précisément ce segment. Si vous ne le faites pas, le procédural ne comprendra pas quoi va où et fera des "
       "touffes partout."),

 ("h", "Choisir l'organe à habiller", "Choosing the organ"),
 ("p", "Choisissez le type d'organe, puis naviguez entre les organes d'un même type (tip 1/3). L'organe sélectionné "
       "s'affiche en orange. Le compte affiché à côté de chaque type vous dit combien d'organes de ce type portent "
       "déjà quelque chose."),
 ("p", "Pour un arbre de petite taille, commencez par une pointe."),

 ("h", "Poser les feuilles", "Placing leaves"),
 ("p", "Clic gauche pour poser, clic droit pour retirer, Ctrl + Z pour annuler. Les cases occupées par un segment ne "
       "seront pas remplies par du feuillage, gardez-le en tête."),
 ("note", "Ne remplissez que l'organe sélectionné. Évitez également les feuilles qui volent : recopiée sur une autre "
          "branche, une cellule qui ne touche ni le bois ni une autre feuille sera retirée en jeu."),

 ("h", "Se relire", "Checking your work"),
 ("p", "Passez en Solid view pour visualiser le résultat. S'il vous plaît, on continue ; si un trou vous dérange sur "
       "le dessus, il se comble en deux clics."),

 ("h", "Copier au lieu de recommencer", "Copying instead of starting over"),
 ("p", "Plutôt que de refaire la même opération sur chaque organe, la plupart du temps on voudra simplement répéter "
       "le même motif. Deux possibilités :"),
 ("list", [
   "Copy et Paste : copier le feuillage de l'organe courant, puis le coller sur un organe sélectionné.",
   "Copy onto bare organs : copier le feuillage de l'organe courant sur tous les organes du même type encore nus. "
   "Un organe déjà habillé n'est jamais écrasé.",
 ]),

 ("h", "Les réglages du panneau droit", "The right-hand settings"),
 ("p", "Le panneau droit change de contenu pour laisser place aux réglages de feuillage : la densité, l'allure des "
       "touffes avec leur taille, leur orientation et leurs variations, et la teinte de biome. Les onglets Fruit "
       "vous serviront si vous ajoutez des fleurs ou des fruits, ce que {texture|le module suivant} détaille."),

 ("h", "Ce que le procédural en fait", "What the procedural side does with it"),
 ("svg", SVG_REPLAY, "À gauche, l'organe que vous avez habillé. À droite, le même relevé reposé sur l'arbre en jeu, "
                     "puis recopié sur les branches que le procédural a ajoutées."),
 ("p", "Ce que vous avez posé est reposé tel quel sur l'arbre en jeu, au même endroit et dans le même sens. C'est "
       "votre dessin, il n'est ni tourné ni éclairci."),
 ("p", "Le procédural, lui, ajoute ses propres branches, et il les habille en copiant les vôtres. Pour chaque "
       "branche ajoutée, il cherche le relevé du même type dont la hauteur est la plus proche, et s'il n'en trouve "
       "aucun de ce type, il emprunte à un autre : une pointe se rabat sur une branche, puis sur le tronc. C'est "
       "pour cette raison qu'habiller trois pointes suffit à garnir toute la ramure, chaque branche ajoutée "
       "repartant avec une copie de votre touffe."),
 ("p", "Chaque copie est tournée vers la direction de la branche qui la reçoit. Une touffe dessinée sur une branche "
       "qui part au nord suivra donc une branche qui part à l'ouest, sans que vous ayez à la redessiner."),
 ("p", "Le tronc est le seul à pouvoir rester nu. Si aucun relevé ne tombe assez près de la hauteur demandée, le "
       "niveau ne porte rien : c'est ce qui donne le fût nu du bas et les creux dans la couronne. Sur les branches "
       "et les pointes il n'y a pas ce garde, elles reçoivent toujours quelque chose."),
 ("p", "Enfin, une cellule reste une feuille, quelle que soit la taille de l'arbre. Un grand arbre ne porte pas de "
       "plus grosses feuilles, il porte plus d'organes habillés."),
]

M3_EN = [
 ("p", "The Foliage button in the left rail opens foliage mode. It only becomes available once your tree has "
       "something more than a stump, since what you dress are {shape#segment-types|organs}."),

 ("h", "Une touffe par organe", "One tuft per organ"),
 ("p", "When you dress your tree, keep in mind that dressing happens organ by organ: you dress this branch, and this "
       "very segment. If you do not, the procedural side will not know what goes where and will put tufts "
       "everywhere."),

 ("h", "Choisir l'organe à habiller", "Choosing the organ"),
 ("p", "Pick the organ type, then step through the organs of that type (tip 1/3). The selected organ is highlighted "
       "in orange. The count next to each type tells you how many organs of that type already carry something."),
 ("p", "On a small tree, start with a tip."),

 ("h", "Poser les feuilles", "Placing leaves"),
 ("p", "Left click to place, right click to remove, Ctrl + Z to undo. Cells already taken by a segment will not be "
       "filled with foliage, keep that in mind."),
 ("note", "Only fill the selected organ. And avoid floating leaves: once copied onto another branch, a cell that "
          "touches neither wood nor another leaf is removed in game."),

 ("h", "Se relire", "Checking your work"),
 ("p", "Switch to Solid view to see the result. If you like it, carry on; if a hole on top bothers you, it takes two "
       "clicks to fill."),

 ("h", "Copier au lieu de recommencer", "Copying instead of starting over"),
 ("p", "Rather than repeating the same work on every organ, most of the time you simply want the same pattern "
       "again. Two ways:"),
 ("list", [
   "Copy and Paste: copy the current organ's foliage, then paste it onto a selected organ.",
   "Copy onto bare organs: copy the current organ's foliage onto every organ of the same type that is still bare. "
   "An organ that is already dressed is never overwritten.",
 ]),

 ("h", "Les réglages du panneau droit", "The right-hand settings"),
 ("p", "The right panel changes to make room for the foliage settings: density, the look of the tufts with their "
       "size, orientation and variations, and the biome tint. The Fruit tabs will serve you when you add flowers or "
       "fruit, which {texture|the next module} covers."),

 ("h", "Ce que le procédural en fait", "What the procedural side does with it"),
 ("svg", SVG_REPLAY, "On the left, the organ you dressed. On the right, the same reading put back on the tree in "
                     "game, then copied onto the branches the procedural side added."),
 ("p", "What you placed is put back as is on the tree in game, in the same spot and the same direction. It is your "
       "drawing: it is neither rotated nor thinned out."),
 ("p", "The procedural side, for its part, adds branches of its own, and dresses them by copying yours. For each "
       "added branch it looks for the reading of the same type closest in height, and if it finds none of that type "
       "it borrows from another: a tip falls back to a branch, then to the trunk. That is why dressing three tips is "
       "enough to fill out the whole crown, every added branch leaving with a copy of your tuft."),
 ("p", "Each copy is turned towards the direction of the branch that receives it. A tuft drawn on a branch pointing "
       "north will follow a branch pointing west, with nothing to redraw."),
 ("p", "The trunk is the only part that can stay bare. If no reading falls close enough to the height being asked "
       "for, that level carries nothing: this is what gives you the bare lower trunk and the hollows in the crown. "
       "Branches and tips have no such guard, they always receive something."),
 ("p", "Finally, a cell stays one leaf whatever the size of the tree. A large tree does not carry bigger leaves, it "
       "carries more dressed organs."),
]


# --------------------------------------------------------------------- module 4

OAK_FR = [
 ("p", "Ici, la texture de départ est celle du bambou, choisie pour ses feuilles larges et bien définies. Les "
       "feuilles de chêne sont allongées et composées de dents larges."),
 ("p", "Silhouette :"),
 ("list", [
   "Size à 40, pour une forme de feuille mieux définie.",
   "Elongation à 2, la feuille de chêne n'est pas ronde.",
   "Belly à 0.5, l'arrondi de la feuille se trouve plus près de l'extrémité.",
   "Tip à 0.3, pour une forme un peu plus conique.",
   "Serration à 1.0, cela fait ressortir les dentures.",
   "Teeth à 5, ce qui garde des dentures définies ; un nombre trop élevé crée du bruit.",
   "Midrib à 0, les feuilles restent droites.",
 ]),
 ("p", "Tuft :"),
 ("list", [
   "Density à 3.0, le chêne a un feuillage dense, on voit peu à travers.",
   "Coverage à 1.0, pour plusieurs étages de profondeur et des jeux d'ombres.",
   "Spread à 0.5, des feuilles pas trop dispersées, pour garder un amas visible.",
   "Direction ne nous intéresse pas ici.",
 ]),
 ("p", "Colour :"),
 ("list", [
   "Saturation à 0, le feuillage de chêne suit la couleur du biome.",
   "Luminance et Contrast à 0.5, pour un jeu d'ombres équilibré sur la texture.",
 ]),
 ("img", shot("20")),
 ("img", shot("21")),
]

OAK_EN = [
 ("p", "Here the starting texture is bamboo, picked for its wide, well defined leaves. Oak leaves are elongated and "
       "made of broad teeth."),
 ("p", "Silhouette:"),
 ("list", [
   "Size at 40, for a better defined leaf shape.",
   "Elongation at 2, an oak leaf is not round.",
   "Belly at 0.5, the widest part sits closer to the end.",
   "Tip at 0.3, for a slightly more conical shape.",
   "Serration at 1.0, which brings the teeth out.",
   "Teeth at 5, which keeps them readable; too many just makes noise.",
   "Midrib at 0, the leaves stay straight.",
 ]),
 ("p", "Tuft:"),
 ("list", [
   "Density at 3.0, oak foliage is dense, you barely see through it.",
   "Coverage at 1.0, for several layers of depth and some play of shadows.",
   "Spread at 0.5, leaves that are not too scattered, to keep a readable mass.",
   "Direction does not matter here.",
 ]),
 ("p", "Colour:"),
 ("list", [
   "Saturation at 0, oak foliage follows the biome colour.",
   "Luminance and Contrast at 0.5, for balanced shading on the texture.",
 ]),
 ("img", shot("20")),
 ("img", shot("21")),
]

M4_FR = [
 ("p", "Les panneaux latéraux changent pour laisser place à l'éditeur de texture : à droite les réglages de la "
       "feuille, à gauche les choix de texture."),

 ("h", "Deux façons de faire", "Two ways to go about it"),
 ("p", "Pour créer votre texture de feuille, vous avez deux possibilités : partir d'un modèle vanilla puis lui "
       "appliquer vos réglages, ou créer un modèle avec l'éditeur de fleur puis lui appliquer vos réglages. Nous "
       "allons voir les deux, en commençant par la première."),

 ("h", "Sélectionner la texture de base", "Picking the starting texture"),
 ("p", "Sous STARTING MODEL, cliquez sur le bouton Model. Choisissez ensuite le modèle que vous voulez : l'espèce "
       "n'a pas d'importance, seul son contenu compte, celui qui pourrait avoir des formes proches de ce que vous "
       "recherchez."),
 ("p", "La feuille elle-même sera entièrement redessinée, vous ne retrouverez donc pas celle du jeu. En revanche, "
       "vos feuilles sont semées dans les trous de cette texture : c'est elle qui donne la découpe d'ensemble de la "
       "touffe, d'où l'intérêt d'en choisir une dont la masse ressemble à ce que vous cherchez."),
 ("p", "Vous pouvez aussi partir de votre propre image : déposez un PNG dans le dossier leaves/images de votre pack, "
       "il apparaîtra dans la planche à côté des textures du jeu. Elle est relue à chaque ouverture, inutile de "
       "relancer le jeu. Votre image n'entre jamais dans l'atlas, c'est la carte dessinée à partir d'elle qui y va."),
 ("note", "Changer de texture de base en cours de route efface tous vos réglages : la mesure de la nouvelle texture "
          "les remplace, et le lien vers votre fichier de feuille est coupé. On choisit sa base d'abord, on règle "
          "ensuite."),

 ("h", "L'aperçu", "The preview"),
 ("p", "Plus bas, vous voyez l'aperçu de votre feuillage en temps réel. Le feuillage de l'arbre, lui, ne s'actualise "
       "que lorsque vous cliquez sur Apply to the world. Maintenez TAB à tout moment pour voir l'avant et l'après, "
       "relâchez pour revenir."),

 ("h", "Régler votre texture", "Setting up your texture"),
 ("p", "Le panneau droit contient trois groupes :"),
 ("list", [
   "Silhouette définit la forme de la feuille, pas celle de la touffe.",
   "Tuft règle la façon dont la texture place les feuilles, ainsi que leur nombre.",
   "Colour ajuste les couleurs et les ombres de votre texture.",
 ]),
 ("fold", "Une feuille de chêne, réglage par réglage", OAK_FR),

 ("h", "Les fleurs et les fruits", "Flowers and fruit"),
 ("p", "L'atelier permet d'ajouter des fleurs et des fruits dans les arbres. Sous SUBJECT, cliquez sur Flowers : une "
       "nouvelle interface apparaît à l'écran et le panneau gauche accueille de nouveaux éléments."),
 ("p", "+ Add a fruit ajoute un fruit complet, et vous pouvez en ajouter autant que vous voulez. Sous le fruit "
       "sélectionné, dont le numéro est encadré en jaune, vous pouvez ajouter, supprimer ou dupliquer les éléments "
       "de ce fruit."),

 ("h", "Composer à la souris", "Composing with the mouse"),
 ("img", shot("23")),
 ("p", "Les poignées tournent avec l'élément : on les reconnaît à leur couleur, pas à leur place."),
 ("list", [
   "La poignée dorée au centre déplace l'élément.",
   "La poignée dorée à l'extrémité donne la longueur et la direction.",
   "La poignée verte sur le bord le plus large donne la largeur, et selon l'endroit où on la tire le long de l'axe, "
   "elle déplace le ventre.",
   "La poignée verte près de la pointe l'aiguise ou l'arrondit.",
   "La poignée verte en retrait de l'ancre courbe la nervure.",
   "La croix bleue est le pivot de répétition, elle ne touche jamais à la forme.",
 ]),
 ("p", "Maj + clic permet de tenir plusieurs éléments à la fois : la valeur affichée à droite est celle de l'élément "
       "actif, la valeur posée va à tous ceux que vous tenez."),

 ("h", "Répéter un élément", "Repeating an element"),
 ("p", "Sur le panneau de droite, onglet repetition. Quatre modes sont possibles :"),
 ("list", [
   "Single : pas de répétition.",
   "Ring : répétition en cercle autour de l'axe.",
   "Line : répétition en ligne depuis l'axe.",
   "Mirror : répétition en miroir, et ajouter une répétition ajoute un axe de miroir.",
 ]),
 ("p", "Il est possible de déplacer librement l'axe de répétition, la croix bleue."),

 ("h", "Les motifs de coloration", "Colour patterns"),
 ("p", "L'onglet pattern permet d'ajouter un effet au choix sur votre texture : flat, gradient, volume, border, "
       "midrib ou speckled. La texture sera compressée, cela sert donc surtout à ajouter un peu de détail dans les "
       "couleurs, mais restera peu visible."),

 ("h", "Plusieurs éléments, plusieurs fruits", "Several elements, several fruits"),
 ("p", "Vous pouvez ajouter autant d'éléments que vous voulez. L'ordre de calque d'un élément se modifie dans le "
       "dernier onglet, draw order."),
 ("p", "À chaque nouveau fruit ajouté, la texture se compresse un peu plus : plus il y a de fruits, moins il y a de "
       "détails."),

 ("h", "Paramétrer la floraison", "Setting up the bloom"),
 ("p", "On peut retourner en mode Foliage : trois onglets Fruit vous y attendent, où l'on gère la façon dont les "
       "fleurs sont placées, ainsi que leur taille, leur rotation et leur densité."),

 ("h", "Une texture faite de fleurs", "A texture made of flowers"),
 ("p", "C'était la deuxième possibilité annoncée au début. Vous pouvez utiliser vos fleurs pour en faire une "
       "texture : il vous suffit de cocher Foliage made of fruits. Vous n'aurez plus qu'à retourner dans l'onglet "
       "Leaf pour la régler comme vous le voulez. Dans ce cas, pensez à décocher Biome tint, dans le groupe Colour "
       "{foliage|du mode Foliage}."),

 ("h", "Votre bibliothèque de feuilles", "Your leaf library"),
 ("p", "Une feuille est un matériau : elle se réutilise d'un arbre à l'autre et possède son propre dossier."),
 ("list", [
   "Save the leaf enregistre votre travail. Une fois nommée, le bouton affiche le fichier en cours.",
   "Save a copy en fait un deuxième sans toucher au premier, pratique pour décliner une feuille.",
   "Reopen a leaf rouvre une feuille déjà faite, la vôtre ou celle d'un autre arbre de votre pack.",
 ]),
 ("p", "Le nom du fichier est tiré de l'espèce que vous éditez. Une deuxième feuille de chêne devient donc oak-2 : "
       "rien n'est jamais écrasé sans vous le dire."),

 ("h", "À qui appartient la texture", "Who the texture belongs to"),
 ("p", "Une feuille ne déclare pas ce qu'elle remplace : c'est le modèle qui la cite. Elle part avec Save the "
       "variant, comme la forme et le feuillage."),
 ("p", "C'est ce qui permet à deux modèles du même arbre de pousser côte à côte, chacun avec sa feuille, et à deux "
       "packs d'habiller le même chêne sans se marcher dessus."),
 ("p", "Pensez à Apply to the world pour voir votre feuille sur l'arbre : c'est le seul moment où le jeu recharge "
       "ses images, et donc le seul qui prenne un instant."),
]

M4_EN = [
 ("p", "The side panels change to make room for the texture editor: the leaf settings on the right, the texture "
       "choices on the left."),

 ("h", "Deux façons de faire", "Two ways to go about it"),
 ("p", "There are two ways to create your leaf texture: start from a vanilla model and apply your settings to it, or "
       "build a model with the flower editor and apply your settings to that. We will look at both, starting with "
       "the first."),

 ("h", "Sélectionner la texture de base", "Picking the starting texture"),
 ("p", "Under STARTING MODEL, click the Model button. Then pick whichever model you like: the species does not "
       "matter, only its contents do, the one whose shapes come closest to what you are after."),
 ("p", "The leaf itself is entirely redrawn, so you will not find the game's leaf in your result. Your leaves are, "
       "however, sown inside the holes of that texture: it is what gives the tuft its overall cutout, which is why "
       "it is worth picking one whose mass resembles what you want."),
 ("p", "You can also start from your own image: drop a PNG into the leaves/images folder of your pack and it will "
       "show up in the sheet next to the game's textures. The sheet is re-read every time it opens, no need to "
       "restart the game. Your image never enters the atlas, what goes there is the card drawn from it."),
 ("note", "Changing the starting texture halfway erases all your settings: the new texture's measurements replace "
          "them, and the link to your leaf file is cut. Pick your base first, tune afterwards."),

 ("h", "L'aperçu", "The preview"),
 ("p", "Further down you will find a live preview of your foliage. The tree's own foliage, on the other hand, only "
       "updates when you click Apply to the world. Hold TAB at any time to compare before and after, release to come "
       "back."),

 ("h", "Régler votre texture", "Setting up your texture"),
 ("p", "The right panel holds three groups:"),
 ("list", [
   "Silhouette defines the shape of the leaf, not of the tuft.",
   "Tuft controls how the texture lays leaves out, and how many of them.",
   "Colour adjusts the colours and shading of your texture.",
 ]),
 ("fold", "An oak leaf, setting by setting", OAK_EN),

 ("h", "Les fleurs et les fruits", "Flowers and fruit"),
 ("p", "The workshop lets you add flowers and fruit to your trees. Under SUBJECT, click Flowers: a new interface "
       "appears on screen and the left panel gains a few controls."),
 ("p", "+ Add a fruit adds a whole fruit, and you can add as many as you want. Under the selected fruit, whose "
       "number is boxed in gold, you can add, remove or duplicate the elements of that fruit."),

 ("h", "Composer à la souris", "Composing with the mouse"),
 ("img", shot("23")),
 ("p", "The handles turn with the element: you recognise them by their colour, not by their position."),
 ("list", [
   "The gold handle at the centre moves the element.",
   "The gold handle at the end sets the length and the direction.",
   "The green handle on the widest edge sets the width, and depending on where you drag it along the axis, it also "
   "moves the belly.",
   "The green handle near the tip sharpens or rounds it.",
   "The green handle set back from the anchor bends the midrib.",
   "The blue cross is the repetition pivot, it never touches the shape.",
 ]),
 ("p", "Shift + click holds several elements at once: the value shown on the right is the active element's, the "
       "value you set goes to every element you hold."),

 ("h", "Répéter un élément", "Repeating an element"),
 ("p", "On the right panel, repetition tab. Four modes are available:"),
 ("list", [
   "Single: no repetition.",
   "Ring: repeated in a circle around the axis.",
   "Line: repeated in a line from the axis.",
   "Mirror: mirrored, and adding a repetition adds a mirror axis.",
 ]),
 ("p", "The repetition axis, the blue cross, can be moved freely."),

 ("h", "Les motifs de coloration", "Colour patterns"),
 ("p", "The pattern tab adds an effect of your choice on the texture: flat, gradient, volume, border, midrib or "
       "speckled. The texture ends up compressed, so this mostly adds a little detail to the colours and will stay "
       "discreet."),

 ("h", "Plusieurs éléments, plusieurs fruits", "Several elements, several fruits"),
 ("p", "You can add as many elements as you want. An element's layer order is set in the last tab, draw order."),
 ("p", "Every new fruit compresses the texture a little more: the more fruits, the less detail each of them gets."),

 ("h", "Paramétrer la floraison", "Setting up the bloom"),
 ("p", "Back in Foliage mode, three Fruit tabs are waiting for you, where you decide how flowers are placed, along "
       "with their size, their rotation and their density."),

 ("h", "Une texture faite de fleurs", "A texture made of flowers"),
 ("p", "This is the second option announced at the start. You can turn your flowers into the texture itself: tick "
       "Foliage made of fruits, then go back to the Leaf tab to tune it as you please. In that case, remember to "
       "untick Biome tint, in the Colour group of {foliage|Foliage mode}."),

 ("h", "Votre bibliothèque de feuilles", "Your leaf library"),
 ("p", "A leaf is a material: it can be reused from one tree to the next, and it has a folder of its own."),
 ("list", [
   "Save the leaf saves your work. Once named, the button shows the file you are working on.",
   "Save a copy makes a second one without touching the first, handy to derive a variation.",
   "Reopen a leaf opens a leaf you already made, yours or one from another tree in your pack.",
 ]),
 ("p", "The file name comes from the species you are editing. A second oak leaf therefore becomes oak-2: nothing is "
       "ever overwritten without telling you."),

 ("h", "À qui appartient la texture", "Who the texture belongs to"),
 ("p", "A leaf does not declare what it replaces: the model is what cites it. It leaves with Save the variant, just "
       "like the shape and the foliage."),
 ("p", "That is what lets two models of the same tree grow side by side, each with its own leaf, and two packs dress "
       "the same oak without stepping on each other."),
 ("p", "Remember to use Apply to the world to see your leaf on the tree: it is the only moment the game reloads its "
       "images, and therefore the only one that takes a second."),
]


# --------------------------------------------------------------------- module 5

M5_FR = [
 ("h", "À quoi sert ce panneau", "What this panel is for"),
 ("p", "Le panneau de droite vous accompagne depuis le début : c'est lui qui décide de ce que le jeu ajoutera autour "
       "de votre création. Vous avez sculpté une charpente, le procédural la prolonge, la ramifie, l'enracine et la "
       "fait grandir. Ces réglages disent comment."),
 ("p", "Tout ce que vous y touchez est enregistré avec votre variante, en écart par rapport aux réglages du jeu. Ce "
       "que vous ne touchez pas continue de suivre le jeu, et suivra ses évolutions futures. Vous n'emportez donc "
       "que vos décisions, pas une photographie complète des réglages du moment."),

 ("h", "Aucune valeur fixe, seulement des fourchettes", "No fixed values, only ranges"),
 ("p", "La plupart des réglages vont par deux, un minimum et un maximum. Le jeu tire une valeur entre les deux pour "
       "chaque arbre. C'est de là que vient la variété : deux arbres de votre modèle poussent avec le même dessin, "
       "mais pas avec la même longueur de branche ni la même hauteur."),
 ("svg", SVG_RANGE, "Cinq arbres du même modèle, cinq valeurs tirées dans la même fourchette."),
 ("p", "Un minimum égal au maximum donne donc des arbres identiques sur ce point. C'est parfois ce que l'on veut, "
       "souvent non."),

 ("h", "Juger avant de décider", "Judging before deciding"),
 ("p", "Un réglage ne se juge pas sur un arbre. Cochez {shape#the-two-panels|Solid view}, passez en Procedural, et utilisez le bouton Draw "
       "pour relancer le tirage sur le même arbre. Regardez-en cinq ou six avant de valider une fourchette, sans quoi "
       "vous calez votre espèce sur un tirage chanceux."),

 ("h", "Les groupes", "The groups"),
 ("keys", [
   ("Trunk", "la façon dont l'épaisseur diminue vers le haut, la finesse des brindilles, le nettoyage des brindilles "
             "collées au fût, et la graine de tirage."),
   ("Branches", "les branches que le jeu ajoute de lui-même : combien de départs, en combien de segments, de quelle "
                "longueur, avec quel effilement et quel serpentement."),
   ("Ramification", "ce qui repart de ces branches : combien d'enfants, sur combien de générations, avec quelle "
                    "retombée, et la densité de la ramure fine."),
   ("Growth", "de combien l'arbre grandit, et comment ce budget se répartit. Tout mettre en hauteur donne un cou de "
              "girafe ; en laisser au reste donne un arbre moins haut mais plus large et plus dense."),
   ("Roots", "les racines au pied de l'arbre : leur nombre, leur longueur, leur plongée."),
   ("Roots - detail", "le détail de leur propre ramification."),
   ("Burls", "les protubérances du bois."),
 ]),

 ("h", "Revenir en arrière", "Going back"),
 ("p", "Le bouton de retour à côté d'un titre de groupe remet ce groupe aux valeurs qu'il avait au démarrage du jeu. "
       "Back to the game's settings, tout en bas, remet le panneau entier. Ni l'un ni l'autre ne s'annule au "
       "Ctrl + Z, contrairement au reste de l'atelier."),

 ("h", "Tous vos arbres ne porteront pas votre charpente", "Not every tree will carry your framework"),
 ("p", "Par défaut, environ un arbre sur trois reçoit la croissance ajoutée. Les autres gardent la forme que le jeu "
       "leur a donnée : ils portent bien votre écorce et votre feuillage, mais pas les branches que vous avez "
       "sculptées."),
 ("p", "C'est voulu. Un arbre grandi est plus lourd à afficher, pour toujours, et c'est aussi ce qui fait qu'un "
       "grand individu reste remarquable au milieu d'une forêt. Ne soyez donc pas surpris de voir vos arbres "
       "cohabiter avec des chênes plus ordinaires."),

 ("h", "Ce que ce panneau ne contient pas", "What this panel does not hold"),
 ("p", "Certains réglages décrivent la variation d'un arbre à l'autre plutôt que l'arbre lui-même : l'ondulation du "
       "tronc, les individus fins ou trapus, les variations de teinte et d'écorce. Ils sont lus au moment du rendu, "
       "là où plus personne ne sait de quelle espèce il s'agit, et ne peuvent donc pas appartenir à un modèle."),
 ("p", "Ils restent globaux, dans les réglages du jeu, et c'est pour cette raison qu'ils n'apparaissent pas ici."),
]

M5_EN = [
 ("h", "À quoi sert ce panneau", "What this panel is for"),
 ("p", "The right panel has been with you from the start: it decides what the game will add around your creation. "
       "You have sculpted a framework; the procedural side extends it, branches it out, roots it and makes it grow. "
       "These settings say how."),
 ("p", "Everything you touch here is saved with your variant, as a difference from the game's own settings. What you "
       "do not touch keeps following the game, and will follow its future changes. You therefore carry your "
       "decisions only, not a full snapshot of the settings of the day."),

 ("h", "Aucune valeur fixe, seulement des fourchettes", "No fixed values, only ranges"),
 ("p", "Most settings come in pairs, a minimum and a maximum. The game draws a value between the two for every "
       "single tree. That is where variety comes from: two trees of your model grow from the same drawing, but not "
       "with the same branch length nor the same height."),
 ("svg", SVG_RANGE, "Five trees from the same model, five values drawn within the same range."),
 ("p", "A minimum equal to the maximum therefore gives identical trees on that point. Sometimes that is what you "
       "want, often it is not."),

 ("h", "Juger avant de décider", "Judging before deciding"),
 ("p", "A setting cannot be judged on a single tree. Tick {shape#the-two-panels|Solid view}, switch to Procedural, and use the Draw button "
       "to roll again on the same tree. Look at five or six before settling a range, otherwise you are tuning your "
       "species on one lucky roll."),

 ("h", "Les groupes", "The groups"),
 ("keys", [
   ("Trunk", "how thickness decreases towards the top, how fine the twigs are, the cleanup of twigs stuck to the "
             "trunk, and the draw seed."),
   ("Branches", "the branches the game adds on its own: how many starts, in how many segments, how long, with how "
                "much taper and how much twisting."),
   ("Ramification", "what grows out of those branches: how many children, over how many generations, with how much "
                    "droop, and the density of the fine ramification."),
   ("Growth", "how much the tree grows, and how that budget is split. Putting it all into height gives a giraffe "
              "neck; leaving some to the rest gives a shorter but wider and denser tree."),
   ("Roots", "the roots at the foot of the tree: how many, how long, how deep they dive."),
   ("Roots - detail", "the detail of their own ramification."),
   ("Burls", "the knots and swellings of the wood."),
 ]),

 ("h", "Revenir en arrière", "Going back"),
 ("p", "The reset button next to a group title returns that group to the values it had when the game started. Back "
       "to the game's settings, at the very bottom, resets the whole panel. Neither can be undone with Ctrl + Z, "
       "unlike the rest of the workshop."),

 ("h", "Tous vos arbres ne porteront pas votre charpente", "Not every tree will carry your framework"),
 ("p", "By default, about one tree in three receives the added growth. The others keep the shape the game gave them: "
       "they do carry your bark and your foliage, but not the branches you sculpted."),
 ("p", "This is deliberate. A grown tree is heavier to display, forever, and it is also what keeps a large specimen "
       "remarkable in the middle of a forest. Do not be surprised to see your trees living alongside more ordinary "
       "oaks."),

 ("h", "Ce que ce panneau ne contient pas", "What this panel does not hold"),
 ("p", "Some settings describe the variation from one tree to the next rather than the tree itself: the waviness of "
       "the trunk, slender or stocky individuals, shifts in tint and bark. They are read at render time, where "
       "nothing knows which species it is looking at any more, and therefore cannot belong to a model."),
 ("p", "They stay global, in the game's own settings, and that is why they do not appear here."),
]


# -------------------------------------------------------------------- captures
# Où tombe chaque capture : après le paragraphe français qui commence ainsi.

M1_SHOTS = [
 ("Pour accéder à l'éditeur", "1"),
 ("Le menu Add-ons liste", "2"),
 ("Chaque espèce a au minimum", "3"),
 ("La première :", "4"),
 ("La deuxième :", "5"),
 ("La troisième :", "6"),
 ("L'écran des espèces de votre pack", "pub-menu"),
 ("Une fois votre pack publié", "7"),
 ("Une fois validé", "pub-site"),
]

M2_SHOTS = [
 ("Le panneau de gauche rassemble", "8"),
 ("Lorsque vous sélectionnez un segment", "9"),
 ("Utilisez la rotation, les axes", "10"),
 ("Pour vous simplifier la vie", "11"),
 ("Par exemple, pour transformer", "12"),
]

M3_SHOTS = [
 ("Pour un arbre de petite taille", "13"),
 ("Ne remplissez que l'organe", "14"),
 ("Passez en Solid view", "15"),
 ("Plutôt que de refaire", "16"),
 ("Enfin, une cellule reste une feuille", "17"),
]

M4_SHOTS = [
 ("Les panneaux latéraux changent", "18"),
 ("Plus bas, vous voyez l'aperçu", "19"),
 ("+ Add a fruit ajoute un fruit", "22"),
 ("Maj + clic permet de tenir", "handles"),
 ("Il est possible de déplacer librement", "24"),
 ("À chaque nouveau fruit ajouté", "fruits"),
 ("On peut retourner en mode Foliage", "bloom"),
 ("C'était la deuxième possibilité", "flower-tex"),
]

M1_FR, M1_EN = with_shots(M1_FR, M1_EN, M1_SHOTS)
M2_FR, M2_EN = with_shots(M2_FR, M2_EN, M2_SHOTS)
M3_FR, M3_EN = with_shots(M3_FR, M3_EN, M3_SHOTS)
M4_FR, M4_EN = with_shots(M4_FR, M4_EN, M4_SHOTS)


# --------------------------------------------------------------------- le guide
# (titre_fr, titre_en, resume_fr, resume_en, image, corps_fr, corps_en)

CHAPTERS = [
 ("Découverte de l'éditeur", "Discovering the editor",
  "Ouvrir l'atelier, créer un pack, comprendre les espèces, publier et recevoir des créations.",
  "Opening the workshop, creating a pack, reading the species list, publishing and receiving creations.",
  "../img/g4.jpg", M1_FR, M1_EN),
 ("Sculpter la forme", "Shape",
  "Le squelette de l'arbre : les panneaux, les raccourcis, les types de segments, le tronc et les branches.",
  "The tree's skeleton: the panels, the shortcuts, the segment types, the trunk and the branches.",
  None, M2_FR, M2_EN),
 ("Habiller le feuillage", "Foliage",
  "Poser les feuilles organe par organe, et ce que le procédural en fait sur les arbres du monde.",
  "Placing leaves organ by organ, and what the procedural side makes of it on the world's trees.",
  None, M3_FR, M3_EN),
 ("Dessiner la feuille", "Texture",
  "La texture de feuille, les fleurs et les fruits, la bibliothèque, et à qui tout cela appartient.",
  "The leaf texture, flowers and fruit, the library, and who all of it belongs to.",
  None, M4_FR, M4_EN),
 ("Les paramètres procéduraux", "Procedural parameters",
  "Les fourchettes tirées par arbre, ce que chaque groupe règle, et ce qui ne peut pas appartenir à un modèle.",
  "The ranges drawn per tree, what each group controls, and what cannot belong to a model.",
  None, M5_FR, M5_EN),
]
