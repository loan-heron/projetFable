Sur un vrai serveur, il y a des dizaines de milliers de fichiers. On ne les ouvre pas un par un : on **cherche**.

## Trouver des fichiers : `find`

```bash
find / -name "*.bak" 2>/dev/null           # par nom
find /home -type f -name ".*" 2>/dev/null  # fichiers cachés dans /home
find / -user claire 2>/dev/null            # appartenant à claire
find / -newer /etc/hostname 2>/dev/null    # modifiés récemment
```

`2>/dev/null` jette les messages d'erreur (« Permission non accordée ») pour ne garder que les résultats.

## Chercher dans le contenu : `grep`

```bash
grep -r "password" /etc 2>/dev/null       # récursif
grep -ri "mot de passe" /home 2>/dev/null # insensible à la casse
grep -rl "BRECHE{" / 2>/dev/null          # seulement les noms de fichiers
```

## Enchaîner avec le tube `|`

Le tube envoie la sortie d'une commande dans la suivante.

```bash
cat /etc/passwd | cut -d: -f1           # la liste des comptes
history | grep ssh                      # les connexions SSH tapées par l'utilisateur
ls -la ~ | grep "^\."                   # ce qui est caché chez soi
```

## Les endroits qu'on regarde toujours

1. `~/.bash_history` : les commandes déjà tapées, parfois avec un mot de passe dedans.
2. `~/.ssh/` : des clés privées qui ouvrent d'autres machines.
3. Les fichiers `.bak`, `.old`, `.save` : des copies oubliées.
4. Les fichiers cachés dans les dossiers personnels.

## Le lab : La planque

Un employé de la Verrerie Morel a laissé un compte sur un serveur de test. Il dit qu'il n'y cache rien. Connecte-toi, enquête, et rapporte le drapeau.
