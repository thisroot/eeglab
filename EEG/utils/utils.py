# -*- coding: utf-8 -*-
"""
Created on Sun May 28 12:55:02 2017

@author: User
@email:
@package:
"""
import matplotlib.pyplot as plt
import itertools
import numpy as np
import scipy.signal as spsig
import pickle
from sklearn.metrics import confusion_matrix
#import mne
#from mne.time_frequency import psd_multitaper

def load(path,name):
    with open(path + '/' + name, 'rb') as input:
        data = pickle.load(input)
        return data
    
def save(path,name,data):
    with open(path +'/'+ name, 'wb') as output:
        pickle.dump(data, output, pickle.HIGHEST_PROTOCOL)
    
def data_prep(data, sfreq, fmin, fmax):
    [b_high, a_high] = spsig.butter(4, float(fmin) / (sfreq / 2), 'high')
    [b_low, a_low] = spsig.butter(4, float(fmax) / (sfreq / 2), 'low')

    chunk_high = spsig.lfilter(b_high, a_high, data)
    chunk_low = spsig.lfilter(b_low, a_low, chunk_high)
    return chunk_low


def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    #print(cm)

    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, cm[i, j],
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    pass

def plot_mult_conf_matrices(conf_matrices,classes,method='mean', mode = 'plot', normalize = True, title = 'Confusion matrix'):
    if(len(conf_matrices) < 2):
        print "is not a matrices set"
        return 0
    if(conf_matrices[0].shape[0] != conf_matrices[0].shape[1]):
        print "is not a square matrix"
        return 0

    n = conf_matrices[0].shape[0]
    
    if(method == 'mean'):
        matrices = np.mean([conf_matrices[n-j] for j in range(1,n)], axis = 0)
    elif(method == 'max'):
        matrices = np.max([conf_matrices[n-j] for j in range(1,n)], axis = 0)
    elif(method == 'min'):
        matrices = np.min([conf_matrices[n-j] for j in range(1,n)], axis = 0)
    else:
        print "incorrect method";
    if(mode == 'plot'):
        plt.figure()
        plot_confusion_matrix(matrices, classes,
                      title=title, normalize = normalize)
    else:
        return matrices


def psd(raw,picks,tmax,fmax):
    psds, freqs = psd_multitaper(raw, low_bias=True, tmax=4.499,
                              fmax=50., proj=True, picks=picks,
                              n_jobs=1)
    psds = 10 * np.log10(psds)
    psds_mean = psds.mean(0)
    psds_std = psds.std(0)
    
    return psds_mean, psds_std

