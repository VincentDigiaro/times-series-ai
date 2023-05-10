import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent / 'utils'))

import pdb
import matplotlib.pyplot as plt
import requests
import json
import pandas as pd
import io
import datetime
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from utils import *
import pickle

with open('data/rawdata.pkl', 'rb') as f:
    indexes = pickle.load(f)

print("CREATE DATASET")

data = indexes[0]['ri']

# Convertir les chaînes de date en objets datetime
data = [(datetime.strptime(date, '%Y-%m-%d'), value) for date, value in data]

# Trouver la première et la dernière date
start_date = data[0][0]
end_date = data[-1][0]

# Créer un dictionnaire à partir des données pour faciliter la recherche
data_dict = {date: value for date, value in data}

# Parcourir la plage de dates et ajouter les jours manquants avec une valeur par défaut
current_date = start_date
while current_date <= end_date:
    if current_date not in data_dict:
        # Remplacez 0 par la valeur par défaut souhaitée
        futureval = data_dict[current_date-timedelta(days=1)]
        for i in range(len(data)):
            if  current_date+timedelta(days=i) in data_dict:
                futureval = data_dict[current_date+timedelta(days=i)]
                break

        data_dict[current_date] = (futureval + data_dict[current_date-timedelta(days=1)])/2
    current_date += timedelta(days=1)

# Convertir le dictionnaire en liste et trier par date
result = sorted(data_dict.items())

# Si vous souhaitez convertir les objets datetime en chaînes de date, décommentez la ligne suivante
result = [(date.strftime('%Y-%m-%d'), value) for date, value in result]

nbDaysInput = 30
nbDaysOutput = 7
decoupe = decoupe(result, nbDaysOutput)
dataSet = []

for i, el in enumerate(decoupe):
    pv = getPreviousTime(result, decoupe[i].iloc[0].date,nbDaysInput)
    if pv.values.shape[0] == nbDaysInput and decoupe[i].shape[0] == nbDaysOutput:
        dataSet.append([ replaceDate(pv.values), cleanDate(decoupe[i].values)])


with open('data/data.txt', 'w') as f:
    # Écriture du texte dans le fichier
    f.write(str(dataSet))

# Ouverture du fichier en mode écriture binaire
with open('data/data.pkl', 'wb') as f:
    # Écriture de l'objet dans le fichier
    pickle.dump(dataSet, f)

