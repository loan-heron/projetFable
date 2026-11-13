#!/usr/bin/env bash
# Brèche · crée la VM Brèche (plateforme) et la VM Labs à partir de Debian 12 cloud.
set -euo pipefail
cd "$(dirname "$0")"; source ./config.env

for id in "$BRECHE_VMID" "$LABS_VMID"; do
  if qm status "$id" >/dev/null 2>&1 || pct status "$id" >/dev/null 2>&1; then
    echo "L'identifiant $id est déjà pris : arrêt. Change-le dans config.env."; exit 1
  fi
done
[ -f "$SSH_PUBKEY_FILE" ] || { echo "Clé $SSH_PUBKEY_FILE absente (ssh-keygen -t ed25519 puis ajuste SSH_PUBKEY_FILE)."; exit 1; }
[ -f "$DEBIAN_IMG" ] || wget -q --show-progress -O "$DEBIAN_IMG" "$DEBIAN_IMG_URL"

creer_vm() { # id nom cœurs ram disque pont ip passerelle
  local id=$1 nom=$2 cores=$3 ram=$4 disk=$5 br=$6 ip=$7 gw=$8
  qm create "$id" --name "$nom" --cores "$cores" --memory "$ram" --cpu host \
     --net0 "virtio,bridge=$br" --scsihw virtio-scsi-single --ostype l26 \
     --agent enabled=1 --serial0 socket --vga serial0 --onboot 1 --tags breche
  qm set "$id" --scsi0 "$STORAGE:0,import-from=$DEBIAN_IMG,discard=on"
  qm resize "$id" scsi0 "$disk"
  qm set "$id" --ide2 "$STORAGE:cloudinit" --boot order=scsi0 \
     --ciuser "$VM_USER" --sshkeys "$SSH_PUBKEY_FILE" \
     --ipconfig0 "ip=$ip/24,gw=$gw" --nameserver 1.1.1.1
  echo "VM $id ($nom) créée."
}
creer_vm "$BRECHE_VMID" breche-plateforme "$BRECHE_CORES" "$BRECHE_RAM_MB" "$BRECHE_DISK" "$PLAT_BRIDGE" "$PLAT_VM_IP" "${PLAT_HOST_IP%/*}"
creer_vm "$LABS_VMID"   breche-labs       "$LABS_CORES"   "$LABS_RAM_MB"   "$LABS_DISK"   "$LABS_BRIDGE" "$LABS_VM_IP" "${LABS_HOST_IP%/*}"
qm start "$BRECHE_VMID"; qm start "$LABS_VMID"
echo "VM démarrées. Attends ~1 min puis : ssh $VM_USER@$LABS_VM_IP (depuis l'hôte)."
