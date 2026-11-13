#!/usr/bin/env bash
# Brèche · retire tout ce que la phase 1 a ajouté. Demande confirmation.
set -uo pipefail
cd "$(dirname "$0")"; source ./config.env
read -r -p "Supprimer les VM $BRECHE_VMID et $LABS_VMID, les ponts $PLAT_BRIDGE/$LABS_BRIDGE et le pare-feu Brèche ? (tape OUI) " r
[ "$r" = "OUI" ] || { echo "Annulé."; exit 0; }
for id in "$BRECHE_VMID" "$LABS_VMID"; do qm stop "$id" 2>/dev/null; qm destroy "$id" --purge 2>/dev/null; done
systemctl disable --now breche-pare-feu.service 2>/dev/null; rm -f /etc/systemd/system/breche-pare-feu.service
nft delete table inet breche 2>/dev/null
rm -f /etc/network/interfaces.d/breche && ifreload -a
rm -f /etc/sysctl.d/90-breche.conf
echo "Phase 1 retirée."
