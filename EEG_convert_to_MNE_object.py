
# coding: utf-8

# In[1]:

#get_ipython().magic(u'matplotlib inline')

import pickle, os, glob
from EEG.info import info_exp

root = "C:\\eeg\\01exp\\"
name = "20161129_DBS_001"


import matplotlib.pyplot as plt

# In[2]:

def load(path,name):
    with open(path + '/' + name, 'rb') as input:
        data = pickle.load(input)
        return data


# In[3]:

test = load(root + name,'exp_data_aligned.cls')


# In[4]:

test.getinfo()


# In[45]:

import numpy as np
import neo
import mne

class converter_mne:
    def __init__(self,data):
        self.obj = data
        self.list_tests = self.obj.info.list_tests
        self.num_tests = self.obj.info.num_tests
        
    def mne_info(self):
        return mne.create_info(ch_names = self.obj.info.chanels_names, 
                               sfreq = self.obj.info.frequency,
                               ch_types = self.obj.info.ch_types, 
                               montage = self.obj.info.montage)
        
        #info = mne.create_info(ch_names=ch_names, sfreq=sfreq, ch_types=ch_types)
        
    def train_raw(self):
        return mne.io.RawArray(self.obj.data['data_train'].reshape(len(self.obj.info.chanels_names), -1), self.mne_info()).set_eeg_reference(self.obj.info.chanels_names)
    
    def test_raw(self,idx):
        if(idx >= self.num_tests):
            print idx, " out the range: ", self.num_tests - 1
            return False
        return mne.io.RawArray(self.obj.datadata['tests'][idx]['data_test'].reshape(len(self.obj.info.chanels_names), -1), self.mne_info()).set_eeg_reference(self.obj.info.chanels_names)
        
        
    def train_events(self):
        events = []
        for i in range(0, len(self.obj.data['stop'])):
            events.append([int(self.obj.data['stop'][i]),0,int(self.obj.data['states_train'][i])])
        return np.array(events)
        
    def train_epochs(self):
        labels = dict.fromkeys(self.obj.info.labels_names)
        for idx, i in enumerate(labels):
            labels[i] = idx
        labels.pop(u'удалено', None)
        #return mne.EpochsArray(np.array(self.obj.data['data_train']), info=self.mne_info(), events=np.array(self.train_events()),
        #                 event_id=labels)
        return mne.Epochs(self.train_raw(),np.array(self.train_events()),event_id=labels,add_eeg_ref=False, preload = True, tmin = 0, tmax =(self.obj.data['time'][0]-1.)/1000, baseline = None)
        pass
    
    def test_events(self,idx):
        if(idx >= self.num_tests):
            print idx, " out the range: ", self.num_tests - 1
            return False
        events = []
        for i in range(0, len(self.obj.data['tests'][idx]['stop'])):
            events.append([int(self.obj.data['tests'][idx]['stop'][i]),0,int(self.obj.data['tests'][idx]['states_test'][i])])
        return np.array(events)
    
    
    def test_epochs(self,idx):
        if(idx >= self.num_tests):
            print idx, " out the range: ", self.num_tests - 1
            return False
        labels = dict.fromkeys(self.obj.info.labels_names)
        for idx, i in enumerate(labels):
            labels[i] = idx
        labels.pop(u'удалено', None)
        
        #return mne.EpochsArray(np.array(self.obj.data['tests'][idx]['data_test']), info=self.mne_info(), events=np.array(self.test_events(idx)),
        #                 event_id=labels)
        return mne.Epochs(self.test_raw(idx),np.array(self.test_events(idx)),event_id=labels, add_eeg_ref=False, preload = True, tmin = 0, tmax =(self.obj.data['time'][0]-1.)/1000, baseline = None)
        
    pass
        
# In[49]:

test2  = converter_mne(test)
epochs = test2.train_epochs()
picks = mne.pick_types(info=test2.mne_info(), meg=False, eeg=True, misc=False)


test2.train_epochs()
raw = test2.train_raw()
print raw.info

Y_train = epochs.events[:,-1]
X_train = epochs.get_data().reshape(len(Y_train), -1)

print X_train.shape, Y_train

#plt.rcParams['figure.figsize'] = 100, 10
#epochs.plot(picks=picks, scalings='auto', show=True, block=True)
#plt.rcParams['figure.figsize'] = 15, 10
#epochs.plot_psd(tmax=np.inf, fmax = 100)
#print '1'

# In[ ]:

