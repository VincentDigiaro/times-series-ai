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
import utils as ut
import pickle

print("CREATE DATASET")

consolidateSeries = ut.getIndicesFiltered(ut.STARTDATE,ut.ENDDATE )
outputSerie = consolidateSeries[0]  # futur predicted one
decoupe = ut.decoupe(outputSerie, ut.OUTPUT_DIMENSION) # cut in periods of ut.OUTPUT_DIMENSION, return array 

data = []
for i, el in enumerate(decoupe):
    dataSet = []
    for k in consolidateSeries:
        pv = ut.getPreviousTime(k, decoupe[i].iloc[0].date,ut.INPUT_DIMENSION) # get the periods before each cut from the decoupe array
        if pv.values.shape[0] == ut.INPUT_DIMENSION and decoupe[i].shape[0] == ut.OUTPUT_DIMENSION:  # check data consistency
            dataSet.append( ut.cleanDate(pv.values))  # we dont need the date string for training since our dates are aligned

    if len(dataSet) == len(consolidateSeries):
        data.append([(dataSet), ut.cleanDate(decoupe[i].values)])  # objects used in training 
   

with open('data/data.txt', 'w') as f:
    f.write(str(data))

with open('data/data.pkl', 'wb') as f:
    pickle.dump(data, f)
