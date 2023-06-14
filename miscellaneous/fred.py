import requests
import json

api_key = "87044f3ed1e26ef8c6a1076eb443418f" 
base_url = "https://api.stlouisfed.org/fred/series/observations"

series_ids = {
    "Corporate Profits After Tax": "CP",
    "Industrial Production: Total Index": "INDPRO",
    "Consumer Sentiment": "UMCSENT",
    "Retail Sales: Total (Excluding Food Services)": "RSAFS"
}

for name, series_id in series_ids.items():
    params = {
        "series_id": series_id,
        "api_key": api_key,
        "file_type": "json"
    }
    response = requests.get(base_url, params=params)
    data = response.json()

    print(f"{name}:\n")
    for observation in data['observations']:
        print(f"Date: {observation['date']}, Value: {observation['value']}\n")
