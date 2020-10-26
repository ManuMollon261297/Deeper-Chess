#!/usr/bin/env python
# coding: utf-8

# Load Libraries
import numpy as np
import tensorflow as tf
import pandas as pd
import timeit

from keras import backend as K
from keras import initializers
from keras.models import Sequential
from keras.models import load_model
from keras.layers import Input
from keras.layers import Dense
from keras.callbacks import ModelCheckpoint
from keras.callbacks import EarlyStopping
from keras.callbacks import ReduceLROnPlateau
from keras.callbacks import Callback
from keras.optimizers import SGD
from keras.optimizers import Adam

device_name = tf.test.gpu_device_name()
if device_name != '/device:GPU:0':
  raise SystemError('GPU device not found')
print('Found GPU at: {}'.format(device_name))

def cpu():
  with tf.device('/cpu:0'):
    random_image_cpu = tf.random.normal((100, 100, 100, 3))
    net_cpu = tf.keras.layers.Conv2D(32, 7)(random_image_cpu)
    return tf.math.reduce_sum(net_cpu)

def gpu():
  with tf.device('/device:GPU:0'):
    random_image_gpu = tf.random.normal((100, 100, 100, 3))
    net_gpu = tf.keras.layers.Conv2D(32, 7)(random_image_gpu)
    return tf.math.reduce_sum(net_gpu)
# We run each op once to warm up; see: https://stackoverflow.com/a/45067900
cpu()
gpu()

# Run the op several times.
print('Time (s) to convolve 32x7x7x3 filter over random 100x100x100x3 images '
      '(batch x height x width x channel). Sum of ten runs.')
print('CPU (s):')
cpu_time = timeit.timeit('cpu()', number=10, setup="from __main__ import cpu")
print(cpu_time)
print('GPU (s):')
gpu_time = timeit.timeit('gpu()', number=10, setup="from __main__ import gpu")
print(gpu_time)
print('GPU speedup over CPU: {}x'.format(int(cpu_time/gpu_time)))

def trainDBN(layers,xTrain):
  pop = 1
  push = 0
  model = Sequential()
  opt = Adam(lr=0.01)
  for i in range(len(layers)-1):
    auxLayers = list()
    if push != 0:
      # Mark layers as non-trainable
      for layer in model.layers:
        layer.trainable = False
      for j in range(pop):
        # remember the current output layer
        auxLayers.append(model.layers[-1])
        # remove the output layer
        for layer in model.layers:
          print(layer)
        model.pop()
    # Generate new hidden layers
    if push == 0:
    	model.add(Dense(input_shape=(773,), units=layers[i], activation='relu'))
    	model.add(Dense(units=layers[i+1], activation='relu'))
    	model.add(Dense(units=layers[i], activation='relu'))
    else:
    	model.add(Dense(units=layers[i], activation='relu'))
    	model.add(Dense(units=layers[i+1], activation='relu'))
    	model.add(Dense(units=layers[i], activation='relu'))

    # push
    if push != 0:
      # push saved layers
      for k in range(push):
        model.add(auxLayers[push-1-k])
    # Compile the model
    model.compile(optimizer=opt,
                loss='mean_squared_error',
                metrics=['accuracy'])
    # Train NN
    num_epochs = 200
    batch_size = 256
    history = model.fit(x=xTrain, y=xTrain,
                        epochs=num_epochs,
                        batch_size=batch_size,
                        shuffle=True,
                        validation_data=(xTrain, xTrain),
                        verbose=1)
    pop += 1
    push += 1
    model.summary()
    # Fix possible problems with new model
    model.save('temp.h5')
    model = load_model('temp.h5')
  return model

# Separate Data in arrays
f1 = open('bitStreamPosDataFinalB.txt')
f2 = open('bitStreamPosDataFinalW.txt')

gamesArray = list()
for line in f1:
  gamesArray1 = line.split()
for line in f2:
  gamesArray2 = line.split()
gamesArray = gamesArray1 + gamesArray2 

f1.close()
f2.close()

print(len(gamesArray))

xTrain = np.zeros((len(gamesArray),773), dtype=np.int8) 
i = 0
for string in gamesArray:
  j = 0
  for bit in string:
    xTrain[i][j] = bit
    j += 1
  i += 1
  print (i, end="\r")


print(len(xTrain))

print(len(xTrain[0]))

np.random.shuffle(xTrain)

xTrain = xTrain[:2000000]

print(len(xTrain))

model = trainDBN([773,600,400,200,100],xTrain)


#https://towardsdatascience.com/unsupervised-machine-learning-example-in-keras-8c8bf9e63ee0

def anomalyScores(originalDF, reducedDF):
    loss = np.sum(abs(originalDF - reducedDF))
    loss = loss/(len(originalDF)*len(originalDF[0]))
    loss = np.mean(loss)
    print('Mean for anomaly scores: ', loss)
    return loss

def trimAutoencoder(model):
  for i in range(int(len(model.layers)/2)):
    model.pop()
  return model

predictions = model.predict(xTrain, verbose = 1)
predictions = predictions.istype(np.int8)
anomalyScore = anomalyScores(xTrain, predictions)
model = trimAutoencoder(model)

for layer in model.layers:
  layer.trainable = 

model.summary()
model.save('UDBNweights.h5')

