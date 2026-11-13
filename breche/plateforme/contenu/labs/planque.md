**Objectif** : retrouver le drapeau caché par Julien Faure, technicien à la Verrerie Morel, sur un serveur de test.

## Lancer le lab

Il faut [Docker](https://docs.docker.com/get-docker/) sur ta machine.

```bash
docker run --rm -it --name planque $(docker build -q https://github.com/loan-heron/projetFable.git#claude/project-thread-5ylzcz:breche/cibles/planque)
```

Tu arrives dans un shell, connecté en tant que `stagiaire`.

## Indices (n'ouvre qu'en cas de besoin)

<details><summary>Indice 1</summary>Julien n'est pas toi. Où sont les dossiers des autres utilisateurs ?</details>
<details><summary>Indice 2</summary>Un nom qui commence par un point ne s'affiche pas avec un simple <code>ls</code>.</details>
<details><summary>Indice 3</summary>Les gens notent leurs commandes sans le savoir : regarde l'historique.</details>
