# Morel Optique : boutique fictive de la Verrerie Morel.
# CE CODE EST VOLONTAIREMENT VULNÉRABLE (formation Brèche). Ne pas copier en production.
import os
import sqlite3
from flask import Flask, request, render_template, abort, send_from_directory

app = Flask(__name__)
BASE = os.path.join(os.path.dirname(__file__), "boutique.sqlite")
DRAPEAU_PRIX = os.environ.get("DRAPEAU_PRIX", "BRECHE{l3_cl13nt_n_3st_p4s_l3_c41ss13r}")
DRAPEAU_CLIENTS = os.environ.get("DRAPEAU_CLIENTS", "BRECHE{un10n_s3l3ct_t0ut_l3_f1ch13r}")

PRODUITS = [
    (1, "galilee-dossier", "Lunette de Galilée, édition dossier", 1890.00, "Laiton poli, objectif achromatique 50 mm, numérotée à la main. Série limitée à 12 exemplaires."),
    (2, "prisme-60", "Prisme équilatéral 60°", 39.00, "Verre BK7, 25 mm. Décompose la lumière blanche comme au premier jour."),
    (3, "lentille-f100", "Lentille convergente f = 100 mm", 24.50, "Diamètre 40 mm, traitement antireflet."),
    (4, "loupe-horloger", "Loupe d'horloger ×10", 18.00, "Monture ébène, verre taillé à Lyon."),
    (5, "kit-polarisation", "Kit de polarisation", 64.00, "Deux filtres et un support gradué, pour voir la lumière autrement."),
]

def db():
    c = sqlite3.connect(BASE)
    c.row_factory = sqlite3.Row
    return c

def initialiser():
    c = db()
    c.executescript("""
      DROP TABLE IF EXISTS produits; DROP TABLE IF EXISTS notes_internes; DROP TABLE IF EXISTS clients;
      CREATE TABLE produits (id INTEGER PRIMARY KEY, ref TEXT, nom TEXT, prix REAL, description TEXT, visible INTEGER DEFAULT 1);
      CREATE TABLE clients (id INTEGER PRIMARY KEY, email TEXT, ville TEXT);
      CREATE TABLE notes_internes (id INTEGER PRIMARY KEY, auteur TEXT, contenu TEXT);
    """)
    c.executemany("INSERT INTO produits (id, ref, nom, prix, description) VALUES (?, ?, ?, ?, ?)", PRODUITS)
    c.execute("INSERT INTO produits (ref, nom, prix, description, visible) VALUES ('proto-x', 'Prototype interféromètre (non publié)', 0, 'Ne pas mettre en ligne.', 0)")
    c.executemany("INSERT INTO clients (email, ville) VALUES (?, ?)", [("m.durand@exemple.fr", "Lyon"), ("s.nguyen@exemple.fr", "Grenoble"), ("observatoire@exemple.fr", "Saint-Genis-Laval")])
    c.execute("INSERT INTO notes_internes (auteur, contenu) VALUES ('direction', ?)", (DRAPEAU_CLIENTS,))
    c.commit()

@app.after_request
def entetes(r):
    r.headers["Server"] = "Apache/2.4.29 (Ubuntu)"  # faux bandeau, pour l'énumération
    return r

@app.route("/")
def accueil():
    produits = db().execute("SELECT * FROM produits WHERE visible = 1").fetchall()
    return render_template("accueil.html", produits=produits)

@app.route("/recherche")
def recherche():
    q = request.args.get("q", "")
    # VULNÉRABLE : concaténation directe (module 5, injection SQL)
    sql = "SELECT nom, prix FROM produits WHERE visible = 1 AND nom LIKE '%" + q + "%'"
    try:
        resultats = db().execute(sql).fetchall()
        erreur = None
    except sqlite3.Error as e:
        resultats, erreur = [], f"Erreur SQL : {e}"
    return render_template("recherche.html", q=q, resultats=resultats, erreur=erreur)

@app.route("/produit/<ref>")
def produit(ref):
    p = db().execute("SELECT * FROM produits WHERE ref = ? AND visible = 1", (ref,)).fetchone()
    if not p:
        abort(404)
    return render_template("produit.html", p=p)

@app.route("/commander", methods=["POST"])
def commander():
    ref = request.form.get("ref", "")
    p = db().execute("SELECT * FROM produits WHERE ref = ?", (ref,)).fetchone()
    if not p:
        abort(400)
    # VULNÉRABLE : le prix vient du formulaire, pas de la base (module 3)
    try:
        prix = float(request.form.get("prix", "0"))
    except ValueError:
        abort(400)
    triche = prix < p["prix"]
    return render_template("commande.html", p=p, prix=prix, drapeau=DRAPEAU_PRIX if (triche and ref == "galilee-dossier") else None, triche=triche)

@app.route("/robots.txt")
def robots():
    return "User-agent: *\nDisallow: /panier\nDisallow: /archives-2019/\n", 200, {"Content-Type": "text/plain"}

@app.route("/archives-2019/")
def archives_index():
    # VULNÉRABLE : listing de répertoire oublié (module 4)
    fichiers = sorted(os.listdir(os.path.join(app.root_path, "archives-2019")))
    return render_template("listing.html", fichiers=fichiers)

@app.route("/archives-2019/<path:nom>")
def archives_fichier(nom):
    return send_from_directory(os.path.join(app.root_path, "archives-2019"), nom, mimetype="text/plain")

if __name__ == "__main__":
    initialiser()
    app.run(host="0.0.0.0", port=8090)
