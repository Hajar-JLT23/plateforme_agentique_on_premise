from pathlib import Path
import sys

from smolagents import LiteLLMModel
from smolagents.models import ChatMessage

sys.path.append(str(Path(__file__).parent.parent))

from config import (
    OLLAMA_BASE_URL,
    TIMEOUT
)


def creer_modele(nom_modele):
    return LiteLLMModel(
        model_id=f"ollama/{nom_modele}",
        api_base=OLLAMA_BASE_URL,
        request_timeout=TIMEOUT
    )


def lire_document_base():
    """Lit la base documentaire.
    Priorité : dossier 'base_connaissance/' contenant des fichiers .txt.
    Fallback : fichier unique 'data/base_connaissance.txt' si présent.
    Retourne une chaîne vide si aucune source n'est trouvée.
    """

    dossier = Path("base_connaissance")

    textes = []

    if dossier.exists() and any(dossier.glob("*.txt")):
        for fichier in dossier.glob("*.txt"):
            with open(fichier, "r", encoding="utf-8") as f:
                textes.append(f.read())

        return "\n\n".join(textes)

    # Fallback to a single file (some repos use data/base_connaissance.txt)
    alt = Path("data") / "base_connaissance.txt"
    if alt.exists():
        try:
            return alt.read_text(encoding="utf-8")
        except Exception:
            return ""

    return ""


def rechercher_contexte(question):

    base = lire_document_base()

    if base == "":
        return ""

    paragraphes = base.split("\n\n")

    question = question.lower()

    meilleur = ""

    score = 0

    mots = question.split()

    for paragraphe in paragraphes:

        nb = 0

        texte = paragraphe.lower()

        for mot in mots:

            if mot in texte:
                nb += 1

        if nb > score:
            score = nb
            meilleur = paragraphe

    return meilleur


def lancer_rag(question, modele):

    contexte = rechercher_contexte(question)

    prompt = f"""
Tu es un assistant IA.

Tu dois répondre uniquement avec les informations présentes dans le contexte.

Si le contexte ne contient pas la réponse,
réponds exactement :

Je ne trouve pas cette information dans la base documentaire.

Contexte :

{contexte}

Question :

{question}

Réponse :
"""

    llm = creer_modele(modele)

    messages = [
        ChatMessage(
            role="user",
            content=[
                {
                    "type": "text",
                    "text": prompt
                }
            ]
        )
    ]

    reponse = llm(messages)

    return reponse.content