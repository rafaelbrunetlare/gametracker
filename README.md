# GameTracker – Pipeline ETL

GameTracker est un projet ETL (Extract, Transform, Load) permettant d’ingérer des données
de joueurs et de scores de jeux vidéo à partir de fichiers CSV, de les nettoyer, de les
stocker dans une base de données MySQL, puis de générer un rapport de synthèse automatisé.

---

## Prérequis techniques

- Docker
- Docker Compose
- Git
- (Optionnel) Git Bash ou WSL sous Windows pour exécuter les scripts Bash

---

## Instructions de lancement

### 1. Démarrer les conteneurs
```bash
docker-compose up -d
```
### 2. Lancer le pipeline ETL complet
```bash
bash run_etl.sh
```
Le script exécute automatiquement :
- L’attente de la base de données MySQL
- L’initialisation des tables
- L’exécution du pipeline ETL Python
- La génération du rapport final


### Structure du projet :
gametracker/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .gitignore
├── README.md
├── data/
│   └── raw/
│       ├── Players.csv
│       └── Scores.csv
├── scripts/
│   ├── init-db.sql
│   ├── wait-for-db.sh
│   └── run_pipeline.sh
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── database.py
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   ├── report.py
│   └── main.py
└── output/
    └── rapport.txt



## Problèmes de qualité des données traités : 
### Players
- Suppression des doublons sur player_id
- Nettoyage des espaces dans les username
- Conversion des dates invalides
- Suppression des emails invalides

### Scores
- Suppression des doublons sur score_id
- Conversion des types (dates, scores, durées)
- Suppression des scores négatifs ou nuls
- Suppression des scores liés à des joueurs inexistants

## Rapport généré :
- Le fichier output/rapport.txt contient :
- Statistiques générales (joueurs, scores, jeux)
- Top 5 des meilleurs scores
- Score moyen par jeu
- Répartition des joueurs par pays
- Répartition des sessions par plateforme
