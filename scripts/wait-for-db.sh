#!/bin/bash
# Script d'attente pour la base de données [cite: 11, 93]

set -e

# Récupération des paramètres depuis les variables d'environnement [cite: 93, 94]
HOST="${DB_HOST:-db}"
PORT="${DB_PORT:-3306}"
USER="${DB_USER:-root}"
PASSWORD="${DB_PASSWORD:-root}"

MAX_TRIES=30 # Maximum 30 tentatives 
WAIT_SECONDS=2 # Intervalle de 2 secondes 

echo "Attente de la base de données sur $HOST:$PORT..."

for i in $(seq 1 $MAX_TRIES); do
  # Utilisation de --skip-ssl pour contourner les exigences de certificats MySQL 8
  if mysql --skip-ssl -h "$HOST" -P "$PORT" -u "$USER" -p"$PASSWORD" -e "SELECT 1" > /dev/null 2>&1; then
    echo "Base de données prête !"
    exit 0
  fi

  echo "Tentative $i/$MAX_TRIES"
  sleep "$WAIT_SECONDS"
done

echo "Erreur : La base de données n'est pas disponible après 30 tentatives." 
exit 1