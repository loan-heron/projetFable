Beaucoup d'applications modernes n'ont plus de session en base. Elles donnent au client un **jeton signé** qui contient son identité : le JWT (*JSON Web Token*). Si la signature est mal vérifiée, tu deviens qui tu veux.

## Anatomie

Un JWT, ce sont trois morceaux en base64url séparés par des points :

```
eyJhbGciOiJIUzI1NiJ9.eyJ1dGlsaXNhdGV1ciI6InN0YWdpYWlyZSIsInJvbGUiOiJ1c2VyIn0.4kJ…
      en-tête                          contenu                                 signature
```

Décode les deux premiers :

```bash
echo 'eyJhbGciOiJIUzI1NiJ9' | base64 -d
# {"alg":"HS256"}
echo 'eyJ1dGlsaXNhdGV1ciI6InN0YWdpYWlyZSIsInJvbGUiOiJ1c2VyIn0' | base64 -d
# {"utilisateur":"stagiaire","role":"user"}
```

Si `base64` affiche « invalid input » à la fin, c'est normal : le JWT retire les `=` de remplissage, le texte décodé est bon.

Le contenu est **lisible par tous**. Il n'est pas chiffré, seulement signé. Ne mets jamais de secret dedans.

## Ce qui protège

La signature est calculée avec une clé que seul le serveur connaît. Si tu changes `"role":"user"` en `"role":"admin"`, la signature ne correspond plus et le serveur doit refuser. Toutes les attaques visent ce « doit ».

## Les attaques classiques

1. **`alg: none`** : certaines bibliothèques anciennes acceptent un jeton qui annonce ne pas être signé. On change l'en-tête en `{"alg":"none"}`, on modifie le contenu et on vide la signature.
2. **Clé faible** : avec HS256, la clé est un simple secret partagé. S'il vaut `secret` ou `changeme`, on le retrouve hors ligne :

```bash
hashcat -m 16500 jeton.txt rockyou.txt
```

Une fois la clé connue, tu signes les jetons que tu veux.

3. **Confusion d'algorithme** : le serveur attend RS256 (clé publique/privée) mais accepte HS256. On signe alors avec la **clé publique** comme secret, et elle est publique par définition.
4. **Signature jamais vérifiée** : le code décode le jeton (`jwt.decode(t, options={"verify_signature": False})`) pour lire le rôle, et oublie de le vérifier ailleurs.

L'outil de référence pour tester tout ça est `jwt_tool`, et l'extension *JWT Editor* de Burp.

## Ce qu'il faut retenir

Un JWT ne remplace pas le contrôle d'accès. Même parfaitement signé, il dit seulement *qui* est l'utilisateur. Le serveur doit encore vérifier, pour chaque objet, que cet utilisateur y a droit.
