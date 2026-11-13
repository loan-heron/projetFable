Un proxy d'interception se place entre ton navigateur et le serveur. Chaque requête s'arrête chez lui, tu la lis, tu la modifies, puis tu la laisses repartir.

## Les deux outils

- **Burp Suite Community** : la référence, gratuite dans sa version de base.
- **OWASP ZAP** : entièrement libre et gratuit.

Les deux font la même chose pour ce module. Les exemples utilisent Burp.

## Mettre en place

1. Lance Burp, onglet *Proxy*. Il écoute sur `127.0.0.1:8080`.
2. Ouvre le navigateur intégré de Burp (*Open browser*) : il est déjà configuré.
3. Active *Intercept is on*.

## Intercepter et modifier

1. Dans le navigateur, clique sur un bouton du site.
2. Burp affiche la requête, en attente.
3. Modifie un paramètre, par exemple `quantite=1` en `quantite=-1`.
4. Clique *Forward*. Le serveur reçoit ta version.

## Rejouer : le Repeater

Clic droit sur une requête, *Send to Repeater*. Tu peux la renvoyer autant de fois que tu veux en changeant un détail, et comparer les réponses. C'est l'outil de tous les tests manuels.

## Le lab : Prix cassé

Lance la boutique Morel Optique en local. Achète la **Lunette de Galilée, édition dossier** sans payer son prix. La confirmation de commande contient le drapeau.
