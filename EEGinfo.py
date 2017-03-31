
# coding: utf-8

# In[1]:

class EEGinfo:
    def __init__(self,info = {}) :
        
        # поля по умолчанию
        name = u'John Doe'
        description = 'description'
        labels_names = [u'noise', u'rest', u'left', u'right']
        frequency = 1000
        chanels_names = [u'FC5',u'FT7',u'FC3',u'FCz',u'FC4',u'FT8',u'T3',
          u'C3',u'Cz',u'T4',u'C4',u'TP7',u'CP3',u'CPz',
          u'CP4',u'TP8',u'FC1',u'FC2',u'FC6',u'P4',u'C5',
          u'C1',u'C2',u'C6',u'P3',u'CP5',u'CP1',u'CP2',u'CP6',u'POz']
        
        # консруктор полей
        self.name = (info['name'] if 'name' in info else  name)
        self.description = (info['description'] if 'description' in info else  description)
        self.labels_names = (info['labels_names']  if 'labels_names' in info else  labels_names)
        self.frequency = (info['frequency'] if 'frequency' in info else  frequency)
        self.chanels_names = (info['chanels_names'] if 'chanels_names' in info else  chanels_names)
    
        
    def getinfo(self):
        print "================================================================="
        print 'name: ', self.name
        print 'description:', self.description
        print 'labels_names: [', ', '.join([str(x.encode('utf-8')) for x in self.labels_names]),']'
        print 'frequency:', self.frequency
        print 'chanels_names:'
        print '------------------------------------------------------------------'
        for count, item in enumerate(self.chanels_names):
            print item.ljust(10),
            if count % 6 == 0:
                print
        print
        print '=================================================================='    


# In[ ]:



