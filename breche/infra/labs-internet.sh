#!/usr/bin/env bash
# Brèche · ouvre ou ferme internet pour la VM Labs (le temps de télécharger des images Docker).
# Usage : bash labs-internet.sh on|off|etat   — la maison reste bloquée dans tous les cas.
set -euo pipefail
cd "$(dirname "$0")"; source ./config.env
case "${1:-etat}" in
  on)  nft add element inet breche labs_internet "{ $LABS_VM_IP }"; echo "Internet OUVERT pour $LABS_VM_IP. Pense à refermer : labs-internet.sh off";;
  off) nft flush set inet breche labs_internet; echo "Internet FERMÉ pour les labs.";;
  *)   nft list set inet breche labs_internet;;
esac
