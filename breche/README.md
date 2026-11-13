# Brèche · plateforme de formation cyber

Proposition validée : https://claude.ai/artifact/RYGXvikRh6hXSqeya8j9qi

## Phase 1 · Socle sécurisé

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
2. `bash 01-reseaux.sh` : crée vmbr1 et vmbr2 (sauvegarde de `/etc/network/interfaces` avant).
3. `bash 02-pare-feu.sh` : table nftables `inet breche`, persistante (service `breche-pare-feu`). N'altère aucune autre règle.
4. `bash 03-vms.sh` : VM 9101 `breche-plateforme` (2 cœurs, 4 Go) et VM 9102 `breche-labs` (6 cœurs, 12 Go), Debian 12.
5. `bash 04-installer-labs.sh` : Docker + DVWA + Juice Shop dans la VM Labs ; internet est ouvert puis refermé automatiquement.
6. `bash 05-test-isolement.sh` : **feu vert 1**. Tout doit afficher OK.

Tout annuler : `bash 99-annuler.sh` (demande de taper OUI).

### S'entraîner depuis ton PC

Les labs ne sont pas joignables depuis la maison, seulement à travers l'hôte :

```
ssh -L 8081:10.10.2.10:8081 -L 8082:10.10.2.10:8082 root@192.168.1.200
```

Puis DVWA sur http://localhost:8081 (admin / password) et Juice Shop sur http://localhost:8082.
