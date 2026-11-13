#!/usr/bin/env bash
# Brèche · installe Docker sur la VM plateforme (9101), récupère le code et lance la plateforme.
# Lancé depuis l'hôte Proxmox. Réexécutable : met à jour et redémarre.
set -euo pipefail
cd "$(dirname "$0")"; source ./config.env
BRANCHE="${BRANCHE:-claude/project-thread-5ylzcz}"
SSH="ssh -o StrictHostKeyChecking=accept-new $VM_USER@$PLAT_VM_IP"
$SSH "timeout 300 sudo cloud-init status --wait >/dev/null || true
  APT='-o Acquire::http::Timeout=15 -o Acquire::Retries=2 -o DPkg::Lock::Timeout=120'
  command -v docker >/dev/null || { sudo apt-get \$APT update -q && sudo apt-get \$APT install -yq docker.io docker-compose git qemu-guest-agent; sudo systemctl enable --now qemu-guest-agent; }
  if [ -d ~/projetFable ]; then git -C ~/projetFable fetch -q origin \"$BRANCHE\" && git -C ~/projetFable checkout -q -B \"$BRANCHE\" FETCH_HEAD;
  else git clone -q -b \"$BRANCHE\" https://github.com/loan-heron/projetFable.git ~/projetFable; fi
  cd ~/projetFable/breche/deploiement
  if [ ! -f .env ]; then umask 077; printf 'BRECHE_INVITATION=%s\\n' \"\$(head -c 12 /dev/urandom | base64 | tr -dc A-Za-z0-9 | head -c 12)\" > .env; fi
  sudo docker-compose up -d --build
  sleep 3; curl -sf http://127.0.0.1:${PLAT_APP_PORT}/sante && echo ' : plateforme en ligne sur la VM'
  echo \"Code d'invitation : \$(cut -d= -f2 .env)\""
echo "Depuis la maison : http://192.168.1.200:${PLAT_PUBLIC_PORT}/ (à mettre derrière le reverse proxy HTTPS)."
