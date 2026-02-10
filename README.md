# GameTracker ETL Project

## Description
Pipeline ETL (Extract, Transform, Load) automatisé pour la gestion des statistiques de joueurs et de scores. Le projet utilise Docker pour orchestrer une base de données MySQL et une application Python.

## Prérequis
- Docker & Docker Compose
- Fichiers source : `Players.csv` et `Scores.csv` dans le dossier `data/raw/`

## Instructions de lancement
1. **Démarrer les services :**
   ```bash
   docker compose up -d