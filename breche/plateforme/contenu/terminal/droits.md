Sous Linux, chaque fichier appartient à un **utilisateur** et à un **groupe**, et porte trois séries de droits. Comprendre ces droits, c'est comprendre ce qu'on peut lire, modifier ou lancer, et donc comment on peut monter en privilèges plus tard.

## Lire une ligne de `ls -l`

```
-rwxr-x--- 1 claire compta 4096 nov. 13 10:02 bilan.sh
```

| Partie | Sens |
| --- | --- |
| `-` | type : `-` fichier, `d` dossier, `l` lien |
| `rwx` | droits du propriétaire (claire) : lire, écrire, exécuter |
| `r-x` | droits du groupe (compta) : lire, exécuter |
| `---` | droits de tous les autres : rien |

Pour un dossier, `x` veut dire « pouvoir y entrer » et `r` « pouvoir lister son contenu ».

## Changer les droits

```bash
chmod 640 notes.txt      # rw- r-- ---
chmod +x script.sh       # rendre exécutable
chown claire:compta f    # changer propriétaire et groupe (souvent réservé à root)
```

La notation chiffrée additionne lire (4), écrire (2) et exécuter (1) : `7 = rwx`, `6 = rw-`, `5 = r-x`, `4 = r--`.

## Les cas qui intéressent un attaquant

- Un fichier de configuration lisible par tous (`-rw-r--r--`) qui contient un mot de passe.
- Un script lancé par root mais modifiable par un simple utilisateur.
- Un binaire avec le bit **SUID** (`-rwsr-xr-x`) : il s'exécute avec les droits de son propriétaire. On y reviendra au module 9.

```bash
find / -perm -4000 -type f 2>/dev/null   # lister les binaires SUID
```

## À retenir

Les droits sont la frontière entre « je vois » et « je contrôle ». Dans un audit, une mauvaise permission vaut souvent plus qu'une faille logicielle.
