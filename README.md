````markdown
# Plateforme Agentique On-Premise

## Présentation du projet

Cette plateforme a été développée dans le cadre d’un stage chez **Novelis** autour des architectures agentiques locales basées sur des modèles de langage exécutés entièrement en local.

L’objectif principal du projet est de concevoir une plateforme IA modulaire, professionnelle et extensible capable de :

- anonymiser automatiquement des documents contenant des données sensibles ;
- générer des contenus professionnels via des modèles de langage locaux ;
- comparer plusieurs modèles IA locaux ;
- exécuter l’ensemble des traitements sans dépendre d’API cloud externes ;
- proposer une démonstration visuelle crédible d’une plateforme agentique on-premise.

La plateforme repose exclusivement sur des modèles locaux exécutés via **Ollama**.

---

# Auteur

**Hajar JELTHI**  
L3 MIAGE — Université Paris Nanterre  
Stage Développement IA Agentique — Novelis

---

# Contexte du stage

Le stage s’inscrit dans une démarche d’exploration des architectures IA agentiques exécutées localement.

L’objectif était de :

- étudier l’intégration de modèles LLM locaux ;
- concevoir une architecture multi-agents ;
- développer une interface de démonstration professionnelle ;
- industrialiser les prototypes existants ;
- préparer une base extensible pour de futurs cas d’usage IA.

Le projet a progressivement évolué d’un ensemble de prototypes indépendants vers une véritable plateforme agentique unifiée.

---

# Objectifs du projet

Le projet vise à consolider plusieurs cas d’usage IA dans une architecture cohérente et industrialisable.

## Objectifs techniques

- centraliser plusieurs agents IA dans une plateforme unique ;
- exécuter tous les traitements localement ;
- éviter l’utilisation d’API cloud externes ;
- standardiser les appels modèles via LiteLLM ;
- comparer plusieurs modèles locaux ;
- proposer une architecture facilement extensible.

## Objectifs fonctionnels

- anonymiser des données sensibles ;
- générer automatiquement des contenus professionnels ;
- benchmarker plusieurs modèles ;
- proposer une interface moderne et démonstrative ;
- exporter les résultats ;
- suivre l’historique des traitements.

---

# Technologies utilisées

## Backend

- Python 3.11
- LiteLLM
- Smolagents
- Ollama
- Regex

## Frontend / Interface

- Gradio
- HTML/CSS personnalisé

## Conteneurisation

- Docker
- Docker Compose

## Modèles locaux testés

- llama3.2:3b
- mistral
- phi3

---

# Fonctionnalités principales

# 1. Agent d’anonymisation

L’agent d’anonymisation permet de détecter et masquer automatiquement des données sensibles présentes dans des documents texte.

## Détections via Regex

- emails ;
- numéros de téléphone ;
- dates ;
- numéros de sécurité sociale.

## Détections via LLM

- noms ;
- adresses ;
- informations sensibles contextuelles.

## Fonctionnalités disponibles

- upload de fichiers `.txt` ;
- chargement automatique d’exemples ;
- anonymisation automatique du contenu ;
- affichage JSON des détections ;
- score de confidentialité ;
- historique des traitements ;
- temps d’exécution ;
- export TXT ;
- export JSON ;
- comparaison avant / après anonymisation ;
- timeline d’exécution IA.

## Pipeline d’anonymisation

```text
Chargement du document
↓
Détection Regex
↓
Analyse LLM locale
↓
Fusion des détections
↓
Anonymisation du texte
↓
Export des résultats
````

---

# 2. Agent de génération de texte

L’agent de génération permet de produire automatiquement des contenus professionnels à partir d’un brief utilisateur.

## Cas d’usage supportés

* résumé documentaire ;
* résumé intelligent ;
* reformulation professionnelle ;
* rédaction d’email ;
* génération de compte rendu ;
* question / réponse.

## Fonctionnalités disponibles

* chargement dynamique des prompts ;
* génération via modèles locaux ;
* export automatique des résultats ;
* historique des générations ;
* benchmark multi-modèles ;
* comparaison des temps d’exécution ;
* choix du ton de réponse ;
* choix du format de sortie ;
* timeline IA ;
* détection automatique d’intention.

## Tons disponibles

* professionnel ;
* simple ;
* technique ;
* synthétique ;
* pédagogique.

## Formats disponibles

* structuré ;
* court ;
* détaillé ;
* bullet points ;
* réponse directe.

---

# 3. Benchmark multi-modèles

Le module benchmark permet de comparer plusieurs modèles locaux sur une même tâche.

## Fonctionnalités disponibles

* comparaison simultanée de plusieurs modèles ;
* mesure des temps d’exécution ;
* aperçu des résultats générés ;
* historique benchmark ;
* graphique des performances ;
* classement automatique des modèles ;
* aide à l’analyse des performances.

## Exemple d’utilisation

Un même texte peut être exécuté sur :

* Llama 3.2 ;
* Mistral ;
* Phi3.

La plateforme compare ensuite :

* les temps d’exécution ;
* la rapidité ;
* la qualité de génération.

---

# Interface utilisateur

La plateforme utilise une interface moderne développée avec **Gradio**.

## Fonctionnalités UX intégrées

* vue d’ensemble dynamique ;
* assistant robot interactif ;
* dashboard statistiques ;
* historique des traitements ;
* exports téléchargeables ;
* badge IA locale ;
* architecture visuelle ;
* benchmark interactif ;
* score confidentialité ;
* timeline IA ;
* loader animé ;
* système d’upload ;
* comparaison avant / après.

---

# Dashboard statistiques

Le dashboard permet de suivre :

* le nombre total de traitements ;
* le nombre d’anonymisations ;
* le nombre de générations ;
* le temps moyen d’exécution ;
* le modèle le plus utilisé.

Les statistiques sont sauvegardées automatiquement dans :

```text
resultats/stats.json
```

Cela permet de conserver les données même après redémarrage de Docker.

---

# Détection automatique d’intention

Le module génération inclut une détection automatique d’intention.

Exemples :

```text
Résume ce texte
→ Résumé
```

```text
Reformule cet email
→ Reformulation
```

```text
C’est quoi la capitale de la France ?
→ Question / Réponse
```

---

# Architecture globale

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

# Architecture technique détaillée

## Interface

L’interface utilisateur est développée avec Gradio.

Elle centralise :

* les interactions utilisateur ;
* les uploads ;
* les résultats ;
* les benchmarks ;
* les exports.

## Agents IA

Deux agents principaux sont utilisés :

* agent_anonymisation.py ;
* agent_generation.py.

Chaque agent encapsule sa logique métier.

## LiteLLM

LiteLLM standardise les appels aux modèles locaux.

## Ollama

Ollama exécute les modèles LLM localement.

Aucune donnée n’est envoyée vers des serveurs externes.

## Docker

Docker permet :

* la reproductibilité ;
* l’isolation ;
* le packaging simplifié ;
* le déploiement local.

---

# Structure du projet

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
│   ├── exports/
│   └── stats.json
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

# Installation du projet

## 1. Cloner le repository

```bash
git clone <url-du-repository>
cd plateforme_agentique
```

---

## 2. Installer Docker Desktop

Télécharger Docker Desktop :

* Windows
* Linux
* macOS

---

## 3. Vérifier Ollama

Installer Ollama puis vérifier :

```bash
ollama list
```

Télécharger les modèles :

```bash
ollama pull llama3.2:3b
ollama pull mistral
ollama pull phi3
```

---

## 4. Lancer la plateforme

```bash
docker compose up --build
```

---

## 5. Accéder à l’interface

```text
http://localhost:7860
```

---

# Exemple de démonstration

## Anonymisation

1. Charger un fichier `.txt`.
2. Sélectionner un modèle.
3. Lancer l’anonymisation.
4. Observer :

* le texte anonymisé ;
* le JSON ;
* le score confidentialité ;
* le benchmark ;
* l’historique.

---

## Génération

1. Choisir une tâche.
2. Entrer un texte.
3. Choisir un ton.
4. Lancer la génération.
5. Exporter le résultat.

---

## Benchmark

1. Sélectionner plusieurs modèles.
2. Lancer la comparaison.
3. Observer :

* les temps ;
* les résultats ;
* le classement automatique.

---

# Résultats obtenus

Le projet a permis de :

* construire une architecture agentique cohérente ;
* intégrer plusieurs agents IA ;
* exécuter les traitements localement ;
* proposer une interface professionnelle ;
* benchmarker plusieurs modèles ;
* préparer une base extensible pour de futurs agents.

---

# Limites actuelles

Certaines limites restent présentes :

* temps de chargement initial des modèles ;
* précision variable selon les modèles ;
* absence de mémoire conversationnelle ;
* absence de RAG documentaire avancé ;
* benchmark limité à des tests simples.

---

# Perspectives d’amélioration

Améliorations possibles :

* ajout d’un système RAG ;
* support PDF et DOCX ;
* ajout d’agents supplémentaires ;
* orchestration avancée multi-agents ;
* mémoire conversationnelle ;
* déploiement serveur ;
* intégration cybersécurité ;
* gestion de rôles utilisateurs.

---

# Conclusion

Cette plateforme démontre la faisabilité d’une architecture agentique locale capable de combiner plusieurs cas d’usage IA dans une interface unique.

Le projet met en avant :

* l’utilisation de modèles locaux ;
* l’intégration multi-agents ;
* l’orchestration IA ;
* la confidentialité des données ;
* la modularité de l’architecture ;
* la démonstration d’une plateforme IA professionnelle.

Le projet constitue une base solide pour des évolutions futures autour des systèmes IA agentiques on-premise.

```
```
