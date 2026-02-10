"""Module de chargement des données ETL dans MySQL."""

import pandas as pd

def clean_for_mysql(df: pd.DataFrame) -> pd.DataFrame:
    """Convertit les types Pandas (NaN, NaT) en None pour MySQL."""
    return df.where(pd.notnull(df), None)

def load_players(df: pd.DataFrame, conn):
    """Insère les joueurs transformés dans la table 'players'."""
    df = clean_for_mysql(df)
    cursor = conn.cursor()

    # Requête utilisant 'registration_date' (conforme à ta structure SQL)
    sql = """
    INSERT INTO players (player_id, username, email, registration_date)
    VALUES (%s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        username = VALUES(username),
        email = VALUES(email),
        registration_date = VALUES(registration_date)
    """

    for _, row in df.iterrows():
        cursor.execute(
            sql,
            (
                row["player_id"],
                row["username"],
                row["email"],
                row["registration_date"]
            ),
        )

    conn.commit()
    cursor.close()
    print(f"✅ {len(df)} joueurs chargés ou mis à jour.")

def load_scores(df: pd.DataFrame, conn):
    """Insère les scores transformés dans la table 'scores'."""
    df = clean_for_mysql(df)
    cursor = conn.cursor()

    sql = """
    INSERT INTO scores (score_id, player_id, game, score, duration_minutes, played_at, platform)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        player_id = VALUES(player_id),
        game = VALUES(game),
        score = VALUES(score),
        duration_minutes = VALUES(duration_minutes),
        played_at = VALUES(played_at),
        platform = VALUES(platform)
    """

    for _, row in df.iterrows():
        cursor.execute(
            sql,
            (
                row["score_id"],
                row["player_id"],
                row.get("game", "Inconnu"),
                row["score"],
                row.get("duration_minutes", 0),
                row["played_at"],
                row.get("platform", "PC")
            ),
        )

    conn.commit()
    cursor.close()
    print(f"✅ {len(df)} scores chargés ou mis à jour.")