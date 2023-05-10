import numpy as np
import tensorflow as tf
import os
import pickle
import matplotlib.pyplot as plt
import pdb
import requests
import json
import datetime as dt
import pandas as pd
import io
from utils import *
from datetime import datetime, timedelta

# Ouverture du fichier en mode lecture binaire
with open('model.pkl', 'rb') as f:
    # Chargement des données sérialisées
    model = pickle.load(f)


jsonData = getDataFromUrl(f"https://www.scientificbeta.com/factor/proxy/indexSeries/ADU-xxES-xPx?currency=USD")

indexes = [{'label': 'id'}]
variants = [{'id':'ri', 'color': 'r'}]


raw = jsonData["data"]["response"][0][variants[0]['id']]
tab = []
for k, l in enumerate(jsonData["data"]["response"][0]['date']):
    tab.append((l, raw[k]))
indexes[0][variants[0]['id']] = tab


fig, ax = plt.subplots()

for l, e in enumerate(indexes):
    for i, el in enumerate(variants):
            dates = [datetime.strptime(x, '%Y-%m-%d') for x, y in indexes[l][variants[i]['id']]]
            valeurs = np.array([y for x, y in indexes[l][variants[i]['id']]])
            ax.plot(dates, valeurs, color=variants[i]['color'], label=indexes[l]['label'] + '-' + variants[i]['id'])


xs = []
lastDates = indexes[0][variants[0]['id']][-22:]
for i , el in enumerate(lastDates):
    xs.append(round(lastDates[i][1]))

x_test = np.array([xs])
print("CREATE PREDICTION")
y_pred = model.predict(x_test)

lastDate = pd.to_datetime(indexes[0][variants[0]['id']][-1][0])


next_dates = []
for i in range(1, 6):
    next_date = lastDate + timedelta(days=i)
    next_dates.append(next_date)



print(next_dates)
print(y_pred)
ax.plot(next_dates, y_pred[0], 'g',)

ax.legend(loc='upper left')
plt.show()



