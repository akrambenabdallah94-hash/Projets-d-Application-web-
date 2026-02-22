# controlers/dashboard_controller.py

# importer les modules nécessaires
from flask import Blueprint, render_template, request # pour gérer les routes et les requêtes
from models import dashboard_utils as dbu                   # pour accéder aux fonctions de manipulation des données

# Créer un Blueprint pour regrouper les routes du tableau de bord
dashboard = Blueprint('dashboard', __name__)

# Route pour afficher le tableau de bord
# Ce tableau de bord affiche des statistiques clés sur la population mondiale en comparant l'évolution des données entre 1950 et 2023
@dashboard.route('/dashboard')
def show_dashboard():
    # Récupérer les statistiques clés
    stats = dbu.generate_population_dashboard()
    
    title = "Indicateurs clés 1950-2023"

    # Rendre le template du tableau de bord avec les statistiques
    return render_template('dashboard.html', stats=stats, title=title)