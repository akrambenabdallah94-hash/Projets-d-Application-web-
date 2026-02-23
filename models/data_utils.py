# models/data_utils.py

# modules nécessaires
import config                   # importer la configuration de l'application
from models.db_utils import get_db_connection # pour se connecter à la base de données
import json                 # pour manipuler les données GeoJSON
import plotly.express as px # pour la création de graphiques interactifs
import pandas as pd         # pour la manipulation et l'analyse des données 
import folium               # pour la création de cartes interactives

###################################################################
# NOUVEL ONGLET : Part des pays dans la région (Treemap)

# models/data_utils.py

# ... (garder les autres imports)

def get_country_region_share():
    conn = get_db_connection()
    cursor = conn.cursor()
    # Nouvelle requête SQL fournie
    query = """
    SELECT
        r.name        AS region,
        c.name        AS country,
        fp.year       AS year,
        SUM(fp."TOTAL POPULATION. AS OF 1 JULY (THOUSANDS)" * 1000) AS country_population,
        rt.region_population,
        ROUND(
            (SUM(fp."TOTAL POPULATION. AS OF 1 JULY (THOUSANDS)" * 1000)
            / rt.region_population) * 100, 
            2
        ) AS population_rate_percent
    FROM fact_population fp
    JOIN country c    ON fp.location_code = c.location_code
    JOIN subregion sr ON c.parent_code = sr.location_code
    JOIN region r     ON sr.parent_code = r.location_code
    JOIN (
        SELECT
            r2.location_code,
            fp2.year,
            SUM(fp2."TOTAL POPULATION. AS OF 1 JULY (THOUSANDS)" * 1000) AS region_population
        FROM fact_population fp2
        JOIN country c2    ON fp2.location_code = c2.location_code
        JOIN subregion sr2 ON c2.parent_code = sr2.location_code
        JOIN region r2     ON sr2.parent_code = r2.location_code
        GROUP BY r2.location_code, fp2.year
    ) rt
      ON rt.location_code = r.location_code
     AND rt.year = fp.year
    GROUP BY
        r.name,
        c.name,
        fp.year,
        rt.region_population
    ORDER BY
        fp.year DESC,
        r.name,
        population_rate_percent DESC;
    """
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

def generate_share_treemap():
    data = get_country_region_share()
    # Adaptation des colonnes au DataFrame pour le Treemap
    df = pd.DataFrame(data, columns=["Région", "Pays", "Année", "Pop. Pays", "Pop. Région", "Part (%)"])
    
    latest_year = df['Année'].max()
    df_latest = df[df['Année'] == latest_year]

    fig = px.treemap(
        df_latest, 
        path=[px.Constant("Monde"), 'Région', 'Pays'], 
        values='Pop. Pays',
        color='Part (%)',
        hover_data=['Part (%)'],
        color_continuous_scale='RdBu',
        title=f"Répartition de la population par pays et région ({latest_year})"
    )
    
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
    return fig.to_html(full_html=False)



###################################################################
# NOUVEL ONGLET : Ratio H/F (CORRIGÉ)

def get_sex_ratio_data():
    conn = get_db_connection()
    cursor = conn.cursor() # <--- Modification effectuée ici
    # On calcule le ratio (Hommes/Femmes * 100) directement en SQL
    query = """
    SELECT
        year,
        "MALE POPULATION. AS OF 1 JULY (THOUSANDS)" * 1000 AS male_pop,
        "FEMALE POPULATION. AS OF 1 JULY (THOUSANDS)" * 1000 AS female_pop,
        ROUND(("MALE POPULATION. AS OF 1 JULY (THOUSANDS)" * 1.0 / 
               "FEMALE POPULATION. AS OF 1 JULY (THOUSANDS)") * 100, 2) AS ratio
    FROM fact_population
    WHERE location_code = 900 
      AND year BETWEEN 1950 AND 2023
    ORDER BY year;
    """
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

def generate_sex_ratio_plot():
    data = get_sex_ratio_data()
    df = pd.DataFrame(data, columns=["Année", "Hommes", "Femmes", "Ratio"])
    
    fig = px.line(df, x="Année", y="Ratio", 
                  title="Évolution du Sex-Ratio mondial (Nombre d'hommes pour 100 femmes)",
                  labels={"Ratio": "Hommes pour 100 Femmes"})
    
    # Ajout d'une ligne de référence à 100 (équilibre parfait)
    fig.add_hline(y=100, line_dash="dash", line_color="red", annotation_text="Équilibre (100)")
    
    fig.update_layout(hovermode="x unified")
    return fig.to_html(full_html=False)

###################################################################
# NOUVEL ONGLET : Population par Continent (item "Continents")

def get_population_by_continent():
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
        SELECT 
            CASE 
                WHEN r.name LIKE '%Africa%' THEN 'Africa'
                WHEN r.name LIKE '%Europe%' THEN 'Europe'
                WHEN r.name LIKE '%Asia%' THEN 'Asia'
                WHEN r.name LIKE '%Northern America%' THEN 'North America'
                WHEN r.name LIKE '%South America%' THEN 'South America'
                WHEN r.name LIKE '%Oceania%' THEN 'Oceania'
                ELSE 'Other'
            END AS continent,
            fp.year AS year,
            SUM(fp."TOTAL POPULATION. AS OF 1 JULY (THOUSANDS)" * 1000) AS population
        FROM fact_population fp
        JOIN region r ON fp.location_code = r.location_code
        GROUP BY continent, fp.year
        ORDER BY fp.year, population DESC;
    """
    try:
        cursor.execute(query)
        results = cursor.fetchall()
    except Exception as e:
        print(f"Erreur SQL : {e}")
        results = []
    finally:
        conn.close()
    return results

def generate_continent_pie_plot():
    data = get_population_by_continent()
    # On définit bien les 3 colonnes ici
    df = pd.DataFrame(data, columns=["Continent", "Année", "Population"])
    
    fig = px.pie(df, values='Population', names='Continent', 
                  title="Répartition de la population mondiale par continent (2023)",
                  hole=0.4, 
                  color_discrete_sequence=px.colors.sequential.RdBu)
    
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)')
    return fig.to_html(full_html=False)

###################################################################
# Population mondiale par sexe et par année (item "Population mondiale")

def get_world_population_by_year():
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
        SELECT
            year,
            SUM(CASE WHEN   fp."MALE POPULATION. AS OF 1 JULY (THOUSANDS)" IS NOT NULL
                     THEN fp."MALE POPULATION. AS OF 1 JULY (THOUSANDS)" * 1000
                     ELSE 0 END) AS male_population,
            SUM(CASE WHEN   fp."FEMALE POPULATION. AS OF 1 JULY (THOUSANDS)" IS NOT NULL
                     THEN fp."FEMALE POPULATION. AS OF 1 JULY (THOUSANDS)" * 1000   
                     ELSE 0 END) AS female_population,
            SUM(CASE WHEN fp."MALE POPULATION. AS OF 1 JULY (THOUSANDS)" IS NOT NULL
                     THEN fp."MALE POPULATION. AS OF 1 JULY (THOUSANDS)" * 1000
                     ELSE 0 END) +
            SUM(CASE WHEN fp."FEMALE POPULATION. AS OF 1 JULY (THOUSANDS)" IS NOT NULL
                     THEN fp."FEMALE POPULATION. AS OF 1 JULY (THOUSANDS)" * 1000
                     ELSE 0 END) AS total_population
        FROM
            fact_population fp
        WHERE
            fp.location_code IN (SELECT location_code FROM region)
        GROUP BY
            fp.year
        ORDER BY
            fp.year;
    """
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

def generate_population_plot():
    data = get_world_population_by_year()
    df = pd.DataFrame(data, columns=["Année", "Hommes", "Femmes", "Total"])
    fig = px.area(
        df,
        x="Année",
        y=["Hommes", "Femmes"],
        title="Évolution de la population mondiale par sexe",
        labels={"value": "Population", "Année": "Année", "variable": "Sexe"},
    )
    fig.add_scatter(
        x=df["Année"],
        y=df["Total"],
        mode="lines",
        name="Total (H+F)",
        line=dict(color="black", width=4),
        opacity=0.7,
    )
    fig.update_layout(
        xaxis_title="Année",
        yaxis_title="Population mondiale",
        hovermode="x unified",
    )
    return fig.to_html(full_html=False)

###################################################################
# Récupérer la population par région et par année (item "Population par région")

def get_population_by_region():
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
        SELECT
            r.name AS region_name,
            fp.year,
            SUM(fp."TOTAL POPULATION. AS OF 1 JULY (THOUSANDS)" * 1000) AS total_population
        FROM
            fact_population fp
        JOIN
            region r ON fp.location_code = r.location_code
        GROUP BY
            r.name, fp.year
        ORDER BY
            r.name, fp.year;
    """
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

def generate_region_plot():
    data = get_population_by_region()
    df = pd.DataFrame(data, columns=["Région", "Année", "Population"])
    fig = px.line(df, x="Année", y="Population", color="Région",
                  title="Évolution de la population par région",
                  markers=True)    
    fig.update_layout(
        xaxis_title="Année",
        yaxis_title="Population",
        hovermode="x unified",
    )
    return fig.to_html(full_html=False)

###################################################################
# Récupérer le top 10 des pays les plus peuplés (item "Top 10")

def get_top_10_countries():
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
        SELECT
            year, country_name, subregion_name, region_name, continent_name, population
        FROM (
            SELECT
                fp.year,
                c.name AS country_name,
                sr.name AS subregion_name,
                r.name AS region_name,
                ct.name AS continent_name,
                fp."TOTAL POPULATION. AS OF 1 JULY (THOUSANDS)" * 1000 AS population,
                ROW_NUMBER() OVER (
                    PARTITION BY fp.year
                    ORDER BY fp."TOTAL POPULATION. AS OF 1 JULY (THOUSANDS)" * 1000 DESC
                ) AS rn
            FROM fact_population fp
            JOIN country c ON fp.location_code = c.location_code
            JOIN subregion sr ON c.parent_code = sr.location_code
            JOIN region r ON sr.parent_code = r.location_code
            JOIN continent ct ON r.parent_code = ct.location_code
        )
        WHERE rn <= 10
        ORDER BY year, population DESC;
    """
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

def generate_top_10_bar_plot():
    data = get_top_10_countries()
    df = pd.DataFrame(data, columns=[ "Année", "Pays", "Sous-région", "Région", "Continent", "Population"])
    fig = px.bar(
        df,
        x="Pays",
        y="Population",
        labels={"Population": "Population", "Pays": "Pays"},
        color_discrete_sequence=["#F3B94E"],
        animation_frame="Année",
        title="Top 10 des pays les plus peuplés suivant l'année",
    )
    ymax = 1.2*df["Population"].max()
    fig.update_layout(
        xaxis_title="Pays",
        yaxis_title="Population",
        xaxis={'categoryorder': 'total descending', 'tickangle': 10},
        yaxis=dict(range=[0, ymax])
    )
    return fig.to_html(full_html=False)

###################################################################
# Démographie européenne (item "Europe")

def get_europe_population_by_year():
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
    SELECT
        fp.year, c.name AS country_name,
        fp."TOTAL POPULATION. AS OF 1 JULY (THOUSANDS)" * 1000 AS population,
        fp."POPULATION DENSITY. AS OF 1 JULY (PERSONS PER SQUARE KM)" AS population_density
    FROM fact_population fp
    JOIN country c ON fp.location_code = c.location_code
    JOIN subregion s ON c.parent_code = s.location_code
    JOIN region r ON s.parent_code = r.location_code
    WHERE r.name = 'Europe'
    ORDER BY c.name, fp.year;
    """
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

def generate_europe_dens_map():
    data = get_europe_population_by_year()
    df = pd.DataFrame(data, columns=["Année", "Pays", "Population", "Densité"])
    latest_year = 2023
    df_latest = df[df["Année"] == latest_year]
    
    # Nettoyage micro-états
    for p in ["Monaco", "Gibraltar", "Holy See", "Malta", "San Marino", "Guernsey", "Jersey"]:
        df_latest = df_latest[df_latest["Pays"] != p]

    with open(config.GEOJSON_10M, 'r', encoding='utf-8') as f:
        geojson_data = json.load(f)

    europe_countries = df_latest["Pays"].unique().tolist()
    dens_dict = df_latest.set_index("Pays")["Densité"].to_dict()

    filtered_features = []
    for feature in geojson_data["features"]:
        country_name = feature["properties"].get("NAME_ENGL")
        if country_name in europe_countries:
            feature["properties"]["DENSITÉ"] = float(dens_dict[country_name])
            filtered_features.append(feature)
    geojson_data["features"] = filtered_features

    m = folium.Map(location=[60, 74], zoom_start=3, width="100%", height="450px")
    folium.Choropleth(
        geo_data=geojson_data,
        name="Densité",
        data=df_latest,
        columns=["Pays", "Densité"],
        key_on="feature.properties.NAME_ENGL",
        fill_color="YlGnBu",
        bins=[0, 50, 100, 200, 400, df_latest["Densité"].max()],
        fill_opacity=0.6,
        line_opacity=0.4,
        legend_name="Densité (hab/km²)"
    ).add_to(m)

    folium.GeoJson(
        geojson_data,
        style_function=lambda x: {'weight': 1, 'color': 'black', 'fillOpacity': 0},
        tooltip=folium.GeoJsonTooltip(fields=["NAME_ENGL", "DENSITÉ"], aliases=["Pays :", "Densité :"])
    ).add_to(m)

    return m._repr_html_()

###################################################################
# Informations sur le projet (item "À propos")

def get_about_data():
    about = [
        ["Projet", "Visualisation des données de population mondiale de 1950 à 2023"],
        ["Source(s) des données", "Base de données World Population Prospects 2024 de l'ONU"],
        ["Auteur(s)", "Nom(s) de l'auteur ou des auteurs"],
        ["Année", "2025-2026"],
        ["Technologies", "Python, Flask, SQLite, Plotly, Pandas, DataTables, Folium."],
    ]
    return about