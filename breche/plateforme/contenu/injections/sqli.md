Une injection arrive quand un programme mélange des **données** fournies par l'utilisateur avec du **code**. La plus célèbre est l'injection SQL.

## Le code fautif

La boutique cherche des produits ainsi :

```python
requete = "SELECT nom, prix FROM produits WHERE nom LIKE '%" + recherche + "%'"
```

Si tu cherches `prisme`, la base reçoit :

```sql
SELECT nom, prix FROM produits WHERE nom LIKE '%prisme%'
```

Si tu cherches `prisme'`, la base reçoit une apostrophe de trop, la requête est cassée, et la page affiche une erreur. **Une erreur sur une apostrophe est le premier signe d'une injection.**

## Changer le sens de la requête

```
' OR 1=1 --
```

devient

```sql
SELECT nom, prix FROM produits WHERE nom LIKE '%' OR 1=1 -- %'
```

`OR 1=1` est toujours vrai, `--` transforme la suite en commentaire. La base renvoie **tous** les produits, y compris ceux qui ne devaient pas apparaître.

## Contourner une connexion

Sur un formulaire de connexion vulnérable :

```
Identifiant : admin' --
Mot de passe : n'importe quoi
```

La vérification du mot de passe passe en commentaire. On est connecté en admin.

## Pourquoi c'est grave

Une injection SQL donne accès à toute la base : comptes, mots de passe, données clients, parfois le serveur lui-même. Elle figure depuis vingt ans dans le classement OWASP des risques web.
