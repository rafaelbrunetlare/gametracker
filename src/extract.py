import os
import pandas as pd

def extract(filepath: str) -> pd.DataFrame:
    """
    Lit un fichier CSV et retourne un DataFrame pandas.

    Args:
        filepath (str): Chemin vers le fichier CSV.

    Returns:
        pd.DataFrame: Contenu du CSV sous forme de DataFrame.

    Raises:
        FileNotFoundError: Si le fichier n'existe pas.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Le fichier '{filepath}' n'existe pas.")

    df = pd.read_csv(filepath)
    print(f"Extraction terminée : {len(df)} lignes extraites depuis '{filepath}'.")
    return df
