# Tactile — vitrine

Site vitrine de la **suite Tactile**, une série de mods Minecraft qui remplacent les
interfaces par des interactions physiques et gestuelles dans le monde.

Le site est un ensemble de pages HTML statiques, sans build ni dépendance :
il est servi tel quel par GitHub Pages.

## Structure

```
index.html            page d'accueil
assets/               favicon + images de l'accueil
<module>/index.html   une page par module
<module>/img/         les images de ce module
```

## Modifier une image

Remplacer le fichier dans `<module>/img/` en gardant le même nom.
Les proportions utilisées à l'affichage :

| Fichier | Emplacement | Format |
| --- | --- | --- |
| `hero.jpg` | bandeau du haut | large (~3:1) |
| `1.jpg`, `2.jpg`, … | rangées de présentation | 16:10 |
| `g1.jpg`, `g2.jpg`, … | galerie | 16:9 |

Le cadrage se fait au centre : garder le sujet centré.

## Langues

Chaque texte porte ses deux versions dans les attributs `data-fr` et `data-en`.
Le sélecteur FR/EN les échange et retient le choix d'une page à l'autre.
