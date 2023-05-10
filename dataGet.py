import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent / 'utils'))
from utils import *
import pickle

print("GET DATA")



jsonData = getDataFromUrl(f"https://www.scientificbeta.com/factor/proxy/indexSeries/ADU-xxES-xPx?currency=USD")

with open('data/scidata.pkl', 'wb') as f:
    pickle.dump(jsonData, f)

indexes = [{'label': 'id'},{'label': 'cw'},{'label': 'rf'}]
variants = [{'id':'ri', 'color': 'r'}, {'id':'nr', 'color': 'g'}, {'id': 'pi', 'color': 'b'}]

for i, el in enumerate(indexes):
    for j, element in enumerate(variants):
        raw = jsonData["data"]["response"][i][variants[j]['id']]
        tab = []
        for k, l in enumerate(jsonData["data"]["response"][i]['date']):
            tab.append((l,raw[k]))
        indexes[i][variants[j]['id']] = tab
with open('data/rawdata.pkl', 'wb') as f:
    pickle.dump(indexes, f)
