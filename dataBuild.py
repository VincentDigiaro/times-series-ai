import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent / 'utils'))
import sys


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



consolidateSeries = ut.getIndicesFiltered(ut.STARTDATE,ut.ENDDATE )




print("CREATE DATASET")
#pdb.set_trace()

outputSerie = consolidateSeries[0]



#consolidateSeries[0] = outputSerie
# decoupe

decoupe = ut.decoupe(outputSerie, ut.OUTPUT_DIMENSION)
data = []


for i, el in enumerate(decoupe):

    dataSet = []
    for k in consolidateSeries:
   
        pv = ut.getPreviousTime(k, decoupe[i].iloc[0].date,ut.INPUT_DIMENSION)
       
        if pv.values.shape[0] == ut.INPUT_DIMENSION and decoupe[i].shape[0] == ut.OUTPUT_DIMENSION:
            #dataSet.append([ pv, decoupe[i]])
            dataSet.append( ut.replaceDate(pv.values))
          #  print(dataSet)
    if len(dataSet) == len(consolidateSeries):
        data.append([(dataSet), ut.cleanDate(decoupe[i].values)])




with open('data/data.txt', 'w') as f:
    # Écriture du texte dans le fichier
    f.write(str(data))

# Ouverture du fichier en mode écriture binaire
with open('data/data.pkl', 'wb') as f:
    # Écriture de l'objet dans le fichier
    pickle.dump(data, f)
