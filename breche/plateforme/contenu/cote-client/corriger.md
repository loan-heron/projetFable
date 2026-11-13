Corriger une XSS, c'est rendre au texte son statut de texte. Comme pour l'injection SQL, le problème est le mélange entre donnée et code.

## Échapper à l'affichage

Avant d'insérer une donnée dans du HTML, on remplace les caractères spéciaux :

| Caractère | Devient |
|---|---|
| `<` | `&lt;` |
| `>` | `&gt;` |
| `&` | `&amp;` |
| `"` | `&quot;` |
| `'` | `&#39;` |

Le navigateur affiche alors `<script>` comme du texte, sans l'exécuter. Ne le fais jamais à la main : tous les moteurs de gabarits le font **par défaut** (Jinja, Twig, React, Blade). La faille vient presque toujours de quelqu'un qui a **désactivé** cette protection :

```jinja
{{ m.texte }}        {# échappé : sûr #}
{{ m.texte|safe }}   {# brut : XSS #}
```

Équivalents à chercher dans un code : `|raw` (Twig), `{!! !!}` (Blade), `dangerouslySetInnerHTML` (React), `innerHTML =` (JavaScript).

## Les défenses en profondeur

1. **`HttpOnly`** sur tout cookie de session ou sensible. Une XSS reste grave, mais elle ne vole plus la session.
2. **`Secure`** et **`SameSite=Lax`** sur ces mêmes cookies.
3. **Une CSP** (*Content Security Policy*), un en-tête qui interdit les scripts en ligne :

```
Content-Security-Policy: default-src 'self'; script-src 'self'; object-src 'none'
```

Avec cette ligne, même un `<script>` injecté ne s'exécute pas. Regarde les en-têtes de Brèche (`F12`, onglet *Réseau*) : elle en a une.

4. **Si tu dois accepter du HTML** (éditeur de texte riche), passe-le dans un nettoyeur maintenu comme DOMPurify ou bleach, avec une liste blanche de balises.

## Exercice de défense

Dans le dossier de la cible `intranet`, ouvre `templates/messages.html` et retire le `|safe`. Dans `app.py`, le robot ajoute le cookie `jeton_direction` : ajoute-lui `"httpOnly": True`. Reconstruis l'image et relance-la : ton message piégé doit s'afficher comme du texte, et le journal du collecteur doit rester vide.
