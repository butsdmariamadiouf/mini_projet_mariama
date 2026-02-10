import pandas as pd
import mysql.connector

def load_players(df: pd.DataFrame, conn) -> int:
    """Charge les joueurs dans la table Players."""
    cursor = conn.cursor()
    query = """
    INSERT INTO Players 
    (player_id, username, email, registration_date, country, level)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
    username = VALUES(username),
    email = VALUES(email),
    registration_date = VALUES(registration_date),
    country = VALUES(country),
    level = VALUES(level)
    """
    count = 0
    for _, row in df.iterrows():
        values = (
            int(row['player_id']),
            row['username'],
            row['email'] if pd.notna(row['email']) else None,
            row['registration_date'].strftime('%Y-%m-%d') if pd.notna(row['registration_date']) else None,
            row['country'],
            int(row['level']) if pd.notna(row['level']) else 0
        )
        cursor.execute(query, values)
        count += 1
    
    conn.commit()  # Très important : valide l'insertion
    print(f" Chargement réussi : {count} joueurs insérés/mis à jour.")
    return count

def load_scores(df: pd.DataFrame, conn) -> int:
    """Charge les scores dans la table Scores."""
    cursor = conn.cursor()
    query = """
    INSERT INTO Scores 
    (score_id, player_id, game, score, duration_minutes, played_at, platform)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
    score = VALUES(score),
    duration_minutes = VALUES(duration_minutes),
    platform = VALUES(platform)
    """
    count = 0
    for _, row in df.iterrows():
        values = (
            row['score_id'],
            int(row['player_id']),
            row['game'],
            int(row['score']),
            int(row['duration_minutes']) if pd.notna(row['duration_minutes']) else 0,
            row['played_at'].strftime('%Y-%m-%d %H:%M:%S') if pd.notna(row['played_at']) else None,
            row['platform']
        )
        cursor.execute(query, values)
        count += 1
    
    conn.commit()  # Valide l'insertion
    print(f" Chargement réussi : {count} scores insérés/mis à jour.")
    return count