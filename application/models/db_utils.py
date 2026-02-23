# models/db_utils.py

# modules nécessaires
import config               # importer la configuration de l'application
import sqlite3              # pour interagir avec la base de données SQLite

# Fonction pour se connecter à la base de données
def get_db_connection():
    conn = sqlite3.connect(config.DATABASE)
    conn.row_factory = sqlite3.Row
    return conn