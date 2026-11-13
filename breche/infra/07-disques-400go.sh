#!/usr/bin/env bash
# Brèche · agrandit les disques des VM au budget de 400 Go (40 Go plateforme + 360 Go labs).
# Agrandir est sans risque ; rétrécir est impossible avec qm resize.
set -euo pipefail
cd "$(dirname "$0")"; source ./config.env
for couple in "$BRECHE_VMID:$BRECHE_DISK:$PLAT_VM_IP" "$LABS_VMID:$LABS_DISK:$LABS_VM_IP"; do
  IFS=: read -r id taille ipvm <<<"$couple"
  qm resize "$id" scsi0 "$taille"
  ssh -o StrictHostKeyChecking=accept-new "$VM_USER@$ipvm" 'sudo growpart /dev/sda 1 || true; sudo resize2fs /dev/sda1; df -h / | tail -1'
done
