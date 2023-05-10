import pdb
import matplotlib.pyplot as plt
import requests
import json
import datetime as dt
import pandas as pd
import io
import datetime
import numpy as np
import pandas as pd
from datetime import timedelta
from utils import *
import pickle

print("GET DATA")

jsonData = getDataFromUrl(f"https://www.scientificbeta.com/factor/proxy/indexSeries/ADU-xxES-xPx?currency=USD")
indexes = [{'label': 'id'},{'label': 'cw'},{'label': 'rf'}]
variants = [{'id':'ri', 'color': 'r'}, {'id':'nr', 'color': 'g'}, {'id': 'pi', 'color': 'b'}]

for i, el in enumerate(indexes):
    for j, element in enumerate(variants):
        raw = jsonData["data"]["response"][i][variants[j]['id']]
        tab = []
        for k, l in enumerate(jsonData["data"]["response"][i]['date']):
            tab.append((l,raw[k]))
        indexes[i][variants[j]['id']] = tab


print("CREATE DATASET")
decoupe = decoupe(indexes[0][variants[0]['id']])
dataSet = []
for i, el in enumerate(decoupe):
    pv = getPreviousTime(indexes[0][variants[0]['id']], decoupe[i].iloc[0].date,30)
    if pv.values.shape[0] > 10:
        dataSet.append([ replaceDate(pv.values), cleanDate(decoupe[i].values)])


with open('mon_fichier.txt', 'w') as f:
    # Écriture du texte dans le fichier
    f.write(str(dataSet))

# Ouverture du fichier en mode écriture binaire
with open('data.pkl', 'wb') as f:
    # Écriture de l'objet dans le fichier
    pickle.dump(dataSet, f)

