Énumérer, c'est faire l'inventaire méthodique de ce qu'une cible expose.

## Les ports avec Nmap

```bash
nmap 127.0.0.1                   # les 1000 ports les plus courants
nmap -p- 127.0.0.1               # les 65 535 ports
nmap -sV -p 8090 127.0.0.1       # la version du service sur ce port
```

La sortie dit quels ports sont **ouverts**, quel service y répond, et souvent sa version. Une version ancienne est une piste.

## Les chemins web

Un site a souvent plus de pages que ses liens n'en montrent.

1. **`/robots.txt`** : la liste des pages que le site demande aux moteurs de recherche de ne pas indexer. C'est, très souvent, la liste de ce qu'il veut cacher.
2. **`/sitemap.xml`** : le plan du site.
3. **Le code source** (Ctrl+U) : commentaires de développeurs, liens morts, fichiers JavaScript.
4. **La force brute de chemins** : tester des milliers de noms courants.

```bash
gobuster dir -u http://127.0.0.1:8090 -w /usr/share/wordlists/dirb/common.txt
ffuf -u http://127.0.0.1:8090/FUZZ -w common.txt
```

## Les fichiers oubliés

Les développeurs laissent des traces : `backup.zip`, `index.php.bak`, `.git/`, `config.old`. Ces fichiers ne sont pas exécutés par le serveur : ils sont servis tels quels, avec leur contenu.

## Le lab : Archives oubliées

Le site de Morel Optique cache quelque chose à Google. Trouve quoi, et ce qui traîne dedans.
