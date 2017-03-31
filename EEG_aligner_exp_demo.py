# coding: utf-8

# In[3]:


from EEG.info import info_exp
from EEG.preprocessing import aligner_exp

# In[2]:

root = "C:\\eeg\\01exp\\"
name = "20161129_DBS_001"

test = aligner_exp(root + name)
test.align(250,250)

test.getinfo()
test.save(mode = 'data')
test.save()
