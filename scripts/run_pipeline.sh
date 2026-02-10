#!/bin/bash

# Configuration pour s'arrêter si une commande échoue
set -e

echo "===================================================="
echo "   DEMARRAGE DE L'AUTOMATISATION GAMETRACKER"
echo "===================================================="

# 1. Attente de la base de données
echo "1/4 Attente de la base de données..."
# On suppose que ton script d'attente existe déjà
bash ./scripts/wait-for-db.sh --timeout=30 --strict -- echo "La DB est prête !"

# 2. Initialisation des tables (optionnel si Docker le fait déjà, mais demandé par l'énoncé)
echo "2/4 Initialisation de la structure SQL..."
mysql -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASSWORD" --skip-ssl "$DB_NAME" < ./scripts/init-db.sql

# 3. Exécution du pipeline ETL Python
echo "3/4 Exécution du pipeline ETL (Extract, Transform, Load)..."
python3 -m src.main

# 4. Génération du rapport (Si ce n'est pas déjà appelé dans main.py)
echo "4/4 Génération du rapport final..."
python3 -m src.report

echo "===================================================="
echo "   PROCESSUS TERMINE AVEC SUCCES !"
echo "===================================================="