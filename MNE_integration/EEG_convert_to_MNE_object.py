
# coding: utf-8

# In[1]:

get_ipython().magic(u'matplotlib inline')

import pickle, os, glob
from EEG.info import info_exp

root = "C:\\eeg\\01exp\\"
name = "20161129_DBS_001"


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

class converter:
    def __init__(self,data):
        self.obj = data
        
    def get_mne_info(self):
        return mne.create_info(ch_names = self.obj.info.chanels_names, 
                               sfreq = self.obj.info.frequency,
                               ch_types = 'eeg', 
                               montage = 'standard_1005')
    def get_events(self):
        events = []
        for i in range(0, len(test.data['stop'])):
            events.append([int(self.obj.data['stop'][i]),0,int(self.obj.data['states_train'][i])])
            return np.array(events)
        
    def get_epochs(self):
        labels = dict.fromkeys(self.obj.info.labels_names)
        for idx, i in enumerate(labels):
            labels[i] = idx
            
        labels.pop(u'удалено', None)
        
        return mne.EpochsArray(np.array(self.obj.data['data_train']), info=self.get_mne_info(), events=np.array(events),
                         event_id=labels)
    pass
        


# In[49]:

test2  = converter(test)
epochs = test2.get_epochs()
picks = mne.pick_types(info=test2.get_mne_info(), meg=False, eeg=True, misc=False)
epochs.plot(picks=picks, scalings='auto', show=True, block=True)
epochs.plot_psd(tmax=np.inf)
print '1'


# In[ ]:



