Wireshark affiche, paquet par paquet, tout ce qui est passé sur un réseau. C'est l'outil de l'écoute, mais aussi celui de l'enquête après incident.

## Installer et ouvrir

Installe Wireshark (gratuit, [wireshark.org](https://www.wireshark.org)) puis ouvre le fichier de capture `.pcap` fourni avec le lab : *Fichier, Ouvrir*.

## Lire l'écran

1. **En haut** : la liste des paquets (numéro, heure, source, destination, protocole, résumé).
2. **Au milieu** : le détail du paquet sélectionné, couche par couche.
3. **En bas** : les octets bruts.

## Filtrer

La barre de filtre est ton meilleur outil.

```
http                      # seulement le web
ip.addr == 10.0.0.5       # tout ce qui touche cette machine
tcp.port == 21            # FTP
http.request.method == "POST"   # les formulaires envoyés
```

## Suivre une conversation

Clic droit sur un paquet, *Suivre, Flux TCP*. Wireshark recolle tous les morceaux et affiche l'échange complet, comme un dialogue. Pour un protocole en clair, tu lis la requête et la réponse telles quelles.

## Le lab : L'écoute

Un technicien de la Verrerie Morel s'est connecté à l'interface d'administration d'une imprimante depuis le Wi-Fi invité. Quelqu'un a enregistré le trafic. Trouve ce qu'il a envoyé.
