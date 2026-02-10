import os
import sys
# Ajout de la sécurité pour les imports de modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database import get_connection # Vérifie le nom ici
from src.extract import extract
from src.transform import transform_players, transform_scores
from src.load import load_players, load_scores

def main():
    # 1️⃣ Chemins des fichiers (Le sujet place les fichiers dans data/raw/)
    players_file = "data/raw/Players.csv"
    scores_file = "data/raw/Scores.csv"

    # 2️⃣ Extraction
    print("Extraction...")
    df_players_raw = extract(players_file)
    df_scores_raw = extract(scores_file)

    # 3️⃣ Transformation
    print("Transformation...")
    df_players = transform_players(df_players_raw)
    valid_player_ids = df_players["player_id"].tolist()
    df_scores = transform_scores(df_scores_raw, valid_player_ids)

    # 4️⃣ Chargement
    print("Connexion à la base...")
    conn = get_connection()
    try:
        print("Chargement des joueurs...")
        load_players(df_players, conn)
        print("Chargement des scores...")
        load_scores(df_scores, conn)
        print("Pipeline ETL terminé avec succès !")
    finally:
        conn.close()

if __name__ == "__main__":
    main()