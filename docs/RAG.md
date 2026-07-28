# Agent RAG — Architecture et mode d'emploi

Cette documentation décrit l'architecture Retrieval-Augmented Generation (RAG) implémentée dans ce dépôt, comment l'agent a été conçu et comment le tester localement.

## Objectif
Fournir des réponses factuelles ancrées sur une base documentaire locale afin de réduire les hallucinations et d'assurer la confidentialité (tout est exécuté en local).

## Composants principaux
- `agents/agentRaG.py` : implémentation de l'agent RAG.
  - `lire_document_base()` : lit tous les fichiers `.txt` du dossier `base_connaissance/` et retourne un grand texte concaténé.
  - `rechercher_contexte(question)` : recherche par correspondance de mots le(s) paragraphe(s) les plus pertinents. Méthode simple et déterministe (score = nombre de mots communs).
  - `lire_prompt_rag()` : lit le prompt depuis `prompts/prompt_rag.txt` pour séparer le texte de consignes du code.  
  - `creer_modele(nom_modele)` : construit un objet `LiteLLMModel` (smolagents) pointant vers Ollama (via `OLLAMA_BASE_URL` dans `config.py`).  
  - `lancer_rag(question, modele)` : assemble un prompt avec le contexte retenu, la question, et appelle le modèle pour générer la réponse. La fonction retourne la réponse et le contexte utilisé.  
  - `interface/app.py` : UI Gradio. Un onglet `Agent RAG` permet de poser une question, afficher le contexte retenu et obtenir la réponse.
- `config.py` : contient `OLLAMA_BASE_URL`, `TIMEOUT`, `MODELES_DISPONIBLES`.

## Flux RAG (haut niveau)
1. Ingestion : déposer/des fichiers `.txt` dans `base_connaissance/`.
2. Retrieval : `rechercher_contexte` calcule le paragraphe le plus pertinent par correspondance lexicale.
3. Prompting : le paragraphe sélectionné est inséré dans un template de prompt qui demande explicitement au modèle de n'utiliser que ce contexte.
4. Generation : appel au LLM local via LiteLLMModel → Ollama → modèle local.
5. Fallback : si aucun contexte pertinent n'est trouvé, l'agent renvoie un message clair ("Je ne trouve pas cette information dans la base documentaire.").

## Limites et améliorations recommandées
- Limites actuelles :
  - Recherche lexicale simple (ne retrouve pas bien les synonymes ou paraphrases).
  - Pas d'index vectoriel ni de reranking.
  - Pas de pagination ni chunking optimisé pour les gros documents.

- Améliorations possibles :
  1. Index vectoriel (FAISS, Chroma, Milvus) + embeddings pour retrieval sémantique.
  2. Chunking + overlap pour mieux couvrir les passages longs.
  3. Reranker (BM25 ou modèle léger) avant d'envoyer le contexte au LLM.
  4. Exposer la source / extrait retourné pour traçabilité.
  5. Tests automatisés e2e et monitoring (latence, erreurs modèle).

## Commandes pour exécuter localement
Pré-requis : Docker et Docker Compose, Ollama (ou service LLM accessible via `config.OLLAMA_BASE_URL`).

1. Construire et démarrer (depuis la racine du repo) :

```powershell
docker compose up -d --build
```

2. Ouvrir l'interface Gradio :

- http://localhost:7860

3. Tester RAG :
- Placer des fichiers `.txt` dans `base_connaissance/` (ex. `base_connaissance/guide_produit.txt`).
- Aller dans l'onglet "Agent RAG", poser une question présente dans la base documentaire et lancer.

## Fichier important à lire pour l'entretien
- `agents/agentRaG.py` : c'est le coeur — montrez `rechercher_contexte` et `lancer_rag`.
- `interface/app.py` : montrer l'onglet RAG, expliquer comment l'UI appelle l'agent (bouton.click)

## Script de démonstration rapide (PowerShell)
Contenu du script `demo/run_demo.ps1` :

```powershell
# Lance le stack et ouvre le navigateur sur l'UI
cd "$(Split-Path -Parent $MyInvocation.MyCommand.Definition)"\..\
docker compose up -d --build
Start-Sleep -s 3
Start-Process "http://localhost:7860"
Write-Output "Gradio should be available at http://localhost:7860"
```

## Texte d'explication à dire pendant l'entretien
- "J'ai implémenté un agent RAG simple et reproductible. Les documents sont stockés en local dans `base_connaissance/`. L'agent recherche le paragraphe le plus pertinent par correspondance de mots, puis assemble un prompt où il est explicitement demandé au modèle de n'utiliser que ce contexte. Le modèle local est appelé via LiteLLM/Ollama. Cette approche permet de contrôler les données (on-prem), mais pour la production je recommanderais d'ajouter un index vectoriel, chunking et un reranker avant le LLM pour fiabiliser la récupération sémantique."

---

Si tu veux, je peux aussi :
- ajouter un exemple `base_connaissance/exemple.txt` et commit le tout ;
- créer la PR automatiquement (si le remote est configuré) ;
- générer un petit fichier `docs/CHANGELOG.md` résumant ce que j'ai modifié dans cet exercice.

Dis-moi si tu veux que je pousse ces fichiers maintenant sur GitHub (git push).