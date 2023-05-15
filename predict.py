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


nbTest = 1



consolidateSeries = ut.getIndicesFiltered(ut.STARTDATE,ut.ENDDATE )


cac = consolidateSeries[0]



labels = [ 
    {'text': 'CAC 40', 'rgb': '#51CBCB'},
    {'text': 'GOLD', 'rgb': '#FFC612'},
    {'text': 'Dow Jones', 'rgb': '#C7254E'},
    {'text': 'NASDAQ', 'rgb':'#B67250'},
    {'text': 'N225', 'rgb': '#E466C4'},
    {'text': 'Hang Seng Index', 'rgb': '#4974B7'},
    {'text': 'CAC 40 Vincent\'s AI predictions', 'rgb': ''}
 ]


fig, ax = plt.subplots()
for i,series in enumerate(ut.getAllIndices()):

    dates = [x for x in cac.keys()]
    
    ax.plot(series.keys(),series.values, labels[i]['rgb'])




alldata = []
allnewDates = []
newDate = pd.to_datetime(ut.STARTDATE) + timedelta(days= ut.INPUT_DIMENSION)
while newDate < pd.to_datetime(ut.ENDDATE) - timedelta(days=3*ut.OUTPUT_DIMENSION):
    newDate += timedelta(days=(2*ut.OUTPUT_DIMENSION))
    allnewDates.append(newDate)
    x_data = []
    for x in consolidateSeries:
        pv = ut.getPreviousTime(x,newDate ,ut.INPUT_DIMENSION)
        
        x_data.append([a for a in pv.value])
   
    alldata.append(x_data)



newDate = datetime.strptime(ut.ENDDATE, '%Y-%m-%d') - timedelta(days=2)


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

for m in range(0,len(y_pred)):
    newDates = [allnewDates[m] + timedelta(days=a) for a in range(0, len(y_pred[m]))]
   # pdb.set_trace()
    ax.plot(newDates,y_pred[m], 'g')




plt.legend([a['text'] for a in labels])
plt.show()



