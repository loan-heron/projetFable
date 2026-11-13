Toute attaque à distance commence par un paquet envoyé sur un réseau. Il faut savoir ce qu'il contient et par où il passe.

## Le modèle simplifié

| Couche | Rôle | Exemples |
| --- | --- | --- |
| Application | ce que veut dire le message | HTTP, DNS, SSH, SMB |
| Transport | quel programme, quelle fiabilité | TCP, UDP, et les **ports** |
| Réseau | quelle machine | IP, les **adresses** |
| Liaison | quel câble, quelle carte | Ethernet, Wi-Fi, adresses MAC |

Chaque couche enveloppe la précédente, comme une lettre dans une enveloppe, elle-même dans un sac postal.

## Adresses et ports

- Une **adresse IP** désigne une machine : `192.168.1.20`.
- Un **port** désigne un service sur cette machine : `80` pour le web, `443` pour le web chiffré, `22` pour SSH, `3306` pour MySQL.
- Le couple `192.168.1.20:22` désigne donc « le SSH de cette machine ».

## TCP : la poignée de main

Avant d'échanger, TCP établit la connexion en trois temps : **SYN**, **SYN-ACK**, **ACK**. C'est sur ce mécanisme que reposent les scanners de ports : envoyer un SYN et regarder si la porte répond.

## DNS : l'annuaire

Le DNS traduit `boutique.verrerie-morel.fr` en adresse IP. Pour un attaquant, l'annuaire révèle aussi des noms de machines qu'on n'aurait pas dû voir : `intranet`, `vpn`, `test`.

```bash
dig verrerie-morel.fr
dig +short boutique.verrerie-morel.fr
```

## En clair ou chiffré

HTTP, FTP et Telnet circulent **en clair** : quiconque est sur le chemin lit tout, mots de passe compris. HTTPS et SSH chiffrent. C'est l'objet du lab de ce module.
