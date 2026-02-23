# app.py

# Programme principal pour lancer l'application Flask

# Importer les modules nécessaires
from flask import Flask                                 # pour créer l'application Flask
from controllers.main_controller import main            # importer le Blueprint principal 
from controllers.dashboard_controller import dashboard  # importer le Blueprint du tableau de bord

# Créer l'application Flask
app = Flask(__name__)

# Enregistrer les Blueprints
# Le Blueprint 'main' gère la route principale de l'application
app.register_blueprint(main)
# Le Blueprint 'dashboard' gère la route du tableau de bord
app.register_blueprint(dashboard)

# Lancer l'application Flask
if __name__ == '__main__':
    # Lancer l'application en mode debug sur localhost via le port 5000
    app.run(host='127.0.0.1', port=5000, debug=True)

    # Après avoir lancé l'application, accédez à l'URL suivante dans un navigateur web :
    # http://127.0.0.1:5000
