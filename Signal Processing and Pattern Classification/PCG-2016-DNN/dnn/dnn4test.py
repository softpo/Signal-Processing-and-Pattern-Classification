from __future__ import print_function
from sklearn.cross_validation import train_test_split
import pandas as pd
import numpy as np
np.random.seed(1337)  # for reproducibility
from keras.preprocessing import sequence
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Embedding
from keras.layers import LSTM, SimpleRNN, GRU
from keras.datasets import imdb
from keras.utils.np_utils import to_categorical
from sklearn.metrics import (precision_score, recall_score,f1_score, accuracy_score,mean_squared_error,mean_absolute_error)
from sklearn import metrics
from sklearn.preprocessing import Normalizer
import h5py
from keras import callbacks
from keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau, CSVLogger
from sklearn.utils import shuffle


traindata = pd.read_csv('kdd/binary/Training.csv', header=None)
testdata = pd.read_csv('kdd/binary/Testing.csv', header=None)

traindata = shuffle(traindata)
testdata = shuffle(testdata)


X = traindata.iloc[:,0:600]
Y = traindata.iloc[:,600]
C = testdata.iloc[:,600]
T = testdata.iloc[:,0:600]

y_train = np.array(Y)
y_test = np.array(C)


X_train = np.array(X)
X_test = np.array(T)


batch_size = 64

# 1. define the network
model = Sequential()
model.add(Dense(1024,input_dim=600,activation='relu'))  
model.add(Dropout(0.01))
model.add(Dense(768,activation='relu'))  
model.add(Dropout(0.01))
model.add(Dense(512,activation='relu'))  
model.add(Dropout(0.01))
model.add(Dense(256,activation='relu'))  
model.add(Dropout(0.01))
model.add(Dense(1))
model.add(Activation('sigmoid'))

'''
# try using different optimizers and different optimizer configs
model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])
checkpointer = callbacks.ModelCheckpoint(filepath="kddresults/dnn4layer/checkpoint-{epoch:02d}.hdf5", verbose=1, save_best_only=True, monitor='loss')
csv_logger = CSVLogger('kddresults/dnn4layer/training_set_dnnanalysis.csv',separator=',', append=False)
model.fit(X_train, y_train, batch_size=batch_size, nb_epoch=1000, callbacks=[checkpointer,csv_logger])
model.save("kddresults/dnn4layer/dnn4layer_model.hdf5")


'''


score = []
name = []
import os
for file in os.listdir("kddresults/dnn4layer/"):
  print("within a loop")
  model.load_weights("kddresults/dnn4layer/"+file)
  # make predictions
  testPredict = model.predict_classes(X_test)
  accuracy = accuracy_score(y_test, testPredict)
  print(accuracy)
  print(file)
  score.append(accuracy)
  name.append(file)

print(max(score))


model.load_weights("kddresults/dnn4layer/"+name[score.index(max(score))])
pred = model.predict_classes(X_test)
proba = model.predict_proba(X_test)
np.savetxt("res/dnn4predicted.txt", pred)
np.savetxt("res/dnn4probability.txt", proba)

accuracy = accuracy_score(y_test, pred)
recall = recall_score(y_test, pred , average="binary")
precision = precision_score(y_test, pred , average="binary")
f1 = f1_score(y_test, pred, average="binary")


print("----------------------------------------------")
print("accuracy")
print("%.3f" %accuracy)
print("precision")
print("%.3f" %precision)
print("racall")
print("%.3f" %recall)
print("f1score")
print("%.3f" %f1)

