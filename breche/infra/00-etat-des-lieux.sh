#!/usr/bin/env bash
# Brèche · état des lieux du serveur. LECTURE SEULE : ne modifie rien.
# À lancer en root sur l'hôte Proxmox : bash 00-etat-des-lieux.sh
set -u
sec() { printf '\n===== %s =====\n' "$1"; }
sec "Version Proxmox";        pveversion 2>/dev/null || echo "pveversion introuvable"
sec "CPU";                    nproc; grep -m1 'model name' /proc/cpuinfo
sec "Mémoire";                free -h
sec "Stockages Proxmox";      pvesm status 2>/dev/null
sec "Disques";                df -h -x tmpfs -x devtmpfs
sec "VM existantes";          qm list 2>/dev/null
sec "Conteneurs existants";   pct list 2>/dev/null
sec "Ponts réseau";           ip -br addr show type bridge
sec "Route par défaut";       ip route show default
sec "Fichier interfaces";     cat /etc/network/interfaces
sec "Pare-feu Proxmox";       pve-firewall status 2>/dev/null
sec "Tables nftables";        nft list tables 2>/dev/null
sec "Transfert IP";           sysctl net.ipv4.ip_forward
sec "Clé SSH root";           ls /root/.ssh/*.pub 2>/dev/null || echo "aucune clé publique"
sec "Fin";                    echo "Rien n'a été modifié."
