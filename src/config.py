"""Configuration du projet ETL."""
import os

class Config:
    """Configuration centralisée via variables d'environnement."""

    DB_HOST = os.environ.get('DB_HOST', 'db')
    DB_PORT = int(os.environ.get('DB_PORT', 3306))
    DB_NAME = os.environ.get('DB_NAME', 'gametracker')
    DB_USER = os.environ.get('DB_USER', 'user_gt')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'user_password')
    DATA_DIR = os.environ.get('DATA_DIR', '/app/data/raw')