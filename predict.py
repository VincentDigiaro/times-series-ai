import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent / 'utils'))

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
from tensorflow.keras.models import load_model




model = load_model('data/model.h5')

with open('data/scidata.pkl', 'rb') as f:
    jsonData = pickle.load(f)


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
lastDates = indexes[0][variants[0]['id']][-30:]
for i , el in enumerate(lastDates):
    xs.append(round(lastDates[i][1]))

x_test = np.array([xs])
print("CREATE PREDICTION")
y_pred = model.predict(x_test)

lastDate = pd.to_datetime(indexes[0][variants[0]['id']][-1][0])


next_dates = []
for i in range(1, 8):
    next_date = lastDate + timedelta(days=i)
    next_dates.append(next_date)



print(next_dates)
print(y_pred)
#pdb.set_trace()
prediction = np.insert(y_pred[0], 0,  indexes[0][variants[0]['id']][-1][1])

ax.plot([lastDate]+next_dates,prediction, 'g',)

ax.legend(loc='upper left')
plt.show()



