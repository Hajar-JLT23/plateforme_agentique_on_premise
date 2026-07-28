# config.py — Configuration centralisée
import os

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://host.docker.internal:11434")

TIMEOUT = int(os.getenv("TIMEOUT", "180"))

MODELES_DISPONIBLES = [
    "mistral",
    "llama3.2:3b",
    "phi3:mini"
]

MODELE_PAR_DEFAUT = os.getenv("MODELE_PAR_DEFAUT", "mistral")

DOSSIER_DATA = "data"

DOSSIER_PROMPTS = "prompts"

DOSSIER_RESULTATS = "resultats"