#!/usr/bin/env bash
# Brèche · feu vert 1 : vérifie que la VM Labs ne joint ni internet, ni la maison, ni l'hôte,
# et que les cibles répondent. Lancé depuis l'hôte Proxmox.
set -uo pipefail
cd "$(dirname "$0")"; source ./config.env
SSH="ssh -o BatchMode=yes $VM_USER@$LABS_VM_IP"
GW_LAN=$(ip route show default | awk '{print $3; exit}')
ok=0; ko=0
doit_echouer() { if $SSH "timeout 4 bash -c '</dev/tcp/$1/$2'" 2>/dev/null; then echo "ÉCHEC  la VM Labs joint $3 ($1:$2)"; ko=$((ko+1)); else echo "OK     bloqué : $3"; ok=$((ok+1)); fi; }
doit_marcher() { if $2 >/dev/null 2>&1; then echo "OK     $1"; ok=$((ok+1)); else echo "ÉCHEC  $1"; ko=$((ko+1)); fi; }

bash labs-internet.sh off >/dev/null
doit_echouer 1.1.1.1 443                    "internet (1.1.1.1)"
doit_echouer "$GW_LAN" 80                   "la box ($GW_LAN)"
doit_echouer 192.168.1.200 8006             "l'interface Proxmox"
doit_echouer 192.168.1.201 22               "Ulysse (192.168.1.201)"
doit_echouer "${LABS_HOST_IP%/*}" 8006      "l'hôte via le pont labs"
doit_echouer "$PLAT_VM_IP" 22               "la VM plateforme"
doit_marcher "DVWA répond (depuis l'hôte)"       "curl -sf -m 5 http://$LABS_VM_IP:8081/login.php"
doit_marcher "Juice Shop répond (depuis l'hôte)" "curl -sf -m 5 http://$LABS_VM_IP:8082/"
doit_marcher "Boutique Morel répond (depuis l'hôte)" "curl -sf -m 5 http://$LABS_VM_IP:8090/"
doit_marcher "Intranet Morel répond (depuis l'hôte)" "curl -sf -m 5 http://$LABS_VM_IP:8091/"
echo; echo "Résultat : $ok OK, $ko échec(s)."
[ "$ko" -eq 0 ] && echo "FEU VERT 1 : isolement confirmé." || { echo "Isolement NON confirmé."; exit 1; }
