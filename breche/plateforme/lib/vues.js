'use strict';
// Gabarits HTML. Tout texte venant d'un utilisateur passe par esc().

const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

function page({ titre, corps, utilisateur, csrf, classe = '' }) {
  const nav = utilisateur
    ? `<a href="/carte">La carte</a>
       <span class="nav-pseudo">Agent ${esc(utilisateur.pseudo)}</span>
       <form method="post" action="/deconnexion" class="nav-form"><input type="hidden" name="csrf" value="${esc(csrf)}"><button class="lien">Sortir</button></form>`
    : `<a href="/connexion">Se connecter</a><a class="bouton bouton-petit" href="/inscription">Ouvrir un dossier</a>`;
  return `<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(titre)} · Brèche</title>
<meta name="description" content="Brèche, école de cybersécurité en français : on attaque une entreprise fictive, module après module, puis on répare.">
<link rel="icon" href="/public/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@700;900&family=Courier+Prime:wght@400;700&family=IBM+Plex+Sans:ital,wght@0,400;0,500;0,600;1,400&display=swap">
<link rel="stylesheet" href="/public/style.css">
</head>
<body class="${esc(classe)}">
<header class="entete">
  <a class="marque" href="/" aria-label="Brèche, accueil"><img src="/public/logo.svg" alt="" width="34" height="34"><span>Brèche</span></a>
  <nav>${nav}</nav>
</header>
<main>${corps}</main>
<footer class="pied">
  <p>Brèche · école de cybersécurité offensive et défensive · Les techniques enseignées ne s'utilisent que sur les cibles de la formation ou avec une autorisation écrite (art. 323-1 du Code pénal).</p>
</footer>
</body>
</html>`;
}

function accueil(parcours) {
  const nbOuverts = parcours.modules.filter((m) => m.ouvert).length;
  return `
<section class="une">
  <p class="tampon tampon-rouge">Dossier ouvert</p>
  <h1>Entre par la vitrine.<br>Ressors par le contrôleur de domaine.</h1>
  <p class="chapeau">Brèche est une école de cybersécurité en français. Tu suis l'intrusion complète d'une entreprise fictive, ${esc(parcours.entreprise.nom)}, module après module. Chaque leçon finit dans une vraie cible à attaquer, puis tu corriges la faille toi-même.</p>
  <p><a class="bouton" href="/inscription">Ouvrir mon dossier</a> <a class="lien-fort" href="/connexion">J'ai déjà un dossier</a></p>
</section>

<section class="fiche-cible">
  <div class="fiche-entete"><span class="etiquette">Cible</span><span class="etiquette">Réf. VM-1931</span></div>
  <h2>${esc(parcours.entreprise.nom)}</h2>
  <p>${esc(parcours.entreprise.resume)}</p>
  <ol class="etapes">
    <li><strong>Lire</strong> une leçon courte, avec les commandes exactes.</li>
    <li><strong>Lancer</strong> la cible sur ta machine, en une commande Docker.</li>
    <li><strong>Attaquer</strong> jusqu'au drapeau qui prouve la réussite.</li>
    <li><strong>Réparer</strong> la faille et vérifier que l'attaque échoue.</li>
  </ol>
</section>

<section class="colonnes">
  <div><h3>14 modules</h3><p>Des fondations Linux et réseau jusqu'à l'Active Directory, la détection et un examen final avec rapport. ${nbOuverts} modules sont ouverts aujourd'hui.</p></div>
  <div><h3>Tes labs, chez toi</h3><p>Les cibles tournent sur ta machine, isolées, jamais exposées sur internet. La plateforme garde ta progression et valide tes drapeaux.</p></div>
  <div><h3>Attaquer, puis réparer</h3><p>Chaque faille exploitée se termine par sa correction. Utile aux futurs pentesteurs comme aux développeurs web.</p></div>
</section>`;
}

function formulaireCompte({ mode, erreur, valeurs = {}, csrf, invitation }) {
  const ins = mode === 'inscription';
  return `
<section class="formulaire">
  <h1>${ins ? 'Ouvrir un dossier' : 'Reprendre mon dossier'}</h1>
  ${erreur ? `<p class="erreur" role="alert">${esc(erreur)}</p>` : ''}
  <form method="post" action="/${mode}" novalidate>
    <input type="hidden" name="csrf" value="${esc(csrf)}">
    <label>Adresse e-mail<input type="email" name="email" autocomplete="email" required value="${esc(valeurs.email)}"></label>
    ${ins ? `<label>Nom de code <small>(public, 3 à 24 caractères)</small><input name="pseudo" autocomplete="nickname" required minlength="3" maxlength="24" value="${esc(valeurs.pseudo)}"></label>` : ''}
    <label>Mot de passe ${ins ? '<small>(12 caractères minimum)</small>' : ''}<input type="password" name="mdp" autocomplete="${ins ? 'new-password' : 'current-password'}" required ${ins ? 'minlength="12"' : ''}></label>
    ${ins && invitation ? `<label>Code d'invitation <small>(accès bêta)</small><input name="invitation" required autocomplete="off" value="${esc(valeurs.invitation)}"></label>` : ''}
    ${ins ? `<label class="case"><input type="checkbox" name="charte" value="1" required> Je n'utiliserai ces techniques que sur les cibles de la formation ou avec une autorisation écrite.</label>` : ''}
    <button class="bouton">${ins ? 'Ouvrir le dossier' : 'Entrer'}</button>
  </form>
  <p class="bascule">${ins ? 'Déjà un dossier ? <a href="/connexion">Se connecter</a>' : 'Pas encore de dossier ? <a href="/inscription">En ouvrir un</a>'}</p>
</section>`;
}

function carte({ parcours, progression, utilisateur }) {
  const parNiveau = parcours.niveaux.map((n) => {
    const mods = parcours.modules.filter((m) => m.niveau === n.id).map((m) => {
      const fait = progression.drapeaux.has(m.lab?.id);
      const lus = (m.lecons || []).filter((l) => progression.lectures.has(`${m.id}/${l.id}`)).length;
      const total = (m.lecons || []).length;
      const etat = !m.ouvert ? 'ferme' : fait ? 'compromis' : lus > 0 ? 'en-cours' : 'ouvert';
      const contenu = `
        <span class="mod-num">${String(m.numero).padStart(2, '0')}</span>
        <span class="mod-zone">${esc(m.zone)}</span>
        <strong class="mod-titre">${esc(m.titre)}</strong>
        <span class="mod-resume">${esc(m.resume)}</span>
        ${m.ouvert ? `<progress class="mod-jauge" max="${total}" value="${lus}" aria-label="${lus} leçons lues sur ${total}"></progress>` : '<span class="mod-bientot">Bientôt</span>'}
        ${fait ? '<span class="tampon tampon-rouge tampon-carte">Compromis</span>' : ''}`;
      return m.ouvert
        ? `<a class="mod mod-${etat}" href="/module/${esc(m.id)}">${contenu}</a>`
        : `<div class="mod mod-${etat}" aria-disabled="true">${contenu}</div>`;
    }).join('');
    return `<section class="niveau"><h2><span>Niveau ${n.id}</span> ${esc(n.nom)}</h2>${n.note ? `<p class="note">${esc(n.note)}</p>` : ''}<div class="mods">${mods}</div></section>`;
  }).join('');
  const total = parcours.modules.filter((m) => m.lab).length;
  return `
<section class="carte-entete">
  <p class="etiquette">Dossier de l'agent ${esc(utilisateur.pseudo)}</p>
  <h1>Plan d'intrusion · ${esc(parcours.entreprise.nom)}</h1>
  <p class="compteur"><strong>${progression.drapeaux.size}</strong> / ${total} zones compromises</p>
</section>
<div class="carte">${parNiveau}</div>`;
}

function module_({ m, progression }) {
  const lecons = m.lecons.map((l, i) => `
    <li class="${progression.lectures.has(`${m.id}/${l.id}`) ? 'lu' : ''}">
      <a href="/lecon/${esc(m.id)}/${esc(l.id)}"><span class="num">${i + 1}</span>${esc(l.titre)}</a>
    </li>`).join('');
  const fait = progression.drapeaux.has(m.lab.id);
  return `
<nav class="fil"><a href="/carte">La carte</a> / Module ${m.numero}</nav>
<section class="module-entete">
  <p class="etiquette">Module ${String(m.numero).padStart(2, '0')} · ${esc(m.zone)}</p>
  <h1>${esc(m.titre)}</h1>
  <p class="chapeau">${esc(m.resume)}</p>
</section>
<ol class="lecons">${lecons}</ol>
<a class="lab-carte ${fait ? 'lab-fait' : ''}" href="/lab/${esc(m.lab.id)}">
  <span class="etiquette">Lab de fin de module</span>
  <strong>${esc(m.lab.titre)}</strong>
  <span>${fait ? 'Drapeau validé' : 'Lancer la cible et rapporter le drapeau'}</span>
  ${fait ? '<span class="tampon tampon-rouge">Compromis</span>' : ''}
</a>`;
}

function lecon({ m, l, html, suivante }) {
  return `
<nav class="fil"><a href="/carte">La carte</a> / <a href="/module/${esc(m.id)}">Module ${m.numero}</a></nav>
<article class="lecon">
  <p class="etiquette">Module ${String(m.numero).padStart(2, '0')} · ${esc(m.titre)}</p>
  <h1>${esc(l.titre)}</h1>
  <div class="prose">${html}</div>
  <p class="suite">${suivante
    ? `<a class="bouton" href="/lecon/${esc(m.id)}/${esc(suivante.id)}">Leçon suivante : ${esc(suivante.titre)}</a>`
    : `<a class="bouton" href="/lab/${esc(m.lab.id)}">Passer au lab : ${esc(m.lab.titre)}</a>`}</p>
</article>`;
}

function lab({ m, html, fait, message, erreur, csrf }) {
  return `
<nav class="fil"><a href="/carte">La carte</a> / <a href="/module/${esc(m.id)}">Module ${m.numero}</a></nav>
<article class="lecon">
  <p class="etiquette">Lab · Module ${String(m.numero).padStart(2, '0')}</p>
  <h1>${esc(m.lab.titre)}</h1>
  <div class="prose">${html}</div>
  <section class="rapport ${fait ? 'rapport-fait' : ''}">
    <h2>Rapporter le drapeau</h2>
    ${message ? `<p class="succes" role="status">${esc(message)}</p>` : ''}
    ${erreur ? `<p class="erreur" role="alert">${esc(erreur)}</p>` : ''}
    ${fait
      ? '<p class="tampon tampon-rouge">Compromis</p><p>Drapeau validé. Prochaine étape : corrige la faille dans le code de la cible, relance-la et vérifie que ton attaque échoue.</p>'
      : `<form method="post" action="/lab/${esc(m.lab.id)}">
          <input type="hidden" name="csrf" value="${esc(csrf)}">
          <label>Drapeau<input name="drapeau" placeholder="BRECHE{...}" autocomplete="off" required spellcheck="false"></label>
          <button class="bouton">Valider</button>
        </form>`}
  </section>
</article>`;
}

function erreurPage(code, texte) {
  return `<section class="formulaire"><p class="tampon tampon-rouge">${esc(code)}</p><h1>${esc(texte)}</h1><p><a href="/">Retour à l'accueil</a></p></section>`;
}

module.exports = { esc, page, accueil, formulaireCompte, carte, module_, lecon, lab, erreurPage };
