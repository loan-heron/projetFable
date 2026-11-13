#!/usr/bin/env bash
# Brèche · crée les deux ponts isolés (vmbr1 plateforme, vmbr2 labs).
# Ne touche pas aux ponts existants : tout est écrit dans /etc/network/interfaces.d/breche.
# Annulation : bash 99-annuler.sh
set -euo pipefail
cd "$(dirname "$0")"; source ./config.env

for br in "$PLAT_BRIDGE" "$LABS_BRIDGE"; do
  if ip link show "$br" >/dev/null 2>&1 || grep -rqs "iface $br" /etc/network/interfaces /etc/network/interfaces.d/; then
    echo "Le pont $br existe déjà : arrêt, rien n'a été modifié. Change PLAT_BRIDGE/LABS_BRIDGE dans config.env."; exit 1
  fi
done

grep -q "source /etc/network/interfaces.d/\*" /etc/network/interfaces || { echo "La ligne source interfaces.d/* manque dans /etc/network/interfaces : arrêt."; exit 1; }
cat > /etc/network/interfaces.d/breche <<NET

# --- Brèche : réseau plateforme (internet oui, maison non) ---
auto $PLAT_BRIDGE
iface $PLAT_BRIDGE inet static
	address $PLAT_HOST_IP
	bridge-ports none
	bridge-stp off
	bridge-fd 0

# --- Brèche : réseau labs (ni internet, ni maison, ni hôte) ---
auto $LABS_BRIDGE
iface $LABS_BRIDGE inet static
	address $LABS_HOST_IP
	bridge-ports none
	bridge-stp off
	bridge-fd 0
NET

ifreload -a
sysctl -w net.ipv4.ip_forward=1 >/dev/null
echo 'net.ipv4.ip_forward=1' > /etc/sysctl.d/90-breche.conf
ip -br addr show "$PLAT_BRIDGE" "$LABS_BRIDGE"
echo "Ponts créés. Étape suivante : 02-pare-feu.sh"
