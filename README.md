# Plateforme Agentique On-Premise

## Objectif du projet

L’objectif de cette plateforme est de consolider plusieurs cas d’usage d’intelligence artificielle dans une architecture agentique locale et cohérente.

Le projet repose exclusivement sur des modèles de langage exécutés localement via Ollama, sans utilisation d’API cloud externes.

La plateforme permet actuellement de couvrir deux cas d’usage principaux :

- anonymisation automatique de documents
- génération automatique de texte

Cette phase correspond à une étape de consolidation et d’industrialisation légère des prototypes développés durant les semaines précédentes du stage.

---

# Cas d’usage intégrés

## 1. Agent d’anonymisation

Cet agent permet de détecter et masquer automatiquement plusieurs types de données sensibles présentes dans des documents texte.

### Approche utilisée

Détection hybride Regex + LLM :

#### Regex
- emails
- téléphones
- dates
- numéros de sécurité sociale

#### LLM
- noms
- adresses

### Fonctionnalités

- lecture automatique des documents
- détection des PII
- anonymisation du contenu
- sauvegarde des résultats

---

## 2. Agent de génération de texte

Cet agent permet de générer automatiquement différents types de contenus professionnels.

### Sous-tâches supportées

- résumé documentaire
- reformulation professionnelle
- rédaction d’email
- génération de compte rendu structuré

### Fonctionnalités

- chargement automatique des prompts
- génération via modèles locaux
- sauvegarde automatique des outputs
- benchmark multi-modèles

---

# Architecture de la plateforme

La plateforme repose sur une architecture modulaire organisée autour :

- d’un orchestrateur central
- d’agents spécialisés
- d’une configuration centralisée
- d’un système de prompts séparés du code

## Structure du projet

```text
plateforme_agentique/
│
├── agents/
│   ├── agent_anonymisation.py
│   └── agent_generation.py
│
├── prompts/
│   ├── prompt_anonymisation.txt
│   ├── prompt_resume.txt
│   ├── prompt_email.txt
│   ├── prompt_reformulation.txt
│   └── prompt_compte_rendu.txt
│
├── data/
│
├── resultats/
│
├── config.py
├── orchestrateur.py
├── main.py
├── requirements.txt
└── README.md
```

---

# Description des composants

## agents/

Contient les agents spécialisés de la plateforme.

### agent_anonymisation.py

Responsable de :

- la détection des données sensibles
- l’anonymisation
- la sauvegarde des résultats

### agent_generation.py

Responsable de :

- la génération des textes
- le chargement des prompts
- la sauvegarde des outputs

---

## prompts/

Contient les prompts utilisés par les modèles.


- prompt_anonymisation.txt
- prompt_resume.txt
- prompt_email.txt
- prompt_reformulation.txt
- prompt_compte_rendu.txt

Cette séparation permet de modifier les instructions sans modifier le code Python.

---

## data/

Contient les données d’entrée utilisées pour les tests.


- documents d’anonymisation
- briefs email
- notes de réunion
- documents à résumer

---

## resultats/

Contient les résultats générés par les agents.



- textes anonymisés
- sorties de génération
- résultats benchmark
- résultats LLM-as-a-Judge

---

# Configuration centralisée

Le fichier `config.py` centralise :

- URL Ollama
- timeout
- modèles disponibles
- modèle par défaut
- chemins des dossiers

Cette approche permet une maintenance plus simple et facilite l’ajout futur de nouveaux agents.

---

# Orchestrateur

Le fichier `orchestrateur.py` agit comme orchestrateur principal de la plateforme.

Il permet :

- de sélectionner le cas d’usage
- de choisir le modèle
- de lancer les agents automatiquement

Cas supportés :

1. anonymisation
2. génération de texte
3. exécution des deux agents

---

# Modèles testés

Les modèles locaux évalués :

- Mistral
- Phi3 Mini
- Llama 3.2:3b

## Résultat principal du benchmark

Llama 3.2:3b présente le meilleur équilibre global entre :

- qualité
- cohérence
- fluidité
- stabilité
- latence

---

# Technologies utilisées

- Python
- Ollama
- Smolagents
- LiteLLM
- GitHub

---

# Installation

## Installer les dépendances

```bash
pip install -r requirements.txt
```

## Vérifier Ollama

```bash
ollama list
```

---

# Lancement de la plateforme

```bash
python main.py
```

---

# Fonctionnement

Au lancement, l’utilisateur peut :

- choisir le cas d’usage
- sélectionner le modèle local
- lancer un ou plusieurs agents

Les résultats sont automatiquement sauvegardés dans le dossier `resultats/`.

---

# Perspectives

Les prochaines améliorations prévues :

- ajout d’une interface Streamlit ou Gradio
- packaging Docker
- docker-compose
- ajout d’un système RAG
- ajout de nouveaux agents IA
- automatisation complète des benchmarks

---

# Auteur

Hajar JELTHI

Stage Développement IA Agentique — Novelis