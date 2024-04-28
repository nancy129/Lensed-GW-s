# -*- coding: utf-8 -*-
"""Classification_model_2 .ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1rdJArbFl0eBWt2WYGxpIm3nZNnVVZOwg
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os
import cv2

from google.colab import drive
drive.mount('/content/drive')

path="/content/drive/MyDrive/trimmed_waveform_1"

[200,614,1]

path = r"/content/drive/MyDrive/trimmed_waveform_1"

unlensed_waveform = glob.glob(path+"/*.npy")

lensed_waveform = []  # Initialize lists to store filenames
unlensed_waveform = []

for i in glob.glob(path + "/L*.npy"):
    lensed_waveform.append(i)

for i in glob.glob(path + "/*.npy"):
    if not any(i == lwf for lwf in lensed_waveform):
        unlensed_waveform.append(i)

len(lensed_waveform)

len(unlensed_waveform)

type(lensed_waveform)
plt.plot(np.load(lensed_waveform[9]))
plt.plot(np.load(unlensed_waveform[9]))

lensed_waveform = [np.load(file) for file in lensed_waveform]
unlensed_waveform = [np.load(file) for file in unlensed_waveform]

plt.plot(lensed_waveform[9])
plt.figure(figsize=(614, 1))
plt.savefig('plot.png')
plt.show()

desired_shape = (614, 1)
lensed_waveform = [np.resize(waveform, desired_shape) for waveform in lensed_waveform]
unlensed_waveform = [np.resize(waveform, desired_shape) for waveform in unlensed_waveform]

plt.plot(lensed_waveform[9])

(lensed_waveform[0].shape)

# Created labels
lensed_labels = np.ones(len(lensed_waveform))
unlensed_labels = np.zeros(len(unlensed_waveform))

# Combine data and labels
import numpy as np
import tensorflow as tf
np.random.seed(42)
tf.random.set_seed(42)

from sklearn.model_selection import train_test_split
X = np.concatenate([lensed_waveform, unlensed_waveform])
y = np.concatenate([lensed_labels, unlensed_labels])

# Split data into training and testing sets
# from sklearn.model_selection import train_test_split

# Assuming your data is in X and y variables
# X represents the features, and y represents the target variable

# Split the data into training and testing sets (80% training, 20% test+validation)
X_train, X_test_val, y_train, y_test_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Further split the test+validation set into test and validation sets (50% test, 50% validation)
X_test, X_val, y_test, y_val = train_test_split(X_test_val, y_test_val, test_size=0.5, random_state=42)

y_train.shape

y_val.shape
X_train.shape

plt.plot(X[9])
print(y[9])

plt.plot(X_train[3])

import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

model = MobileNetV2(weights='imagenet', include_top=False)  # Load the pre-trained model without the top classification layers

'''from tensorflow.keras import layers, models, regularizers
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ReduceLROnPlateau
from tensorflow.keras.optimizers import SGD

model = models.Sequential()


model.add(layers.Input(shape=(614, 1)))

model.add(layers.Conv1D(64, 3, activation='relu', padding='same', kernel_regularizer=regularizers.l2(0.001)))
model.add(layers.MaxPooling1D(2))
model.add(layers.Dropout(0.3))

model.add(layers.Conv1D(128, 3, activation='relu', padding='same', kernel_regularizer=regularizers.l2(0.001)))
model.add(layers.MaxPooling1D(2))
model.add(layers.Dropout(0.4))

model.add(layers.Conv1D(256, 3, activation='relu', padding='same', kernel_regularizer=regularizers.l2(0.001)))
model.add(layers.MaxPooling1D(2))
model.add(layers.Dropout(0.5))

model.add(layers.Flatten())

model.add(layers.Dense(256, activation='relu', kernel_regularizer=regularizers.l2(0.001)))
model.add(layers.Dropout(0.5))

model.add(layers.Dense(128, activation='relu', kernel_regularizer=regularizers.l2(0.001)))
model.add(layers.Dropout(0.5))


model.add(layers.Dense(1, activation='sigmoid'))


reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=3, min_lr=0.00001)

model.compile(optimizer=SGD(lr=0.0001), loss='binary_crossentropy', metrics=['accuracy'])

test_loss, test_accuracy = model.evaluate(X_test, y_test)
print(f"Test accuracy: {test_accuracy}")

from tensorflow.keras import layers, models, regularizers
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ReduceLROnPlateau
from tensorflow.keras.optimizers import SGD

model = models.Sequential()


model.add(layers.Input(shape=(614, 1)))

model.add(layers.Conv1D(64, 3, activation='relu', padding='same', kernel_regularizer=regularizers.l2(0.001)))
model.add(layers.BatchNormalization())
model.add(layers.MaxPooling1D(2))
model.add(layers.Dropout(0.3))

model.add(layers.Conv1D(128, 3, activation='relu', padding='same', kernel_regularizer=regularizers.l2(0.001)))
model.add(layers.BatchNormalization())
model.add(layers.MaxPooling1D(2))
model.add(layers.Dropout(0.4))

model.add(layers.Conv1D(256, 3, activation='relu', padding='same', kernel_regularizer=regularizers.l2(0.001)))
model.add(layers.BatchNormalization())
model.add(layers.MaxPooling1D(2))
model.add(layers.Dropout(0.5))

model.add(layers.Flatten())

model.add(layers.Dense(256, activation='relu', kernel_regularizer=regularizers.l2(0.001)))
model.add(layers.BatchNormalization())
model.add(layers.Dropout(0.5))

model.add(layers.Dense(128, activation='relu', kernel_regularizer=regularizers.l2(0.001)))
model.add(layers.BatchNormalization())
model.add(layers.Dropout(0.5))


model.add(layers.Dense(1, activation='sigmoid'))


reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=3, min_lr=0.00001)

model.compile(optimizer=SGD(lr=0.0001), loss='binary_crossentropy', metrics=['accuracy'])

test_loss, test_accuracy = model.evaluate(X_test, y_test)
print(f"Test accuracy: {test_accuracy}")

"""model = models.Sequential()
model.add(layers.Input(shape=(614, 1)))
model.add(layers.Conv1D(filters=256, kernel_size=2, activation='relu'))
model.add(layers.Dropout(0.2))
model.add(layers.Conv1D(filters=256, kernel_size=2, activation='relu'))
model.add(layers.Dropout(0.2))
model.add(layers.Conv1D(filters=128, kernel_size=2, activation='relu'))
model.add(layers.Dropout(0.2))
model.add(layers.Conv1D(filters=128, kernel_size=2, activation='relu'))
model.add(layers.Dropout(0.2))
model.add(layers.Conv1D(filters=64, kernel_size=2, activation='relu'))
model.add(layers.Dropout(0.2))
model.add(layers.Conv1D(filters=64, kernel_size=2, activation='relu'))
model.add(layers.Dropout(0.2))
model.add(layers.Conv1D(filters=64, kernel_size=2, activation='relu'))
model.add(layers.Flatten())
model.add(layers.Dense(32, activation='relu'))
model.add(layers.Dense(7656,activation='relu'))
model.add(layers.Dense(1, activation='sigmoid'))

model.compile(optimizer=Adam(lr=0.00001), loss='binary_crossentropy', metrics=['accuracy'])
model.fit(X_train, y_train, epochs=10)
test_loss, test_accuracy = model.evaluate(X_test, y_test)
print(f"Test accuracy: {test_accuracy}")

from tensorflow.keras import layers, models

model = models.Sequential()
model.add(layers.Input(shape=(614, 1)))

model.add(layers.Conv1D(filters=256, kernel_size=2, activation='relu'))
model.add(layers.BatchNormalization())
model.add(layers.Dropout(0.2))

model.add(layers.Conv1D(filters=256, kernel_size=2, activation='relu'))
model.add(layers.BatchNormalization())
model.add(layers.Dropout(0.2))

model.add(layers.Conv1D(filters=128, kernel_size=2, activation='relu'))
model.add(layers.BatchNormalization())
model.add(layers.Dropout(0.2))

model.add(layers.Conv1D(filters=128, kernel_size=2, activation='relu'))
model.add(layers.BatchNormalization())
model.add(layers.Dropout(0.2))

model.add(layers.Conv1D(filters=64, kernel_size=2, activation='relu'))
model.add(layers.BatchNormalization())
model.add(layers.Dropout(0.2))

model.add(layers.Conv1D(filters=64, kernel_size=2, activation='relu'))
model.add(layers.BatchNormalization())
model.add(layers.Dropout(0.2))

model.add(layers.Conv1D(filters=64, kernel_size=2, activation='relu'))
model.add(layers.BatchNormalization())
model.add(layers.Flatten())

model.add(layers.Dense(32, activation='relu'))
model.add(layers.BatchNormalization())

model.add(layers.Dense(7656, activation='relu'))
model.add(layers.BatchNormalization())

model.add(layers.Dense(1, activation='sigmoid'))

model.compile(optimizer=Adam(lr=0.00001), loss='binary_crossentropy', metrics=['accuracy'])
model.fit(X_train, y_train, epochs=10)
test_loss, test_accuracy = model.evaluate(X_test, y_test)
print(f"Test accuracy: {test_accuracy}")

"""model = models.Sequential()
model.add(layers.Input(shape=(614, 1)))
model.add(layers.Conv1D(filters=256, kernel_size=2, activation='relu'))
model.add(layers.Dropout(0.2))
model.add(layers.Conv1D(filters=256, kernel_size=2, activation='relu'))
model.add(layers.Dropout(0.2))
model.add(layers.Conv1D(filters=128, kernel_size=2, activation='relu'))
model.add(layers.Dropout(0.2))
model.add(layers.Conv1D(filters=128, kernel_size=2, activation='relu'))
model.add(layers.Dropout(0.2))
model.add(layers.Conv1D(filters=64, kernel_size=2, activation='relu'))
model.add(layers.Dropout(0.2))
model.add(layers.Conv1D(filters=64, kernel_size=2, activation='relu'))
model.add(layers.Dropout(0.2))
model.add(layers.Conv1D(filters=64, kernel_size=2, activation='relu'))
model.add(layers.Flatten())
model.add(layers.Dense(32, activation='relu'))
model.add(layers.Dense(7656,activation='relu'))
model.add(layers.Dense(1, activation='sigmoid'))

model.compile(optimizer=Adam(lr=0.00001), loss='binary_crossentropy', metrics=['accuracy'])
model.fit(X_train, y_train, epochs=20)
test_loss, test_accuracy = model.evaluate(X_test, y_test)
print(f"Test accuracy: {test_accuracy}")

from tensorflow.keras import layers, models

model = models.Sequential()
model.add(layers.Input(shape=(614, 1)))

model.add(layers.Conv1D(filters=256, kernel_size=2, activation='relu'))
model.add(layers.BatchNormalization())
model.add(layers.Dropout(0.2))

model.add(layers.Conv1D(filters=256, kernel_size=2, activation='relu'))
model.add(layers.BatchNormalization())
model.add(layers.Dropout(0.2))

model.add(layers.Conv1D(filters=128, kernel_size=2, activation='relu'))
model.add(layers.BatchNormalization())
model.add(layers.Dropout(0.2))

model.add(layers.Conv1D(filters=128, kernel_size=2, activation='relu'))
model.add(layers.BatchNormalization())
model.add(layers.Dropout(0.2))

model.add(layers.Conv1D(filters=64, kernel_size=2, activation='relu'))
model.add(layers.BatchNormalization())
model.add(layers.Dropout(0.2))

model.add(layers.Conv1D(filters=64, kernel_size=2, activation='relu'))
model.add(layers.BatchNormalization())
model.add(layers.Dropout(0.2))

model.add(layers.Conv1D(filters=64, kernel_size=2, activation='relu'))
model.add(layers.BatchNormalization())
model.add(layers.Flatten())

model.add(layers.Dense(32, activation='relu'))
model.add(layers.BatchNormalization())

model.add(layers.Dense(7656, activation='relu'))
model.add(layers.BatchNormalization())

model.add(layers.Dense(1, activation='sigmoid'))

model.compile(optimizer=Adam(lr=0.00001), loss='binary_crossentropy', metrics=['accuracy'])
model.fit(X_train, y_train, epochs=20)
test_loss, test_accuracy = model.evaluate(X_test, y_test)
print(f"Test accuracy: {test_accuracy}")

model.save

"""from keras import models, layers
from keras.optimizers import SGD

# Assuming X_train, X_val, y_train, y_val, X_test, y_test are already defined

model = models.Sequential()
model.add(layers.Input(shape=(614, 1)))
model.add(layers.Conv1D(filters=256, kernel_size=2, activation='relu'))
model.add(layers.Dropout(0.2))
model.add(layers.Conv1D(filters=256, kernel_size=2, activation='relu'))
model.add(layers.Dropout(0.2))
model.add(layers.Conv1D(filters=128, kernel_size=2, activation='relu'))
model.add(layers.Dropout(0.2))
model.add(layers.Conv1D(filters=128, kernel_size=2, activation='relu'))
model.add(layers.Dropout(0.2))
model.add(layers.Conv1D(filters=64, kernel_size=2, activation='relu'))
model.add(layers.Dropout(0.2))
model.add(layers.Conv1D(filters=64, kernel_size=2, activation='relu'))
model.add(layers.Dropout(0.2))
model.add(layers.Conv1D(filters=64, kernel_size=2, activation='relu'))
model.add(layers.Flatten())
model.add(layers.Dense(32, activation='relu'))
model.add(layers.Dense(7656,activation='relu'))
model.add(layers.Dense(1, activation='sigmoid'))

model.compile(optimizer=Adam(lr=0.00001), loss='binary_crossentropy', metrics=['accuracy'])
history = model.fit(X_train, y_train, epochs=30, validation_data=(X_val, y_val))
test_loss, test_accuracy = model.evaluate(X_test, y_test)
print(f"Test accuracy: {test_accuracy}")

from keras import models, layers
from keras.optimizers import SGD

# Assuming X_train, X_val, y_train, y_val, X_test, y_test are already defined

model = models.Sequential()
model.add(layers.Input(shape=(614, 1)))

model.add(layers.Conv1D(filters=256, kernel_size=2, activation='relu'))
model.add(layers.BatchNormalization())
model.add(layers.Dropout(0.2))

model.add(layers.Conv1D(filters=256, kernel_size=2, activation='relu'))
model.add(layers.BatchNormalization())
model.add(layers.Dropout(0.2))

model.add(layers.Conv1D(filters=128, kernel_size=2, activation='relu'))
model.add(layers.BatchNormalization())
model.add(layers.Dropout(0.2))

model.add(layers.Conv1D(filters=128, kernel_size=2, activation='relu'))
model.add(layers.BatchNormalization())
model.add(layers.Dropout(0.2))

model.add(layers.Conv1D(filters=64, kernel_size=2, activation='relu'))
model.add(layers.BatchNormalization())
model.add(layers.Dropout(0.2))

model.add(layers.Conv1D(filters=64, kernel_size=2, activation='relu'))
model.add(layers.BatchNormalization())
model.add(layers.Dropout(0.2))

model.add(layers.Conv1D(filters=64, kernel_size=2, activation='relu'))
model.add(layers.BatchNormalization())
model.add(layers.Flatten())

model.add(layers.Dense(32, activation='relu'))
model.add(layers.BatchNormalization())

model.add(layers.Dense(7656, activation='relu'))
model.add(layers.BatchNormalization())

model.add(layers.Dense(1, activation='sigmoid'))

model.compile(optimizer=Adam(lr=0.00001), loss='binary_crossentropy', metrics=['accuracy'])
history = model.fit(X_train, y_train, epochs=30, validation_data=(X_val, y_val))
test_loss, test_accuracy = model.evaluate(X_test, y_test)
print(f"Test accuracy: {test_accuracy}")