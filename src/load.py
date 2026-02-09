"""Module de chargement des données ETL dans MySQL."""

import pandas as pd
from mysql.connector import Error


def clean_for_mysql(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convertit les NaN/NaT en None pour être compatible avec MySQL.
    """
    return df.where(pd.notnull(df), None)


def load_players(df: pd.DataFrame, conn):
    """
    Insère ou met à jour les joueurs dans la table 'players'.
    
    Args:
        df (pd.DataFrame): DataFrame des joueurs transformés.
        conn: Connexion MySQL active.
    """
    df = clean_for_mysql(df)
    cursor = conn.cursor()

    sql = """
    INSERT INTO players (player_id, username, email, registration_date, country, level)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        username = VALUES(username),
        email = VALUES(email),
        registration_date = VALUES(registration_date),
        country = VALUES(country),
        level = VALUES(level)
    """

    for _, row in df.iterrows():
        cursor.execute(
            sql,
            (
                row["player_id"],
                row["username"],
                row["email"],
                row["registration_date"],
                row["country"],
                row["level"],
            ),
        )

    conn.commit()
    cursor.close()
    print(f"{len(df)} joueurs chargés ou mis à jour.")


def load_scores(df: pd.DataFrame, conn):
    """
    Insère ou met à jour les scores dans la table 'scores'.
    
    Args:
        df (pd.DataFrame): DataFrame des scores transformés.
        conn: Connexion MySQL active.
    """
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
                row["game"],
                row["score"],
                row["duration_minutes"],
                row["played_at"],
                row["platform"],
            ),
        )

    conn.commit()
    cursor.close()
