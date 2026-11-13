# Intranet Morel : webmail interne et portail mutuelle de la Verrerie Morel.
# CE CODE EST VOLONTAIREMENT VULNÉRABLE (formation Brèche, modules 6 et 7). Ne pas copier en production.
import os, secrets, threading, time, datetime
from flask import Flask, request, render_template, redirect, session, abort, make_response

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)
PORT = 8091
DRAPEAU_XSS = os.environ.get("DRAPEAU_DIRECTEUR", "BRECHE{h77p0nly_4ur41t_t0ut_ch4ng3}")
DRAPEAU_IDOR = os.environ.get("DRAPEAU_DOSSIER", "BRECHE{1d0r_l3_num3r0_n_3st_p4s_un3_cl3}")
MDP_DIRECTEUR = os.environ.get("MDP_DIRECTEUR_TEST") or secrets.token_urlsafe(18)

COMPTES = {"stagiaire": {"mdp": "stagiaire", "nom": "Stagiaire", "dossier": 1043},
           "c.morel": {"mdp": MDP_DIRECTEUR, "nom": "Claire Morel, directrice", "dossier": 1001}}
MESSAGES = [{"auteur": "Claire Morel, directrice", "texte": "Bienvenue sur le nouvel intranet. Je lis tous vos messages chaque matin.", "le": "08:02"}]
COLLECTE = []
DOSSIERS = {
    1001: {"titulaire": "Claire Morel", "medecin": "Dr Lambert", "notes": "Suivi cardiologique annuel. " + DRAPEAU_IDOR},
    1002: {"titulaire": "Paul Girard", "medecin": "Dr Benali", "notes": "Arrêt de travail, 12 jours."},
    1043: {"titulaire": "Stagiaire", "medecin": "Dr Benali", "notes": "Visite d'embauche : apte."},
}

def connecte():
    return session.get("compte") in COMPTES

@app.route("/", methods=["GET", "POST"])
def connexion():
    erreur = None
    if request.method == "POST":
        c = request.form.get("compte", "")
        if c in COMPTES and secrets.compare_digest(COMPTES[c]["mdp"], request.form.get("mdp", "")):
            session["compte"] = c
            return redirect("/messages")
        erreur = "Identifiants incorrects."
    return render_template("connexion.html", erreur=erreur)

@app.route("/deconnexion")
def deconnexion():
    session.clear()
    return redirect("/")

@app.route("/messages", methods=["GET", "POST"])
def messages():
    if not connecte():
        return redirect("/")
    if request.method == "POST":
        texte = request.form.get("texte", "")[:2000]
        if texte.strip():
            MESSAGES.append({"auteur": COMPTES[session["compte"]]["nom"], "texte": texte, "le": datetime.datetime.now().strftime("%H:%M")})
        return redirect("/messages")
    # VULNÉRABLE : le gabarit affiche les messages avec |safe (XSS stockée, module 6)
    return render_template("messages.html", messages=MESSAGES[-30:], moi=COMPTES[session["compte"]])

@app.route("/collecteur/<path:reste>")
@app.route("/collecteur/", defaults={"reste": ""})
def collecteur(reste):
    # Serveur de l'attaquant, fourni pour ne pas dépendre d'un service externe.
    COLLECTE.append({"le": datetime.datetime.now().strftime("%H:%M:%S"), "url": request.full_path, "de": request.headers.get("User-Agent", "")[:80]})
    del COLLECTE[:-50]
    return "", 204

@app.route("/collecteur-journal")
def journal():
    return render_template("journal.html", lignes=reversed(COLLECTE))

@app.route("/mutuelle/dossier")
def dossier():
    if not connecte():
        return redirect("/")
    try:
        n = int(request.args.get("id", ""))
    except ValueError:
        abort(400)
    # VULNÉRABLE : aucune vérification que le dossier appartient à l'utilisateur (IDOR, module 7)
    d = DOSSIERS.get(n)
    if not d:
        abort(404)
    return render_template("dossier.html", n=n, d=d, moi=COMPTES[session["compte"]])

def robot_directrice():
    # Toutes les 20 s, la directrice « lit » les messages dans un vrai navigateur.
    from playwright.sync_api import sync_playwright
    time.sleep(5)
    with sync_playwright() as p:
        while True:
            try:
                nav = p.chromium.launch(args=["--no-sandbox"], executable_path=os.environ.get("CHROMIUM_PATH") or None)
                ctx = nav.new_context()
                page = ctx.new_page()
                page.goto(f"http://127.0.0.1:{PORT}/")
                page.fill("input[name=compte]", "c.morel")
                page.fill("input[name=mdp]", MDP_DIRECTEUR)
                page.click("button")
                # VULNÉRABLE : cookie sensible sans HttpOnly, lisible par JavaScript
                ctx.add_cookies([{"name": "jeton_direction", "value": DRAPEAU_XSS, "url": f"http://127.0.0.1:{PORT}/"}])
                page.goto(f"http://127.0.0.1:{PORT}/messages")
                page.wait_for_timeout(4000)
                nav.close()
            except Exception as e:
                print("robot :", e, flush=True)
            time.sleep(20)

if __name__ == "__main__":
    if os.environ.get("ROBOT", "1") == "1":
        threading.Thread(target=robot_directrice, daemon=True).start()
    app.run(host="0.0.0.0", port=PORT, threaded=True)
