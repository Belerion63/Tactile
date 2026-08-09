# Générateurs du site

Le site est écrit par ces scripts. **Les fichiers HTML ne se modifient pas à la
main** : ils sont réécrits à chaque exécution.

## Régénérer

```
python build_landing4.py    accueil (index.html)
python build_all.py         les 15 pages de modules
python build_addons.py      la galerie des créations
```

Les trois écrivent directement dans `website/`. Aucun ordre imposé.

| Fichier | Rôle |
| --- | --- |
| `build_landing4.py` | accueil : bannière, tuiles, vision, pistes, pied de page |
| `build_all.py` | une page par module ; le contenu des modules réels y est écrit en dur |
| `concepts.py` | textes et schémas des 12 fiches conceptuelles, importé par `build_all` |
| `build_addons.py` | galerie des créations, lit `addons/addons.json` |
| `make_og.py` | carte de partage `assets/og.jpg`, à relancer si l'accroche change |
| `optimize_imgs.py` | réencode pour le web toute image de plus de 400 Ko |

## Règles

**Les images ne sont jamais écrasées.** Une image déjà présente dans
`<module>/img/` ou `assets/img/` appartient à son auteur : les générateurs ne
créent que celles qui manquent. Pour remplacer une image, il suffit de déposer
le fichier au même nom.

**Les images lourdes passent par `optimize_imgs.py`.** Tout ce qui entre dans
git y reste pour toujours : une capture de 8 Mo poussée une fois pèsera sur le
dépôt à jamais. Le script sauvegarde les originaux dans
`Documentation/site-originaux/` avant de réencoder.

**Le texte est bilingue.** Chaque chaîne porte ses deux versions, et l'anglais
est la langue affichée par défaut : `en_first()` réécrit le texte visible en
anglais à la génération, pour qu'aucun français n'apparaisse avant que le script
de langue ne s'exécute.

## Dossiers

- `preview/` : aperçus hors ligne, non publiés, régénérés à volonté
- `src/` : images d'origine, utiles seulement pour amorcer une image absente du
  site. Vide par défaut : tout ce dont le site a besoin est déjà dans `website/`.

## Ajouter une création à la galerie

1. Attacher l'archive à une Release GitHub
2. Déposer les images dans `addons/img/`
3. Ajouter l'entrée dans `addons/addons.json`
4. `python build_addons.py`

Le format d'une entrée et la chaîne complète sont décrits dans
`Documentation/ADDONS.md`.
