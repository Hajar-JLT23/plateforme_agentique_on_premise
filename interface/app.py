import sys
import json
import time
from datetime import datetime
from pathlib import Path
from agents.agentRaG import lancer_rag

import gradio as gr

sys.path.append(str(Path(__file__).parent.parent))

from config import MODELES_DISPONIBLES
from agents.agent_anonymisation import (
    detecter_regex,
    detecter_llm,
    fusionner_detections,
    anonymiser_texte
)
from agents.agent_generation import generer, lire_fichier


CUSTOM_CSS = """
.gradio-container {
    max-width: 1450px !important;
    margin: auto !important;
}

.hero {
    background: linear-gradient(135deg, #020617, #312e81, #4f46e5);
    padding: 40px;
    border-radius: 26px;
    color: white;
    margin-bottom: 24px;
    box-shadow: 0 24px 55px rgba(0,0,0,0.35);
    position: relative;
    overflow: hidden;
}

.hero h1 {
    font-size: 44px;
    margin-bottom: 10px;
}

.hero p {
    font-size: 17px;
    opacity: 0.95;
}

.hero::after {
    content: "";
    position: absolute;
    width: 220px;
    height: 220px;
    right: -60px;
    top: -60px;
    background: rgba(255,255,255,0.12);
    border-radius: 50%;
}

.badge {
    display: inline-block;
    background: rgba(255,255,255,0.14);
    padding: 8px 14px;
    border-radius: 999px;
    margin-right: 8px;
    margin-top: 10px;
    font-size: 14px;
}

.creator-card {
    background: linear-gradient(135deg, #111827, #1e1b4b);
    border: 1px solid #4338ca;
    border-radius: 18px;
    padding: 18px;
    color: #e5e7eb;
    margin-bottom: 20px;
    box-shadow: 0 14px 30px rgba(0,0,0,0.22);
}

.creator-card strong {
    color: #c4b5fd;
}

.robot-card {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    border: 1px solid #334155;
    border-radius: 20px;
    padding: 22px;
    color: white;
    margin-bottom: 18px;
    box-shadow: 0 14px 30px rgba(0,0,0,0.25);
}

.robot {
    font-size: 54px;
    animation: floatRobot 2.5s ease-in-out infinite;
    display: inline-block;
    margin-right: 15px;
}

.robot-text {
    display: inline-block;
    vertical-align: top;
    max-width: 900px;
}

.robot-text h3 {
    color: #c4b5fd;
    margin-bottom: 6px;
}

.robot-buttons {
    margin-bottom: 22px;
}

@keyframes floatRobot {
    0% { transform: translateY(0px) rotate(0deg); }
    50% { transform: translateY(-8px) rotate(3deg); }
    100% { transform: translateY(0px) rotate(0deg); }
}

.overview-box {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    border: 1px solid #334155;
    border-radius: 18px;
    padding: 22px;
    min-height: 180px;
    box-shadow: 0 12px 28px rgba(0,0,0,0.22);
}

.overview-box h3 {
    color: #c4b5fd;
    margin-bottom: 10px;
}

.stats-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 14px;
    margin: 18px 0;
}

.stat-card {
    background: linear-gradient(135deg, #111827, #1e293b);
    border: 1px solid #334155;
    border-radius: 18px;
    padding: 18px;
    color: white;
    box-shadow: 0 12px 28px rgba(0,0,0,0.22);
}

.stat-card h3 {
    color: #a5b4fc;
    font-size: 14px;
    margin-bottom: 8px;
}

.stat-card p {
    font-size: 26px;
    font-weight: bold;
    margin: 0;
}

.score-card {
    border-radius: 18px;
    padding: 18px;
    margin: 12px 0;
    color: white;
    box-shadow: 0 12px 28px rgba(0,0,0,0.22);
}

.score-low {
    background: linear-gradient(135deg, #064e3b, #047857);
    border: 1px solid #10b981;
}

.score-medium {
    background: linear-gradient(135deg, #78350f, #d97706);
    border: 1px solid #f59e0b;
}

.score-high {
    background: linear-gradient(135deg, #7f1d1d, #dc2626);
    border: 1px solid #ef4444;
}

.generation-help {
    background: linear-gradient(135deg, #111827, #1e293b);
    border: 1px solid #334155;
    border-radius: 18px;
    padding: 16px;
    color: #dbeafe;
    margin: 12px 0;
}

.generation-help strong {
    color: #c4b5fd;
}

.timeline {
    background: #020617;
    border: 1px solid #334155;
    border-radius: 18px;
    padding: 18px;
    color: #dbeafe;
    line-height: 1.8;
    margin-top: 12px;
}

.timeline h3 {
    color: #c4b5fd;
}

.benchmark-bars {
    background: #020617;
    border: 1px solid #334155;
    border-radius: 18px;
    padding: 18px;
    color: white;
    margin-top: 12px;
}

.bar-row {
    margin-bottom: 14px;
}

.bar-label {
    margin-bottom: 6px;
    color: #c4b5fd;
    font-weight: bold;
}

.bar-track {
    background: #1e293b;
    border-radius: 999px;
    overflow: hidden;
    height: 18px;
}

.bar-fill {
    height: 18px;
    background: linear-gradient(90deg, #6366f1, #a855f7);
    border-radius: 999px;
}

.loader-ai {
    display: inline-block;
    width: 12px;
    height: 12px;
    background: #a5b4fc;
    border-radius: 50%;
    animation: pulseAI 1.2s infinite ease-in-out;
    margin-right: 8px;
}

@keyframes pulseAI {
    0% { transform: scale(0.8); opacity: 0.5; }
    50% { transform: scale(1.2); opacity: 1; }
    100% { transform: scale(0.8); opacity: 0.5; }
}

.architecture {
    background: #020617;
    border: 1px solid #334155;
    border-radius: 18px;
    padding: 22px;
    font-family: monospace;
    color: #dbeafe;
    line-height: 1.9;
    box-shadow: inset 0 0 20px rgba(99,102,241,0.12);
}

.footer {
    text-align: center;
    color: #9ca3af;
    font-size: 13px;
    margin-top: 30px;
}
"""


EXEMPLE_ANONYMISATION = """Bonjour,
Je m'appelle Jean Dupont.
Mon adresse email est jean.dupont@gmail.com.
Mon numéro de téléphone est 06 00 12 00 01.
J'habite au 12 rue Victor Hugo à Paris."""

EXEMPLE_RESUME = """L'intelligence artificielle générative est de plus en plus utilisée dans les entreprises pour automatiser des tâches comme la synthèse documentaire, la rédaction d'emails ou la génération de comptes rendus. Cependant, son utilisation pose des défis liés aux hallucinations, à la confidentialité des données et à la qualité des réponses. Certaines entreprises privilégient donc des modèles locaux afin de mieux contrôler leurs données."""

EXEMPLE_REFORMULATION = """Bonjour,

Nous n’avons pas encore reçu les documents nécessaires pour préparer la réunion de demain.

Serait-il possible de nous les transmettre dès que possible afin que nous puissions finaliser la présentation dans de bonnes conditions ?

Merci par avance pour votre retour."""

EXEMPLE_EMAIL = """La recruteuse a proposé un entretien mardi à 10h pour une alternance en intelligence artificielle. Je veux confirmer ma disponibilité et demander si l'entretien sera en présentiel ou en visioconférence."""

EXEMPLE_COMPTE_RENDU = """Réunion projet IA du 12 mai 2026.
Participants : tuteur entreprise, équipe R&D, stagiaire IA.
Points abordés : résultats anonymisation, comparaison Mistral Phi3 Llama, lancement génération de texte, dataset de test, benchmark.
Décisions : tester quatre tâches, garder modèles locaux, documenter sur GitHub.
Actions : préparer prompts, créer fichiers test, développer agent, lancer benchmark jeudi."""

EXEMPLE_QUESTION_REPONSE = """C’est quoi la capitale de la France ?"""

EXEMPLE_RESUME_INTELLIGENT = """Le projet consiste à développer une plateforme IA locale capable d’anonymiser des documents et de générer du texte à l’aide de modèles locaux. La plateforme utilise Docker, Gradio, Ollama et LiteLLM. L’objectif est de garantir la confidentialité des données tout en proposant une interface simple pour tester plusieurs cas d’usage."""


HISTORIQUE_ANONYMISATION = []
HISTORIQUE_GENERATION = []
HISTORIQUE_BENCHMARK = []

STATS_FILE = Path("resultats") / "stats.json"

DEFAULT_STATS = {
    "anonymisations": 0,
    "generations": 0,
    "benchmarks": 0,
    "exports": 0,
    "temps_total": 0.0,
    "temps_mesures": 0,
    "modeles": {}
}


def charger_stats():
    if STATS_FILE.exists():
        try:
            return json.loads(
                STATS_FILE.read_text(encoding="utf-8")
            )
        except Exception:
            pass

    return DEFAULT_STATS.copy()


def sauvegarder_stats():
    STATS_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    STATS_FILE.write_text(
        json.dumps(
            STATS,
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf-8"
    )


STATS = charger_stats()


def charger_fichier(fichier):
    if fichier is None:
        return ""

    with open(fichier.name, "r", encoding="utf-8") as f:
        return f.read()


def enregistrer_stats(type_traitement, modele, temps_execution, exports=0):
    if type_traitement == "anonymisation":
        STATS["anonymisations"] += 1
    elif type_traitement == "generation":
        STATS["generations"] += 1
    elif type_traitement == "benchmark":
        STATS["benchmarks"] += 1

    STATS["exports"] += exports
    STATS["temps_total"] += temps_execution
    STATS["temps_mesures"] += 1

    if modele:
        STATS["modeles"][modele] = STATS["modeles"].get(modele, 0) + 1

    sauvegarder_stats()


def dashboard_stats_html():
    total_traitements = (
        STATS["anonymisations"]
        + STATS["generations"]
        + STATS["benchmarks"]
    )

    if STATS["temps_mesures"] > 0:
        temps_moyen = round(STATS["temps_total"] / STATS["temps_mesures"], 2)
    else:
        temps_moyen = 0

    if STATS["modeles"]:
        modele_plus_utilise = max(STATS["modeles"], key=STATS["modeles"].get)
    else:
        modele_plus_utilise = "Aucun"

    return f"""
    <div class="stats-grid">
        <div class="stat-card">
            <h3>Total traitements</h3>
            <p>{total_traitements}</p>
        </div>
        <div class="stat-card">
            <h3>Anonymisations</h3>
            <p>{STATS["anonymisations"]}</p>
        </div>
        <div class="stat-card">
            <h3>Générations</h3>
            <p>{STATS["generations"]}</p>
        </div>
        <div class="stat-card">
            <h3>Temps moyen</h3>
            <p>{temps_moyen}s</p>
        </div>
        <div class="stat-card">
            <h3>Modèle le plus utilisé</h3>
            <p style="font-size: 16px;">{modele_plus_utilise}</p>
        </div>
    </div>
    """


def score_confidentialite_html(detections):
    nombre = len(detections)
    types_detectes = sorted(set(item.get("type", "INCONNU") for item in detections))

    if nombre == 0:
        classe = "score-low"
        niveau = "Faible"
        message = "Aucune donnée sensible détectée."
        recommandation = "Le document peut être partagé après une vérification rapide."
    elif nombre <= 3:
        classe = "score-medium"
        niveau = "Moyen"
        message = "Quelques données sensibles ont été détectées."
        recommandation = "Une vérification manuelle est recommandée avant diffusion."
    else:
        classe = "score-high"
        niveau = "Élevé"
        message = "Plusieurs données sensibles ont été détectées."
        recommandation = "Une anonymisation est fortement recommandée avant tout partage externe."

    types_texte = ", ".join(types_detectes) if types_detectes else "Aucun"

    return f"""
    <div class="score-card {classe}">
        <h3>Niveau de risque confidentialité : {niveau}</h3>
        <p>{message}</p>
        <p><strong>Données détectées :</strong> {nombre}</p>
        <p><strong>Types détectés :</strong> {types_texte}</p>
        <p><strong>Recommandation :</strong> {recommandation}</p>
    </div>
    """


def timeline_html(titre, etapes):
    lignes = "".join([f"<li>✅ {etape}</li>" for etape in etapes])

    return f"""
    <div class="timeline">
        <h3><span class="loader-ai"></span>{titre}</h3>
        <ul>
            {lignes}
        </ul>
    </div>
    """


def benchmark_graph_html(lignes_tableau):
    valeurs = []

    for ligne in lignes_tableau:
        modele = ligne[0]
        temps = ligne[1]

        try:
            temps_float = float(temps)
            valeurs.append((modele, temps_float))
        except Exception:
            pass

    if not valeurs:
        return """
        <div class="benchmark-bars">
            <h3>Graphique benchmark</h3>
            <p>Aucune donnée exploitable pour afficher le graphique.</p>
        </div>
        """

    temps_max = max(temps for _, temps in valeurs)
    barres = ""

    for modele, temps in valeurs:
        largeur = int((temps / temps_max) * 100) if temps_max > 0 else 0
        barres += f"""
        <div class="bar-row">
            <div class="bar-label">{modele} — {temps} sec</div>
            <div class="bar-track">
                <div class="bar-fill" style="width: {largeur}%;"></div>
            </div>
        </div>
        """

    return f"""
    <div class="benchmark-bars">
        <h3>Graphique des temps d’exécution</h3>
        {barres}
    </div>
    """


def message_robot(action):
    messages = {
        "accueil": """
        <div class="robot-card">
            <span class="robot">🤖</span>
            <div class="robot-text">
                <h3>Bonjour, je suis l’assistant de démonstration.</h3>
                <p>Je vous accompagne dans l’utilisation de la plateforme. Sélectionnez un conseil pour comprendre chaque module : anonymisation, génération ou benchmark multi-modèles.</p>
            </div>
        </div>
        """,
        "anonymisation": """
        <div class="robot-card">
            <span class="robot">🛡️</span>
            <div class="robot-text">
                <h3>Module anonymisation</h3>
                <p>Importez un fichier texte ou chargez un exemple. L’agent détecte les informations personnelles, produit un texte anonymisé, affiche les détections JSON et génère des exports TXT/JSON.</p>
            </div>
        </div>
        """,
        "generation": """
        <div class="robot-card">
            <span class="robot">✍️</span>
            <div class="robot-text">
                <h3>Module génération enrichie</h3>
                <p>
                La plateforme peut :
                générer des résumés,
                reformuler un texte,
                produire des emails,
                répondre à des questions simples,
                et adapter automatiquement le ton de réponse.
                </p>

                <p style="margin-top:10px;color:#c4b5fd;">
                💡 Smart tip :
                 utilisez “Réponse directe” pour les questions simples
                 et “Structuré” pour les documents professionnels.
                 </p>
             </div>
         </div>
      """,
        "benchmark": """
        <div class="robot-card">
            <span class="robot">📊</span>
            <div class="robot-text">
                <h3>Benchmark multi-modèles</h3>
                <p>Comparez plusieurs modèles locaux sur le même contenu. Le tableau affiche les temps d’exécution et un aperçu des réponses pour analyser les performances.</p>
            </div>
        </div>
        """,
        "architecture": """
        <div class="robot-card">
            <span class="robot">⚙️</span>
            <div class="robot-text">
                <h3>Architecture locale</h3>
                <p>La plateforme fonctionne en local : Gradio pour l’interface, agents Python pour les traitements, LiteLLM pour l’appel modèle, Ollama pour exécuter les LLM locaux, et Docker pour le packaging.</p>
            </div>
        </div>
        """
    }

    return messages.get(action, messages["accueil"])


def scenario_demo():
    return """Scénario conseillé pour la démonstration :

1. Présenter la vue d’ensemble et l’architecture globale.
2. Ouvrir l’onglet Anonymisation.
3. Charger un exemple ou importer un fichier .txt.
4. Lancer l’anonymisation avec un modèle local.
5. Observer le texte anonymisé, le JSON des détections, l’historique et les exports.
6. Ouvrir l’onglet Génération de texte.
7. Tester un résumé, une reformulation, un email ou une question/réponse.
8. Ouvrir l’onglet Comparaison multi-modèles.
9. Comparer les temps d’exécution et la qualité des modèles locaux.
"""


def generation_help_html():
    return """
    <div class="generation-help">
        <strong>Module génération enrichie</strong><br>
        Ce module permet de tester plusieurs intentions utilisateur :
        résumé, reformulation, email, compte rendu et question/réponse.
        Le ton et le format de sortie permettent d’adapter la réponse selon le contexte métier.
    </div>
    """


def detecter_intention_auto(contenu):
    texte = contenu.lower()

    if any(mot in texte for mot in ["résume", "resume", "résumé", "synthèse", "synthese"]):
        return "Résumé"

    if any(mot in texte for mot in ["reformule", "reformulation", "corrige", "rends plus professionnel"]):
        return "Reformulation"

    if any(mot in texte for mot in ["mail", "email", "e-mail", "objet :", "cordialement"]):
        return "Email"

    if any(mot in texte for mot in ["compte rendu", "réunion", "reunion", "participants", "actions à faire"]):
        return "Compte rendu"

    if "?" in texte:
        return "Question / Réponse"

    return None


def construire_prompt_generation(tache, ton, format_sortie):
    base = {
        "Résumé": "prompt_resume.txt",
        "Reformulation": "prompt_reformulation.txt",
        "Email": "prompt_email.txt",
        "Compte rendu": "prompt_compte_rendu.txt",
        "Résumé intelligent": "prompt_resume.txt"
    }

    if tache == "Question / Réponse":
        prompt = """
Tu es un assistant IA professionnel.
Réponds clairement à la question posée.
Si la question est simple, donne une réponse directe.
Si la question demande une explication, structure la réponse.
N'invente pas d'information incertaine.
"""
    else:
        prompt = lire_fichier(Path("prompts") / base[tache])

    consignes = f"""

Contraintes supplémentaires :
- Ton attendu : {ton}
- Format de sortie : {format_sortie}
- Réponds uniquement en français correct.
- Ne rajoute pas d'informations inutiles.
- Structure la réponse de manière claire et professionnelle.
"""

    if tache == "Résumé intelligent":
        consignes += """
- Fournis un résumé structuré.
- Ajoute les points clés.
- Ajoute une courte conclusion.
"""

    return prompt + consignes


def creer_fichiers_export_anonymisation(texte_anonymise, detections_json):
    dossier_export = Path("resultats") / "exports"
    dossier_export.mkdir(parents=True, exist_ok=True)

    fichier_txt = dossier_export / "texte_anonymise_export.txt"
    fichier_json = dossier_export / "detections_export.json"

    fichier_txt.write_text(texte_anonymise, encoding="utf-8")
    fichier_json.write_text(detections_json, encoding="utf-8")

    return str(fichier_txt), str(fichier_json)


def creer_fichier_export_generation(resultat, tache):
    dossier_export = Path("resultats") / "exports"
    dossier_export.mkdir(parents=True, exist_ok=True)

    nom_tache = tache.lower().replace(" ", "_").replace("/", "_")
    fichier_txt = dossier_export / f"generation_{nom_tache}_export.txt"

    fichier_txt.write_text(resultat, encoding="utf-8")

    return str(fichier_txt)


def lancer_anonymisation_interface(texte, modele):
    if not texte or not texte.strip():
        return (
            "",
            "Veuillez entrer un texte.",
            "[]",
            "0 donnée détectée",
            None,
            None,
            "",
            score_confidentialite_html([]),
            "",
            dashboard_stats_html()
        )

    debut = time.time()

    try:
        detections_regex = detecter_regex(texte)
        detections_llm = detecter_llm(texte, modele)
        detections = fusionner_detections(detections_regex, detections_llm)

        texte_anonymise = anonymiser_texte(texte, detections)
        temps_execution = round(time.time() - debut, 2)

        json_detections = json.dumps(detections, ensure_ascii=False, indent=2)

        resume = (
            f"{len(detections)} donnée(s) détectée(s) "
            f"• Temps d’exécution : {temps_execution} sec"
        )

        fichier_txt, fichier_json = creer_fichiers_export_anonymisation(
            texte_anonymise=texte_anonymise,
            detections_json=json_detections
        )

        enregistrer_stats(
            type_traitement="anonymisation",
            modele=modele,
            temps_execution=temps_execution,
            exports=2
        )

        entree_historique = (
            f"{datetime.now().strftime('%H:%M:%S')} | "
            f"Anonymisation | "
            f"Modèle : {modele} | "
            f"{len(detections)} détection(s) | "
            f"{temps_execution} sec"
        )

        HISTORIQUE_ANONYMISATION.insert(0, entree_historique)
        historique_texte = "\n".join(HISTORIQUE_ANONYMISATION[:10])

        timeline = timeline_html(
            "Pipeline anonymisation terminé",
            [
                "Chargement du texte",
                "Détection Regex",
                "Analyse LLM locale",
                "Fusion des détections",
                "Génération du texte anonymisé",
                "Évaluation du risque confidentialité",
                "Création des exports TXT/JSON"
            ]
        )

        return (
            texte,
            texte_anonymise,
            json_detections,
            resume,
            fichier_txt,
            fichier_json,
            historique_texte,
            score_confidentialite_html(detections),
            timeline,
            dashboard_stats_html()
        )

    except Exception as erreur:
        return (
            "",
            f"Erreur : {erreur}",
            "[]",
            "Erreur",
            None,
            None,
            "",
            score_confidentialite_html([]),
            "",
            dashboard_stats_html()
        )


def charger_exemple_anonymisation():
    return EXEMPLE_ANONYMISATION


def charger_exemple_generation(tache):
    exemples = {
        "Résumé": EXEMPLE_RESUME,
        "Résumé intelligent": EXEMPLE_RESUME_INTELLIGENT,
        "Reformulation": EXEMPLE_REFORMULATION,
        "Email": EXEMPLE_EMAIL,
        "Compte rendu": EXEMPLE_COMPTE_RENDU,
        "Question / Réponse": EXEMPLE_QUESTION_REPONSE
    }

    return exemples.get(tache, "")


def lancer_generation_interface(tache, contenu, modele, ton, format_sortie):
    if not contenu or not contenu.strip():
        return "Veuillez entrer un contenu.", None, "", "", dashboard_stats_html()

    debut = time.time()
    intention_auto = detecter_intention_auto(contenu)

    if intention_auto is not None:
        tache = intention_auto

    try:
        prompt = construire_prompt_generation(tache, ton, format_sortie)
        resultat = generer(prompt, contenu, modele)

        temps_execution = round(time.time() - debut, 2)

        resultat_final = (
            f"{resultat}\n\n"
            f"---\n"
            f"Tâche : {tache}\n"
            f"Ton : {ton}\n"
            f"Format : {format_sortie}\n"
            f"Temps d’exécution : {temps_execution} sec"
        )

        fichier_export = creer_fichier_export_generation(
            resultat=resultat_final,
            tache=tache
        )

        enregistrer_stats(
            type_traitement="generation",
            modele=modele,
            temps_execution=temps_execution,
            exports=1
        )

        entree_historique = (
            f"{datetime.now().strftime('%H:%M:%S')} | "
            f"{tache} | "
            f"Ton : {ton} | "
            f"Modèle : {modele} | "
            f"{temps_execution} sec"
        )

        HISTORIQUE_GENERATION.insert(0, entree_historique)
        historique_texte = "\n".join(HISTORIQUE_GENERATION[:10])

        timeline = timeline_html(
            "Pipeline génération terminé",
            [
                "Identification de la tâche utilisateur",
                "Chargement du prompt adapté",
                "Application du ton et du format",
                "Appel du modèle local",
                "Génération du résultat",
                "Création de l’export TXT"
            ]
        )

        return (
            resultat_final,
            fichier_export,
            historique_texte,
            timeline,
            dashboard_stats_html()
        )

    except Exception as erreur:
        return f"Erreur : {erreur}", None, "", "", dashboard_stats_html()


def comparer_modeles_generation(tache, contenu, modeles_selectionnes):
    if not contenu or not contenu.strip():
        return [], "Veuillez entrer un contenu à comparer.", "", "", dashboard_stats_html()

    if not modeles_selectionnes:
        return [], "Veuillez sélectionner au moins un modèle.", "", "", dashboard_stats_html()

    lignes_tableau = []

    for modele in modeles_selectionnes:
        debut = time.time()

        try:
            prompt = construire_prompt_generation(
                tache=tache,
                ton="Professionnel",
                format_sortie="Structuré"
            )

            resultat = generer(prompt, contenu, modele)
            temps_execution = round(time.time() - debut, 2)

            apercu = resultat[:500].replace("\n", " ")
            if len(resultat) > 500:
                apercu += "..."

            lignes_tableau.append([
                modele,
                temps_execution,
                apercu
            ])

            enregistrer_stats(
                type_traitement="benchmark",
                modele=modele,
                temps_execution=temps_execution,
                exports=0
            )

            entree_historique = (
                f"{datetime.now().strftime('%H:%M:%S')} | "
                f"Benchmark | {tache} | "
                f"{modele} | {temps_execution} sec"
            )
            HISTORIQUE_BENCHMARK.insert(0, entree_historique)

        except Exception as erreur:
            lignes_tableau.append([
                modele,
                "Erreur",
                str(erreur)
            ])

    historique_texte = "\n".join(HISTORIQUE_BENCHMARK[:10])

    timeline = timeline_html(
        "Pipeline benchmark terminé",
        [
            "Chargement du prompt de comparaison",
            "Exécution séquentielle des modèles sélectionnés",
            "Mesure des temps d’exécution",
            "Génération du tableau comparatif",
            "Création du graphique benchmark"
        ]
    )

    valeurs_valides = []

    for ligne in lignes_tableau:
        try:
            valeurs_valides.append(
                (ligne[0], float(ligne[1]))
            )
        except Exception:
            pass

    if valeurs_valides:
        valeurs_valides.sort(key=lambda x: x[1])

        classement_html = """
        <div class="benchmark-bars">
        <h3>Classement automatique</h3>
        """

        emojis = ["🥇", "🥈", "🥉"]

        for i, (modele, temps) in enumerate(valeurs_valides[:3]):
            emoji = emojis[i] if i < len(emojis) else "🏅"

            classement_html += f"""
            <p>
            {emoji} <strong>{modele}</strong>
            — {temps} sec
            </p>
            """

        classement_html += "</div>"

    else:
        classement_html = ""

    return (
        lignes_tableau,
        historique_texte,
        benchmark_graph_html(lignes_tableau) + classement_html,
        timeline,
        dashboard_stats_html()
    )


with gr.Blocks(
    theme=gr.themes.Soft(primary_hue="indigo", neutral_hue="slate"),
    css=CUSTOM_CSS,
    title="Plateforme Agentique On-Premise"
) as app:

    gr.HTML("""
    <div class="hero">
        <h1>Plateforme Agentique On-Premise</h1>
        <p>Démonstration locale d’une plateforme multi-agents pour l’anonymisation de documents, la génération de texte et la comparaison de modèles locaux.</p>
        <span class="badge">100% local</span>
        <span class="badge">Ollama</span>
        <span class="badge">Docker</span>
        <span class="badge">Gradio</span>
        <span class="badge">LLM locaux</span>
        <span class="badge">Sans API cloud</span>
    </div>
    """)

    with gr.Tabs():

        with gr.Tab("Vue d’ensemble"):
            gr.Markdown("## Vue d’ensemble de la plateforme")
            gr.Markdown("Cette interface présente une plateforme agentique locale intégrant anonymisation, génération de texte, export de résultats, historique et benchmark multi-modèles.")
        with gr.Tab("Agent RAG"):
            gr.Markdown("## Agent RAG (Retrieval-Augmented Generation)")

            gr.Markdown(
                """
Posez une question.

L'agent recherche d'abord les informations dans la base documentaire locale
avant de générer une réponse avec le modèle local.
"""
            )

            question_rag = gr.Textbox(
                label="Votre question",
                lines=5,
                placeholder="Exemple : Quels modèles sont utilisés dans la plateforme ?"
            )

            modele_rag = gr.Dropdown(
                choices=MODELES_DISPONIBLES,
                value="mistral",
                label="Modèle"
            )

            bouton_rag = gr.Button(
                "Lancer le RAG",
                variant="primary"
            )

            reponse_rag = gr.Textbox(
                label="Réponse",
                lines=12
            )

            bouton_rag.click(
                fn=lancer_rag,
                inputs=[
                    question_rag,
                    modele_rag
                ],
                outputs=reponse_rag
            )
            gr.HTML("""
            <div class="creator-card">
                <strong>Projet réalisé par :</strong> Hajar JELTHI<br>
                <strong>Formation :</strong> L3 MIAGE — Université Paris Nanterre<br>
                <strong>Entreprise d’accueil :</strong> Novelis<br>
                <strong>Contexte :</strong> Stage en développement d’agents IA on-premise
            </div>
            """)

            dashboard_stats = gr.HTML(dashboard_stats_html())

            gr.HTML("""
            <div style="
            background: linear-gradient(135deg,#052e16,#166534);
            border:1px solid #22c55e;
            padding:14px;
            border-radius:16px;
            margin-bottom:18px;
            color:white;
            font-weight:bold;
            box-shadow:0 10px 25px rgba(0,0,0,0.2);
            ">
            🟢 Docker actif &nbsp;&nbsp;
            🟢 Ollama connecté &nbsp;&nbsp;
            🟢 Modèles locaux disponibles
            </div>
            """)

            robot_output = gr.HTML(message_robot("accueil"))

            with gr.Row(elem_classes="robot-buttons"):
                btn_robot_anon = gr.Button("Conseil anonymisation")
                btn_robot_gen = gr.Button("Conseil génération")
                btn_robot_bench = gr.Button("Conseil benchmark")
                btn_robot_archi = gr.Button("Architecture locale")

            btn_robot_anon.click(
                fn=lambda: message_robot("anonymisation"),
                outputs=robot_output
            )

            btn_robot_gen.click(
                fn=lambda: message_robot("generation"),
                outputs=robot_output
            )

            btn_robot_bench.click(
                fn=lambda: message_robot("benchmark"),
                outputs=robot_output
            )

            btn_robot_archi.click(
                fn=lambda: message_robot("architecture"),
                outputs=robot_output
            )

            with gr.Row():
                gr.HTML("""
                <div class="overview-box">
                    <h3>Objectif</h3>
                    <p>Proposer une démonstration fonctionnelle d’une plateforme IA on-premise capable de traiter des documents sans envoyer de données vers le cloud.</p>
                </div>
                """)

                gr.HTML("""
                <div class="overview-box">
                    <h3>Cas d’usage</h3>
                    <p>Agents intégrés : anonymisation, génération de texte, question/réponse et benchmark multi-modèles.</p>
                </div>
                """)

                gr.HTML("""
                <div class="overview-box">
                    <h3>Valeur technique</h3>
                    <p>Architecture modulaire, modèles locaux via Ollama, orchestration LiteLLM, interface Gradio, exports, historique et packaging Docker.</p>
                </div>
                """)

            gr.Markdown("## Architecture simplifiée")

            gr.HTML("""
            <div class="architecture">
            Utilisateur<br>
            ↓<br>
            Interface Gradio<br>
            ↓<br>
            Agents IA : anonymisation / génération / question-réponse / benchmark<br>
            ↓<br>
            LiteLLM<br>
            ↓<br>
            Ollama<br>
            ↓<br>
            Modèles locaux : Mistral · Llama 3.2 · Phi3
            </div>
            """)

            gr.Markdown("## Scénario de démonstration")

            btn_scenario = gr.Button("Afficher le scénario recommandé", variant="primary")
            sortie_scenario = gr.Textbox(
                label="Déroulé de démonstration",
                lines=10,
                interactive=False
            )

            btn_scenario.click(
                fn=scenario_demo,
                outputs=sortie_scenario
            )
        with gr.Tab("Anonymisation de documents"):
            gr.Markdown("## Agent d’anonymisation")
            gr.Markdown("Importez un fichier `.txt` ou collez un texte contenant des données personnelles.")

            with gr.Row():
                with gr.Column(scale=1):
                    upload_fichier = gr.File(
                        label="Importer un fichier texte",
                        file_types=[".txt"]
                    )

                    texte_input = gr.Textbox(
                        label="Texte source",
                        placeholder="Collez ici un texte contenant un nom, un email, un téléphone ou une adresse...",
                        lines=12
                    )

                    with gr.Row():
                        btn_exemple_anon = gr.Button("Charger un exemple")
                        btn_anon = gr.Button("Lancer l’anonymisation", variant="primary")

                    modele_anon = gr.Dropdown(
                        choices=MODELES_DISPONIBLES,
                        value="llama3.2:3b",
                        label="Modèle local"
                    )

                    resume_detection = gr.Textbox(
                        label="Synthèse",
                        interactive=False
                    )

                    score_confidentialite = gr.HTML(score_confidentialite_html([]))

                    historique_anon = gr.Textbox(
                        label="Historique anonymisation",
                        lines=6,
                        interactive=False
                    )

                    timeline_anon = gr.HTML()

                with gr.Column(scale=1):
                    gr.Markdown("### Comparaison avant / après")

                    apercu_original = gr.Textbox(
                        label="Texte original",
                        lines=8,
                        interactive=False
                    )

                    texte_anonymise_output = gr.Textbox(
                        label="Texte anonymisé",
                        lines=12
                    )

                    detections_output = gr.Code(
                        label="Détections JSON",
                        language="json",
                        lines=10
                    )

                    export_txt = gr.File(
                        label="Télécharger le texte anonymisé"
                    )

                    export_json = gr.File(
                        label="Télécharger les détections JSON"
                    )

            upload_fichier.change(
                fn=charger_fichier,
                inputs=upload_fichier,
                outputs=texte_input
            )

            btn_exemple_anon.click(
                fn=charger_exemple_anonymisation,
                outputs=texte_input
            )

            btn_anon.click(
                fn=lancer_anonymisation_interface,
                inputs=[texte_input, modele_anon],
                outputs=[
                    apercu_original,
                    texte_anonymise_output,
                    detections_output,
                    resume_detection,
                    export_txt,
                    export_json,
                    historique_anon,
                    score_confidentialite,
                    timeline_anon,
                    dashboard_stats
                ]
            )

        with gr.Tab("Génération de texte"):
            gr.Markdown("## Agent de génération enrichie")
            gr.Markdown("Choisissez une tâche, un ton et un format de sortie. Le module peut aussi répondre à une question simple, comme un assistant IA local.")

            gr.HTML(generation_help_html())

            with gr.Row():
                with gr.Column(scale=1):
                    tache_input = gr.Dropdown(
                        choices=[
                            "Résumé",
                            "Résumé intelligent",
                            "Reformulation",
                            "Email",
                            "Compte rendu",
                            "Question / Réponse"
                        ],
                        value="Résumé",
                        label="Type de génération"
                    )

                    ton_input = gr.Dropdown(
                        choices=[
                            "Professionnel",
                            "Simple",
                            "Technique",
                            "Synthétique",
                            "Pédagogique"
                        ],
                        value="Professionnel",
                        label="Ton de réponse"
                    )

                    format_input = gr.Dropdown(
                        choices=[
                            "Structuré",
                            "Court",
                            "Détaillé",
                            "Bullet points",
                            "Réponse directe"
                        ],
                        value="Structuré",
                        label="Format de sortie"
                    )

                    contenu_input = gr.Textbox(
                        label="Contenu source ou question",
                        placeholder="Exemple : C’est quoi la capitale de la France ?",
                        lines=12
                    )

                    with gr.Row():
                        btn_exemple_gen = gr.Button("Charger un exemple")
                        btn_gen = gr.Button("Générer", variant="primary")

                    modele_gen = gr.Dropdown(
                        choices=MODELES_DISPONIBLES,
                        value="llama3.2:3b",
                        label="Modèle local"
                    )

                    historique_gen = gr.Textbox(
                        label="Historique génération",
                        lines=6,
                        interactive=False
                    )

                    timeline_gen = gr.HTML()

                with gr.Column(scale=1):
                    resultat_gen = gr.Textbox(
                        label="Résultat généré",
                        lines=18
                    )

                    export_generation = gr.File(
                        label="Télécharger le résultat généré"
                    )

            btn_exemple_gen.click(
                fn=charger_exemple_generation,
                inputs=tache_input,
                outputs=contenu_input
            )

            btn_gen.click(
                fn=lancer_generation_interface,
                inputs=[
                    tache_input,
                    contenu_input,
                    modele_gen,
                    ton_input,
                    format_input
                ],
                outputs=[
                    resultat_gen,
                    export_generation,
                    historique_gen,
                    timeline_gen,
                    dashboard_stats
                ]
            )

        with gr.Tab("Comparaison multi-modèles"):
            gr.Markdown("## Benchmark interactif multi-modèles")
            gr.Markdown("Comparez plusieurs modèles locaux sur une même tâche de génération.")

            with gr.Row():
                with gr.Column(scale=1):
                    benchmark_tache = gr.Dropdown(
                        choices=[
                            "Résumé",
                            "Résumé intelligent",
                            "Reformulation",
                            "Email",
                            "Compte rendu",
                            "Question / Réponse"
                        ],
                        value="Résumé",
                        label="Tâche à comparer"
                    )

                    benchmark_contenu = gr.Textbox(
                        label="Contenu source",
                        placeholder="Collez ici le texte utilisé pour comparer les modèles...",
                        lines=12
                    )

                    benchmark_modeles = gr.CheckboxGroup(
                        choices=MODELES_DISPONIBLES,
                        value=["llama3.2:3b"],
                        label="Modèles à comparer"
                    )

                    with gr.Row():
                        btn_exemple_benchmark = gr.Button("Charger un exemple")
                        btn_benchmark = gr.Button("Comparer les modèles", variant="primary")

                    historique_benchmark = gr.Textbox(
                        label="Historique benchmark",
                        lines=6,
                        interactive=False
                    )

                    timeline_benchmark = gr.HTML()

                with gr.Column(scale=1):
                    tableau_benchmark = gr.Dataframe(
                        headers=["Modèle", "Temps d’exécution (sec)", "Aperçu du résultat"],
                        datatype=["str", "str", "str"],
                        label="Résultats de comparaison"
                    )

                    graphique_benchmark = gr.HTML()

            btn_exemple_benchmark.click(
                fn=charger_exemple_generation,
                inputs=benchmark_tache,
                outputs=benchmark_contenu
            )

            btn_benchmark.click(
                fn=comparer_modeles_generation,
                inputs=[
                    benchmark_tache,
                    benchmark_contenu,
                    benchmark_modeles
                ],
                outputs=[
                    tableau_benchmark,
                    historique_benchmark,
                    graphique_benchmark,
                    timeline_benchmark,
                    dashboard_stats
                ]
            )

    gr.HTML("""
    <div class="footer">
        Plateforme locale — Python · Ollama · LiteLLM · Smolagents · Gradio · Docker
    </div>
    """)


app.launch(
    server_name="0.0.0.0",
    server_port=7860
)