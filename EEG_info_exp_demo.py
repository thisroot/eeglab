# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 09:51:35 2017

@author: Egor Mikheev
@email: mail@nebesa.me
@package: github/thisroot/eeglab

Формат каталогов 20170222_162856 - маска поиска каталога [0-9]*_[0-9]*
надо чтобы в папке не было подпадающих под маску каталогов
"""

# In[2]:
    
import pickle
from EEG.info import info_exp

root = "C:\\eeg\\01exp\\"
name = "20161210_GSH_001"

# In[3]:


def load(path,name):
    with open(path + '/' + name, 'rb') as input:
        data = pickle.load(input)
        return data


# In[4]:

test = info_exp(root + name)
test.resp_name = 'Иван Иванов'
test.description = 'Эксперимент с обратной связью'
test.labels_names = [u'шум', u'левое', u'правое', u'отдых']
test.getinfo()


# In[5]:

test.save()


# In[6]:

#eegtest = load(root + name,'exp_info.dat')


# In[7]:

#eegtest.getinfo()
