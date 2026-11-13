'use strict';
// Comptes et sessions : mots de passe en scrypt, jetons de session aléatoires stockés hachés.
const crypto = require('node:crypto');

const DUREE_SESSION_MS = 1000 * 60 * 60 * 24 * 14; // 14 jours
const SCRYPT = { N: 16384, r: 8, p: 1 };

function hacherMotDePasse(mdp) {
  const sel = crypto.randomBytes(16);
  const cle = crypto.scryptSync(mdp, sel, 64, SCRYPT);
  return `scrypt$${sel.toString('base64')}$${cle.toString('base64')}`;
}

function verifierMotDePasse(mdp, stocke) {
  const [algo, selB64, cleB64] = String(stocke).split('$');
  if (algo !== 'scrypt' || !selB64 || !cleB64) return false;
  const attendu = Buffer.from(cleB64, 'base64');
  const calcule = crypto.scryptSync(mdp, Buffer.from(selB64, 'base64'), attendu.length, SCRYPT);
  return crypto.timingSafeEqual(attendu, calcule);
}

// Hash factice pour que la connexion prenne le même temps quand l'email n'existe pas.
const HASH_FACTICE = hacherMotDePasse('breche-factice');

const sha256 = (s) => crypto.createHash('sha256').update(String(s)).digest('hex');
const aleatoire = (n = 32) => crypto.randomBytes(n).toString('base64url');

function creerSession(db, utilisateurId) {
  const jeton = aleatoire();
  const csrf = aleatoire(24);
  db.prepare('DELETE FROM sessions WHERE expire_le < ?').run(Date.now());
  db.prepare('INSERT INTO sessions (jeton_hash, utilisateur_id, csrf, expire_le) VALUES (?, ?, ?, ?)')
    .run(sha256(jeton), utilisateurId, csrf, Date.now() + DUREE_SESSION_MS);
  return jeton;
}

function lireSession(db, jeton) {
  if (!jeton) return null;
  const ligne = db.prepare(`
    SELECT s.csrf, s.expire_le, u.id, u.email, u.pseudo, u.admin
    FROM sessions s JOIN utilisateurs u ON u.id = s.utilisateur_id
    WHERE s.jeton_hash = ?`).get(sha256(jeton));
  if (!ligne) return null;
  if (ligne.expire_le < Date.now()) {
    db.prepare('DELETE FROM sessions WHERE jeton_hash = ?').run(sha256(jeton));
    return null;
  }
  return { id: ligne.id, email: ligne.email, pseudo: ligne.pseudo, admin: !!ligne.admin, csrf: ligne.csrf };
}

function detruireSession(db, jeton) {
  if (jeton) db.prepare('DELETE FROM sessions WHERE jeton_hash = ?').run(sha256(jeton));
}

// Comparaison à temps constant de deux chaînes (drapeaux, jetons CSRF).
function egaux(a, b) {
  const ha = crypto.createHash('sha256').update(String(a)).digest();
  const hb = crypto.createHash('sha256').update(String(b)).digest();
  return crypto.timingSafeEqual(ha, hb);
}

module.exports = { hacherMotDePasse, verifierMotDePasse, HASH_FACTICE, creerSession, lireSession, detruireSession, sha256, aleatoire, egaux };
