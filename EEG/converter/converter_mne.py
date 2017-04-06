# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 09:51:35 2017

@author: Egor Mikheev
@email: mail@nebesa.me
@package: github/thisroot/eeglab
"""

import pickle, os, glob
import numpy as np
import neo
import mne
from EEG.info import info_exp

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
        
        return mne.EpochsArray(np.array(self.obj.data['data_train']), info=self.mne_info(), events=np.array(self.train_events()),
                         event_id=labels)
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
        
        return mne.EpochsArray(np.array(self.obj.data['tests'][idx]['data_test']), info=self.mne_info(), events=np.array(self.test_events(idx)),
                         event_id=labels)    
    pass