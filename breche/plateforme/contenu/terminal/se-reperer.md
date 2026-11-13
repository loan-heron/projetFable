Un serveur n'a pas d'écran. Tout ce que tu feras sur une machine compromise passera par un **shell**, ce programme qui lit tes commandes et les exécute. Avant d'attaquer quoi que ce soit, il faut s'y sentir chez soi.

## Où suis-je, qui suis-je

```bash
whoami        # quel utilisateur je suis
hostname      # sur quelle machine
pwd           # dans quel dossier
id            # mon identifiant et mes groupes
```

Ces quatre commandes sont les premières que tape un attaquant qui vient d'obtenir un accès. Elles répondent à la seule question qui compte : *qu'est-ce que je peux faire d'ici ?*

## Se déplacer

```bash
ls            # lister
ls -la        # tout lister, y compris les fichiers cachés (ceux qui commencent par un point)
cd /etc       # aller dans /etc
cd ..         # remonter d'un cran
cd ~          # revenir chez soi
```

> Sous Linux, un fichier est « caché » simplement parce que son nom commence par un point. Ce n'est pas une protection, c'est une convention d'affichage. Retiens-le : c'est la clé du lab de ce module.

## Lire sans abîmer

```bash
cat fichier           # afficher en entier
less fichier          # feuilleter (q pour quitter)
head -n 20 fichier    # les 20 premières lignes
file inconnu          # deviner le type d'un fichier
```

## L'arborescence à connaître

| Dossier | Ce qu'on y trouve | Pourquoi ça intéresse un attaquant |
| --- | --- | --- |
| `/etc` | la configuration | mots de passe en clair oubliés, services installés |
| `/home` | les dossiers des utilisateurs | notes, clés SSH, historiques de commandes |
| `/var/log` | les journaux | ce qui s'est passé, et ce que l'admin voit |
| `/tmp` | les fichiers temporaires | tout le monde peut y écrire |
| `/opt` | les logiciels ajoutés à la main | souvent mal configurés |

## À retenir

Un bon enquêteur ne se précipite pas. Il regarde où il est, qui il est, et ce qui traîne autour de lui. C'est exactement ce que tu feras dans **La planque**.
