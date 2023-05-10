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
from urllib3.exceptions import InsecureRequestWarning

def build_data(data_weekly, data_monthly):

   # print(data_monthly)
    #print(data_weekly)
    df_weekly = pd.DataFrame(data_weekly, columns=["date", "value"])
    df_weekly["date"] = pd.to_datetime(df_weekly["date"])

    df_monthly = pd.DataFrame(data_monthly, columns=["date", "value"])
    df_monthly["date"] = pd.to_datetime(df_monthly["date"])


    def get_previous_month(date):
        return date - relativedelta(months=1)

    result = []

    for index, row in df_weekly.iterrows():
        week_date = row["date"]
        previous_month_date = get_previous_month(week_date)
        previous_month_date = previous_month_date.replace(day=1)
        
        previous_month_data = df_monthly[df_monthly["date"] == previous_month_date]
        
        if not previous_month_data.empty:
            previous_month_value = previous_month_data["value"].iloc[0]
        else:
            previous_month_value = None
        
        result.append({"week_date": week_date, "week_value": row["value"], "previous_month_date": previous_month_date, "previous_month_value": previous_month_value})

    result_df = pd.DataFrame(result)
    return result


def getPreviousTime(weekly, certain_date, days):
    #pdb.set_trace()
    df_weekly = pd.DataFrame(weekly, columns=["date", "value"])
    df_weekly["date"] = pd.to_datetime(df_weekly["date"])
    
    start_date = certain_date - timedelta(days=days+1)
    end_date = certain_date - timedelta(days=1)
    last_30_days = df_weekly[(df_weekly["date"] > start_date) & (df_weekly["date"] <= end_date)]
    return last_30_days


def draw(indexes, variants):
    fig, ax = plt.subplots()
    for l, e in enumerate(indexes):
        for i, el in enumerate(variants):
                dates = [datetime.strptime(x, '%Y-%m-%d') for x, y in indexes[l][variants[i]['id']]]
                valeurs = np.array([y for x, y in indexes[l][variants[i]['id']]])
                ax.plot(dates, valeurs, color=variants[i]['color'], label=indexes[l]['label'] + '-' + variants[i]['id'])
    ax.legend(loc='upper left')             
    plt.show()

def decoupe(data):
    df = pd.DataFrame(data, columns=["date", "value"])
    df["date"] = pd.to_datetime(df["date"])
    min_date = df["date"].min()
    max_date = df["date"].max()
    week_slices = []
    while min_date <= max_date:
        week_end = min_date + timedelta(days=6)
        week_slice = df[(df["date"] >= min_date) & (df["date"] <= week_end)]
        week_slices.append(week_slice)
        min_date += timedelta(days=7)
    return week_slices


def replaceDate(tableau):
    new = []
    for i in range(len(tableau)):
        new.append( round(tableau[i][1]))
        #new.append((tableau[i][0].month,tableau[i][0].weekday(), round(tableau[i][1], 2)))
    return new

def cleanDate(tableau):
    new = []
    for i in range(len(tableau)):
        new.append( round(tableau[i][1]))
    return new


def getDataFromUrl(url):
    warnings.filterwarnings('ignore', category=InsecureRequestWarning)
    response = requests.get(url, verify=False)
    if response.status_code != 200:
        print("Erreur lors de la récupération des données :", response.status_code)

    return json.loads(response.text)





