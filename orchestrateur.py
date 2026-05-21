from config import MODELES_DISPONIBLES
from agents.agent_anonymisation import lancer_anonymisation
from agents.agent_generation import lancer_generation


def afficher_banniere():
    print("\n" + "=" * 60)
    print("        PLATEFORME AGENTIQUE ON-PREMISE")
    print("=" * 60)


def choisir_modele():
    print("\nModèles disponibles :")

    for i, modele in enumerate(MODELES_DISPONIBLES, start=1):
        print(f"{i} — {modele}")

    try:
        choix = int(input("\nChoisissez un modèle (numéro) : ").strip())

        if 1 <= choix <= len(MODELES_DISPONIBLES):
            return MODELES_DISPONIBLES[choix - 1]

        print("Numéro invalide.")
        return None

    except ValueError:
        print("Entrée invalide.")
        return None


def lancer_plateforme():

    afficher_banniere()

    print("\nQuel cas d'usage voulez-vous lancer ?")
    print("1 — Anonymisation de documents")
    print("2 — Génération de texte")
    print("3 — Les deux")

    choix = input("\nVotre choix (1/2/3) : ").strip()

    modele = choisir_modele()

    if modele is None:
        return

    print(f"\nModèle sélectionné : {modele}")

    if choix == "1":

        lancer_anonymisation(modele)

    elif choix == "2":

        lancer_generation(modele)

    elif choix == "3":

        print("\n--- Lancement agent anonymisation ---")
        lancer_anonymisation(modele)

        print("\n--- Lancement agent génération ---")
        lancer_generation(modele)

    else:
        print("Choix invalide.")


if __name__ == "__main__":
    lancer_plateforme()