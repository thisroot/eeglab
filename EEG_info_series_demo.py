# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 09:51:35 2017

@author: Egor Mikheev
@email: mail@nebesa.me
@package: github/thisroot/eeglab

Формат вложеных каталогов тестов 20170222_PEM_002 - маска поиска каталога *_*_*
надо чтобы в папке не было подпадающих под маску каталогов

"""

import pickle
from EEG.info import info_exp, info_series

# In[2]:

path = "C:\\eeg\\01exp\\"

test = info_series(path)
test.exp_name = "Первая серия экспериментов"
test.save()
# In[18]:

def load(path,name):
    with open(path + '/' + name, 'rb') as input:
        data = pickle.load(input)
        return data


# In[19]:

data = load(path, 'series_info.dat')


# In[20]:

data.getinfo()
