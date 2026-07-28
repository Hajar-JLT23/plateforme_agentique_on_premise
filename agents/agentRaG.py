from pathlib import Path
import re
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
        for fichier in sorted(dossier.glob("*.txt")):
            with open(fichier, "r", encoding="utf-8") as f:
                textes.append(f.read())

        return "\n\n".join(textes)

    alt = Path("data") / "base_connaissance.txt"
    if alt.exists():
        try:
            return alt.read_text(encoding="utf-8")
        except Exception:
            return ""

    return ""


def normaliser_texte(texte):
    texte = texte.lower()
    texte = re.sub(r"[^a-z0-9àâäéèêëîïôöùûüç\s]", " ", texte)
    texte = re.sub(r"\s+", " ", texte).strip()
    return texte


def extraire_mots(texte):
    mots = normaliser_texte(texte).split()
    stopwords = {
        "le", "la", "les", "un", "une", "des", "et", "ou", "de", "du", "dans", "sur",
        "a", "au", "aux", "pour", "par", "avec", "sans", "ce", "cette", "cet", "ces",
        "que", "qui", "dont", "où", "est", "sont", "ne", "pas", "en", "se", "sa",
        "son", "ses", "mon", "ton", "son", "leur", "nos", "vos", "ils", "elles",
        "ceci", "cela", "ici", "là", "bien", "très", "plus", "moins", "comme", "mais",
        "si", "quand", "donc", "aussi", "ou", "on"
    }
    return [mot for mot in mots if mot and mot not in stopwords]


def lire_prompt_rag():
    prompt_path = Path(__file__).parent.parent / "prompts" / "prompt_rag.txt"
    if prompt_path.exists():
        try:
            return prompt_path.read_text(encoding="utf-8")
        except Exception:
            return "Tu es un assistant IA spécialisé dans la plateforme Agentique On-Premise."

    return "Tu es un assistant IA spécialisé dans la plateforme Agentique On-Premise."


def rechercher_contexte(question):
    base = lire_document_base()
    if not base.strip():
        return ""

    paragraphes = [p.strip() for p in base.split("\n\n") if p.strip()]
    question_mots = set(extraire_mots(question))

    meilleur = ""
    score = 0

    for paragraphe in paragraphes:
        texte_mots = set(extraire_mots(paragraphe))
        nb = len(question_mots & texte_mots)

        if nb > score:
            score = nb
            meilleur = paragraphe

    return meilleur


def lancer_rag(question, modele):
    contexte = rechercher_contexte(question)
    prompt_systeme = lire_prompt_rag()

    if not contexte:
        return (
            "Je ne dispose pas de cette information dans la base documentaire.",
            ""
        )

    prompt = f"""
{prompt_systeme}

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
    return reponse.content, contexte