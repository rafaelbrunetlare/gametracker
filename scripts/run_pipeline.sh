#!/bin/bash

# ---------------------------------------------------
# Script d'automatisation du pipeline ETL
# ---------------------------------------------------

set -e  # Arrêt immédiat à la première erreur

# Charger les variables pour éviter les erreurs de commande mysql
# Si elles ne sont pas chargées par l'environnement Docker, on définit des défauts
HOST="${DB_HOST:-db}"
USER="${DB_USER:-root}"
PASSWORD="${DB_PASSWORD:-root}"
DATABASE="${DB_NAME:-etl_db}"

echo "============================"
echo "Début du pipeline ETL"
echo "============================"

# 1️⃣ Attente de la base de données
echo "[1/4] Attente de la base de données..."
./scripts/wait-for-db.sh
echo "Base de données prête ✅"

# 2️⃣ Initialisation des tables
# IMPORTANT : On appelle mysql directement puisqu'on est déjà dans le conteneur app
echo "[2/4] Initialisation des tables..."
mysql --skip-ssl -h "$HOST" -u "$USER" -p"$PASSWORD" "$DATABASE" < scripts/init-db.sql
echo "Tables initialisées ✅"

# 3️⃣ Exécution du pipeline ETL Python
echo "[3/4] Exécution du pipeline ETL..."
python -m src.main 
echo "Pipeline ETL exécuté ✅"

# 4️⃣ Génération du rapport
echo "[4/4] Génération du rapport..."
python -m src.report
echo "Rapport généré ✅"

echo "============================"
echo "Pipeline ETL terminé avec succès !"
echo "============================"