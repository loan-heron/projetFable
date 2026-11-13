# Brèche · plateforme de formation cyber

Proposition validée : https://claude.ai/artifact/RYGXvikRh6hXSqeya8j9qi

## Phase 1 · Socle sécurisé

Nœud cible : **192.168.1.200** (Ryzen 7 5700G, 30 Go dont environ 13 Go libres, PVE 9.2.5, ~700 Go libres sur local-lvm).

Objectif : deux réseaux virtuels isolés sur le nœud Proxmox, une VM plateforme, une VM labs,
et les premières cibles d'entraînement (DVWA, OWASP Juice Shop), sans qu'aucune cible
puisse joindre la maison, internet ou l'hôte Proxmox.

| Réseau | Pont | Plage | Internet | Maison | Hôte Proxmox |
| --- | --- | --- | --- | --- | --- |
| Maison (existant) | vmbr0 | 192.168.1.0/24 | oui | oui | oui |
| Plateforme | vmbr1 | 10.10.1.0/24 | oui (NAT) | **non** | **non** |
| Labs | vmbr2 | 10.10.2.0/24 | **non** (sauf `labs-internet.sh on`) | **non** | **non** |

### Ordre d'exécution (en root sur l'hôte Proxmox, dans `breche/infra/`)

1. `bash 00-etat-des-lieux.sh` : lecture seule, puis ajuster `config.env` (pont maison, stockage, RAM, identifiants de VM).
2. `bash 01-reseaux.sh` : crée vmbr1 et vmbr2 (dans `/etc/network/interfaces.d/breche`, rien d’autre n’est modifié).
3. `bash 02-pare-feu.sh` : table nftables `inet breche`, persistante (service `breche-pare-feu`). N'altère aucune autre règle.
4. `bash 03-vms.sh` : VM 9101 `breche-plateforme` (2 cœurs, 2 Go) et VM 9102 `breche-labs` (4 cœurs, 6 Go), Debian 12.
5. `bash 04-installer-labs.sh` : Docker + DVWA + Juice Shop dans la VM Labs ; internet est ouvert puis refermé automatiquement.
6. `bash 05-test-isolement.sh` : **feu vert 1**. Tout doit afficher OK.

Tout annuler : `bash 99-annuler.sh` (demande de taper OUI).

### S'entraîner depuis ton PC

Les labs ne sont pas joignables depuis la maison, seulement à travers l'hôte :

```
ssh -L 8081:10.10.2.10:8081 -L 8082:10.10.2.10:8082 root@192.168.1.200
```

Puis DVWA sur http://localhost:8081 (admin / password) et Juice Shop sur http://localhost:8082.

## Phase 2 et suivantes · La plateforme

| Dossier | Contenu |
| --- | --- |
| `plateforme/` | Serveur Node 22 sans framework (http et SQLite natifs, `marked`) : comptes, carte de progression, leçons, validation des drapeaux. |
| `plateforme/contenu/` | Parcours (`parcours.json`), 12 leçons et 5 labs des modules 1 à 5, en Markdown. |
| `plateforme/public/` | Charte « dossier d'enquête » : `style.css`, logo, favicon. Mode sombre automatique. |
| `cibles/planque/` | Lab du module 1 (shell Linux). |
| `cibles/boutique/` | Morel Optique, cible **volontairement vulnérable** des modules 3, 4 et 5. |
| `outils/generer-ecoute.py` | Génère la capture réseau du module 2. |
| `deploiement/` | `docker-compose.yml` de la plateforme sur la VM 9101. |

### Lancer la plateforme en local

```
cd plateforme && npm ci && npm start   # http://localhost:8080
```

Variables : `BRECHE_INVITATION` (code exigé à l'inscription ; vide = inscriptions ouvertes), `BRECHE_COOKIE_SECURE=1` derrière HTTPS, `BRECHE_ADMIN_EMAIL`.

### Déployer sur le serveur (depuis l'hôte, dans `infra/`)

1. `bash 02-pare-feu.sh` : recharge l'isolement, avec la redirection 192.168.1.200:8443 vers la plateforme (seul port ouvert depuis la maison).
2. `bash 07-disques-400go.sh` : disques à 40 Go + 360 Go = 400 Go.
3. `bash 06-deployer-plateforme.sh` : installe et lance la plateforme, affiche le code d'invitation.
4. `bash 04-installer-labs.sh` puis `bash 05-test-isolement.sh` : ajoute la boutique aux labs et revérifie l'isolement.
5. Reverse proxy HTTPS du réseau maison : `breche.<domaine>` vers `http://192.168.1.200:8443`.

### Ce qui est public, ce qui ne l'est pas

- **Public** : la plateforme (cours, comptes, progression), en HTTPS, inscription par code d'invitation.
- **Jamais public** : les cibles vulnérables. Les apprenants les lancent sur leur machine (`docker build` depuis ce dépôt), publiées sur 127.0.0.1. Celles du serveur restent dans vmbr2, sans route depuis internet ni depuis la maison.
- **Limite connue** : comme les cibles tournent chez l'apprenant et que le dépôt est public, un drapeau peut être lu dans le code. C'est un parcours d'apprentissage, pas un concours.
