import numpy as np
import tensorflow as tf
import os
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, Flatten, Dense, Reshape
from tensorflow.keras.callbacks import TensorBoard



import matplotlib.pyplot as plt


def draw(inputs, output):
    inputs.append(output)
    # Pour chaque sous-liste dans output_data, créer une liste de coordonnées x et y
    for sublist in inputs:
        x = [point[0] for point in sublist]
        y = [point[1] for point in sublist]
        
        # Dessiner les points avec une couleur différente pour chaque sous-liste
        plt.scatter(x, y)

    # Ajouter une légende pour indiquer la signification des couleurs
    plt.legend(["input1", "input2", "output"])

    # Afficher le graphique
    plt.show()





# Exemple de données d'entraînement
input_data = [
    [
        [(0.0, 1.2), (1.0, 3.0),    (2.0, 8.1),    (3.0, 21.6),(4.0, 56.2),    (5.0, 150.3), (6.0, 410.1)],
        [(0.0, 0.9),  (1.0, 2.5),    (2.0, 7.0),    (3.0, 19.5),    (4.0, 53.1),    (5.0, 145.0),    (6.0, 395.2)]
    ],
    [
        [    (0.0, 1.1),    (1.0, 2.9),    (2.0, 6.8),    (3.0, 18.3),    (4.0, 50.9),    (5.0, 140.1),    (6.0, 380.5)],
        [(0.0, 1.2), (1.0, 3.0),    (2.0, 8.1),    (3.0, 21.6),(4.0, 56.2),    (5.0, 150.3), (6.0, 410.1)]
    ],
    # ...
]

output_data = [
    [(0.0, 1.3),    (1.0, 3.2),    (2.0, 9.0),    (3.0, 23.0),    (4.0, 58.0),    (5.0, 152.3),    (6.0, 420.0)],
        [ (0.0, 1.1),    (1.0, 2.9),    (2.0, 6.8),    (3.0, 18.3),    (4.0, 50.9),    (5.0, 140.1),    (6.0, 380.5)]
    # ...
]

train_input_data = np.array(input_data)
train_output_data = np.array(output_data)

model = Sequential([
    Input(shape=(train_input_data.shape[1:])),
    Flatten(),
    Dense(64, activation="relu"),
    Dense(64, activation="relu"),
    Dense(train_output_data.shape[1] * train_output_data.shape[2]),
    Reshape(train_output_data.shape[1:])
])

model.compile(optimizer="adam", loss="mse")

log_dir = "logs/"
os.makedirs(log_dir, exist_ok=True)
tensorboard_callback = TensorBoard(log_dir=log_dir, histogram_freq=1, write_graph=True)

model.fit(train_input_data, train_output_data, epochs=1000, callbacks=[tensorboard_callback])

# Test data
test_input_data = [
    [
         [(0.0, 0.9),  (1.0, 2.5),    (2.0, 7.0),    (3.0, 19.5),    (4.0, 53.1),    (5.0, 145.0),    (6.0, 395.2)],
         [    (0.0, 1.1),    (1.0, 2.9),    (2.0, 6.8),    (3.0, 18.3),    (4.0, 50.9),    (5.0, 140.1),    (6.0, 380.5)],
    ]
]

# Prediction
predicted_output = model.predict(np.array(test_input_data))

# Enregistrement du graphe de calcul
print(predicted_output)

draw(input_data[0], output_data[0])
draw(input_data[1], output_data[1])
draw(test_input_data[0], predicted_output[0])





