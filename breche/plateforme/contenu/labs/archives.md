**Objectif** : trouver ce que la boutique ne voulait pas montrer aux moteurs de recherche.

## Lancer la boutique Morel Optique

Il faut [Docker](https://docs.docker.com/get-docker/) sur ta machine. La même cible sert aux labs des modules 3, 4 et 5.

```bash
docker build -t breche/boutique https://github.com/loan-heron/projetFable.git#claude/project-thread-5ylzcz:breche/cibles/boutique
docker run --rm -p 127.0.0.1:8090:8090 breche/boutique
```

Puis ouvre http://127.0.0.1:8090. La boutique n'écoute que sur ta machine : personne d'autre ne peut l'atteindre.

## Indices

<details><summary>Indice 1</summary>Il y a un fichier que tous les robots lisent en premier.</details>
<details><summary>Indice 2</summary>Une archive peut contenir une configuration complète.</details>
