import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense


t = np.arange(0, 1000)
x = np.sin(0.02*t)

l=100

X_train = np.empty((len(x)-l, l))
y_train = np.empty((len(x)-l,))

for i in range(len(X_train)):
    X_train[i, :] = x[i:i+l]
    y_train[i] = x[i+l]

X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))


model = Sequential()
model.add(LSTM(50, activation='relu', input_shape=(l, 1)))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mse')


model.fit(X_train, y_train, epochs=10, verbose=1)



test_input = np.reshape(x[-l:], (1, l, 1))
test_output = []
for _ in range(l):
    prediction = model.predict(test_input, verbose=0)
    test_output.append(prediction[0][0])
    test_input = np.roll(test_input, -1)
    test_input[0][-1][0] = prediction


plt.figure(figsize=(14,7))
plt.plot(t, x, label='Original data')
plt.plot(np.arange(1000, 1000+l), test_output, label='Predicted data')
plt.legend()
plt.show()
