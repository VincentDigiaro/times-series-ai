import pandas as pd
import requests
import pdb

api_key = "0WKSGBXE9TW2ITV8"
import yfinance as yf

import pickle


# Print the data

indices = ["^DJI",  # Dow Jones
                   "^IXIC",  # NASDAQ Composite
                   "^GSPC",  # S&P 500
                   "^FTSE",  # FTSE 100
                   "^N225",  # Nikkei 225
                   "^GDAXI",  # DAX Index
                   "^FCHI",  # CAC 40
                   "^HSI",  # Hang Seng Index
                   "^BSESN",  # BSE Sensex
                   ]




data = {}
for indice in indices:
    data[indice] = ( yf.download(indice, start="2003-01-01"))


with open('data/indices.pkl', 'wb') as f:
        pickle.dump(data, f)


 #with open('data/scidata.pkl', 'rb') as f:
 #   result = pickle.load(f)
