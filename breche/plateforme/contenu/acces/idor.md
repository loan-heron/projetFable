Être connecté ne veut pas dire avoir le droit de tout voir. Le contrôle d'accès répond à une question simple, à chaque requête : **cet utilisateur a-t-il le droit sur cette donnée précise ?** C'est la faille numéro un du classement OWASP.

## Authentification et autorisation

- **Authentification** : qui es-tu ? (le mot de passe, le cookie)
- **Autorisation** : as-tu le droit de faire ça ? (lire ce dossier, supprimer ce compte)

Beaucoup de sites font très bien la première et oublient la seconde.

## L'IDOR

Une IDOR (*Insecure Direct Object Reference*) : l'URL ou le formulaire contient l'identifiant d'un objet, et le serveur le sert sans vérifier à qui il appartient.

```
/facture?id=5521        → ta facture
/facture?id=5520        → celle de quelqu'un d'autre ?
```

Où chercher les identifiants :

- dans l'URL (`?id=`, `/utilisateur/42/`) ;
- dans le corps des requêtes POST et le JSON des API (`"compte_id": 42`) ;
- dans les champs cachés des formulaires ;
- dans les cookies.

## Méthode

1. **Crée deux comptes** quand c'est possible (A et B). Note les identifiants de chacun.
2. Connecté en A, rejoue les requêtes de B avec les identifiants de B. Dans Burp, le *Repeater* est fait pour ça.
3. Si les identifiants sont des nombres qui se suivent, essaie les voisins. Un petit script suffit :

```bash
for i in $(seq 1000 1050); do
  curl -s -b "session=TON_COOKIE" "http://cible/dossier?id=$i" -o /dev/null -w "$i %{http_code}\n"
done
```

Les `200` sont des dossiers qui existent **et** qu'on te donne.

## Les identifiants aléatoires ne suffisent pas

Remplacer `1043` par un UUID rend la devinette difficile, mais ne corrige rien : l'identifiant finit par fuiter (un lien partagé, un journal, une autre API). La seule vraie correction est la vérification côté serveur, qu'on verra dans la dernière leçon.

## Les variantes

- **Élévation verticale** : un utilisateur appelle une fonction d'administrateur (`/admin/supprimer`) parce que seul le bouton était caché.
- **Logique métier** : le serveur vérifie chaque étape séparément mais pas l'enchaînement (passer à « payé » sans passer par le paiement, comme le prix dans le module 3).
