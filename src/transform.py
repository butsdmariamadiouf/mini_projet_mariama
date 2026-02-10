import pandas as pd
import numpy as np

def transform_players(df: pd.DataFrame) -> pd.DataFrame:
    """Nettoie les données des joueurs (Players)."""
    df = df.copy()

    # 1. Doublons (Problème 1)
    df = df.drop_duplicates(subset=['player_id'])

    # 2. Espaces parasites dans username (Problème 4)
    if 'username' in df.columns:
        df['username'] = df['username'].str.strip()

    # 3. Emails invalides (Problème 2 & 6)
    # On garde seulement les emails avec un '@' et on gère les vides
    df['email'] = df['email'].where(
        df['email'].str.contains('@', na=False) & df['email'].notna(), 
        None
    )

    # 4. Dates incohérentes (Problème 3)
    df['registration_date'] = pd.to_datetime(df['registration_date'], errors='coerce')
    # Conversion en format string YYYY-MM-DD pour MySQL ou garder en datetime
    
    # 5. Niveaux (Optionnel : s'assurer que le level est positif)
    if 'level' in df.columns:
        df['level'] = pd.to_numeric(df['level'], errors='coerce').fillna(0).astype(int)

    print(f" Transformation terminée : {len(df)} joueurs valides.")
    return df

def transform_scores(df: pd.DataFrame, valid_player_ids: pd.Series) -> pd.DataFrame:
    """Nettoie les données des scores et gère les références orphelines."""
    df = df.copy()

    # 1. Doublons (Problème 1)
    df = df.drop_duplicates(subset=['score_id'])

    # 2. Dates incohérentes (Problème 3)
    df['played_at'] = pd.to_datetime(df['played_at'], errors='coerce')

    # 3. Scores négatifs et manquants (Problème 5 & 6)
    df['score'] = pd.to_numeric(df['score'], errors='coerce')
    df = df[df['score'] >= 0] # On supprime les scores négatifs
    df = df.dropna(subset=['score']) # On supprime les scores vides

    # 4. Références orphelines (Problème 7)
    # On ne garde que les scores dont le player_id existe dans la table Players
    initial_count = len(df)
    df = df[df['player_id'].isin(valid_player_ids)]
    orphans_removed = initial_count - len(df)
    
    if orphans_removed > 0:
        print(f"{orphans_removed} scores orphelins supprimés.")

    print(f" Transformation terminée : {len(df)} scores valides.")
    return df