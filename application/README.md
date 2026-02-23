# Application Web de Visualisation de Données Démographiques
 
##  Description du projet
 
Ce projet consiste à développer une application web permettant la **visualisation et l’analyse de données démographiques mondiales** à partir d’une base de données SQLite.
 
L’application est développée en **Python avec Flask** et repose sur une architecture **MVC (Modèle – Vue – Contrôleur)**.  
Elle propose des **graphiques interactifs**, des **tableaux dynamiques** et des **cartes géographiques** afin de rendre les données accessibles et compréhensibles pour tout type d’utilisateur.
 
Ce projet est réalisé dans le cadre de la **SAE 1.01 / SAE 1.04 – Données démographiques mondiales** du **BUT Informatique**.
 
---
 
##  Objectifs
 
- Visualiser l’évolution de la population mondiale
- Comparer les pays, régions et continents
- Analyser des indicateurs démographiques clés
- Proposer une interface claire, interactive et intuitive
- Appliquer une architecture logicielle propre (MVC)
 
---
 
##  Architecture du projet
 
code-SAE101-beta/
│
├── app.py # Point d’entrée de l’application Flask
├── config.py # Configuration (base de données, GeoJSON)
│
├── controllers/ # Contrôleurs (routes et logique applicative)
│ ├── main_controller.py
│ └── dashboard_controller.py
│
├── models/ # Modèles (accès et traitement des données)
│ ├── db_utils.py
│ ├── data_utils.py
│ └── dashboard_utils.py
│
├── database/
│ └── WorldPopulation.db # Base de données SQLite
│
├── templates/ # Vues HTML (Jinja2)
│ ├── home.html
│ ├── index.html
│ ├── dashboard.html
│ └── header.html
│
├── static/ # Fichiers statiques
│ ├── css/
│ │ ├── style.css
│ │ └── home.css
│ ├── geojson/
│ └── images/
│
└── README.md
 
 
---
 
##  Prérequis techniques
 
- **Python 3.x**
- Bibliothèques Python :
  - Flask
  - pandas
  - plotly
  - folium
 
> Le module `sqlite3` est inclus par défaut avec Python.
 
---
 
##  Installation
 
### 1️ Récupération du projet
 
Cloner ou télécharger le projet puis se placer dans le dossier :
 
```bash
cd code-SAE101-beta
Installation des dépendances
pip install Flask pandas plotly folium
Lancement de l’application
Dans le dossier du projet :
 
python app.py
Puis ouvrir un navigateur et accéder à :
 
http://127.0.0.1:5000
Fonctionnalités principales
Population mondiale par année (1950–2023)
Population par continent et par région
Top 10 des pays les plus peuplés
Ratio homme / femme
Taux de migration par pays
Cartes interactives de densité (Europe)
Espérance de vie
Prévisions de population sur 50 ans (2023–2073)
Tableaux interactifs (tri, recherche, filtres)
Tableau de bord avec KPI
Navigation centralisée via un menu commun
 
Architecture MVC
L’application suit le modèle MVC :
Modèle
Accès à la base de données SQLite
Traitement et préparation des données avec Pandas
Fichiers : db_utils.py, data_utils.py, dashboard_utils.py
 
Vue
Templates HTML avec Jinja2
Composants réutilisables (header.html)
Graphiques et cartes intégrés (Plotly, Leaflet)
Contrôleur
Gestion des routes Flask
Utilisation de Blueprints pour organiser l’application
Routage dynamique selon les paramètres URL
Cette architecture améliore la lisibilité, la maintenance et l’évolution du projet.
 
🛠 Technologies utilisées
Python
Flask
SQLite
Pandas
Plotly
Folium / Leaflet
Jinja2
HTML / CSS
DataTables
 
Auteurs
Projet réalisé par :
MARDAUS Sebastien
PARIMELALAGAN Rakul
HARMALKAR Sumith
BEN ABDALLAH Akram
CHAMBI LEBLANC Rémy
 
Remarques
La base de données WorldPopulation.db est indispensable au fonctionnement
Les fichiers GeoJSON sont utilisés pour l’affichage des cartes
L’application est lancée en mode debug=True pour le développement
Améliorations possibles
Ajout de filtres avancés (années, pays, régions)
Export des données (CSV / Excel)
Analyses statistiques avancées
Prévisions plus détaillées
Amélioration du design (Bootstrap, Tailwind)
Authentification utilisateur
 
Conclusion
Ce projet combine la légèreté de Flask, la puissance de Pandas et l’interactivité de Plotly pour offrir une application claire et pédagogique autour des données démographiques mondiales.
Grâce à une architecture MVC solide, l’application constitue une base fiable et évolutive pour l’analyse de données à grande échelle.
