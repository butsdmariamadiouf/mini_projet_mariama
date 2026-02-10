from src.config import Config
from src.database import database_connection
from src.extract import extract
from src.transform import transform_players, transform_scores
from src.load import load_players, load_scores
from src.report import generate_report # Ne pas oublier l'étape 4

def run_pipeline():
    print("=" * 50)
    print("PIPELINE ETL GAMETRACKER - ORCHESTRATION")
    print("=" * 50)

    try:
        with database_connection() as conn:
            # 1. TRAITEMENT DES JOUEURS (Indispensable avant les scores)
            print("\n>>> ETAPE 1 : JOUEURS")
            df_players_raw = extract(f"{Config.DATA_DIR}/Players.csv")
            df_players_clean = transform_players(df_players_raw)
            load_players(df_players_clean, conn)
            
            # On récupère les IDs valides pour l'étape suivante (Contrainte 5.1)
            valid_ids = df_players_clean['player_id']

            # 2. TRAITEMENT DES SCORES
            print("\n>>> ETAPE 2 : SCORES")
            df_scores_raw = extract(f"{Config.DATA_DIR}/Scores.csv")
            # On passe les valid_ids ici pour filtrer les orphelins
            df_scores_clean = transform_scores(df_scores_raw, valid_player_ids=valid_ids)
            load_scores(df_scores_clean, conn)

            # 3. GENERATION DU RAPPORT
            print("\n>>> ETAPE 3 : RAPPORT")
            generate_report()

        print("\n" + "=" * 50)
        print("PROJET TERMINE AVEC SUCCES !")
        print("=" * 50)

    except Exception as e:
        print(f"\n[ERREUR CRITIQUE] : {e}")
        import sys
        sys.exit(1)

if __name__ == '__main__':
    run_pipeline()