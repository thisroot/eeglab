# -*- coding: utf-8 -*-
"""
Created on Sat Apr 08 15:53:45 2017

@author: Mikheev Egor
@email: mail@nebesa.me
@package:
"""

from IPython import get_ipython
get_ipython().run_line_magic('matplotlib', 'inline')


import warnings
warnings.filterwarnings('ignore')
import pickle, os, glob
from EEG.info import info_exp
from EEG.converter import converter_mne
import mne
import numpy as np
import sys
import scipy.signal as spsig


root = "C:\\eeg\\01exp\\"
name = "20161129_DBS_001"

def load(path,name):
    with open(path + '/' + name, 'rb') as input:
        data = pickle.load(input)
        return data
    
def data_prep(data, sfreq, fmin, fmax):
    [b_high, a_high] = spsig.butter(4, float(fmin) / (sfreq / 2), 'high')
    [b_low, a_low] = spsig.butter(4, float(fmax) / (sfreq / 2), 'low')

    chunk_high = spsig.lfilter(b_high, a_high, data)
    chunk_low = spsig.lfilter(b_low, a_low, chunk_high)
    return chunk_low

    
test = load(root + name,'exp_data_aligned.cls')
test.getinfo()

data  = converter_mne(test)
#raw = data.train_raw()
#epochs = mne.Epochs(raw,data.train_events(),event_id=data.labels, add_eeg_ref=False, preload = True, tmin = 0, tmax =(data.obj.data['time'][0]-1.)/1000)
epochs = data.train_epochs()

X_train = epochs.get_data()
print X_train.shape

print data.labels
print data.labels

print X_train[1][0]

X_train = data_prep(X_train, 1000, 6, 16)
y_train = data.labels

