import json
import re
from pathlib import Path
import sys

from smolagents import LiteLLMModel
from smolagents.models import ChatMessage

sys.path.append(str(Path(__file__).parent.parent))

from config import (
    OLLAMA_BASE_URL,
    TIMEOUT,
    DOSSIER_DATA,
    DOSSIER_PROMPTS,
    DOSSIER_RESULTATS,
    MODELE_PAR_DEFAUT
)

TYPES_LLM_AUTORISES = {"NOM", "ADRESSE"}
def est_adresse_valide(texte):
    texte_min = texte.lower()

    mots_adresse = [
        "rue",
        "avenue",
        "boulevard",
        "bd",
        "place",
        "impasse",
        "chemin"
    ]

    contient_numero = any(caractere.isdigit() for caractere in texte_min)
    contient_mot_adresse = any(mot in texte_min for mot in mots_adresse)

    return contient_numero and contient_mot_adresse


def creer_modele(nom_modele):
    return LiteLLMModel(
        model_id=f"ollama/{nom_modele}",
        api_base=OLLAMA_BASE_URL,
        request_timeout=TIMEOUT
    )


def lire_fichier(chemin):
    with open(chemin, "r", encoding="utf-8") as fichier:
        return fichier.read()


def sauvegarder_fichier(chemin, contenu):
    with open(chemin, "w", encoding="utf-8") as fichier:
        fichier.write(contenu)


def detecter_regex(texte):
    detections = []

    patterns = {
        "EMAIL": r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        "TELEPHONE": r"(?<!\d)(?:\+33\s?|0)[1-9](?:[\s.-]?\d{2}){4}(?!\d)",
        "DATE": r"\b\d{2}/\d{2}/\d{4}\b",
        "NUMERO_SECURITE_SOCIALE": r"(?<!\d)[12]\d{12}(?!\d)",
        "ADRESSE": r"\b\d+\s+(?:rue|avenue|boulevard|bd|impasse|place|chemin)\s+[A-Za-zÀ-ÿ'\-\s]+(?:,\s*\d{5}\s+[A-Za-zÀ-ÿ'\-\s]+| à [A-Za-zÀ-ÿ'\-\s]+)?",
    }

    for type_pii, pattern in patterns.items():
        for match in re.finditer(pattern, texte):
            detections.append({
                "text": match.group(),
                "type": type_pii
            })

    return detections


def nettoyer_reponse_llm(reponse):
    reponse = reponse.strip()

    if reponse.startswith("```"):
        reponse = reponse.replace("```json", "").replace("```", "").strip()

    try:
        donnees = json.loads(reponse)
    except json.JSONDecodeError:
        return []

    if not isinstance(donnees, list):
        return []

    detections = []

    for item in donnees:
        if isinstance(item, list):
            for sous_item in item:
                if isinstance(sous_item, dict):
                    texte = sous_item.get("text")
                    type_pii = sous_item.get("type")

                    if texte and type_pii in TYPES_LLM_AUTORISES:
                        texte =  texte.strip()
                        if type_pii == "ADRESSE" and not est_adresse_valide(texte):
                            continue 
                        detections.append({
                            "text": texte,
                            "type": type_pii
                        })
                            
                            
                    

        elif isinstance(item, dict):
            texte = item.get("text")
            type_pii = item.get("type")

            if texte and type_pii in TYPES_LLM_AUTORISES:

                texte = texte.strip()

                if type_pii == "ADRESSE" and not est_adresse_valide(texte):
                 continue

                detections.append({
                 "text": texte,
                 "type": type_pii
    })
    
                
                    
                

    return detections


def detecter_llm(texte, nom_modele):

    modele = creer_modele(nom_modele)

    prompt_systeme = lire_fichier(
        Path(DOSSIER_PROMPTS) / "prompt_anonymisation.txt"
    )

    prompt = f"""
{prompt_systeme}

Document :
{texte}
"""

    messages = [
        ChatMessage(
            role="user",
            content=[{"type": "text", "text": prompt}]
        )
    ]

    reponse = modele(messages)

    return nettoyer_reponse_llm(reponse.content)


def fusionner_detections(detections_regex, detections_llm):
    toutes_detections = detections_regex + detections_llm

    detections_uniques = []
    deja_vus = set()

    for detection in toutes_detections:
        cle = (detection["text"].strip(), detection["type"])
        detection["text"] = detection["text"].strip()

        if cle not in deja_vus:
            detections_uniques.append(detection)
            deja_vus.add(cle)

    return detections_uniques


def anonymiser_texte(texte, detections):
    texte_anonymise = texte

    detections_triees = sorted(
        detections,
        key=lambda x: len(x["text"]),
        reverse=True
    )

    for detection in detections_triees:
        valeur = detection["text"]
        type_pii = detection["type"]
        texte_anonymise = texte_anonymise.replace(valeur, f"[{type_pii}]")

    return texte_anonymise


def traiter_document(chemin_fichier, nom_modele):
    texte = lire_fichier(chemin_fichier)

    detections_regex = detecter_regex(texte)
    detections_llm = detecter_llm(texte, nom_modele)

    detections = fusionner_detections(detections_regex, detections_llm)

    texte_anonymise = anonymiser_texte(texte, detections)

    dossier_resultats = Path(DOSSIER_RESULTATS)
    dossier_resultats.mkdir(exist_ok=True)

    nom_base = chemin_fichier.stem

    fichier_sortie_txt = dossier_resultats / f"{nom_base}_anonymise.txt"
    fichier_sortie_json = dossier_resultats / f"{nom_base}_detections.json"

    sauvegarder_fichier(fichier_sortie_txt, texte_anonymise)

    with open(fichier_sortie_json, "w", encoding="utf-8") as fichier:
        json.dump(detections, fichier, ensure_ascii=False, indent=2)

    return texte_anonymise, detections


def lancer_anonymisation(nom_modele=MODELE_PAR_DEFAUT):
    dossier_data = Path(DOSSIER_DATA)

    fichiers = sorted(dossier_data.glob("anonymisation_*.txt"))

    if not fichiers:
        fichiers = sorted(dossier_data.glob("doc*.txt"))

    if not fichiers:
        print("Aucun fichier d'anonymisation trouvé dans le dossier data.")
        return

    for fichier in fichiers:
        print("\n" + "=" * 60)
        print(f"DOCUMENT : {fichier.name}")
        print(f"MODELE : {nom_modele}")
        print("=" * 60)

        try:
            texte_anonymise, detections = traiter_document(fichier, nom_modele)

            print("\nDétections :")
            print(json.dumps(detections, ensure_ascii=False, indent=2))

            print("\nTexte anonymisé :")
            print(texte_anonymise)

        except Exception as erreur:
            print(f"ERREUR : {erreur}")


if __name__ == "__main__":
    lancer_anonymisation()