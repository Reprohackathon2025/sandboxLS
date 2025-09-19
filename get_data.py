import requests
import csv

# 1. Télécharger le fichier
url = "https://www.data.gouv.fr/fr/datasets/r/dc7663c7-5da9-4765a98b-ba4bc9de9079"
response = requests.get(url)
response.raise_for_status()

with open("covid_data.txt", "w", encoding="utf-8") as f:
    f.write(response.text)

# 2. Lire et agréger les données
grouped = {}

with open("covid_data.txt", newline='', encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    next(reader)  # sauter l'en-tête

    for row in reader:
        key = row[1]  # champ 2
        try:
            value = float(row[3])  # champ 4
        except ValueError:
            continue  # ignorer les lignes non numériques
        grouped[key] = grouped.get(key, 0) + value

# 3. Trier et écrire le résultat
with open("covid_aggregated.txt", "w", encoding="utf-8") as out:
    for key in sorted(grouped):
        out.write(f"{key}\t{grouped[key]}\n")