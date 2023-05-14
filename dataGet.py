import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent / 'utils'))
import utils as ut
import pickle
from datetime import datetime, timedelta


print("GET DATA")
import pandas as pd
import requests
import pdb

api_key = "0WKSGBXE9TW2ITV8"
import yfinance as yf

import pickle



import quandl

# Set your API key
quandl.ApiConfig.api_key = 'rBBh3BQLu3jW-YZxyJTt'

# Get the gold price data
dataGold = quandl.get('LBMA/GOLD', start_date='2003-01-01')

print('got gold')

#pdb.set_trace()
#exit()

# Print the data

indices = [
                        
                     "^FCHI",  # CAC 40
                    "^DJI",  # Dow Jones
                   "^IXIC",  # NASDAQ Composite
                   #"^GSPC",  # S&P 500
                   #"^FTSE",  # FTSE 100
                   "^N225",  # Nikkei 225
                   #"^GDAXI",  # DAX Index              
                   "^HSI",  # Hang Seng Index
                   #"^BSESN",  # BSE Sensex
                   ]




data = {}
for indice in indices:
    data[indice] = ( yf.download(indice, start="2003-01-01"))

allSeries = [data[k]['Close'] for k in data] + [  dataGold['USD (PM)'] ]
consolidateSeries = []

for series in allSeries:
    # Assurez-vous que l'index est de type datetime
    series.index = pd.to_datetime(series.index)
    series = series.resample('D').mean()
    series = series.interpolate()
    consolidateSeries.append(series)




with open('data/indices.pkl', 'wb') as f:
        pickle.dump(consolidateSeries, f)


 #with open('data/scidata.pkl', 'rb') as f:
 #   result = pickle.load(f)
