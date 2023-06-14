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
from sklearn.model_selection import train_test_split
from tensorflow.keras.regularizers import l2
from datetime import datetime


print("TRAINING START")

with open('data/data.pkl', 'rb') as f:
    data = pickle.load(f)

x_data = [item[0] for item in data]   # inputs 
y_data = [item[1] for item in data]   # coressponding outputs

input_shape = (len(data[0][0]), ut.INPUT_DIMENSION)  # expeted ouput and input length

x_train, x_val, y_train, y_val = train_test_split(x_data, y_data, test_size=0.2, random_state=42) # split data to have a validation set

x_train = np.array(x_train) # training inputs 
y_train = np.array(y_train) # coressponding trainingoutputs
x_val = np.array(x_val)     # validation inputs  
y_val = np.array(y_val)     # coressponding validation outputs

model = Sequential()

model.add(LSTM(ut.INPUT_DIMENSION, activation='relu', input_shape=input_shape))
model.add(Dense(ut.INPUT_DIMENSION, activation='relu'))
#model.add(Dense(ut.INPUT_DIMENSION, activation='relu'))
model.add(Dense(1, activation='tanh'))  # change here, now the model will output a single value between -1 and 1

model.compile(optimizer='adam', loss='mse', metrics=['mae'])

history = model.fit(x_train, y_train, epochs=50, batch_size=10, validation_data=(x_val, y_val))

model.save('data/model.h5')

#model.add(Dropout(0.3))
#, kernel_regularizer=l2(0.01)

#activation='relu':
#Rectified Linear Unit (ReLU). Non-linear function, outputs positive inputs directly, otherwise zero. Commonly used in hidden layers, mitigates vanishing gradient problem.

#mse, mae:
# Mean Squared Error (MSE), squares and averages differences between actual and predicted values, sensitive to outliers. Mean Absolute Error (MAE), averages absolute differences between actual and predicted values, robust to outliers.

#kernel_regularizer=l2(0.01):
# Applies L2 regularization, adding a penalty proportional to the square of weight magnitudes to loss function. Prevents overfitting by pushing weights towards zero.

#optimizer='adam': 
#Adam (Adaptive Moment Estimation), optimization algorithm updates network weights based on training data. Combines benefits of AdaGrad and RMSProp, efficient and memory-friendly.

#loss='binary_crossentropy':
# Binary cross-entropy, loss function for binary classification problems. Measures error between binary model's predictions and true values.

#loss and accuracy:
# Loss quantifies disparity between actual and predicted values. Accuracy measures proportion of correct predictions. Low loss and high accuracy indicate good performance.

#activation='softmax':
# Softmax activation transforms outputs to probabilities summing to one. Used in output layer for multi-class classification, gives probabilities of input belonging to each class.

plt.figure(figsize=(12, 4))

plt.subplot(1, 2, 1)
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.legend()
plt.title('Losses')

plt.subplot(1, 2, 2)
plt.plot(history.history['mae'], label='Training MAE')
plt.plot(history.history['val_mae'], label='Validation MAE')
plt.legend()
plt.title('Mean Absolute Error')
plt.savefig('img/'+str(int(datetime.now().timestamp()))+ '.png')
plt.show()

