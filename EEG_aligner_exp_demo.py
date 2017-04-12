
# coding: utf-8

# In[1]:

from EEG.preprocessing import aligner_exp


# In[3]:

root = "C:\\eeg\\01exp\\"
name = "20161129_DBS_001"

test = aligner_exp(root + name)
flag = test.align(250,250)

print flag
test.getinfo()
test.save(mode = 'data')