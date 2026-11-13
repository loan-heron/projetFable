Attaquer puis réparer : c'est la règle de Brèche. Corriger une injection SQL tient en une idée.

## Ne jamais concaténer

Le problème n'est pas l'apostrophe, c'est le mélange. La correction ne consiste **pas** à filtrer les caractères dangereux : on en oublie toujours un.

## Les requêtes préparées

On envoie à la base la requête **et** les données séparément. La base sait que la donnée est une donnée, quoi qu'elle contienne.

```python
# Vulnérable
db.execute("SELECT nom, prix FROM produits WHERE nom LIKE '%" + q + "%'")

# Corrigé
db.execute("SELECT nom, prix FROM produits WHERE nom LIKE ?", (f"%{q}%",))
```

```php
// PHP avec PDO
$st = $pdo->prepare('SELECT nom, prix FROM produits WHERE nom LIKE ?');
$st->execute(['%' . $q . '%']);
```

## Les défenses en plus

1. **Moindre privilège** : le compte SQL de la boutique n'a besoin que de lire les produits, pas d'accéder à toute la base.
2. **Pas d'erreurs détaillées** en production : elles guident l'attaquant.
3. **Un ORM** (SQLAlchemy, Prisma, Eloquent) prépare les requêtes pour toi, tant que tu n'écris pas de SQL brut.

## Exercice de défense

Dans le dossier de la cible `boutique`, ouvre `app.py`, trouve les requêtes concaténées et réécris-les avec des paramètres. Relance la boutique : ton injection du lab doit maintenant échouer, et la recherche normale doit toujours marcher.
