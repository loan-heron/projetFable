La correction d'une IDOR tient en une ligne, mais il faut l'écrire **partout**.

## Vérifier l'appartenance côté serveur

Le serveur sait qui est connecté (la session). Il ne doit jamais croire l'identifiant envoyé sans le comparer :

```python
# Vulnérable
d = DOSSIERS.get(n)

# Corrigé
d = DOSSIERS.get(n)
if not d or n != COMPTES[session["compte"]]["dossier"]:
    abort(404)
```

On répond `404` plutôt que `403` : inutile de confirmer à l'attaquant que le dossier existe.

## Mieux : ne pas demander l'identifiant

Si un utilisateur ne peut voir que **son** dossier, l'URL n'a pas besoin de numéro :

```
/mutuelle/mon-dossier
```

Le serveur prend le numéro dans la session. Il n'y a plus rien à falsifier.

## Avec une base de données

Filtre directement dans la requête, avec le propriétaire :

```sql
SELECT * FROM factures WHERE id = ? AND client_id = ?
```

Si la ligne n'appartient pas à l'utilisateur, la requête ne renvoie rien. C'est plus sûr qu'une vérification après coup, qu'on finit par oublier sur une route.

## Centraliser

Une règle écrite dans quarante routes sera oubliée dans la quarante et unième. Les frameworks proposent un point unique : les *policies* de Laravel, les permissions de Django REST, un middleware maison. Brèche fait pareil : toutes ses pages privées passent par la même vérification avant d'arriver à la route.

## Pour les JWT

- Fixe l'algorithme attendu côté serveur (`algorithms=["HS256"]`), ne le lis pas dans le jeton.
- Une clé longue et aléatoire, au moins 32 octets, rangée hors du code.
- Une durée de vie courte (`exp`), et un moyen de révoquer.

## Exercice de défense

Dans `app.py` de la cible `intranet`, corrige la route `/mutuelle/dossier` pour qu'un utilisateur ne puisse lire que son propre dossier. Relance : `?id=1043` doit marcher pour le stagiaire, `?id=1001` doit renvoyer une erreur.
