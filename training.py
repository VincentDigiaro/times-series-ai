import numpy as np
import tensorflow as tf
import os
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, Flatten, Dense, Reshape, LSTM
from tensorflow.keras.callbacks import TensorBoard
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent / 'utils'))
import pickle

import matplotlib.pyplot as plt
import pdb
import utils as ut
print("TRAINING START")


# Ouverture du fichier en mode lecture binaire
with open('data/data.pkl', 'rb') as f:
    # Chargement des données sérialisées
    data = pickle.load(f)

x_data = [item[0] for item in data]
y_data = [item[1] for item in data]

x_train = np.array(x_data)
y_train = np.array(y_data)

# print(y_train)
# Créer le modèle
#pdb.set_trace()


# Définition des dimensions de l'entrée
input_shape = (len(data[0][0]), ut.INPUT_DIMENSION)  # 3 pas de temps, 7 caractéristiques

# Création du modèle
model = Sequential()

# Ajout d'une couche LSTM
model.add(LSTM(ut.INPUT_DIMENSION, activation='relu', input_shape=input_shape))
model.add(Dense(ut.INPUT_DIMENSION, activation='relu'))
#
#model.add(Flatten(input_shape=input_shape))
#model.add(Dense(50, activation='relu'))
# Ajout d'une couche Dense pour la sortie
model.add(Dense(ut.OUTPUT_DIMENSION))

# Compilation du modèle

model.compile(optimizer='adam', loss='mse')
#model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])




# Entraîner le modèle
model.fit(x_train, y_train, epochs=200, batch_size=1000) # Modifier le nombre d'epochs et la taille du batch si nécessaire

# Pour enregistrer le modèle
model.save('data/model.h5')

