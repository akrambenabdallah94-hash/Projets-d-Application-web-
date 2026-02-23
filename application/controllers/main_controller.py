# controllers/main_controller.py

# importer les modules nécessaires
import io
import csv
import pandas as pd # NOUVEAU : pour la gestion Excel
from flask import Blueprint, render_template, request, Response # pour gérer les routes, requêtes et réponses
from models import data_utils as du                   # pour accéder aux fonctions de manipulation des données

# Créer un Blueprint pour regrouper les routes
main = Blueprint('main', __name__)

# --- NOUVELLE FONCTION UTILITAIRE (pour éviter de répéter le code dans CSV et Excel) ---
def get_data_for_query(query_type):
    if query_type == 'world':
        return du.get_world_population_by_year(), ["Année", "Hommes", "Femmes", "Total"]
    elif query_type == 'continent':
        return du.get_population_by_continent(), ["Continent", "Année", "Population"]
    elif query_type == 'sex_ratio':
        return du.get_sex_ratio_data(), ["Année", "Population Masculine", "Population Féminine", "Ratio"]
    elif query_type == 'region':
        return du.get_population_by_region(), ["Région", "Année", "Population"]
    elif query_type == 'top10':
        return du.get_top_10_countries(), ["Année", "Pays", "Sous-région", "Région", "Continent", "Population"]
    elif query_type == 'europe':
        return du.get_europe_population_by_year(), ["Année", "Pays", "Population", "Densité"]
    # AJOUT : Part de population par pays dans sa région
    elif query_type == 'share':
        return du.get_country_region_share(), ["Région", "Pays", "Année", "Pop. Pays", "Pop. Région", "Part (%)"]
    
    return [], []

@main.route('/')
def index():
    # Récupérer les paramètres d'URL
    query_type = request.args.get('query', 'world') # Par défaut : population mondiale
    view_type = request.args.get('view', 'table')  # Par défaut : tableau

    # Utiliser la fonction utilitaire pour les données de base
    data, headers = get_data_for_query(query_type)
    
    # Titre spécifique
    titles = {
        'world': "Population mondiale par année",
        'continent': "Répartition par Continent",
        'sex_ratio': "Ratio Homme/Femme (1950-2023)",
        'region': "Population par région et par année",
        'top10': "Top 10 des pays les plus peuplés par année",
        'europe': "Population des pays d'Europe par année",
        'share': "Part de la population par pays dans sa région", # AJOUT TITRE
        'about': "Informations sur le projet"
    }
    title = titles.get(query_type, "Aucune donnée")

    if query_type == 'about':
        data = du.get_about_data()
        headers = []
    
    # --- GÉNÉRATION DES GRAPHIQUES ---
    plot_html = None

    if view_type == 'graph':
        if query_type == 'world': plot_html = du.generate_population_plot()
        elif query_type == 'continent': plot_html = du.generate_continent_pie_plot()
        elif query_type == 'sex_ratio': plot_html = du.generate_sex_ratio_plot()
        elif query_type == 'region': plot_html = du.generate_region_plot()
        elif query_type == 'top10': plot_html = du.generate_top_10_bar_plot()
        # AJOUT : Génération du graphique pour la part de population
        elif query_type == 'share': plot_html = du.generate_share_treemap()
    
    elif query_type == 'europe' and view_type == 'dens_map':
        plot_html = du.generate_europe_dens_map()

    return render_template(
        'index.html',
        data=data,
        title=title,
        headers=headers,
        query_type=query_type,
        view_type=view_type,
        plot_html=plot_html
    )

@main.route('/download_csv')
def download_csv():
    query_type = request.args.get('query', 'world')
    data, headers = get_data_for_query(query_type)

    if not data:
        return "Type de données non supporté", 400

    output = io.StringIO()
    writer = csv.writer(output, delimiter=';') 
    writer.writerow(headers)
    writer.writerows(data)
    
    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-disposition": f"attachment; filename=export_{query_type}.csv"}
    )

# --- NOUVELLE ROUTE : TÉLÉCHARGEMENT EXCEL ---
@main.route('/download_excel')
def download_excel():
    query_type = request.args.get('query', 'world')
    data, headers = get_data_for_query(query_type)

    if not data:
        return "Type de données non supporté", 400

    # Création du DataFrame
    df = pd.DataFrame(data, columns=headers)

    # Création du fichier Excel en mémoire
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Données')
    
    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-disposition": f"attachment; filename=export_{query_type}.xlsx"}
    )