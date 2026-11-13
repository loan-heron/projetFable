Ton navigateur cache l'essentiel. Derrière chaque clic, il envoie un texte très simple à un serveur, et reçoit un texte en retour.

## Une requête

```http
POST /panier/ajouter HTTP/1.1
Host: boutique.verrerie-morel.fr
Cookie: session=4f9a...
Content-Type: application/x-www-form-urlencoded

produit=12&quantite=1&prix=89.00
```

- La **première ligne** : la méthode (`GET` pour lire, `POST` pour envoyer), le chemin, la version.
- Les **en-têtes** : qui on est (`Cookie`), ce qu'on envoie (`Content-Type`).
- Le **corps** : les données du formulaire.

## Une réponse

```http
HTTP/1.1 302 Found
Location: /panier
Set-Cookie: session=4f9a...; HttpOnly
```

Le code `200` veut dire « OK », `302` « va voir ailleurs », `403` « interdit », `404` « introuvable », `500` « le serveur a planté », souvent un bon signe pour un attaquant.

## Les sessions

HTTP n'a pas de mémoire. Pour savoir que c'est toi, le serveur te donne un **cookie** de session, que le navigateur renvoie à chaque requête. Voler ce cookie, c'est devenir toi.

## La règle d'or

**Tout ce qui vient du navigateur peut être modifié par l'utilisateur.** Les champs cachés, les menus déroulants, les prix, les identifiants dans l'adresse : rien de tout cela n'est fiable. Un serveur qui fait confiance au navigateur est un serveur vulnérable.

C'est exactement l'erreur de la boutique de la Verrerie Morel dans le lab **Prix cassé**.
