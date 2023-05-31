from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from kerastuner.tuners import RandomSearch
import numpy as np
import tensorflow as tf
import os
from tensorflow.keras.callbacks import TensorBoard
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent / 'utils'))
import pickle
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import pdb
import utils as ut
from sklearn.model_selection import train_test_split
from tensorflow.keras.regularizers import l2
from datetime import datetime


print("TRAINING START")

with open('data/data.pkl', 'rb') as f:
    data = pickle.load(f)

x_data = [item[0] for item in data]
y_data = [item[1] for item in data]

input_shape = (len(data[0][0]), ut.INPUT_DIMENSION) 

x_train, x_val, y_train, y_val = train_test_split(x_data, y_data, test_size=0.2, random_state=42)

x_train = np.array(x_train)
y_train = np.array(y_train)
x_val = np.array(x_val)
y_val = np.array(y_val)
 
def build_model(hp):
    units = hp.Int('units', min_value=32, max_value=512, step=32)
    model = Sequential()

    model.add(LSTM(ut.INPUT_DIMENSION, activation='relu', input_shape=input_shape))
    model.add(Dense(ut.INPUT_DIMENSION, activation='relu'))
    model.add(Dense(ut.OUTPUT_DIMENSION))


    model.compile(optimizer=keras.optimizers.Adam(
                        hp.Choice('learning_rate', values=[1e-2, 1e-3, 1e-4])),
                  loss='mse',
                  metrics=['mae'])
    
    return model

# Initialise le tuner
tuner = RandomSearch(
    build_model,
    objective='val_mae',
    max_trials=5,  
    executions_per_trial=3,  
    directory='keras_tuner_trials',
    project_name='time_series_tuning'
)


tuner.search(x_train, y_train, epochs=100, batch_size=1000, validation_data=(x_val, y_val))
best_model = tuner.get_best_models(num_models=1)[0]

best_model.save('data/best_model.h5')




