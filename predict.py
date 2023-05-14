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
import random
import utils as ut
from datetime import datetime, time, timedelta
from tensorflow.keras.models import load_model


nbTest = 20


with open('data/indices.pkl', 'rb') as f:
    consolidateSeries = pickle.load(f)


consolidateSeries = ut.normaliseSeries(consolidateSeries)
cac = consolidateSeries[0]



fig, ax = plt.subplots()
for i,series in enumerate(consolidateSeries):

    dates = [x for x in cac.keys()]
    
    ax.plot(series.keys(),series.values, 'r' if i else 'y')




alldata = []
allnewDates = []
newDate = ut.generer_datetime_entre('2005-01-10', '2005-02-10')
for m in range(0,nbTest):
    newDate += timedelta(days=(2*ut.OUTPUT_DIMENSION))
    allnewDates.append(newDate)
    x_data = []
    for x in consolidateSeries:
        pv = ut.getPreviousTime(x,newDate ,ut.INPUT_DIMENSION)
        
        x_data.append([a for a in pv.value])
   
    alldata.append(x_data)


newDate = datetime.now() - timedelta(days=1)


#pdb.set_trace()
allnewDates.append(newDate)
x_data = []
for x in consolidateSeries:
    pv = ut.getPreviousTime(x,newDate ,ut.INPUT_DIMENSION)
    x_data.append([a for a in pv.value])

alldata.append(x_data)


#pdb.set_trace()

x_test = np.array(alldata)

model = load_model('data/model.h5')
y_pred = model.predict(x_test)

adjust = consolidateSeries[0].values[-1]

diff = y_pred[-1][0]-adjust

y_pred[-1] = [a-diff for a in y_pred[-1]]

for m in range(0,nbTest +1):
    newDates = [allnewDates[m] + timedelta(days=a) for a in range(0, len(y_pred[m]))]
   # pdb.set_trace()
    ax.plot(newDates,y_pred[m], 'g')





plt.show()



