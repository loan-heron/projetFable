**Objectif** : lire le dossier médical de la directrice sur le portail mutuelle. Tu n'es que stagiaire.

## Lancer l'intranet Morel

C'est la même cible que pour le lab du module 6. Si elle tourne déjà, rien à faire.

```bash
docker build -t breche/intranet https://github.com/loan-heron/projetFable.git#claude/project-thread-5ylzcz:breche/cibles/intranet
docker run --rm -p 127.0.0.1:8091:8091 breche/intranet
```

Ouvre http://127.0.0.1:8091 et connecte-toi en `stagiaire` / `stagiaire`, puis clique sur « Mon dossier mutuelle ».

## Indices

<details><summary>Indice 1</summary>Regarde l'adresse de ton propre dossier.</details>
<details><summary>Indice 2</summary>Les numéros se suivent. La directrice était là bien avant toi.</details>
<details><summary>Indice 3</summary>Essaie les dossiers à partir de <code>?id=1001</code>.</details>
