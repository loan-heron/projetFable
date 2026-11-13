'use strict';
// Brèche · serveur de la plateforme. Node 22, sans framework : http natif, SQLite natif, marked pour les leçons.
const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');
const { marked } = require('marked');
const { ouvrir } = require('./lib/db');
const A = require('./lib/auth');
const V = require('./lib/vues');

const CONFIG = {
  port: Number(process.env.PORT || 8080),
  base: process.env.BRECHE_BASE || path.join(__dirname, 'donnees', 'breche.sqlite'),
  invitation: process.env.BRECHE_INVITATION || '', // vide = inscriptions ouvertes
  cookieSecure: process.env.BRECHE_COOKIE_SECURE === '1',
  adminEmail: (process.env.BRECHE_ADMIN_EMAIL || '').toLowerCase(),
};

const CONTENU = path.join(__dirname, 'contenu');
const PUBLIC = path.join(__dirname, 'public');
const parcours = JSON.parse(fs.readFileSync(path.join(CONTENU, 'parcours.json'), 'utf8'));
const moduleParId = new Map(parcours.modules.map((m) => [m.id, m]));
const moduleParLab = new Map(parcours.modules.filter((m) => m.lab).map((m) => [m.lab.id, m]));

// Leçons rendues une fois au démarrage (contenu de confiance, écrit par nous).
const rendu = new Map();
for (const m of parcours.modules.filter((x) => x.ouvert)) {
  for (const l of m.lecons) rendu.set(`${m.id}/${l.id}`, marked.parse(fs.readFileSync(path.join(CONTENU, m.id, `${l.id}.md`), 'utf8')));
  rendu.set(`lab/${m.lab.id}`, marked.parse(fs.readFileSync(path.join(CONTENU, 'labs', `${m.lab.id}.md`), 'utf8')));
}

function creerApp(db) {
  const limites = new Map(); // anti force brute en mémoire : clé -> [horodatages]
  function limite(cle, max, fenetreMs) {
    const t = Date.now();
    const l = (limites.get(cle) || []).filter((x) => t - x < fenetreMs);
    l.push(t);
    limites.set(cle, l);
    if (limites.size > 10000) limites.clear();
    return l.length > max;
  }

  const TYPES = { '.css': 'text/css; charset=utf-8', '.svg': 'image/svg+xml', '.png': 'image/png', '.woff2': 'font/woff2', '.pcap': 'application/vnd.tcpdump.pcap' };
  const CSP = "default-src 'self'; style-src 'self' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; img-src 'self' data:; form-action 'self'; frame-ancestors 'none'; base-uri 'none'; object-src 'none'";

  function entetes(res) {
    res.setHeader('Content-Security-Policy', CSP);
    res.setHeader('X-Content-Type-Options', 'nosniff');
    res.setHeader('Referrer-Policy', 'same-origin');
    res.setHeader('X-Frame-Options', 'DENY');
    res.setHeader('Permissions-Policy', 'camera=(), microphone=(), geolocation=()');
    if (CONFIG.cookieSecure) res.setHeader('Strict-Transport-Security', 'max-age=31536000');
  }

  function cookies(req) {
    const o = {};
    for (const p of String(req.headers.cookie || '').split(';')) {
      const i = p.indexOf('=');
      if (i > 0) o[p.slice(0, i).trim()] = decodeURIComponent(p.slice(i + 1).trim());
    }
    return o;
  }
  const cookie = (nom, val, maxAge) => `${nom}=${encodeURIComponent(val)}; Path=/; HttpOnly; SameSite=Lax${CONFIG.cookieSecure ? '; Secure' : ''}${maxAge !== undefined ? `; Max-Age=${maxAge}` : ''}`;

  function lireCorps(req) {
    return new Promise((ok, ko) => {
      let taille = 0; const morceaux = [];
      req.on('data', (c) => { taille += c.length; if (taille > 16384) { ko(new Error('trop gros')); req.destroy(); } else morceaux.push(c); });
      req.on('end', () => ok(Object.fromEntries(new URLSearchParams(Buffer.concat(morceaux).toString('utf8')))));
      req.on('error', ko);
    });
  }

  const html = (res, code, corps) => { res.writeHead(code, { 'Content-Type': 'text/html; charset=utf-8', 'Cache-Control': 'no-store' }); res.end(corps); };
  const rediriger = (res, ou, extra = {}) => { res.writeHead(303, { Location: ou, ...extra }); res.end(); };

  function progression(uid) {
    return {
      lectures: new Set(db.prepare('SELECT lecon FROM lectures WHERE utilisateur_id = ?').all(uid).map((r) => r.lecon)),
      drapeaux: new Set(db.prepare('SELECT lab FROM drapeaux WHERE utilisateur_id = ?').all(uid).map((r) => r.lab)),
    };
  }

  // Jeton CSRF pour les visiteurs non connectés : cookie + champ caché (double soumission).
  function csrfVisiteur(req, res) {
    let t = cookies(req).breche_csrf;
    if (!t || t.length < 20) { t = A.aleatoire(24); res.setHeader('Set-Cookie', cookie('breche_csrf', t)); }
    return t;
  }

  return async function app(req, res) {
    entetes(res);
    const url = new URL(req.url, 'http://local');
    const chemin = decodeURIComponent(url.pathname);
    const jeton = cookies(req).breche_session;
    const u = A.lireSession(db, jeton);
    const rendre = (code, titre, corps, classe) => html(res, code, V.page({ titre, corps, utilisateur: u, csrf: u?.csrf, classe }));
    const ip = req.headers['x-forwarded-for']?.split(',')[0].trim() || req.socket.remoteAddress;

    try {
      // Fichiers statiques
      if (req.method === 'GET' && chemin.startsWith('/public/')) {
        const f = path.normalize(path.join(PUBLIC, chemin.slice(8)));
        if (!f.startsWith(PUBLIC + path.sep) || !fs.existsSync(f) || !fs.statSync(f).isFile()) return rendre(404, 'Introuvable', V.erreurPage(404, 'Cette pièce n’est pas au dossier.'));
        res.writeHead(200, { 'Content-Type': TYPES[path.extname(f)] || 'application/octet-stream', 'Cache-Control': 'public, max-age=3600' });
        return fs.createReadStream(f).pipe(res);
      }
      if (chemin === '/sante') { res.writeHead(200, { 'Content-Type': 'text/plain' }); return res.end('ok'); }

      if (req.method === 'GET' && chemin === '/') {
        if (u) return rediriger(res, '/carte');
        return rendre(200, 'Formation cybersécurité', V.accueil(parcours), 'page-accueil');
      }

      // Inscription et connexion
      if (chemin === '/inscription' || chemin === '/connexion') {
        const mode = chemin.slice(1);
        if (u) return rediriger(res, '/carte');
        if (req.method === 'GET') {
          const csrf = csrfVisiteur(req, res);
          return rendre(200, mode === 'inscription' ? 'Ouvrir un dossier' : 'Connexion', V.formulaireCompte({ mode, csrf, invitation: !!CONFIG.invitation }));
        }
        if (req.method === 'POST') {
          const f = await lireCorps(req);
          const csrf = cookies(req).breche_csrf;
          const erreur = (msg, code = 400) => rendre(code, 'Erreur', V.formulaireCompte({ mode, erreur: msg, valeurs: { email: f.email, pseudo: f.pseudo }, csrf: csrfVisiteur(req, res), invitation: !!CONFIG.invitation }));
          if (!csrf || !f.csrf || !A.egaux(csrf, f.csrf)) return erreur('La page a expiré. Recharge-la et recommence.');
          if (limite(`compte:${ip}`, 10, 10 * 60 * 1000)) return erreur('Trop de tentatives. Réessaie dans 10 minutes.', 429);
          const email = String(f.email || '').trim().toLowerCase();
          const mdp = String(f.mdp || '');
          if (mode === 'inscription') {
            const pseudo = String(f.pseudo || '').trim();
            if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email) || email.length > 200) return erreur('Adresse e-mail invalide.');
            if (!/^[\p{L}\p{N}_.-]{3,24}$/u.test(pseudo)) return erreur('Nom de code : 3 à 24 lettres, chiffres, point, tiret ou souligné.');
            if (mdp.length < 12 || mdp.length > 200) return erreur('Le mot de passe doit faire au moins 12 caractères.');
            if (CONFIG.invitation && !A.egaux(String(f.invitation || '').trim(), CONFIG.invitation)) return erreur('Code d’invitation incorrect.');
            if (f.charte !== '1') return erreur('Il faut accepter la charte d’usage.');
            const existe = db.prepare('SELECT 1 FROM utilisateurs WHERE email = ? OR pseudo = ?').get(email, pseudo);
            if (existe) return erreur('Cette adresse ou ce nom de code est déjà pris.');
            const r = db.prepare('INSERT INTO utilisateurs (email, pseudo, hash, admin) VALUES (?, ?, ?, ?)').run(email, pseudo, A.hacherMotDePasse(mdp), email === CONFIG.adminEmail ? 1 : 0);
            return rediriger(res, '/carte', { 'Set-Cookie': cookie('breche_session', A.creerSession(db, Number(r.lastInsertRowid)), 60 * 60 * 24 * 14) });
          }
          const ligne = db.prepare('SELECT id, hash FROM utilisateurs WHERE email = ?').get(email);
          const ok = A.verifierMotDePasse(mdp, ligne ? ligne.hash : A.HASH_FACTICE) && !!ligne;
          if (!ok) return erreur('Adresse ou mot de passe incorrect.', 401);
          return rediriger(res, '/carte', { 'Set-Cookie': cookie('breche_session', A.creerSession(db, ligne.id), 60 * 60 * 24 * 14) });
        }
      }

      if (req.method === 'POST' && chemin === '/deconnexion') {
        const f = await lireCorps(req);
        if (u && f.csrf && A.egaux(f.csrf, u.csrf)) A.detruireSession(db, jeton);
        return rediriger(res, '/', { 'Set-Cookie': cookie('breche_session', '', 0) });
      }

      // Tout le reste exige d'être connecté
      if (!u) {
        if (/^\/(carte|module|lecon|lab|fichiers)(\/|$)/.test(chemin)) return rediriger(res, '/connexion');
        return rendre(404, 'Introuvable', V.erreurPage(404, 'Cette pièce n’est pas au dossier.'));
      }
      const prog = () => progression(u.id);

      if (req.method === 'GET' && chemin === '/carte') return rendre(200, 'La carte', V.carte({ parcours, progression: prog(), utilisateur: u }), 'page-carte');

      let m;
      if (req.method === 'GET' && (m = chemin.match(/^\/module\/([a-z0-9-]+)$/))) {
        const mod = moduleParId.get(m[1]);
        if (!mod || !mod.ouvert) return rendre(404, 'Introuvable', V.erreurPage(404, 'Ce module n’est pas encore ouvert.'));
        return rendre(200, mod.titre, V.module_({ m: mod, progression: prog() }));
      }

      if (req.method === 'GET' && (m = chemin.match(/^\/lecon\/([a-z0-9-]+)\/([a-z0-9-]+)$/))) {
        const mod = moduleParId.get(m[1]);
        const i = mod?.ouvert ? mod.lecons.findIndex((l) => l.id === m[2]) : -1;
        if (i < 0) return rendre(404, 'Introuvable', V.erreurPage(404, 'Cette leçon n’existe pas.'));
        db.prepare('INSERT OR IGNORE INTO lectures (utilisateur_id, lecon) VALUES (?, ?)').run(u.id, `${mod.id}/${mod.lecons[i].id}`);
        return rendre(200, mod.lecons[i].titre, V.lecon({ m: mod, l: mod.lecons[i], html: rendu.get(`${mod.id}/${mod.lecons[i].id}`), suivante: mod.lecons[i + 1] }));
      }

      if ((m = chemin.match(/^\/lab\/([a-z0-9-]+)$/))) {
        const mod = moduleParLab.get(m[1]);
        if (!mod || !mod.ouvert) return rendre(404, 'Introuvable', V.erreurPage(404, 'Ce lab n’existe pas.'));
        const fait = () => !!db.prepare('SELECT 1 FROM drapeaux WHERE utilisateur_id = ? AND lab = ?').get(u.id, mod.lab.id);
        const vue = (code, extra) => rendre(code, mod.lab.titre, V.lab({ m: mod, html: rendu.get(`lab/${mod.lab.id}`), fait: fait(), csrf: u.csrf, ...extra }));
        if (req.method === 'GET') return vue(200, {});
        if (req.method === 'POST') {
          const f = await lireCorps(req);
          if (!f.csrf || !A.egaux(f.csrf, u.csrf)) return vue(400, { erreur: 'La page a expiré. Recharge-la et recommence.' });
          const recentes = db.prepare('SELECT COUNT(*) AS n FROM tentatives WHERE utilisateur_id = ? AND lab = ? AND le > ?').get(u.id, mod.lab.id, Date.now() - 10 * 60 * 1000).n;
          if (recentes >= 15) return vue(429, { erreur: 'Trop de tentatives sur ce lab. Réessaie dans 10 minutes.' });
          db.prepare('INSERT INTO tentatives (utilisateur_id, lab, le) VALUES (?, ?, ?)').run(u.id, mod.lab.id, Date.now());
          const propose = String(f.drapeau || '').trim();
          if (A.egaux(A.sha256(propose), mod.lab.drapeau_sha256)) {
            db.prepare('INSERT OR IGNORE INTO drapeaux (utilisateur_id, lab) VALUES (?, ?)').run(u.id, mod.lab.id);
            return vue(200, { message: 'Drapeau validé. Zone compromise.' });
          }
          return vue(200, { erreur: 'Ce n’est pas le bon drapeau.' });
        }
      }

      if (req.method === 'GET' && chemin === '/fichiers/ecoute.pcap') {
        const f = path.join(__dirname, 'fichiers', 'ecoute.pcap');
        res.writeHead(200, { 'Content-Type': TYPES['.pcap'], 'Content-Disposition': 'attachment; filename="ecoute.pcap"' });
        return fs.createReadStream(f).pipe(res);
      }

      return rendre(404, 'Introuvable', V.erreurPage(404, 'Cette pièce n’est pas au dossier.'));
    } catch (e) {
      console.error(e);
      if (!res.headersSent) return rendre(500, 'Erreur', V.erreurPage(500, 'Quelque chose a cassé de notre côté.'));
      res.end();
    }
  };
}

if (require.main === module) {
  const db = ouvrir(CONFIG.base);
  http.createServer(creerApp(db)).listen(CONFIG.port, () => console.log(`Brèche écoute sur :${CONFIG.port}`));
}

module.exports = { creerApp, parcours };
