import sys
import json
import time
from datetime import datetime
from pathlib import Path

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

.metric-card {
    background: linear-gradient(135deg, #111827, #1f2937);
    border: 1px solid #374151;
    border-radius: 18px;
    padding: 18px;
    min-height: 120px;
    box-shadow: 0 12px 30px rgba(0,0,0,0.18);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.metric-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 18px 40px rgba(0,0,0,0.28);
}

.metric-card h3 {
    margin-bottom: 6px;
    color: #a5b4fc;
}

.metric-card p {
    color: #d1d5db;
    font-size: 14px;
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


HISTORIQUE_ANONYMISATION = []
HISTORIQUE_GENERATION = []
HISTORIQUE_BENCHMARK = []


def charger_fichier(fichier):
    if fichier is None:
        return ""

    with open(fichier.name, "r", encoding="utf-8") as f:
        return f.read()


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
                <h3>Module génération</h3>
                <p>Choisissez une tâche : résumé, reformulation, email ou compte rendu. Le modèle local génère un résultat professionnel avec historique et export du fichier généré.</p>
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
7. Tester un résumé, une reformulation, un email ou un compte rendu.
8. Ouvrir l’onglet Comparaison multi-modèles.
9. Comparer les temps d’exécution et la qualité des modèles locaux.
"""


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

    nom_tache = tache.lower().replace(" ", "_")
    fichier_txt = dossier_export / f"generation_{nom_tache}_export.txt"

    fichier_txt.write_text(resultat, encoding="utf-8")

    return str(fichier_txt)


def lancer_anonymisation_interface(texte, modele):
    if not texte or not texte.strip():
        return "Veuillez entrer un texte.", "[]", "0 donnée détectée", None, None, ""

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

        entree_historique = (
            f"{datetime.now().strftime('%H:%M:%S')} | "
            f"Anonymisation | "
            f"Modèle : {modele} | "
            f"{len(detections)} détection(s) | "
            f"{temps_execution} sec"
        )

        HISTORIQUE_ANONYMISATION.insert(0, entree_historique)
        historique_texte = "\n".join(HISTORIQUE_ANONYMISATION[:10])

        return (
            texte_anonymise,
            json_detections,
            resume,
            fichier_txt,
            fichier_json,
            historique_texte
        )

    except Exception as erreur:
        return f"Erreur : {erreur}", "[]", "Erreur", None, None, ""


def charger_exemple_anonymisation():
    return EXEMPLE_ANONYMISATION


def charger_exemple_generation(tache):
    exemples = {
        "Résumé": EXEMPLE_RESUME,
        "Reformulation": EXEMPLE_REFORMULATION,
        "Email": EXEMPLE_EMAIL,
        "Compte rendu": EXEMPLE_COMPTE_RENDU
    }

    return exemples.get(tache, "")


def lancer_generation_interface(tache, contenu, modele):
    if not contenu or not contenu.strip():
        return "Veuillez entrer un contenu.", None, ""

    debut = time.time()

    prompts = {
        "Résumé": "prompt_resume.txt",
        "Reformulation": "prompt_reformulation.txt",
        "Email": "prompt_email.txt",
        "Compte rendu": "prompt_compte_rendu.txt"
    }

    try:
        prompt = lire_fichier(Path("prompts") / prompts[tache])
        resultat = generer(prompt, contenu, modele)

        temps_execution = round(time.time() - debut, 2)

        resultat_final = (
            f"{resultat}\n\n"
            f"---\n"
            f"Temps d’exécution : {temps_execution} sec"
        )

        fichier_export = creer_fichier_export_generation(
            resultat=resultat_final,
            tache=tache
        )

        entree_historique = (
            f"{datetime.now().strftime('%H:%M:%S')} | "
            f"{tache} | "
            f"Modèle : {modele} | "
            f"{temps_execution} sec"
        )

        HISTORIQUE_GENERATION.insert(0, entree_historique)
        historique_texte = "\n".join(HISTORIQUE_GENERATION[:10])

        return resultat_final, fichier_export, historique_texte

    except Exception as erreur:
        return f"Erreur : {erreur}", None, ""


def comparer_modeles_generation(tache, contenu, modeles_selectionnes):
    if not contenu or not contenu.strip():
        return [], "Veuillez entrer un contenu à comparer."

    if not modeles_selectionnes:
        return [], "Veuillez sélectionner au moins un modèle."

    prompts = {
        "Résumé": "prompt_resume.txt",
        "Reformulation": "prompt_reformulation.txt",
        "Email": "prompt_email.txt",
        "Compte rendu": "prompt_compte_rendu.txt"
    }

    prompt = lire_fichier(Path("prompts") / prompts[tache])
    lignes_tableau = []

    for modele in modeles_selectionnes:
        debut = time.time()

        try:
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

    return lignes_tableau, historique_texte


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

            gr.HTML("""
            <div class="creator-card">
                <strong>Projet réalisé par :</strong> Hajar JELTHI<br>
                <strong>Formation :</strong> L3 MIAGE — Université Paris Nanterre<br>
                <strong>Entreprise d’accueil :</strong> Novelis<br>
                <strong>Contexte :</strong> Stage en développement d’agents IA on-premise
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
                    <p>Deux agents principaux : un agent d’anonymisation des informations personnelles et un agent de génération de contenus professionnels.</p>
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
            Agents IA : anonymisation / génération / benchmark<br>
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

                    historique_anon = gr.Textbox(
                        label="Historique anonymisation",
                        lines=6,
                        interactive=False
                    )

                with gr.Column(scale=1):
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
                    texte_anonymise_output,
                    detections_output,
                    resume_detection,
                    export_txt,
                    export_json,
                    historique_anon
                ]
            )

        with gr.Tab("Génération de texte"):
            gr.Markdown("## Agent de génération")
            gr.Markdown("Choisissez une tâche, chargez un exemple ou collez votre propre contenu, puis générez un texte professionnel.")

            with gr.Row():
                with gr.Column(scale=1):
                    tache_input = gr.Dropdown(
                        choices=["Résumé", "Reformulation", "Email", "Compte rendu"],
                        value="Résumé",
                        label="Type de génération"
                    )

                    contenu_input = gr.Textbox(
                        label="Contenu source",
                        placeholder="Collez ici le texte, les notes ou le brief...",
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
                inputs=[tache_input, contenu_input, modele_gen],
                outputs=[
                    resultat_gen,
                    export_generation,
                    historique_gen
                ]
            )

        with gr.Tab("Comparaison multi-modèles"):
            gr.Markdown("## Benchmark interactif multi-modèles")
            gr.Markdown("Comparez plusieurs modèles locaux sur une même tâche de génération.")

            with gr.Row():
                with gr.Column(scale=1):
                    benchmark_tache = gr.Dropdown(
                        choices=["Résumé", "Reformulation", "Email", "Compte rendu"],
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

                with gr.Column(scale=1):
                    tableau_benchmark = gr.Dataframe(
                        headers=["Modèle", "Temps d’exécution (sec)", "Aperçu du résultat"],
                        datatype=["str", "str", "str"],
                        label="Résultats de comparaison"
                    )

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
                    historique_benchmark
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