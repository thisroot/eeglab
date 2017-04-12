# -*- coding: utf-8 -*-
"""
Created on Sat Apr 08 14:15:01 2017

@author: User
@email:
@package:
"""

import pickle, os, glob

root = "C:\\eeg\\01exp\\"
name = "20161129_DBS_001"

def load(path,name):
    with open(path + '/' + name, 'rb') as input:
        data = pickle.load(input)
        return data
    
test = load(root + name,'exp_data_aligned.dat')

print test.keys()

                            
import numpy as np
from mne.decoding import CSP
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
import scipy.signal as spsig

def data_prep(data, sfreq, fmin, fmax):
    [b_high, a_high] = spsig.butter(4, float(fmin) / (sfreq / 2), 'high')
    [b_low, a_low] = spsig.butter(4, float(fmax) / (sfreq / 2), 'low')

    chunk_high = spsig.lfilter(b_high, a_high, data)
    chunk_low = spsig.lfilter(b_low, a_low, chunk_high)
    return chunk_low

srate = 1000

data_train = test['data_train']

data_train = data_prep(data_train, srate, 6, 16)
states_train = test['states_train']

print  "данные трейнов: ", data_train.shape
print "значения: ", data_train[3][4][3499],",",data_train[6][27][140]
print  "метки трейнов: ", states_train.shape, "\n метки:  ", states_train

# train classifier
svc = LinearDiscriminantAnalysis()
csp = CSP(n_components=4, reg='ledoit_wolf', log=True)


X_train = csp.fit_transform(data_train, states_train)
svc.fit(X_train, states_train)

data_test = test['tests'][0]['data_test']
data_test =  data_prep(data_test, srate, 6, 16)
states_test = test['tests'][0]['states_test']



print "данные тестов: ", data_test.shape
print "метки тестов: ", states_test.shape, "\n метки:  ", states_test

X_test = csp.transform(data_test)
print svc.score(X_test, states_test)

