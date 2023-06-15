import pandas as pd

# Lire le fichier CSV
df = pd.read_csv('../data/CP.csv')
df['DATE'] = pd.to_datetime(df['DATE'])
df.set_index('DATE', inplace=True)
print(df.head())
