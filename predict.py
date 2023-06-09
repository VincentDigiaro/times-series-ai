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

allIndices = ut.getAllIndices()
consolidateSeries = ut.getIndicesFiltered(ut.STARTDATE,ut.ENDDATE )
cac = consolidateSeries[0]
max_diff = cac.rolling(window=ut.OUTPUT_DIMENSION + 1).apply(lambda x: x.max() - x.min(), raw=True).max()


labels = [ 
    {'text': 'SP500', 'rgb': '#51CBCB', 'active': 1},
    {'text': 'Dow Jones', 'rgb': '#C7254E', 'active': 1},
    {'text': 'NASDAQ', 'rgb':'#B67250', 'active': 1},
    {'text': 'N225', 'rgb': '#E466C4', 'active': 1},
    {'text': 'Hang Seng Index', 'rgb': '#4974B7', 'active': 1},
    {'text': 'BDI', 'rgb': '#000000', 'active': 1},
    {'text': 'GOLD', 'rgb': '#FFC612', 'active': 1},
    {'text': 'GAS', 'rgb': '#2F2612', 'active': 1},
    {'text': 'CP', 'rgb': '#aF26ee', 'active': 1},

    {'text': 'SP500 Vincent\'s AI predictions', 'active': 1}
 ]


fig, ax = plt.subplots()
for i,series in enumerate(allIndices):
    if labels[i]['active']:
        dates = [x for x in cac.keys()]
        ax.plot(series.keys(),series.values, labels[i]['rgb'])


alldata = []
allnewDates = []
newDate = pd.to_datetime(ut.STARTDATE) + timedelta(days= ut.INPUT_DIMENSION)
timeStep = 2*ut.OUTPUT_DIMENSION

# create toPredict inputs on the past
while newDate < pd.to_datetime(ut.ENDDATE) - timedelta(days=timeStep + ut.OUTPUT_DIMENSION):
    newDate += timedelta(days=(timeStep))
    allnewDates.append(newDate)
    x_data = []
    for x in consolidateSeries:
        pv = ut.getPreviousTime(x,newDate ,ut.INPUT_DIMENSION)
        x_data.append([a for a in pv.value])
        if not len([a for a in pv.value]):
            pdb.set_trace()
    alldata.append(x_data)


# create toPredict inputs on the future
newDate = datetime.strptime(ut.ENDDATE, '%Y-%m-%d') - timedelta(days=1)
allnewDates.append(newDate)
x_data = []
for x in consolidateSeries:
    pv = ut.getPreviousTime(x,newDate ,ut.INPUT_DIMENSION)
    x_data.append([a for a in pv.value])
alldata.append(x_data)

x_test = np.array(alldata)
#pdb.set_trace()
model = load_model('data/model.h5')
y_pred = model.predict(x_test)

#adjust = consolidateSeries[0].values[-1]
#diff = y_pred[-1][0]-adjust
#y_pred[-1] = [a-diff for a in y_pred[-1]]

#for m in range(0,len(y_pred)):
#    newDates = [allnewDates[m] + timedelta(days=a) for a in range(0, len(y_pred[m]))]
#    ax.plot(newDates,y_pred[m], 'g')


for m in range(0,len(y_pred)):
    #newDates = [allnewDates[m] + timedelta(days=a) for a in range(0, len(y_pred[m]))]
    newDates = [allnewDates[m], allnewDates[m] + timedelta(days=14)]
    #pdb.set_trace()
    vals =  [ allIndices[0][newDates[0]],  allIndices[0][newDates[0]] + y_pred[m][0]*max_diff ] 
    ax.plot(newDates, vals , 'g')

plt.legend([a['text'] for a in labels if a['active']])
plt.savefig('img/'+str(int(datetime.now().timestamp()))+ 'chart.png')
plt.show()



