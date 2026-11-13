#!/usr/bin/env bash
# Brèche · installe la table nftables d'isolement et la rend persistante au redémarrage.
set -euo pipefail
cd "$(dirname "$0")"; source ./config.env
mkdir -p /etc/breche
sed -e "s|@LABS@|$LABS_BRIDGE|g" -e "s|@PLAT@|$PLAT_BRIDGE|g" -e "s|@LAN@|$LAN_BRIDGE|g" \
    -e "s|@LAN_SUBNET@|$LAN_SUBNET|g" -e "s|@PLAT_SUBNET@|$PLAT_SUBNET|g" -e "s|@LABS_VM_IP@|$LABS_VM_IP|g" \
    breche.nft.tpl > /etc/breche/breche.nft
nft -c -f /etc/breche/breche.nft
nft list table inet breche >/dev/null 2>&1 && nft delete table inet breche
nft -f /etc/breche/breche.nft

cat > /etc/systemd/system/breche-pare-feu.service <<UNIT
[Unit]
Description=Brèche : isolement des réseaux labs et plateforme
After=network-online.target pve-firewall.service

[Service]
Type=oneshot
RemainAfterExit=yes
ExecStart=/bin/sh -c 'nft list table inet breche >/dev/null 2>&1 && nft delete table inet breche; nft -f /etc/breche/breche.nft'
ExecStop=/usr/sbin/nft delete table inet breche

[Install]
WantedBy=multi-user.target
UNIT
systemctl daemon-reload
systemctl enable --now breche-pare-feu.service >/dev/null
echo "Pare-feu Brèche actif et persistant."
nft list table inet breche >/dev/null && echo "Table inet breche chargée."
