'use strict';
// Base SQLite (module natif de Node 22). Un seul fichier, sauvegardable tel quel.
const { DatabaseSync } = require('node:sqlite');
const path = require('node:path');
const fs = require('node:fs');

function ouvrir(fichier) {
  if (fichier !== ':memory:') fs.mkdirSync(path.dirname(fichier), { recursive: true });
  const db = new DatabaseSync(fichier);
  db.exec(`
    PRAGMA journal_mode = WAL;
    PRAGMA foreign_keys = ON;
    CREATE TABLE IF NOT EXISTS utilisateurs (
      id INTEGER PRIMARY KEY,
      email TEXT NOT NULL UNIQUE COLLATE NOCASE,
      pseudo TEXT NOT NULL UNIQUE COLLATE NOCASE,
      hash TEXT NOT NULL,
      admin INTEGER NOT NULL DEFAULT 0,
      cree_le TEXT NOT NULL DEFAULT (datetime('now'))
    );
    CREATE TABLE IF NOT EXISTS sessions (
      jeton_hash TEXT PRIMARY KEY,
      utilisateur_id INTEGER NOT NULL REFERENCES utilisateurs(id) ON DELETE CASCADE,
      csrf TEXT NOT NULL,
      expire_le INTEGER NOT NULL
    );
    CREATE TABLE IF NOT EXISTS lectures (
      utilisateur_id INTEGER NOT NULL REFERENCES utilisateurs(id) ON DELETE CASCADE,
      lecon TEXT NOT NULL,
      le TEXT NOT NULL DEFAULT (datetime('now')),
      PRIMARY KEY (utilisateur_id, lecon)
    );
    CREATE TABLE IF NOT EXISTS drapeaux (
      utilisateur_id INTEGER NOT NULL REFERENCES utilisateurs(id) ON DELETE CASCADE,
      lab TEXT NOT NULL,
      le TEXT NOT NULL DEFAULT (datetime('now')),
      PRIMARY KEY (utilisateur_id, lab)
    );
    CREATE TABLE IF NOT EXISTS tentatives (
      utilisateur_id INTEGER NOT NULL REFERENCES utilisateurs(id) ON DELETE CASCADE,
      lab TEXT NOT NULL,
      le INTEGER NOT NULL
    );
    CREATE INDEX IF NOT EXISTS idx_tentatives ON tentatives(utilisateur_id, lab, le);
  `);
  return db;
}

module.exports = { ouvrir };
