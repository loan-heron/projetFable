# Démos avant / après de Rampe

Trois boutiques en ligne **fictives** (noms, marques et produits inventés), chacune en deux versions :

| Boutique | Secteur | Page | Défauts corrigés | Lighthouse avant → après |
|---|---|---|---|---|
| Céladon | Céramique artisanale | Fiche produit | 11 | 61 → 100 |
| Foulée | Running | Page catégorie avec filtres | 10 | 83 → 100 |
| Le Vrac du Coin | Épicerie vrac | Tunnel de commande | 10 | 82 → 100 |

- `*/avant.html` : la page telle qu'on la trouve sur beaucoup de sites marchands (faux boutons, focus effacé, contrastes faibles, carrousel automatique, chrono, CAPTCHA…).
- `*/apres.html` : la même page refaite selon le RGAA 4.1 / WCAG 2.2 AA, avec la même identité visuelle.
- `index.html` : la vitrine qui compare tout (curseur avant / après, chiffres des tests, liste des défauts avec critères RGAA).

## Voir les démos

```bash
cd demos
python3 -m http.server 8765
# puis ouvrir http://localhost:8765/
```

Un serveur local est nécessaire : les icônes sont dans des fichiers `sprites.svg` que les navigateurs ne chargent pas en `file://`.

## Résultats d'audit

`audits/synthese.json` et un fichier JSON par page (règles axe-core en échec, nombre d'occurrences, critères WCAG). Les chiffres :

- erreurs axe-core : 75 / 89 / 55 avant, 0 après ;
- commandes cliquables impossibles au clavier : 20 / 33 / 10 avant, 0 après ;
- arrêts au clavier sans focus visible : 100 % avant, 0 après.

Les défauts que les robots ne voient pas (chrono, CAPTCHA, information par la couleur, pop-up…) sont documentés à la main dans `scripts/build_vitrine.py`.

## Régénérer

Prérequis : Node 18+, Playwright avec Chromium, `npm i axe-core lighthouse chrome-launcher` (en dehors du dépôt).

```bash
node scripts/audit.cjs http://localhost:8765 audits      # axe-core + Lighthouse + tests clavier
node scripts/captures.cjs http://localhost:8765 captures # captures ordinateur et mobile
python3 scripts/build_vitrine.py                          # reconstruit index.html
```

`vitrine-fragment.html` est la même vitrine sans squelette HTML, utilisée pour la publier en Artifact.

Polices : Instrument Serif, Figtree, Barlow, Barlow Condensed, Bricolage Grotesque, Archivo, Atkinson Hyperlegible Next, toutes sous licence SIL Open Font License, hébergées localement dans `fonts/`.
