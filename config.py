# config.py

# Configuration de l'application : chemins de la base de données et des fichiers geojson

# Importer le module os pour gérer les chemins de fichiers
import os

# Définir le chemin de la base de données SQLite
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_NAME = 'WorldPopulation.db'
DATABASE = os.path.join(BASE_DIR, 'database', DB_NAME)

# Définir la résolution des frontières geojson utilisées pour les cartes
GEOJSON_03M = os.path.join(BASE_DIR, 'static/geojson', 'CNTR_RG_03M_2024_4326.geojson')
GEOJSON_10M = os.path.join(BASE_DIR, 'static/geojson', 'CNTR_RG_10M_2024_4326.geojson')
GEOJSON_20M = os.path.join(BASE_DIR, 'static/geojson', 'CNTR_RG_20M_2024_4326.geojson')