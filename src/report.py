import datetime
from src.database import database_connection

def generate_report():
    print("Génération du rapport en cours...")
    
    try:
        with database_connection() as conn:
            cursor = conn.cursor(dictionary=True) # dictionary=True pour manipuler les noms de colonnes facilement

            # 1. Statistiques générales
            cursor.execute("SELECT COUNT(*) as nb FROM Players")
            nb_players = cursor.fetchone()['nb']
            
            cursor.execute("SELECT COUNT(*) as nb FROM Scores")
            nb_scores = cursor.fetchone()['nb']
            
            cursor.execute("SELECT COUNT(DISTINCT game) as nb FROM Scores")
            nb_games = cursor.fetchone()['nb']

            # 2. Top 5 des meilleurs scores (avec JOIN)
            cursor.execute("""
                SELECT p.username, s.game, s.score 
                FROM Scores s
                JOIN Players p ON s.player_id = p.player_id
                ORDER BY s.score DESC
                LIMIT 5
            """)
            top_5 = cursor.fetchall()

            # 3. Score moyen par jeu
            cursor.execute("SELECT game, AVG(score) as avg_score FROM Scores GROUP BY game")
            avg_scores = cursor.fetchall()

            # 4. Répartition par pays
            cursor.execute("SELECT country, COUNT(*) as nb FROM Players GROUP BY country ORDER BY nb DESC")
            countries = cursor.fetchall()

            # 5. Répartition par plateforme
            cursor.execute("SELECT platform, COUNT(*) as nb FROM Scores GROUP BY platform ORDER BY nb DESC")
            platforms = cursor.fetchall()

        # Écriture du fichier rapport.txt
        with open("output/rapport.txt", "w", encoding="utf-8") as f:
            f.write("=" * 52 + "\n")
            f.write("GAMETRACKER - Rapport de synthese\n")
            f.write(f"Genere le : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 52 + "\n\n")

            f.write("--- Statistiques generales ---\n")
            f.write(f"Nombre de joueurs : {nb_players}\n")
            f.write(f"Nombre de scores : {nb_scores}\n")
            f.write(f"Nombre de jeux : {nb_games}\n\n")

            f.write("--- Top 5 des meilleurs scores ---\n")
            for i, row in enumerate(top_5, 1):
                f.write(f"{i}. {row['username']} | {row['game']} | {row['score']}\n")
            
            f.write("\n--- Score moyen par jeu ---\n")
            for row in avg_scores:
                f.write(f"{row['game']} : {row['avg_score']:.1f}\n")

            f.write("\n--- Joueurs par pays ---\n")
            for row in countries:
                country_name = row['country'] if row['country'] else "Inconnu"
                f.write(f"{country_name} : {row['nb']}\n")

            f.write("\n--- Sessions par plateforme ---\n")
            for row in platforms:
                f.write(f"{row['platform']} : {row['nb']}\n")

            f.write("\n" + "=" * 52)

        print("Rapport généré avec succès dans output/rapport.txt")

    except Exception as e:
        print(f"Erreur lors de la génération du rapport : {e}")

if __name__ == "__main__":
    generate_report()