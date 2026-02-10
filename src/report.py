"""Module de génération de rapport pour l'ETL."""

import os
from src.database import database_connection
from datetime import datetime

def generate_report(output_path="output/rapport.txt"):
    """
    Génère un rapport synthétique sur la base de données et l'écrit dans output_path.
    """
    
    # --- SÉCURITÉ : Création du dossier output s'il n'existe pas ---
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with database_connection() as conn:
        cursor = conn.cursor()

        # --- Statistiques générales ---
        cursor.execute("SELECT COUNT(*) FROM players;")
        nb_players = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM scores;")
        nb_scores = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(DISTINCT game) FROM scores;")
        nb_games = cursor.fetchone()[0]

        # --- Top 5 des meilleurs scores ---
        cursor.execute("""
            SELECT p.username, s.game, s.score
            FROM scores s
            JOIN players p ON s.player_id = p.player_id
            ORDER BY s.score DESC
            LIMIT 5;
        """)
        top_scores = cursor.fetchall()

        # --- Score moyen par jeu ---
        cursor.execute("""
            SELECT game, AVG(score)
            FROM scores
            GROUP BY game;
        """)
        avg_scores = cursor.fetchall()

        # --- Joueurs par pays ---
        cursor.execute("""
            SELECT country, COUNT(*)
            FROM players
            GROUP BY country
            ORDER BY COUNT(*) DESC;
        """)
        players_by_country = cursor.fetchall()

        # --- Sessions par plateforme ---
        cursor.execute("""
            SELECT platform, COUNT(*)
            FROM scores
            GROUP BY platform
            ORDER BY COUNT(*) DESC;
        """)
        sessions_by_platform = cursor.fetchall()

    # --- Écriture du rapport dans le fichier ---
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("="*50 + "\n")
        f.write("GAMETRACKER - Rapport de synthese\n")
        f.write(f"Genere le : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("="*50 + "\n\n")

        f.write("--- Statistiques generales ---\n")
        f.write(f"Nombre de joueurs : {nb_players}\n")
        f.write(f"Nombre de scores : {nb_scores}\n")
        f.write(f"Nombre de jeux : {nb_games}\n\n")

        f.write("--- Top 5 des meilleurs scores ---\n")
        for i, (username, game, score) in enumerate(top_scores, start=1):
            f.write(f"{i}. {username} | {game} | {score}\n")
        f.write("\n")

        f.write("--- Score moyen par jeu ---\n")
        for game, avg in avg_scores:
            f.write(f"{game} : {avg:.1f}\n")
        f.write("\n")

        f.write("--- Joueurs par pays ---\n")
        for country, count in players_by_country:
            f.write(f"{country} : {count}\n")
        f.write("\n")

        f.write("--- Sessions par plateforme ---\n")
        for platform, count in sessions_by_platform:
            f.write(f"{platform} : {count}\n")

    print(f"✅ Rapport généré avec succès dans '{output_path}'")

# --- TRÈS IMPORTANT : L'appel qui déclenche l'exécution ---
if __name__ == "__main__":
    generate_report()