"""Module de transformation des données ETL."""

import pandas as pd
import numpy as np


def transform_players(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transforme le DataFrame des joueurs.

    Étapes :
    1. Supprime les doublons sur player_id
    2. Nettoie les espaces des username
    3. Convertit les dates d'inscription
    4. Remplace les emails invalides (sans '@') par None
    """
    df = df.drop_duplicates(subset="player_id").copy()

    # Nettoyage des username
    df["username"] = df["username"].astype(str).str.strip()

    # Conversion de la date d'inscription
    df["registration_date"] = pd.to_datetime(df["registration_date"], errors="coerce")

    # Emails invalides -> None
    df["email"] = df["email"].apply(lambda x: x if isinstance(x, str) and "@" in x else None)

    return df


def transform_scores(df: pd.DataFrame, valid_player_ids: list) -> pd.DataFrame:
    """
    Transforme le DataFrame des scores.

    Étapes :
    1. Supprime les doublons sur score_id
    2. Convertit les dates et les scores en types appropriés
    3. Supprime les lignes avec un score négatif ou nul
    4. Supprime les scores dont le player_id n'est pas dans valid_player_ids
    """
    df = df.drop_duplicates(subset="score_id").copy()

    # Conversion des colonnes
    df["score"] = pd.to_numeric(df["score"], errors="coerce")
    df["duration_minutes"] = pd.to_numeric(df["duration_minutes"], errors="coerce")
    df["played_at"] = pd.to_datetime(df["played_at"], errors="coerce")
    df["player_id"] = pd.to_numeric(df["player_id"], errors="coerce")

    # Supprimer les scores <= 0
    df = df[df["score"] > 0]

    # Supprimer les références orphelines
    df = df[df["player_id"].isin(valid_player_ids)]

    return df
