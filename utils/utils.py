from datetime import datetime, timedelta
import pandas as pd
from datetime import timedelta
from dateutil.relativedelta import relativedelta
import pdb
import matplotlib.pyplot as plt
import numpy as np
import requests
import json
import warnings
import os
from urllib3.exceptions import InsecureRequestWarning
import random
from sklearn.preprocessing import MinMaxScaler
import pickle


INPUT_DIMENSION = 600
OUTPUT_DIMENSION = 150
STARTDATE = '2005-01-01'
ENDDATE = '2014-01-01'
ENDDATA = '2023-01-01'

timeSubDivision = 10
returns = True


def getAllIndices():
    return normaliseSeriesRelative(getIndicesRaw(STARTDATE, ENDDATA), STARTDATE, ENDDATE)


def getIndicesFiltered(start, end):
    return normaliseSeries(getIndicesRaw(start, end))
    

def getIndicesRaw(start, end):
    start_date = pd.to_datetime(start)
    end_date = pd.to_datetime(end)
    with open(r'data/indices.pkl', 'rb') as f:
        res = pickle.load(f)

        cutSeries = []
        for series in res:
            restrictedSeries = series[(series.index >= start_date) & (series.index <= end_date)] 
            if returns:
                restrictedSeries = restrictedSeries.pct_change()  # return of index
                restrictedSeries = (1 + restrictedSeries).cumprod() - 1
                #restrictedSeries = restrictedSeries.pct_change()  # return of index
            cutSeries.append( restrictedSeries )
        return cutSeries


def normaliseSeries(consolidateSeries):
  
    # Initialisez le scaler
    scaler = MinMaxScaler()
    scaled_series_list = []
    for series in consolidateSeries:
        series_values = series.values.reshape(-1, 1)
        scaled_values = scaler.fit_transform(series_values)
        scaled_series = pd.Series(scaled_values.flatten(), index=series.index)
        scaled_series_list.append(scaled_series)
    return scaled_series_list



def normaliseSeriesRelative(consolidateSeries, start_date, end_date):
  
    # Initialisez le scaler
    scaler = MinMaxScaler()
    scaled_series_list = []

    # Assure-toi que les dates sont en format datetime
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    for series in consolidateSeries:
        # Restrict the series to the period of interest for fitting the scaler
        sub_period_series = series[(series.index >= start_date) & (series.index <= end_date)]
        sub_period_values = sub_period_series.values.reshape(-1, 1)

        # Fit the scaler
        scaler.fit(sub_period_values)

        # Apply the scaler to the entire series
        series_values = series.values.reshape(-1, 1)
        scaled_values = scaler.transform(series_values)
        scaled_series = pd.Series(scaled_values.flatten(), index=series.index)
        
        scaled_series_list.append(scaled_series)

    return scaled_series_list




def getPreviousTime(weekly, certain_date, days):
    #pdb.set_trace()
    df_weekly = pd.DataFrame({'date': weekly.index, 'value': weekly.values})
    df_weekly["date"] = pd.to_datetime(df_weekly["date"])
    start_date = certain_date - timedelta(days=days+1)
    end_date = certain_date - timedelta(days=1)
    last_30_days = df_weekly[(df_weekly["date"] >= start_date) & (df_weekly["date"] < end_date)]
 
    return last_30_days



def decoupe(data,gap):
    
    df = pd.DataFrame({'date': data.index, 'value': data.values})
    df["date"] = pd.to_datetime(df["date"])
    min_date = df["date"].min()
    max_date = df["date"].max()
    week_slices = []
    while min_date <= max_date:
        week_end = min_date + timedelta(days=gap-1)
        week_slice = df[(df["date"] >= min_date) & (df["date"] <= week_end)]
        week_slices.append(week_slice)
        min_date += timedelta(days=gap//timeSubDivision)
    return week_slices


def cleanDate(tableau):
    new = []
    for i in range(len(tableau)):
        new.append( (tableau[i][1]))
        #new.append((tableau[i][0].month,tableau[i][0].weekday(), round(tableau[i][1], 2)))
    return new


def getDataFromUrl(url):
    warnings.filterwarnings('ignore', category=InsecureRequestWarning)
    response = requests.get(url, verify=False)
    if response.status_code != 200:
        print("Erreur lors de la récupération des données :", response.status_code)

    return json.loads(response.text)




def generer_datetime_apres(debut, ):
    date_format = "%Y-%m-%d"
    debut_date = datetime.strptime(debut, date_format)
    fin_date = datetime.now()

    # Calculer la différence en jours entre les deux dates
    difference = (fin_date - debut_date).days

    # Générer un nombre aléatoire entre 0 et la différence
    jours_aleatoires = random.randint(0, difference)

    # Ajouter le nombre de jours aléatoires à la date de début
    date_aleatoire = debut_date + timedelta(days=jours_aleatoires)

    return date_aleatoire


def generer_datetime_entre(debut, fin):
    date_format = "%Y-%m-%d"
    debut_date = datetime.strptime(debut, date_format)
    fin_date = datetime.strptime(fin, date_format)

    # Calculer la différence en jours entre les deux dates
    difference = (fin_date - debut_date).days

    # Générer un nombre aléatoire entre 0 et la différence
    jours_aleatoires = random.randint(0, difference)

    # Ajouter le nombre de jours aléatoires à la date de début
    date_aleatoire = debut_date + timedelta(days=jours_aleatoires)

    return date_aleatoire

