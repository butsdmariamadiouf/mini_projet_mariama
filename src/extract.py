import pandas as pd
from pathlib import Path

def extract(filepath: str) -> pd.DataFrame:
    """
    Extrait les données d'un fichier CSV de manière sécurisée.
    
    Args:
        filepath: Chemin vers le fichier CSV.
        
    Returns:
        pd.DataFrame: Le contenu du fichier.
        
    Raises:
        FileNotFoundError: Si le fichier est absent.
        pd.errors.EmptyDataError: Si le fichier est vide.
    """
    path = Path(filepath)
    
    # 1. Vérification de l'existence
    if not path.exists():
        raise FileNotFoundError(f" Erreur : Le fichier est introuvable à l'adresse : {path.absolute()}")
    
    # 2. Tentative de lecture
    try:
        df = pd.read_csv(filepath)
        
        # 3. Vérification si le fichier est vide
        if df.empty:
            print(f" Attention : Le fichier {path.name} est vide.")
        else:
            print(f" Extraction réussie : {len(df)} lignes lues depuis {path.name}")
            
        return df

    except pd.errors.EmptyDataError:
        print(f" Erreur : Le fichier {path.name} ne contient aucune donnée.")
        raise
    except Exception as e:
        print(f" Erreur inattendue lors de la lecture de {path.name} : {e}")
        raise