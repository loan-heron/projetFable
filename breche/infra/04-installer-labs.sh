#!/usr/bin/env bash
# Brèche · installe Docker et les premières cibles (DVWA, Juice Shop) dans la VM Labs.
# Lancé depuis l'hôte : ouvre internet pour la VM, installe, puis referme.
set -euo pipefail
cd "$(dirname "$0")"; source ./config.env
SSH="ssh -o StrictHostKeyChecking=accept-new $VM_USER@$LABS_VM_IP"
bash labs-internet.sh on
trap 'bash labs-internet.sh off' EXIT
$SSH 'timeout 300 sudo cloud-init status --wait >/dev/null || true; APT="-o Acquire::http::Timeout=15 -o Acquire::Retries=2 -o DPkg::Lock::Timeout=120"; sudo apt-get $APT update -q && sudo apt-get $APT install -yq docker.io docker-compose qemu-guest-agent && sudo usermod -aG docker $USER && sudo systemctl enable --now qemu-guest-agent'
scp -o StrictHostKeyChecking=accept-new ../labs/docker-compose.yml "$VM_USER@$LABS_VM_IP:~/docker-compose.yml"
$SSH 'sudo docker-compose -f ~/docker-compose.yml pull && sudo docker-compose -f ~/docker-compose.yml up -d && sudo docker ps --format "{{.Names}}  {{.Status}}"'
echo "Labs installés. Internet est refermé automatiquement."
