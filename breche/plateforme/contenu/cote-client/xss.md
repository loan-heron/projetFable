Jusqu'ici tu attaquais le serveur. Ici, tu attaques **les autres utilisateurs**, à travers leur navigateur.

## L'idée

Une XSS (*cross-site scripting*) arrive quand un site affiche un texte fourni par quelqu'un **sans le neutraliser**. Si ce texte contient `<script>`, le navigateur de chaque visiteur l'exécute, avec les droits du visiteur sur ce site.

Le navigateur ne fait aucune différence entre le JavaScript écrit par les développeurs et celui que tu as glissé dans un commentaire. Il voit une page de `intranet.morel`, il lui fait confiance.

## Trois familles

| Type | Où vit la charge | Qui est touché |
|---|---|---|
| **Réfléchie** | Dans l'URL (`?q=<script>…`) | Celui qui clique sur ton lien |
| **Stockée** | En base (message, profil, avis) | Tous ceux qui affichent la page |
| **DOM** | Dans le JavaScript de la page (`innerHTML = location.hash`) | Celui qui ouvre le lien, sans passage par le serveur |

La stockée est la plus grave : pas besoin de convaincre la victime de cliquer, il suffit qu'elle fasse son travail normalement.

## Détecter

Commence toujours par une charge **inoffensive et visible**, pas par une alerte :

```html
<b>test-gras</b>
```

Si le texte apparaît en gras, le HTML n'est pas neutralisé. Regarde ensuite le code source (`Ctrl+U`) : tes chevrons sont-ils restés `<b>` ou devenus `&lt;b&gt;` ?

Puis vérifie que le JavaScript passe :

```html
<img src=x onerror="document.title='xss'">
```

Si l'onglet change de titre, tu exécutes du code. `<script>` n'est pas toujours nécessaire : un attribut d'événement (`onerror`, `onload`, `onfocus`) suffit souvent, et passe des filtres naïfs.

## Selon le contexte

Ta donnée n'atterrit pas toujours au même endroit. La charge dépend de ce qui l'entoure :

- **Entre deux balises** : `<script>…</script>` ou `<img src=x onerror=…>`.
- **Dans un attribut** `value="ICI"` : ferme d'abord, `"><img src=x onerror=…>`.
- **Dans une chaîne JavaScript** `var q = 'ICI';` : `';alert(1);//`.

Lire le code source autour de ton point d'injection est la moitié du travail.

## Ce qu'un attaquant en fait

Une alerte ne prouve rien à un client. Ce qui compte, c'est l'impact : lire ce que la victime voit, agir à sa place, ou **voler sa session**. C'est la leçon suivante.
