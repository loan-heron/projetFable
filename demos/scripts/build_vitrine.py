#!/usr/bin/env python3
"""Génère demos/index.html (la vitrine avant / après) à partir des défauts
documentés ci-dessous et des résultats d'audit dans demos/audits/synthese.json.
Usage : python3 demos/scripts/build_vitrine.py"""
import json, html, pathlib

ICI = pathlib.Path(__file__).resolve().parent.parent
synthese = {(l["boutique"], l["version"]): l for l in json.loads((ICI / "audits" / "synthese.json").read_text())}

BOUTIQUES = [
    {
        "id": "celadon", "nom": "Céladon", "secteur": "Céramique artisanale", "page": "Fiche produit",
        "pitch": "Une jolie boutique d'atelier, du genre qu'on trouve par centaines sur Shopify. À l'œil, rien ne cloche. Au clavier ou au lecteur d'écran, on ne peut pas acheter le bol.",
        "defauts": [
            ("bloquant", "Le bouton « Ajouter au panier » n'est pas un bouton", "C'est un bloc cliquable à la souris uniquement. Au clavier ou avec un lecteur d'écran, impossible d'acheter.", "Vrai bouton dans un formulaire. L'ajout est confirmé à voix haute : « 1 bol Lichen Céladon ajouté au panier ».", "RGAA 7.1, 7.3, 7.5"),
            ("bloquant", "Le choix de l'émail se fait par pastilles muettes", "Quatre ronds de couleur sans nom, inatteignables au clavier. Un daltonien ou un aveugle ne sait pas ce qu'il choisit.", "Boutons radio natifs groupés sous « Émail », nom de la teinte écrit en toutes lettres à côté du titre.", "RGAA 3.1, 7.1, 11.1"),
            ("majeur", "Le carrousel défile tout seul toutes les 3 secondes", "Pas de bouton pause : la photo change pendant qu'on la regarde ou qu'on la zoome.", "Plus de défilement automatique. Les vignettes sont des boutons qui disent « Photo 2 sur 4 : vue du dessus ».", "RGAA 13.8"),
            ("majeur", "Une pop-up promo s'ouvre au bout de 6 secondes", "Le focus reste derrière, la croix n'est pas un bouton, Échap ne fait rien. Au clavier, la page devient inutilisable.", "Pop-up supprimée. L'offre passe dans la lettre d'information, en bas de page.", "RGAA 7.1, 7.3"),
            ("majeur", "Le focus clavier a été effacé", "Le thème retire le contour de focus : on ne sait jamais où l'on est en naviguant au clavier.", "Anneau de focus de 3 px, contrasté sur chaque élément, y compris les pastilles d'émail.", "RGAA 10.7"),
            ("majeur", "25 textes trop pâles", "Prix en vert céladon à 2,0:1, bandeau blanc sur céladon à 2,3:1, textes gris à 2,0:1. Le minimum légal est 4,5:1.", "Mêmes teintes, foncées juste assez : texte principal à 11,1:1, texte secondaire à 6,2:1.", "RGAA 3.2"),
            ("majeur", "Le zoom est bloqué sur mobile", "La balise viewport interdit d'agrandir : les personnes malvoyantes ne peuvent pas lire les dimensions du bol.", "Zoom libre jusqu'à 200 % et au-delà, mise en page qui suit.", "RGAA 10.4"),
            ("majeur", "Icônes sans nom", "Recherche, compte, panier, Instagram et Pinterest sont annoncés « lien » sans autre précision.", "Chaque icône a un intitulé : « Panier, 2 articles », « Céladon sur Instagram ».", "RGAA 6.2"),
            ("mineur", "Page sans langue, sans titre utile, sans structure", "Pas d'attribut lang, titre d'onglet « Céladon », aucun h1, aucune zone (en-tête, contenu, pied).", "lang=\"fr\", titre « Bol Lichen, grès émaillé céladon », h1, landmarks et lien d'évitement.", "RGAA 8.3, 8.6, 9.1, 12.6, 12.7"),
            ("mineur", "Formulaire de lettre d'info sans étiquette", "Seul un texte gris « Votre e-mail » dans le champ, qui disparaît à la saisie.", "Étiquette visible, format attendu, autocomplétion, message d'erreur clair.", "RGAA 11.1, 11.13"),
            ("mineur", "Lien « cliquez ici » et aucune mention d'accessibilité", "Le lien ne dit pas où il mène. Le pied de page n'indique pas l'état de conformité, pourtant obligatoire.", "« Découvrir l'atelier » et mention « Accessibilité : partiellement conforme » vers la déclaration.", "RGAA 6.1"),
        ],
    },
    {
        "id": "foulee", "nom": "Foulée", "secteur": "Running", "page": "Page catégorie avec filtres",
        "pitch": "Une page catégorie énergique, avec des filtres à la pointe de la mode. Sauf qu'ils ne fonctionnent qu'à la souris, et que la moitié des informations passent par la couleur.",
        "defauts": [
            ("bloquant", "Les filtres ne marchent qu'à la souris", "Terrain, marque, pointure et couleur sont des blocs cliquables : aucun n'est atteignable au clavier ni annoncé comme une case.", "Cases à cocher natives, groupées par fieldset avec un titre (« Terrain », « Pointure »…).", "RGAA 7.1, 7.3, 11.5"),
            ("bloquant", "Les produits ne sont pas des liens", "La carte entière est cliquable en JavaScript, mais il n'existe aucun lien : au clavier, on ne peut ouvrir aucune chaussure.", "Le nom du modèle est un vrai lien, étendu à toute la carte pour la souris.", "RGAA 7.1, 7.3"),
            ("bloquant", "Le menu « Trier par » est un faux menu", "Liste déroulante dessinée en div : impossible à ouvrir au clavier, rien n'est annoncé.", "Liste déroulante native avec son étiquette.", "RGAA 7.1, 11.1"),
            ("majeur", "Les sous-menus s'ouvrent seulement au survol", "« Homme » et « Femme » cachent leurs rubriques à quiconque n'a pas de souris.", "Boutons qui s'ouvrent au clic, à Entrée ou Espace, et se ferment avec Échap.", "RGAA 7.3, 10.13"),
            ("majeur", "Le titre de la page est une image", "« Chaussures de running homme » est dessiné dans le bandeau, sans texte alternatif ni h1.", "Vrai titre h1 en HTML, la chaussure devient une illustration décorative.", "RGAA 1.1, 9.1"),
            ("majeur", "Soldes et ruptures signalés uniquement par la couleur", "Prix soldé en orange, ancien prix juste barré, pointures épuisées simplement plus pâles.", "« Prix soldé : 129,50 € au lieu de 185,00 € » lu à voix haute ; pointures épuisées barrées, en pointillés et annoncées « épuisée ».", "RGAA 3.1"),
            ("majeur", "31 textes trop pâles", "Badges blancs sur orange à 3,1:1, gris clair à 2,4:1 sur blanc.", "Badges en encre sur orange à 5,8:1, gris passé à 7,8:1.", "RGAA 3.2"),
            ("majeur", "Le nombre de résultats change en silence", "Après un filtre, la liste se met à jour mais un lecteur d'écran n'en sait rien.", "Zone de statut : « 2 modèles » est annoncé à chaque changement, avec un message si rien ne correspond.", "RGAA 7.5"),
            ("mineur", "La page se déclare en anglais", "lang=\"en\" sur une page française : le lecteur d'écran lit tout avec l'accent anglais.", "lang=\"fr\" et titre d'onglet « Chaussures de running homme : 6 modèles – Foulée ».", "RGAA 8.4, 8.6"),
            ("mineur", "Pointures et favoris trop petits ou muets", "Pastilles de pointure de 30 px, cœurs « favori » sans nom ni état.", "Cibles de 44 px, bouton « Ajouter Aérien 3 aux favoris » qui annonce s'il est activé.", "WCAG 2.5.8, RGAA 7.1"),
        ],
    },
    {
        "id": "vrac", "nom": "Le Vrac du Coin", "secteur": "Épicerie vrac", "page": "Tunnel de commande",
        "pitch": "Le moment où l'on perd le plus de ventes. Un chrono qui vide le panier, un CAPTCHA illisible, des erreurs en rouge pâle : beaucoup de clients s'arrêtent ici, handicapés ou non.",
        "defauts": [
            ("bloquant", "Le bouton « Continuer » n'est pas un bouton", "Au clavier, impossible de valider la commande. Le paiement est hors d'atteinte.", "« Continuer vers le paiement » est un vrai bouton d'envoi de formulaire.", "RGAA 7.1, 7.3"),
            ("bloquant", "Un compte à rebours vide le panier en 5 minutes", "Aucun avertissement, aucun moyen de prolonger. Avec un lecteur d'écran ou une main qui tremble, 5 minutes ne suffisent pas.", "Panier gardé 7 jours, sans chrono.", "RGAA 13.1"),
            ("bloquant", "Un CAPTCHA image sans alternative", "Un code déformé à recopier, sans version audio ni autre moyen : bloquant pour les personnes aveugles ou malvoyantes.", "CAPTCHA supprimé, remplacé par une protection invisible côté serveur.", "RGAA 1.4, 1.5"),
            ("majeur", "Champs sans étiquette", "Seul le texte gris dans le champ indique quoi saisir, et il disparaît dès la première lettre.", "Étiquettes visibles au-dessus des champs, indications (« 10 chiffres », exemple d'e-mail) reliées au champ.", "RGAA 11.1, 11.2"),
            ("majeur", "Erreurs signalées par une bordure rose pâle", "Un « Erreur dans le formulaire » vague et des bordures rosées : on ne sait ni quel champ ni pourquoi.", "Résumé des erreurs qui prend le focus, avec des liens vers chaque champ, et un message précis sous chaque champ (« Le code postal doit comporter 5 chiffres, par exemple 69001 »).", "RGAA 3.1, 11.10, 11.11"),
            ("majeur", "Pas d'autocomplétion", "Il faut tout retaper. Pénible pour tous, épuisant pour les personnes ayant des troubles moteurs ou cognitifs.", "Chaque champ déclare sa finalité (prénom, e-mail, code postal…) : le navigateur remplit tout.", "RGAA 11.13"),
            ("majeur", "Modes de livraison et étapes en faux contrôles", "Les trois modes de livraison sont des blocs cliquables, l'étape en cours n'est signalée que par la couleur.", "Boutons radio natifs dans un groupe titré, étape annoncée « étape en cours ».", "RGAA 3.1, 7.1, 11.5"),
            ("majeur", "Panier aux commandes muettes", "Poubelles sans nom ni accès clavier, quantités sans étiquette.", "« Retirer les pois chiches du panier », « Quantité de pois chiches ».", "RGAA 7.1, 11.1"),
            ("majeur", "16 textes trop pâles", "Bouton vert clair à 2,1:1, chrono blanc sur jaune à 1,8:1, bords de champs à 1,4:1.", "Bouton à 7,3:1, bords de champs à 4,4:1, textes secondaires à 6,8:1.", "RGAA 3.2, 3.3"),
            ("mineur", "Titre « Checkout » et lien « ici »", "L'onglet ne dit ni l'étape ni la boutique, le lien des CGV ne dit pas où il va.", "« Étape 2 sur 3, livraison – Commande – Le Vrac du Coin », lien « lire les CGV ».", "RGAA 6.1, 8.6"),
        ],
    },
]

GRAVITE = {"bloquant": "Bloquant", "majeur": "Majeur", "mineur": "Mineur"}
e = html.escape


def chiffres(b):
    av, ap = synthese[(b, "avant")], synthese[(b, "apres")]
    lignes = [
        ("Score Lighthouse accessibilité", f"{av['lighthouse']}/100", f"{ap['lighthouse']}/100"),
        ("Erreurs détectées par axe-core", str(av["occurrences"]), str(ap["occurrences"])),
        ("Commandes impossibles au clavier", str(av["horsClavier"]), str(ap["horsClavier"])),
        ("Arrêts au clavier sans focus visible", f"{av['focusInvisible']} sur {av['arretsTab']}", f"{ap['focusInvisible']} sur {ap['arretsTab']}"),
    ]
    out = []
    for nom, a, p in lignes:
        out.append(f'<div class="chiffre"><dt>{e(nom)}</dt><dd><span class="av"><span class="vc">Avant : </span>{e(a)}</span><span class="fleche" aria-hidden="true"></span><span class="ap"><span class="vc">Après : </span>{e(p)}</span></dd></div>')
    return "\n".join(out)


def section(i, b):
    d = b["defauts"]
    nb = {g: sum(1 for x in d if x[0] == g) for g in GRAVITE}
    items = "\n".join(
        f'''<li class="defaut g-{g}">
  <div class="tete"><span class="gravite">{GRAVITE[g]}</span><h4>{e(t)}</h4></div>
  <div class="corps">
    <div><p class="etiq">Avant</p><p>{e(av)}</p></div>
    <div><p class="etiq">Après</p><p>{e(ap)}</p></div>
  </div>
  <p class="ref">{e(ref)}</p>
</li>''' for g, t, av, ap, ref in d)
    return f'''
<section class="boutique" id="{b["id"]}" aria-labelledby="t-{b["id"]}">
  <header class="b-tete">
    <p class="b-meta">{e(b["secteur"])}, {e(b["page"]).lower()}</p>
    <h2 id="t-{b["id"]}">{e(b["nom"])}</h2>
    <p class="b-pitch">{e(b["pitch"])}</p>
  </header>

  <div class="comparo-bloc">
    <div class="vues" role="group" aria-label="Format de la capture">
      <button type="button" class="vue-btn" aria-pressed="true" data-vue="ecran">Ordinateur</button>
      <button type="button" class="vue-btn" aria-pressed="false" data-vue="mobile">Mobile</button>
    </div>
    <figure class="comparo" data-b="{b["id"]}" style="--pos:50%">
      <div class="cadre">
        <img class="img-ap" src="captures/{b["id"]}-apres-ecran.jpg" alt="Version après : {e(b["nom"])}, page corrigée et accessible" width="2880" height="1800">
        <img class="img-av" src="captures/{b["id"]}-avant-ecran.jpg" alt="Version avant : {e(b["nom"])}, page d'origine non conforme" width="2880" height="1800">
        <span class="badge-av" aria-hidden="true">Avant</span><span class="badge-ap" aria-hidden="true">Après</span>
        <span class="poignee" aria-hidden="true"></span>
        <label class="vc" for="r-{b["id"]}">Curseur de comparaison, à gauche la version avant, à droite la version après</label>
        <input class="curseur" id="r-{b["id"]}" type="range" min="0" max="100" value="50">
      </div>
      <figcaption>Faites glisser le curseur, ou utilisez les flèches du clavier, pour comparer.</figcaption>
    </figure>
    <p class="ouvrir">
      <a class="btn btn-av" href="{b["id"]}/avant.html" target="_blank" rel="noopener">Ouvrir la version avant</a>
      <a class="btn btn-ap" href="{b["id"]}/apres.html" target="_blank" rel="noopener">Ouvrir la version après</a>
    </p>
  </div>

  <div class="mesures">
    <h3>Ce que disent les tests</h3>
    <dl class="chiffres">
{chiffres(b["id"])}
    </dl>
  </div>

  <div class="liste">
    <h3>{len(d)} problèmes corrigés <span class="repartition">{nb["bloquant"]} bloquants, {nb["majeur"]} majeurs, {nb["mineur"]} mineurs</span></h3>
    <ol class="defauts">
{items}
    </ol>
  </div>
</section>'''


TOT_AV = sum(synthese[(b["id"], "avant")]["occurrences"] for b in BOUTIQUES)
TOT_DEF = sum(len(b["defauts"]) for b in BOUTIQUES)
SCORES_AV = " / ".join(str(synthese[(b["id"], "avant")]["lighthouse"]) for b in BOUTIQUES)

PAGE = f'''<title>Rampe, avant / après</title>
<meta name="claude:viewport-fit-sides" content="cover">
<meta name="description" content="Trois boutiques en ligne fictives, auditées puis rendues accessibles par Rampe.">
<style>
/* Mise en page : une colonne éditoriale, chaque boutique = comparateur plein cadre, puis chiffres, puis liste des défauts. */
@font-face {{ font-family: "Archivo"; src: url("fonts/archivo-latin-wdth-normal.woff2") format("woff2"); font-weight: 100 900; font-stretch: 62% 125%; font-display: swap; }}
@font-face {{ font-family: "Atkinson Hyperlegible Next"; src: url("fonts/atkinson-hyperlegible-next-latin-400-normal.woff2") format("woff2"); font-weight: 400; font-display: swap; }}
@font-face {{ font-family: "Atkinson Hyperlegible Next"; src: url("fonts/atkinson-hyperlegible-next-latin-700-normal.woff2") format("woff2"); font-weight: 700; font-display: swap; }}
:root {{
  --papier: #f2ede4;
  --papier-2: #e8e1d4;
  --encre: #111111;
  --encre-2: #4a463f;
  --jaune: #ffd400;
  --rouge: #e5322d;       /* défauts : en aplat ou en grand seulement */
  --rouge-texte: #b3201b; /* rouge lisible en petit, 5,5:1 sur papier */
  --bleu: #1f3bff;
  --vert: #1d6b3a;
  --trait: #111111;
  --display: "Archivo", "Arial Narrow", Arial, sans-serif;
  --texte: "Atkinson Hyperlegible Next", "Atkinson Hyperlegible", Verdana, sans-serif;
}}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{ --papier: #141311; --papier-2: #1f1d1a; --encre: #f2ede4; --encre-2: #c9c1b3; --rouge-texte: #ff7a6e; --vert: #6fd08f; --bleu: #8a9bff; --trait: #f2ede4; color-scheme: dark; }} }}
:root[data-theme="dark"] {{ --papier: #141311; --papier-2: #1f1d1a; --encre: #f2ede4; --encre-2: #c9c1b3; --rouge-texte: #ff7a6e; --vert: #6fd08f; --bleu: #8a9bff; --trait: #f2ede4; color-scheme: dark; }}

* {{ box-sizing: border-box; }}
body {{ margin: 0; background: var(--papier); color: var(--encre); font: 400 1.0625rem/1.6 var(--texte); }}
.page {{ max-width: 1180px; margin: 0 auto; padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); padding-block: 0 4rem; }}
a {{ color: inherit; }}
:focus-visible {{ outline: 4px solid var(--bleu); outline-offset: 3px; }}
.vc {{ position: absolute !important; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; }}
h1, h2, h3, h4 {{ text-wrap: balance; }}

/* En-tête */
.haut {{ display: flex; justify-content: space-between; align-items: center; gap: 1rem; padding-block: 1.4rem; border-bottom: 3px solid var(--trait); flex-wrap: wrap; }}
.marque {{ font-family: var(--display); font-stretch: 125%; font-weight: 900; font-size: 1.6rem; letter-spacing: -.02em; line-height: 1; display: flex; align-items: center; gap: .55rem; }}
.marque svg {{ width: 40px; height: 22px; }}
.haut nav ul {{ display: flex; gap: .4rem; list-style: none; margin: 0; padding: 0; flex-wrap: wrap; }}
.haut nav a {{ display: block; padding: .45rem .9rem; border: 2px solid var(--trait); border-radius: 999px; text-decoration: none; font-weight: 700; font-size: .95rem; }}
.haut nav a:hover {{ background: var(--jaune); color: #111; }}

/* Ouverture */
.ouverture {{ padding-block: clamp(2.5rem, 7vw, 5.5rem) clamp(2rem, 5vw, 3.5rem); display: grid; grid-template-columns: minmax(0, 1.5fr) minmax(0, 1fr); gap: 2.5rem; align-items: end; }}
.ouverture h1 {{ font-family: var(--display); font-weight: 900; font-stretch: 112%; font-size: clamp(2.6rem, 7.4vw, 6rem); line-height: .9; letter-spacing: -.035em; margin: 0; }}
.ouverture h1 .marche {{ display: inline-block; transform: translateY(.14em); }}
.ouverture .chapo {{ font-size: 1.2rem; max-width: 38ch; margin: 0 0 1rem; }}
.ouverture .note {{ font-size: .95rem; color: var(--encre-2); margin: 0; max-width: 44ch; }}
.pente {{ height: 26px; background: var(--jaune); clip-path: polygon(0 100%, 100% 0, 100% 100%); margin-bottom: 2.5rem; }}

.bilan {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 0; border: 3px solid var(--trait); margin-bottom: 4rem; }}
.bilan > div {{ padding: 1.2rem 1.3rem 1.3rem; }}
.bilan > div + div {{ border-left: 3px solid var(--trait); }}
.bilan .gros {{ font-family: var(--display); font-weight: 900; font-stretch: 100%; font-size: clamp(2.2rem, 4.5vw, 3.4rem); line-height: 1; letter-spacing: -.03em; font-variant-numeric: tabular-nums; }}
.bilan p {{ margin: .4rem 0 0; font-size: .98rem; }}

/* Boutique */
.boutique {{ padding-top: 3.5rem; border-top: 3px solid var(--trait); margin-top: 1rem; }}
.b-tete {{ display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); gap: .4rem 2.5rem; align-items: end; margin-bottom: 2rem; }}
.b-meta {{ grid-column: 1 / -1; margin: 0; font-weight: 700; color: var(--encre-2); }}
.b-tete h2 {{ font-family: var(--display); font-weight: 900; font-stretch: 125%; font-size: clamp(2.4rem, 6vw, 4.6rem); line-height: .92; letter-spacing: -.03em; margin: 0; }}
.b-pitch {{ margin: 0; max-width: 46ch; }}

.vues {{ display: inline-flex; border: 2px solid var(--trait); border-radius: 999px; padding: 3px; margin-bottom: .9rem; }}
.vue-btn {{ font: 700 .95rem var(--texte); border: 0; background: none; color: var(--encre); padding: .45rem 1rem; border-radius: 999px; cursor: pointer; min-height: 40px; }}
.vue-btn[aria-pressed="true"] {{ background: var(--encre); color: var(--papier); }}

.comparo {{ margin: 0; }}
.cadre {{ position: relative; border: 3px solid var(--trait); overflow: hidden; background: var(--papier-2); max-width: 100%; aspect-ratio: 16 / 10; }}
.comparo.mobile .cadre {{ aspect-ratio: 390 / 844; width: min(390px, 100%); margin-inline: auto; }}
.cadre img {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; object-position: top; display: block; max-width: none; }}
.img-av {{ clip-path: inset(0 calc(100% - var(--pos)) 0 0); }}
.poignee {{ position: absolute; top: 0; bottom: 0; left: var(--pos); width: 4px; margin-left: -2px; background: var(--jaune); box-shadow: 0 0 0 2px #111; pointer-events: none; }}
.poignee::after {{ content: ""; position: absolute; top: 50%; left: 50%; width: 46px; height: 46px; margin: -23px 0 0 -23px; border-radius: 50%; background: var(--jaune); border: 3px solid #111; background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 40 40'%3E%3Cpath d='M15 12l-7 8 7 8M25 12l7 8-7 8' fill='none' stroke='%23111' stroke-width='3.5'/%3E%3C/svg%3E"); background-size: 100%; }}
.badge-av, .badge-ap {{ position: absolute; top: .8rem; font: 900 1rem/1 var(--display); font-stretch: 110%; padding: .45rem .7rem; pointer-events: none; }}
.badge-av {{ left: .8rem; background: var(--rouge); color: #fff; }}
.badge-ap {{ right: .8rem; background: var(--vert); color: #fff; }}
:root[data-theme="dark"] .badge-ap {{ color: #111; }}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) .badge-ap {{ color: #111; }} }}
.curseur {{ position: absolute; inset: 0; width: 100%; height: 100%; margin: 0; opacity: 0; cursor: ew-resize; }}
.cadre:has(.curseur:focus-visible) {{ outline: 4px solid var(--bleu); outline-offset: 3px; }}
.comparo figcaption {{ font-size: .93rem; color: var(--encre-2); margin-top: .6rem; }}
.ouvrir {{ display: flex; flex-wrap: wrap; gap: .6rem; margin: 1rem 0 0; }}
.btn {{ display: inline-flex; align-items: center; min-height: 48px; padding: 0 1.2rem; border: 3px solid var(--trait); font-weight: 700; text-decoration: none; }}
.btn-ap {{ background: var(--jaune); color: #111; border-color: #111; }}
.btn:hover {{ text-decoration: underline; text-underline-offset: 4px; }}

.mesures {{ margin-top: 2.8rem; }}
.boutique h3 {{ font-family: var(--display); font-weight: 800; font-stretch: 100%; font-size: 1.6rem; letter-spacing: -.01em; margin: 0 0 1rem; display: flex; flex-wrap: wrap; align-items: baseline; gap: .3rem 1rem; }}
.repartition {{ font-family: var(--texte); font-weight: 400; font-size: 1rem; color: var(--encre-2); letter-spacing: 0; }}
.chiffres {{ display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 0; margin: 0; border: 3px solid var(--trait); }}
.chiffre {{ padding: 1rem 1.1rem 1.1rem; display: flex; flex-direction: column; justify-content: space-between; gap: .7rem; min-width: 0; }}
.chiffre + .chiffre {{ border-left: 3px solid var(--trait); }}
.chiffre dt {{ font-size: .95rem; font-weight: 700; }}
.chiffre dd {{ margin: 0; display: flex; align-items: center; gap: .55rem; flex-wrap: wrap; font-family: var(--display); font-weight: 900; font-variant-numeric: tabular-nums; }}
.chiffre .av {{ font-size: 1.3rem; color: var(--rouge-texte); text-decoration: line-through; text-decoration-thickness: 3px; }}
.chiffre .ap {{ font-size: 2.1rem; line-height: 1; }}
.fleche {{ width: 26px; height: 14px; background: currentColor; clip-path: polygon(0 40%, 70% 40%, 70% 0, 100% 50%, 70% 100%, 70% 60%, 0 60%); }}

.liste {{ margin-top: 2.8rem; }}
.defauts {{ list-style: none; margin: 0; padding: 0; display: grid; gap: .9rem; }}
.defaut {{ border: 3px solid var(--trait); padding: 1.1rem 1.2rem 1rem; background: var(--papier); }}
.tete {{ display: flex; gap: .8rem; align-items: baseline; flex-wrap: wrap; }}
.tete h4 {{ margin: 0; font-size: 1.15rem; line-height: 1.3; }}
.gravite {{ font: 800 .85rem/1 var(--display); padding: .4rem .55rem; border: 2px solid var(--trait); flex: none; }}
.g-bloquant .gravite {{ background: var(--rouge); color: #fff; border-color: var(--rouge); }}
.g-majeur .gravite {{ background: var(--jaune); color: #111; border-color: #111; }}
.corps {{ display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); gap: 1.5rem; margin-top: .7rem; }}
.corps p {{ margin: 0; }}
.corps .etiq {{ font-weight: 700; font-size: .9rem; margin-bottom: .15rem; }}
.corps > div:first-child .etiq {{ color: var(--rouge-texte); }}
.corps > div:last-child .etiq {{ color: var(--vert); }}
.ref {{ margin: .8rem 0 0; font-size: .9rem; color: var(--encre-2); }}

/* Méthode */
.methode {{ border-top: 3px solid var(--trait); margin-top: 4rem; padding-top: 3rem; display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1.4fr); gap: 2.5rem; }}
.methode h2 {{ font-family: var(--display); font-weight: 900; font-stretch: 112%; font-size: clamp(2rem, 4vw, 3rem); line-height: .95; letter-spacing: -.03em; margin: 0; }}
.methode ul {{ margin: 0; padding-left: 1.2rem; display: grid; gap: .6rem; }}
.methode p {{ margin: 0 0 1rem; }}
.pied {{ margin-top: 3rem; font-size: .93rem; color: var(--encre-2); }}

@media (max-width: 820px) {{
  .ouverture, .b-tete, .methode {{ grid-template-columns: 1fr; }}
  .chiffres {{ grid-template-columns: 1fr 1fr; }}
  .chiffre:nth-child(3) {{ border-left: 0; }}
  .chiffre:nth-child(n+3) {{ border-top: 3px solid var(--trait); }}
  .corps {{ grid-template-columns: 1fr; gap: .8rem; }}
}}
@media (max-width: 560px) {{
  .bilan {{ grid-template-columns: 1fr; }}
  .bilan > div + div {{ border-left: 0; border-top: 3px solid var(--trait); }}
}}
@media (prefers-reduced-motion: no-preference) {{
  .ouverture h1 .marche {{ animation: marche .9s cubic-bezier(.3,1.4,.6,1) .2s both; }}
  @keyframes marche {{ from {{ transform: translateY(0); }} to {{ transform: translateY(.14em); }} }}
}}
</style>

<div class="page">
<header class="haut">
  <p class="marque" style="margin:0"><svg viewBox="0 0 40 22" aria-hidden="true"><path d="M0 22 L40 0 L40 22 Z" fill="var(--jaune)"/><path d="M0 22 L40 0" stroke="var(--encre)" stroke-width="3"/></svg>Rampe</p>
  <nav aria-label="Boutiques">
    <ul>{"".join(f'<li><a href="#{b["id"]}">{e(b["nom"])}</a></li>' for b in BOUTIQUES)}<li><a href="#methode">Méthode</a></li></ul>
  </nav>
</header>

<main>
  <div class="ouverture">
    <h1>Même boutique. <span class="marche">Sans</span> les marches.</h1>
    <div>
      <p class="chapo">Trois boutiques en ligne inventées, chacune avec les défauts qu'on retrouve sur la plupart des sites marchands français. Puis la même page, refaite par Rampe.</p>
      <p class="note">Boutiques, marques et produits fictifs, créés pour la démonstration. Les défauts, eux, sont tirés de vrais sites.</p>
    </div>
  </div>
  <div class="pente" aria-hidden="true"></div>

  <div class="bilan">
    <div><p class="gros">{TOT_DEF}</p><p>problèmes corrigés sur 3 pages clés : fiche produit, catégorie, commande.</p></div>
    <div><p class="gros">{TOT_AV} → 0</p><p>erreurs relevées automatiquement par axe-core, avant puis après.</p></div>
    <div><p class="gros">100/100</p><p>au score d'accessibilité Lighthouse sur les trois pages, contre {SCORES_AV} avant.</p></div>
  </div>

  {"".join(section(i, b) for i, b in enumerate(BOUTIQUES))}

  <section class="methode" id="methode" aria-labelledby="t-methode">
    <h2 id="t-methode">Comment on a mesuré</h2>
    <div>
      <p>Chaque page a été testée dans un vrai navigateur, avant et après correction, avec le même protocole :</p>
      <ul>
        <li><strong>axe-core</strong> (le moteur utilisé par la plupart des outils d'audit) sur les règles WCAG 2.2 niveaux A et AA ;</li>
        <li><strong>Lighthouse</strong>, l'outil de Google intégré à Chrome, catégorie accessibilité ;</li>
        <li>un <strong>parcours au clavier</strong> automatisé : chaque élément cliquable est-il atteignable avec Tab, et voit-on où l'on est ?</li>
        <li>une <strong>revue manuelle</strong> selon le RGAA 4.1, le référentiel officiel français : c'est elle qui trouve le chrono, le CAPTCHA ou les soldes signalés par la seule couleur, que les robots ne voient pas.</li>
      </ul>
      <p style="margin-top:1rem">Les tests automatiques ne détectent qu'environ un tiers des problèmes. Un score de 100 ne prouve pas la conformité : c'est pour ça que les versions « après » affichent « partiellement conforme » tant qu'un audit RGAA complet n'a pas été mené.</p>
    </div>
  </section>

  <p class="pied">Démonstration réalisée par Rampe. Code source, rapports d'audit et captures dans le dossier demos du dépôt.</p>
</main>
</div>

<script>
document.querySelectorAll('.comparo').forEach(fig => {{
  const r = fig.querySelector('.curseur');
  const maj = () => fig.style.setProperty('--pos', r.value + '%');
  r.addEventListener('input', maj); maj();
}});
document.querySelectorAll('.boutique').forEach(sec => {{
  const fig = sec.querySelector('.comparo'), b = fig.dataset.b;
  sec.querySelectorAll('.vue-btn').forEach(btn => btn.addEventListener('click', () => {{
    sec.querySelectorAll('.vue-btn').forEach(x => x.setAttribute('aria-pressed', String(x === btn)));
    const v = btn.dataset.vue;
    fig.classList.toggle('mobile', v === 'mobile');
    fig.querySelector('.img-av').src = `captures/${{b}}-avant-${{v}}.jpg`;
    fig.querySelector('.img-ap').src = `captures/${{b}}-apres-${{v}}.jpg`;
    const [w, h] = v === 'mobile' ? [780, 1688] : [2880, 1800];
    fig.querySelectorAll('img').forEach(i => {{ i.width = w; i.height = h; }});
  }}));
}});
</script>
'''

# Fragment pour l'Artifact (le squelette HTML est ajouté à la publication)
(ICI / "vitrine-fragment.html").write_text(PAGE)
# Page autonome pour le dépôt
(ICI / "index.html").write_text('<!doctype html>\n<html lang="fr">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n' + PAGE.replace("<div class=\"page\">", "</head>\n<body>\n<div class=\"page\">", 1) + "\n</body>\n</html>\n")
print("ok", TOT_DEF, TOT_AV)
