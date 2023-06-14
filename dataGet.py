import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent / 'utils'))
import utils as ut
import pickle
from datetime import datetime, timedelta
import requests
import pdb
import pickle
import pandas as pd

import yfinance as yf
import quandl









print("GET DATA")
#alphavantage api_key = "0WKSGBXE9TW2ITV8"
quandl.ApiConfig.api_key = 'rBBh3BQLu3jW-YZxyJTt'
fredKey = "87044f3ed1e26ef8c6a1076eb443418f"

yfinanceIndexes = [                    
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
quandlIndexes = [
    "LBMA/GOLD",
  #  "EIA/PET_RWTC_D"
]



dataBegin = '2000-01-01'

# Get the indices data
data = {}
for indice in yfinanceIndexes:
    data[indice] = ( yf.download(indice, start=dataBegin)) 

allSeries = [data[k]['Close'] for k in data] # Close = value at the end of the day

#df = pd.read_csv('data/Baltic Dry Index Historical Data.csv')
#df['Open'] = df['Open'].str.replace(',', '').astype(float)
#open_series = pd.Series(df['Open'].values, index=pd.to_datetime(df['Date'], format='%m/%d/%Y'))
#allSeries.append(open_series)

for value in quandlIndexes:
    dataQuandl = quandl.get(value, start_date=dataBegin)
    print('got', value)
    if len(dataQuandl.keys()) == 1:
        allSeries += [  dataQuandl ]# concatenate
    else:
        allSeries += [  dataQuandl['USD (PM)'] ]# concatenate
    #pdb.set_trace()



# fill the missing days in the data
consolidateSeries = []
for series in allSeries:
    series.index = pd.to_datetime(series.index)
    series = series.resample('D').mean()
    series = series.interpolate()
    consolidateSeries.append(series)


with open('data/indices.pkl', 'wb') as f:
        pickle.dump(consolidateSeries, f)
