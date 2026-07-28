
# Plateforme Agentique On-Premise

## Présentation du projet

Cette plateforme a été développée dans le cadre d’un stage chez **Novelis** autour des architectures agentiques locales basées sur des modèles de langage exécutés entièrement en local.

L’objectif principal du projet est de concevoir une plateforme IA modulaire, professionnelle et extensible capable de :

- anonymiser automatiquement des documents contenant des données sensibles ;
- générer des contenus professionnels via des modèles de langage locaux ;
- comparer plusieurs modèles IA locaux ;
- benchmarker les performances des modèles ;
- exécuter l’ensemble des traitements sans dépendre d’API cloud externes ;
- proposer une démonstration visuelle crédible d’une plateforme IA agentique on-premise.

L’ensemble de la plateforme repose sur des modèles locaux exécutés via **Ollama**, sans utilisation d’API payantes ni envoi de données vers des services cloud externes.

---

# Auteur

**Hajar JELTHI**  
Étudiante en L3 MIAGE — Université Paris Nanterre  
Stage Développement IA Agentique — Novelis

---

# Contexte du stage

Le stage s’inscrit dans une démarche d’exploration des architectures IA agentiques exécutées localement.

L’objectif était de :

- étudier l’intégration de modèles LLM locaux ;
- concevoir une architecture multi-agents ;
- développer une plateforme IA unifiée ;
- industrialiser plusieurs prototypes existants ;
- proposer une démonstration professionnelle ;
- préparer une architecture extensible pour de futurs cas d’usage IA.

Le projet a progressivement évolué d’un ensemble de scripts indépendants vers une véritable plateforme agentique modulaire intégrant plusieurs agents spécialisés.

---

# Objectifs du projet

## Objectifs techniques

- centraliser plusieurs agents IA dans une architecture unique ;
- standardiser les appels modèles ;
- exécuter tous les traitements localement ;
- éviter toute dépendance aux API cloud ;
- permettre l’ajout futur de nouveaux agents ;
- proposer une architecture modulaire et industrialisable ;
- intégrer Docker pour la reproductibilité ;
- benchmarker plusieurs modèles locaux.

## Objectifs fonctionnels

- anonymiser automatiquement des documents ;
- détecter des données sensibles ;
- générer des contenus professionnels ;
- produire des réponses intelligentes ;
- comparer plusieurs modèles IA ;
- exporter les résultats ;
- afficher l’historique des traitements ;
- proposer une interface moderne et démonstrative.

---

# Technologies utilisées

## Backend

- Python 3.11
- LiteLLM
- Smolagents
- Regex
- JSON

## Exécution locale des modèles

- Ollama

## Interface utilisateur

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

# Architecture globale

Utilisateur  
↓  
Interface Gradio  
↓  
Orchestrateur IA  
↓  
Agents spécialisés  
↓  
LiteLLM  
↓  
Ollama  
↓  
LLM locaux

---

# Architecture technique

## Interface utilisateur

L’interface utilisateur a été développée avec **Gradio** afin de proposer une démonstration moderne, interactive et facilement utilisable.

Elle centralise :

- les uploads de documents ;
- les traitements IA ;
- les benchmarks ;
- les exports ;
- les dashboards ;
- les historiques ;
- les visualisations des résultats.

L’interface intègre également :

- un assistant IA visuel ;
- des cartes dynamiques ;
- des timelines IA ;
- des scores de confidentialité ;
- des loaders animés ;
- des dashboards statistiques.

---

## Orchestrateur IA

Un orchestrateur commun permet de centraliser :

- la gestion des modèles ;
- les appels LLM ;
- les paramètres globaux ;
- les prompts ;
- les workflows des agents.

Cette approche permet de transformer plusieurs prototypes indépendants en une plateforme cohérente et extensible.

---

## LiteLLM

LiteLLM est utilisé afin de standardiser les appels vers les modèles locaux.

Cela permet :

- de simplifier le changement de modèles ;
- de centraliser les appels IA ;
- de faciliter les benchmarks ;
- de rendre l’architecture plus modulaire.

---

## Ollama

Ollama est utilisé pour exécuter les modèles LLM entièrement en local.

Aucune donnée n’est envoyée vers des services externes.

Cela garantit :

- la confidentialité ;
- le contrôle local des données ;
- l’absence de coûts API ;
- une architecture on-premise.

---

## Docker

Docker permet :

- la reproductibilité de l’environnement ;
- l’isolation des dépendances ;
- le packaging de la plateforme ;
- le déploiement simplifié.

La plateforme peut être relancée avec une seule commande.

---

# Fonctionnalités principales

# 1. Agent d’anonymisation

L’agent d’anonymisation permet de détecter et masquer automatiquement des données sensibles présentes dans des documents texte.

## Détections via Regex

- emails ;
- numéros de téléphone ;
- dates ;
- numéros de sécurité sociale ;
- informations structurées.

## Détections via LLM

- noms ;
- adresses ;
- organisations ;
- informations sensibles contextuelles.

---

## Fonctionnalités disponibles

- upload de fichiers `.txt` ;
- chargement automatique d’exemples ;
- anonymisation automatique ;
- affichage JSON des détections ;
- score de confidentialité ;
- historique des anonymisations ;
- temps d’exécution ;
- export TXT ;
- export JSON ;
- comparaison avant / après ;
- timeline IA ;
- dashboard dynamique.

---

## Pipeline d’anonymisation

- Chargement du document  
↓  
- Détection Regex  
↓  
- Analyse LLM locale  
↓  
- Fusion des détections  
↓  
- Anonymisation du texte  
↓  
- Génération du JSON  
↓  
- Export des résultats

---

## Score de confidentialité

La plateforme calcule automatiquement un score de confidentialité selon :

- le nombre de données sensibles détectées ;
- les types de données détectées ;
- le niveau de risque.

Exemples :

- faible ;
- moyen ;
- élevé.

---

# 2. Agent de génération de texte

L’agent de génération permet de produire automatiquement des contenus professionnels à partir d’un texte utilisateur.

---

## Cas d’usage supportés

- résumé documentaire ;
- résumé intelligent ;
- reformulation professionnelle ;
- rédaction d’emails ;
- génération de compte rendu ;
- question / réponse ;
- réponses structurées ;
- synthèses automatiques.

---

## Fonctionnalités disponibles

- génération locale via LLM ;
- historique des générations ;
- export automatique ;
- benchmark multi-modèles ;
- comparaison des temps d’exécution ;
- sélection du ton ;
- sélection du format ;
- détection automatique d’intention ;
- dashboard IA ;
- timeline IA.

---

## Tons disponibles

- professionnel ;
- simple ;
- technique ;
- pédagogique ;
- synthétique.

---

## Formats disponibles

- structuré ;
- détaillé ;
- court ;
- bullet points ;
- réponse directe.

---

## Détection automatique d’intention

Le système peut détecter automatiquement l’intention utilisateur.

Exemples :

- “Résume ce texte” → Résumé ;
- “Reformule cet email” → Reformulation ;
- “C’est quoi la capitale de la France ?” → Question / Réponse.

---

# 3. Benchmark multi-modèles

Le module benchmark permet de comparer plusieurs modèles locaux sur une même tâche.

---

## Fonctionnalités benchmark

- comparaison simultanée ;
- historique benchmark ;
- mesure des temps d’exécution ;
- aperçu des réponses ;
- graphique des performances ;
- classement automatique ;
- comparaison multi-modèles.

---

## Exemple de modèles comparés

- llama3.2:3b
- mistral
- phi3

---

## Données affichées

- temps d’exécution ;
- rapidité ;
- qualité des réponses ;
- classement des modèles ;
- historique benchmark.

---

# Dashboard statistiques

Le dashboard permet de suivre :

- le nombre total de traitements ;
- le nombre d’anonymisations ;
- le nombre de générations ;
- le temps moyen d’exécution ;
- le modèle le plus utilisé ;
- l’historique global.

Les statistiques sont sauvegardées automatiquement dans :

`resultats/stats.json`

Cela permet de conserver les statistiques même après redémarrage de Docker.

---

# Assistant IA interactif

La plateforme intègre un assistant visuel permettant de guider l’utilisateur dans les différents modules.

L’assistant peut :

- afficher des conseils ;
- expliquer les fonctionnalités ;
- guider les démonstrations ;
- présenter les modules.

---

# Interface utilisateur

L’interface intègre :

- vue d’ensemble ;
- dashboard IA ;
- benchmark interactif ;
- score confidentialité ;
- timeline IA ;
- historique dynamique ;
- assistant robot ;
- loader animé ;
- exports téléchargeables ;
- cartes interactives ;
- comparaison avant/après.

---

# Structure du projet

plateforme_agentique/  
│  
├── agents/  
│ ├── agent_anonymisation.py  
│ └── agent_generation.py  
│  
├── interface/  
│ └── app.py  
│  
├── prompts/  
│ ├── prompt_anonymisation.txt  
│ ├── prompt_resume.txt  
│ ├── prompt_email.txt  
│ ├── prompt_reformulation.txt  
│ └── prompt_compte_rendu.txt  
│  
├── data/  
│ ├── anonymisation_client_1.txt  
│ ├── anonymisation_client_2.txt  
│ ├── anonymisation_client_3.txt  
│ ├── anonymisation_client_4.txt  
│ ├── anonymisation_client_5.txt  
│ ├── document_resume.txt  
│ ├── email_brief.txt  
│ ├── notes_reunion.txt  
│ └── reformulation.txt  
│  
├── resultats/  
│ ├── exports/  
│ └── stats.json  
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

---

# Installation du projet

## 1. Cloner le repository

`git clone <url-du-repository>`

`cd plateforme_agentique`

---

## 2. Installer Ollama

Vérifier Ollama :

`ollama list`

Télécharger les modèles :

`ollama pull llama3.2:3b`

`ollama pull mistral`

`ollama pull phi3`

---

## 3. Lancer Docker

`docker compose up --build`

---

## 4. Accéder à l’interface

`http://localhost:7860`

---

# Exemple de démonstration

## Anonymisation

1. Charger un fichier `.txt`
2. Sélectionner un modèle
3. Lancer l’anonymisation
4. Observer :

- texte anonymisé ;
- JSON ;
- score confidentialité ;
- historique ;
- exports.

---

## Génération

1. Choisir une tâche
2. Entrer un texte
3. Sélectionner un ton
4. Générer le contenu
5. Exporter le résultat

---

## Benchmark

1. Sélectionner plusieurs modèles
2. Lancer la comparaison
3. Observer :

- les temps ;
- les résultats ;
- le classement automatique.

---

# Résultats obtenus

Le projet a permis de :

- construire une architecture agentique cohérente ;
- intégrer plusieurs agents IA ;
- exécuter les traitements localement ;
- proposer une interface professionnelle ;
- benchmarker plusieurs modèles ;
- centraliser plusieurs workflows IA ;
- préparer une architecture extensible.

---

# Limites actuelles

Certaines limites restent présentes :

- temps de chargement initial des modèles ;
- précision variable selon les modèles ;
- absence de mémoire conversationnelle ;
- RAG simple intégré, amélioration possible ;
- benchmark limité à des tests simples.

---

# Perspectives d’amélioration

- amélioration du système RAG existant ;
- support PDF et DOCX ;
- mémoire conversationnelle ;
- nouveaux agents IA ;
- orchestration avancée ;
- système multi-utilisateurs ;
- déploiement serveur ;
- intégration cybersécurité.

---

# Conclusion

Cette plateforme démontre la faisabilité d’une architecture agentique locale capable de combiner plusieurs cas d’usage IA dans une interface unique.

Le projet met en avant :

- l’utilisation de modèles locaux ;
- l’intégration multi-agents ;
- l’orchestration IA ;
- la confidentialité des données ;
- la modularité ;
- l’industrialisation légère ;
- la démonstration d’une plateforme IA professionnelle.

Le projet constitue une base solide pour de futures évolutions autour des systèmes IA agentiques on-premise.
```
