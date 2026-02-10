"""Module de transformation des données ETL."""

import pandas as pd
import numpy as np

def transform_players(df: pd.DataFrame) -> pd.DataFrame:
    """
    Nettoie et prépare les données des joueurs.
    """
    # 1. Copie pour éviter les warnings et suppression des doublons
    df = df.drop_duplicates(subset="player_id").copy()

    # 2. Nettoyage des chaînes de caractères
    df["username"] = df["username"].astype(str).str.strip()

    # 3. Traitement des emails (Sujet : nettoyage des données sales)
    # On met à None les emails invalides
    df["email"] = df["email"].apply(lambda x: x if isinstance(x, str) and "@" in x else None)
    
    # IMPORTANT : On supprime les lignes où l'email ou le pseudo est absent
    # Cela évite l'erreur 'Column email cannot be null'
    df = df.dropna(subset=["email", "username"])

    # 4. Conversion de la date (on garde le nom 'registration_date')
    # Si le fichier CSV utilise un autre nom, on le renomme ici
    if "join_date" in df.columns:
        df = df.rename(columns={"join_date": "registration_date"})
        
    df["registration_date"] = pd.to_datetime(df["registration_date"], errors="coerce")
    
    # On supprime les lignes avec des dates invalides
    df = df.dropna(subset=["registration_date"])

    return df

def transform_scores(df: pd.DataFrame, valid_player_ids: list) -> pd.DataFrame:
    """
    Nettoie les scores et gère les contraintes métier du sujet.
    """
    df = df.drop_duplicates(subset="score_id").copy()

    # Conversion forcée en types numériques et dates
    df["score"] = pd.to_numeric(df["score"], errors="coerce")
    df["player_id"] = pd.to_numeric(df["player_id"], errors="coerce")
    df["played_at"] = pd.to_datetime(df["played_at"], errors="coerce")

    # 1. Contrainte Sujet : "ni scores négatifs"
    df = df[df["score"] >= 0]

    # 2. Suppression des valeurs manquantes critiques
    df = df.dropna(subset=["score", "player_id", "played_at"])

    # 3. Contrainte Sujet : "ni références orphelines"
    # On ne garde que les scores dont le joueur existe dans notre liste nettoyée
    df = df[df["player_id"].isin(valid_player_ids)]

    return df