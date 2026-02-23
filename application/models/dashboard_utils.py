# models/dashboard_utils.py

import pandas as pd
from models import data_utils as du
from models.db_utils import get_db_connection
import locale

# Configurer la locale pour le formatage des nombres en français
locale.setlocale(locale.LC_NUMERIC, 'fr_FR.UTF-8')

# indicateurs clés sur les différentes mesures démographiques et leur évolution entre 1950 et 2023
# les différents indicateurs sont assemblés ausein d'une même page HTML pour former un tableau de bord
# Chaque indicateur est représenté sous forme d'une carte de type "carte de visite" (card)

# Récupération de la mortalité, de l'espérance de vie et du taux de natalité mondiale par année
def get_additional_demographic_data():
    # Connection à la base de données
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
    SELECT
        year, 
        "LIFE EXPECTANCY AT BIRTH. BOTH SEXES (YEARS)" AS life_expectancy,
        "CRUDE DEATH RATE (DEATHS PER 1.000 POPULATION)" AS mortality_rate,
        "CRUDE BIRTH RATE (BIRTHS PER 1.000 POPULATION)" AS birth_rate
    FROM fact_population
    WHERE year IN (1950, 2023) AND location_code = '900'
    ORDER BY year;
    """
    # Exécuter la requête, récupérer et renvoyer les résultats
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

def generate_population_dashboard():
    # Récupérer les données nécessaires
    data = du.get_world_population_by_year()

    # Créer un DataFrame Pandas avec les données
    df = pd.DataFrame(data, columns=["Année", "Hommes", "Femmes", "Total"])

    # Indicateur 1 : Population mondiale en 1950
    population_1950 = df[df["Année"] == 1950]["Total"].values[0]

    # Indicateur 2 : Population mondiale en 2023
    population_2023 = df[df["Année"] == 2023]["Total"].values[0]

    # Indicateur 3 : Croissance de la population entre 1950 et 2023
    growth_population = ((population_2023 - population_1950) / population_1950) * 100

    # Indicateur 4 : Population masculine en 1950
    male_population_1950 = df[df["Année"] == 1950]["Hommes"].values[0]

    # Indicateur 5 : Population masculine en 2023
    male_population_2023 = df[df["Année"] == 2023]["Hommes"].values[0]

    #Indicateur 6 : Croissance de la population masculine entre 1950 et 2023
    growth_male_population = ((male_population_2023 - male_population_1950) / male_population_1950) * 100

    # Indicateur 7 : Population féminine en 1950
    female_population_1950 = df[df["Année"] == 1950]["Femmes"].values[0]

    # Indicateur 8 : Population féminine en 2023
    female_population_2023 = df[df["Année"] == 2023]["Femmes"].values[0]

    # Indicateur 9 : Croissance de la population féminine entre 1950 et 2023
    growth_female_population = ((female_population_2023 - female_population_1950) / female_population_1950) * 100

    additional_data = get_additional_demographic_data()
    
    # Indicateurs 11 : variation de l'espérance de vie entre 1950 et 2023 (en %)
    life_expectancy_1950 = additional_data[0][1]
    life_expectancy_2023 = additional_data[1][1]
    growth_life_expectancy = ((life_expectancy_2023 - life_expectancy_1950) / life_expectancy_1950) * 100
    
    # Indicateurs 10 : variation de la mortalité entre 1950 et 2023 (en %)
    mortality_1950 = additional_data[0][2]
    mortality_2023 = additional_data[1][2]
    growth_mortality = ((mortality_2023 - mortality_1950) / mortality_1950) * 100
    
    # Indicateurs 12 : variation du taux de natalité entre 1950 et 2023 (en %)
    birth_rate_1950 = additional_data[0][3]
    birth_rate_2023 = additional_data[1][3]
    growth_birth_rate = ((birth_rate_2023 - birth_rate_1950) / birth_rate_1950) * 100


    # Retourner les indicateurs sous forme d'un tableau de dictionnaires'
    dashboard_data = [
        {"title": "Population mondiale en 1950", "value": f"{population_1950:,}".replace(',', ' '), "description": "Nombre total d'habitants dans le monde en 1950"},
        {"title": "Population mondiale en 2023", "value": f"{population_2023:,}".replace(',', ' '), "description": "Nombre total d'habitants dans le monde en 2023"},
        {"title": "Croissance de la population mondiale (1950-2023)", "value": f"{growth_population:+.0f}%", "description": "Pourcentage d'augmentation de la population mondiale entre 1950 et 2023"},
        {"title": "Population masculine en 1950", "value": f"{male_population_1950:,}".replace(',', ' '), "description": "Nombre d'hommes dans le monde en 1950"},
        {"title": "Population masculine en 2023", "value": f"{male_population_2023:,}".replace(',', ' '), "description": "Nombre d'hommes dans le monde en 2023"},
        {"title": "Croissance de la population masculine (1950-2023)", "value": f"{growth_male_population:+.0f}%", "description": "Pourcentage d'augmentation de la population masculine entre 1950 et 2023"},
        {"title": "Population féminine en 1950", "value": f"{female_population_1950:,}".replace(',', ' '), "description": "Nombre de femmes dans le monde en 1950"},
        {"title": "Population féminine en 2023", "value": f"{female_population_2023:,}".replace(',', ' '), "description": "Nombre de femmes dans le monde en 2023"},
        {"title": "Croissance de la population féminine (1950-2023)", "value": f"{growth_female_population:+.0f}%", "description": "Pourcentage d'augmentation de la population féminine entre 1950 et 2023"},
        {"title": "Variation du taux de natalité (1950-2023)", "value": f"{growth_birth_rate:+.0f}%", "description": "Pourcentage de variation du taux de natalité entre 1950 et 2023"},
        {"title": "Variation de l'espérance de vie (1950-2023)", "value": f"{growth_life_expectancy:+.0f}%", "description": "Pourcentage de variation de l'espérance de vie entre 1950 et 2023"},
        {"title": "Variation du taux de mortalité (1950-2023)", "value": f"{growth_mortality:+.0f}%", "description": "Pourcentage de variation du taux de mortalité entre 1950 et 2023"},
    ]
    return dashboard_data