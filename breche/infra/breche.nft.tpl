# Brèche · règles d'isolement, table dédiée : ne touche à aucune autre règle.
# Supprimer d'un coup : nft delete table inet breche
table inet breche {
	set labs_internet { type ipv4_addr; }   # vide = labs sans internet (mode normal)

	chain input {
		type filter hook input priority -10; policy accept;
		# Les labs n'ont aucun accès à l'hôte Proxmox (interface 8006, SSH…)
		iifname "@LABS@" ct state established,related accept
		iifname "@LABS@" drop
		# La plateforme non plus, sauf réponses
		iifname "@PLAT@" ct state established,related accept
		iifname "@PLAT@" drop
	}

	chain forward {
		type filter hook forward priority -10; policy accept;
		ct state established,related accept
		# Labs : ne sortent jamais vers la maison
		iifname "@LABS@" ip daddr @LAN_SUBNET@ drop
		# Labs : internet seulement en mode installation (labs-internet.sh on)
		iifname "@LABS@" oifname "@LAN@" ip saddr @labs_internet accept
		iifname "@LABS@" drop
		# Plateforme : internet oui, maison non, labs seulement sur le port de pilotage
		iifname "@PLAT@" ip daddr @LAN_SUBNET@ drop
		iifname "@PLAT@" oifname "@LABS@" ip daddr @LABS_VM_IP@ tcp dport { 22, 8800 } accept
		iifname "@PLAT@" oifname "@LABS@" drop
		iifname "@PLAT@" oifname "@LAN@" accept
		iifname "@PLAT@" drop
		# Personne ne rentre dans les labs, sauf la plateforme (ci-dessus) et l'hôte (sortie locale)
		oifname "@LABS@" drop
	}

	chain postrouting {
		type nat hook postrouting priority 100; policy accept;
		iifname "@PLAT@" oifname "@LAN@" ip saddr @PLAT_SUBNET@ masquerade
		oifname "@LAN@" ip saddr @labs_internet masquerade
	}
}
