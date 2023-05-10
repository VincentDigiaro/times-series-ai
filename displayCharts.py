
import pdb
import matplotlib.pyplot as plt
import requests
import json
import datetime as dt
import pandas as pd
import io
from utils import *


json = getDataFromUrl(f"https://www.scientificbeta.com/factor/proxy/indexSeries/ADU-xxES-xPx?currency=USD")

indexes = [{'label': 'id'},{'label': 'cw'},{'label': 'rf'}]
variants = [{'id':'ri', 'color': 'r'}, {'id':'nr', 'color': 'g'}, {'id': 'pi', 'color': 'b'}]

for i, el in enumerate(indexes):
    for j, element in enumerate(variants):
        raw = json["data"]["response"][i][variants[j]['id']]
        tab = []
        for k, l in enumerate(json["data"]["response"][i]['date']):
            tab.append((l, raw[k]))
        indexes[i][variants[j]['id']] = tab
draw(indexes, variants)

