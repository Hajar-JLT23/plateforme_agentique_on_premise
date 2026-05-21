from pathlib import Path
import sys

from smolagents import LiteLLMModel
from smolagents.models import ChatMessage

sys.path.append(str(Path(__file__).parent.parent))

from config import (
    OLLAMA_BASE_URL,
    TIMEOUT,
    DOSSIER_PROMPTS,
    DOSSIER_DATA,
    DOSSIER_RESULTATS,
    MODELE_PAR_DEFAUT
)


def creer_modele(nom_modele):
    return LiteLLMModel(
        model_id=f"ollama/{nom_modele}",
        api_base=OLLAMA_BASE_URL,
        request_timeout=TIMEOUT
    )


def lire_fichier(chemin):
    with open(chemin, "r", encoding="utf-8") as fichier:
        return fichier.read()


def sauvegarder_resultat(chemin, contenu):
    with open(chemin, "w", encoding="utf-8") as fichier:
        fichier.write(contenu)


def generer(prompt_systeme, contenu, nom_modele):
    modele = creer_modele(nom_modele)

    message_complet = f"{prompt_systeme}\n\n{contenu}"

    messages = [
        ChatMessage(
            role="user",
            content=[{"type": "text", "text": message_complet}]
        )
    ]

    reponse = modele(messages)

    return reponse.content


TACHES = [
    {
        "nom": "resume",
        "prompt_fichier": "prompt_resume.txt",
        "data_fichier": "document_resume.txt",
        "output_fichier": "generation_resume_output.txt"
    },
    {
        "nom": "reformulation",
        "prompt_fichier": "prompt_reformulation.txt",
        "data_fichier": "reformulation.txt",
        "output_fichier": "generation_reformulation_output.txt"
    },
    {
        "nom": "email",
        "prompt_fichier": "prompt_email.txt",
        "data_fichier": "email_brief.txt",
        "output_fichier": "generation_email_output.txt"
    },
    {
        "nom": "compte_rendu",
        "prompt_fichier": "prompt_compte_rendu.txt",
        "data_fichier": "notes_reunion.txt",
        "output_fichier": "generation_compte_rendu_output.txt"
    }
]


def lancer_generation(nom_modele=MODELE_PAR_DEFAUT):

    dossier_resultats = Path(DOSSIER_RESULTATS)
    dossier_resultats.mkdir(exist_ok=True)

    for tache in TACHES:

        print("\n" + "=" * 60)
        print(f"TÂCHE : {tache['nom']}")
        print(f"MODELE : {nom_modele}")
        print("=" * 60)

        try:
            prompt = lire_fichier(
                Path(DOSSIER_PROMPTS) / tache["prompt_fichier"]
            )

            contenu = lire_fichier(
                Path(DOSSIER_DATA) / tache["data_fichier"]
            )

            resultat = generer(
                prompt_systeme=prompt,
                contenu=contenu,
                nom_modele=nom_modele
            )

            print(resultat)

            chemin_sortie = (
                dossier_resultats / tache["output_fichier"]
            )

            sauvegarder_resultat(
                chemin_sortie,
                resultat
            )

            print(f"\nRésultat sauvegardé : {chemin_sortie}")

        except Exception as erreur:
            print(f"ERREUR : {erreur}")


if __name__ == "__main__":
    lancer_generation()