import requests
import json

# Replace "YOUR_API_KEY" with your Alpha Vantage API key
api_key = "0WKSGBXE9TW2ITV8"

# Replace "SYMBOL" with the symbol of the Vanguard fund you want to retrieve


# Alpha Vantage API endpoint to retrieve data for a symbol

#url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=DJI&outputsize=full&apikey=0WKSGBXE9TW2ITV8"


## Make a GET request to the API
#response = requests.get(url)

## Check if the request was successful
#if response.status_code == 200:
#    # Get the JSON data
#    data = response.json()
#    print(data)
#    # Process the data as desired
#    # For example, print the closing prices for the last 5 days
#    #time_series = data["Time Series (Daily)"]
#    #last_five_days = list(time_series.keys())[:5]
#    #for day in last_five_days:
#    #    close_price = time_series[day]["4. close"]
#    #    print(f"Date: {day}, Close Price: {close_price}")
#else:
#    print("API request failed.")


import pandas as pd
import pandas_datareader.data as web
import datetime

start = datetime.datetime(2003, 1, 1)
end = datetime.datetime(2023, 1, 1)

df = web.DataReader('^IXIC', 'yahoo', start.strftime("%Y-%m-%d %H:%M:%S"), end.strftime("%Y-%m-%d %H:%M:%S"))
print(df)



#indices = ["^DJI",  # Dow Jones
#                   "^IXIC",  # NASDAQ Composite
#                   "^GSPC",  # S&P 500
#                   "^FTSE",  # FTSE 100
#                   "^N225",  # Nikkei 225
#                   "^GDAXI",  # DAX Index
#                   "^FCHI",  # CAC 40
#                   "^HSI",  # Hang Seng Index
#                   "^BSESN",  # BSE Sensex
#                   "^SSEC"]  # Shanghai Composite

#data = []
#for i,indice in indices:
#    data.append( yf.download(indice, start="2003-01-01", end="2023-01-01"))
#    print(indices)

#import pickle
#with open('data/dataFinance.pkl', 'wb') as f:
#    pickle.dump(data, f)



