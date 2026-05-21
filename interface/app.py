import sys
import json
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
    background: linear-gradient(135deg, #0f172a, #312e81, #4f46e5);
    padding: 36px;
    border-radius: 22px;
    color: white;
    margin-bottom: 24px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.28);
}

.hero h1 {
    font-size: 40px;
    margin-bottom: 8px;
}

.hero p {
    font-size: 17px;
    opacity: 0.95;
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

.metric-card {
    background: linear-gradient(135deg, #111827, #1f2937);
    border: 1px solid #374151;
    border-radius: 18px;
    padding: 18px;
    min-height: 120px;
    box-shadow: 0 12px 30px rgba(0,0,0,0.18);
}

.metric-card h3 {
    margin-bottom: 6px;
    color: #a5b4fc;
}

.metric-card p {
    color: #d1d5db;
    font-size: 14px;
}

.section-title {
    font-size: 22px;
    font-weight: 800;
    margin-top: 16px;
    margin-bottom: 8px;
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


def lancer_anonymisation_interface(texte, modele):
    if not texte.strip():
        return "Veuillez entrer un texte.", "[]", "0 donnée détectée"

    try:
        detections_regex = detecter_regex(texte)
        detections_llm = detecter_llm(texte, modele)
        detections = fusionner_detections(detections_regex, detections_llm)

        texte_anonymise = anonymiser_texte(texte, detections)

        json_detections = json.dumps(detections, ensure_ascii=False, indent=2)
        resume = f"{len(detections)} donnée(s) détectée(s)"

        return texte_anonymise, json_detections, resume

    except Exception as erreur:
        return f"Erreur : {erreur}", "[]", "Erreur"


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
    if not contenu.strip():
        return "Veuillez entrer un contenu."

    prompts = {
        "Résumé": "prompt_resume.txt",
        "Reformulation": "prompt_reformulation.txt",
        "Email": "prompt_email.txt",
        "Compte rendu": "prompt_compte_rendu.txt"
    }

    try:
        prompt = lire_fichier(Path("prompts") / prompts[tache])
        resultat = generer(prompt, contenu, modele)
        return resultat

    except Exception as erreur:
        return f"Erreur : {erreur}"


with gr.Blocks(
    theme=gr.themes.Soft(primary_hue="indigo", neutral_hue="slate"),
    css=CUSTOM_CSS,
    title="Plateforme Agentique On-Premise"
) as app:

    gr.HTML("""
    <div class="hero">
        <h1>Plateforme Agentique On-Premise</h1>
        <p>Démonstration locale d’une plateforme multi-agents pour l’anonymisation de documents et la génération automatique de texte.</p>
        <span class="badge">100% local</span>
        <span class="badge">Ollama</span>
        <span class="badge">Docker</span>
        <span class="badge">Gradio</span>
        <span class="badge">LLM locaux</span>
    </div>
    """)

    with gr.Row():
        gr.HTML("""
        <div class="metric-card">
            <h3>Agent anonymisation</h3>
            <p>Détection hybride Regex + LLM pour masquer les informations personnelles dans des documents texte.</p>
        </div>
        """)
        gr.HTML("""
        <div class="metric-card">
            <h3>Agent génération</h3>
            <p>Résumé, reformulation professionnelle, email et compte rendu structuré à partir d’un brief utilisateur.</p>
        </div>
        """)
        gr.HTML("""
        <div class="metric-card">
            <h3>Infrastructure locale</h3>
            <p>Exécution on-premise via Docker, Ollama, LiteLLM et Smolagents, sans API cloud externe.</p>
        </div>
        """)

    with gr.Tabs():

        with gr.Tab("Anonymisation de documents"):
            gr.Markdown("## Agent d’anonymisation")
            gr.Markdown("Collez un texte contenant des données personnelles, puis lancez la détection et le masquage automatique.")

            with gr.Row():
                with gr.Column(scale=1):
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

            btn_exemple_anon.click(
                fn=charger_exemple_anonymisation,
                outputs=texte_input
            )

            btn_anon.click(
                fn=lancer_anonymisation_interface,
                inputs=[texte_input, modele_anon],
                outputs=[texte_anonymise_output, detections_output, resume_detection]
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

                with gr.Column(scale=1):
                    resultat_gen = gr.Textbox(
                        label="Résultat généré",
                        lines=18
                    )

            btn_exemple_gen.click(
                fn=charger_exemple_generation,
                inputs=tache_input,
                outputs=contenu_input
            )

            btn_gen.click(
                fn=lancer_generation_interface,
                inputs=[tache_input, contenu_input, modele_gen],
                outputs=resultat_gen
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