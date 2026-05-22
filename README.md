# Plateforme Agentique On-Premise

## Présentation

Cette plateforme a été développée dans le cadre d’un stage chez **Novelis** autour des architectures agentiques locales basées sur des modèles de langage exécutés entièrement en local.

L’objectif principal est de proposer une plateforme IA modulaire capable de :

- anonymiser automatiquement des documents ;
- générer des contenus professionnels ;
- comparer plusieurs modèles locaux ;
- exécuter l’ensemble des traitements sans API cloud externe.

La plateforme repose exclusivement sur des modèles locaux exécutés via **Ollama**.

---

## Auteur

**Hajar JELTHI**  
L3 MIAGE — Université Paris Nanterre  
Stage Développement IA Agentique — Novelis

---

## Objectifs du projet

Le projet vise à consolider plusieurs cas d’usage IA dans une architecture agentique cohérente et industrialisable.

Objectifs :

- centraliser plusieurs agents IA dans une même plateforme ;
- travailler avec des modèles 100 % locaux ;
- éviter l’utilisation d’API cloud externes ;
- proposer une interface professionnelle de démonstration ;
- comparer les performances des modèles locaux ;
- préparer une architecture extensible pour de futurs agents.

---

## Fonctionnalités principales

### Agent d’anonymisation

L’agent d’anonymisation permet de détecter et masquer automatiquement des données sensibles présentes dans des documents texte.

Données détectées par Regex :

- emails ;
- numéros de téléphone ;
- dates ;
- numéros de sécurité sociale.

Données détectées par LLM :

- noms ;
- adresses.

Fonctionnalités :

- upload de fichiers `.txt` ;
- chargement automatique d’exemples ;
- anonymisation du contenu ;
- affichage JSON des détections ;
- export TXT ;
- export JSON ;
- historique des traitements ;
- mesure du temps d’exécution.

---

### Agent de génération de texte

L’agent de génération permet de produire automatiquement des contenus professionnels à partir d’un brief utilisateur.

Tâches supportées :

- résumé documentaire ;
- reformulation professionnelle ;
- rédaction d’email ;
- génération de compte rendu.

Fonctionnalités :

- chargement dynamique des prompts ;
- génération via modèles locaux ;
- export automatique des résultats ;
- historique des générations ;
- benchmark multi-modèles ;
- comparaison des temps d’exécution.

---

### Benchmark multi-modèles

Le module benchmark permet de comparer plusieurs modèles locaux sur une même tâche.

Fonctionnalités :

- comparaison simultanée de plusieurs modèles ;
- mesure des temps d’exécution ;
- aperçu des résultats générés ;
- historique benchmark ;
- aide à l’analyse des performances.

---

## Interface utilisateur

La plateforme utilise une interface moderne développée avec **Gradio**.

L’interface inclut :

- une vue d’ensemble de la plateforme ;
- un assistant robot dynamique ;
- un module d’anonymisation ;
- un module de génération de texte ;
- un benchmark interactif multi-modèles ;
- un système d’upload de fichiers ;
- des exports téléchargeables ;
- un historique des résultats ;
- un scénario de démonstration.

---

## Architecture globale

```text
Utilisateur
↓
Interface Gradio
↓
Agents IA spécialisés
↓
LiteLLM
↓
Ollama
↓
LLM locaux
```

---

## Structure du projet

```text
plateforme_agentique/
│
├── agents/
│   ├── agent_anonymisation.py
│   └── agent_generation.py
│
├── interface/
│   └── app.py
│
├── prompts/
│   ├── prompt_anonymisation.txt
│   ├── prompt_resume.txt
│   ├── prompt_email.txt
│   ├── prompt_reformulation.txt
│   └── prompt_compte_rendu.txt
│
├── data/
│   ├── anonymisation_client_1.txt
│   ├── anonymisation_client_2.txt
│   ├── anonymisation_client_3.txt
│   ├── anonymisation_client_4.txt
│   ├── anonymisation_client_5.txt
│   ├── document_resume.txt
│   ├── email_brief.txt
│   ├── notes_reunion.txt
│   └── reformulation.txt
│
├── resultats/
│   └── exports/
│
├── config.py
├── orchestrateur.py
├── main.py
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Description des composants

### `agents/`

Ce dossier contient les agents spécialisés de la plateforme.

#### `agent_anonymisation.py`

Responsable de :

- la détection Regex ;
- la détection LLM ;
- la fusion des détections ;
- l’anonymisation du texte ;
- la génération des résultats.

#### `agent_generation.py`

Responsable de :

- la lecture des prompts ;
- la génération de texte ;
- l’appel aux modèles locaux ;
- la sauvegarde des résultats.

---

### `interface/`

#### `app.py`

Ce fichier contient l’interface Gradio.

Il gère :

- la vue d’ensemble ;
- le robot assistant dynamique ;
- l’upload de fichiers ;
- l’anonymisation interactive ;
- la génération de texte ;
- le benchmark multi-modèles ;
- l’historique des traitements ;
- les exports téléchargeables.

---

### `prompts/`

Ce dossier contient les prompts utilisés par les modèles.

Cette séparation permet de modifier les consignes données aux modèles sans modifier le code Python.

Prompts disponibles :

- `prompt_anonymisation.txt`
- `prompt_resume.txt`
- `prompt_email.txt`
- `prompt_reformulation.txt`
- `prompt_compte_rendu.txt`

---

### `data/`

Ce dossier contient les fichiers de test utilisés pour les démonstrations.

Il contient notamment :

- des fichiers clients pour l’anonymisation ;
- un document à résumer ;
- un brief email ;
- des notes de réunion ;
- un texte de reformulation.

---

### `resultats/`

Ce dossier contient les résultats produits par les agents.

Le sous-dossier `exports/` contient les fichiers générés depuis l’interface :

- textes anonymisés ;
- fichiers JSON de détection ;
- résultats de génération ;
- sorties exportées.

---

## Configuration centralisée

Le fichier `config.py` centralise les paramètres importants de la plateforme :

- URL Ollama ;
- timeout ;
- modèles disponibles ;
- modèle par défaut ;
- chemins des dossiers ;
- paramètres d’exécution.

Cette approche permet de faciliter la maintenance et l’ajout futur de nouveaux modèles ou agents.

---

## Orchestrateur

Le fichier `orchestrateur.py` agit comme orchestrateur principal en mode terminal.

Il permet :

- de sélectionner le cas d’usage ;
- de choisir le modèle local ;
- de lancer les agents automatiquement.

Cas supportés :

1. anonymisation ;
2. génération de texte ;
3. exécution des deux agents.

---

## Technologies utilisées

- Python
- Gradio
- Ollama
- LiteLLM
- Smolagents
- Docker
- Docker Compose
- GitHub

---

## Modèles locaux testés

Les modèles locaux évalués dans le projet sont :

- Mistral ;
- Llama 3.2:3b ;
- Phi3 Mini.

---

## Résultats de benchmark

### Observations générales

#### Llama 3.2:3b

Llama 3.2:3b présente un bon équilibre global entre :

- qualité ;
- cohérence ;
- stabilité ;
- fluidité ;
- latence.

#### Mistral

Mistral offre une bonne qualité rédactionnelle, mais peut présenter une latence plus élevée selon la machine utilisée.

#### Phi3 Mini

Phi3 Mini est plus léger et rapide, mais peut être moins robuste sur certaines tâches longues ou complexes.

---

## Latence au premier lancement

Une latence plus élevée peut être observée lors du premier appel à un modèle local.

Cela s’explique par le chargement initial du modèle en mémoire par Ollama. Les appels suivants sont généralement plus rapides, car le modèle reste temporairement chargé en RAM.

---

## Installation

### 1. Cloner le projet

```bash
git clone https://github.com/Hajar-JLT23/plateforme_agentique_on_premise.git
```

### 2. Installer les dépendances Python

```bash
pip install -r requirements.txt
```

### 3. Installer Ollama

Ollama doit être installé sur la machine locale.

### 4. Télécharger les modèles locaux

```bash
ollama pull mistral
ollama pull llama3.2:3b
ollama pull phi3:mini
```

---

## Lancement avec Docker

### Construction de l’image

```bash
docker compose build
```

### Lancement de la plateforme

```bash
docker compose up
```

L’interface est ensuite accessible à l’adresse suivante :

```text
http://localhost:7860
```

---

## Lancement en local sans Docker

Il est également possible de lancer l’orchestrateur en local :

```bash
python main.py
```

Ou l’interface Gradio :

```bash
python interface/app.py
```

---

## Fonctionnement général

L’utilisateur peut :

- ouvrir l’interface Gradio ;
- accéder à la vue d’ensemble ;
- importer un fichier texte ;
- lancer une anonymisation ;
- générer un texte professionnel ;
- comparer plusieurs modèles locaux ;
- consulter l’historique ;
- télécharger les résultats générés.

---

## Confidentialité

La plateforme fonctionne entièrement en local.

Aucune donnée n’est envoyée vers :

- OpenAI ;
- Anthropic ;
- Google Gemini ;
- Mistral API ;
- une API cloud externe.

Les modèles sont exécutés localement via **Ollama**.

---

## Limites actuelles

Les limites actuelles du projet sont :

- support limité aux fichiers `.txt` ;
- absence de support natif PDF/DOCX ;
- pas encore de base de données persistante ;
- benchmark encore manuel ;
- dépendance aux ressources locales de la machine ;
- latence plus élevée au premier chargement des modèles ;
- pas encore d’authentification utilisateur.

---

## Perspectives d’amélioration

Améliorations possibles :

- ajout du support PDF et DOCX ;
- intégration d’un système RAG ;
- ajout d’une base vectorielle ;
- historique persistant en base de données ;
- dashboard de monitoring ;
- benchmark automatique avancé ;
- ajout de nouveaux agents spécialisés ;
- authentification utilisateur ;
- déploiement interne sur serveur local ;
- amélioration de l’évaluation des modèles.

---

## Démonstration

La démonstration recommandée consiste à :

1. présenter la vue d’ensemble ;
2. expliquer l’architecture locale ;
3. lancer une anonymisation ;
4. montrer le JSON de détection ;
5. télécharger les exports ;
6. lancer une génération de texte ;
7. comparer plusieurs modèles ;
8. analyser les temps d’exécution.

---

## Conclusion

Cette plateforme constitue une première base fonctionnelle d’architecture agentique locale.

Elle permet d’intégrer plusieurs cas d’usage IA dans une interface unique, cohérente et extensible.

Le projet met en avant :

- l’exécution locale ;
- la confidentialité ;
- la modularité ;
- l’expérimentation multi-modèles ;
- la démonstration technique professionnelle ;
- une première logique d’industrialisation légère.