import numpy as np
import tensorflow as tf
import os
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, Flatten, Dense, Reshape
from tensorflow.keras.callbacks import TensorBoard

import pickle

import matplotlib.pyplot as plt
import pdb

print("TRAINING START")


# Ouverture du fichier en mode lecture binaire
with open('data.pkl', 'rb') as f:
    # Chargement des données sérialisées
    data = pickle.load(f)

max_lengthX = max([len(item[0]) for item in data]) # Trouver la longueur maximale parmi les entrées
max_lengthY = max([len(item[1]) for item in data]) # Trouver la longueur maximale parmi les entrées

x_data = [item[0] for item in data]
y_data = [item[1] for item in data]

# Remplir les entrées avec des zéros pour qu'elles aient la même longueur
x_data_padded = [x + [x[-1]] * (max_lengthX - len(x)) for x in x_data]
y_data_padded = [y + [y[-1]] * (max_lengthY - len(y)) for y in y_data]

x_train = np.array(x_data_padded)
y_train = np.array(y_data_padded)

# print(y_train)
# Créer le modèle
model = Sequential()
model.add(Dense(32, activation='relu', input_shape=(max_lengthX,)))
model.add(Dense(5, activation='linear'))

# Compiler le modèle
model.compile(optimizer='adam', loss='mse', metrics=['mae'])

# Entraîner le modèle
model.fit(x_train, y_train, epochs=10, batch_size=1) # Modifier le nombre d'epochs et la taille du batch si nécessaire

# Prédire une nouvelle entrée
x_test = np.array([[100, 100, 98, 98, 100, 100, 98, 95, 96, 96, 100, 98, 96, 93, 94, 95, 98, 96, 93, 94, 95, 98]])
y_pred = model.predict(x_test)
print(y_pred)


# Ouverture du fichier en mode écriture binaire
with open('model.pkl', 'wb') as f:
    # Écriture de l'objet dans le fichier
    pickle.dump(model, f)


