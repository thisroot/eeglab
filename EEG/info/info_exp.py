# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 09:51:35 2017

@author: Egor Mikheev
@email: mail@nebesa.me
@package: github/thisroot/eeglab
"""

import pickle, os, glob


class info_exp:
    def __init__(self, path = False, info = {}) :
        
        # поля по умолчанию
        resp_name = 'name'
        description = 'description'
        labels_names = [u'noise', u'rest', u'left', u'right']
        frequency = 1000
        chanels_names = [u'FC5',u'FT7',u'FC3',u'FCz',u'FC4',u'FT8',u'T3',
          u'C3',u'Cz',u'T4',u'C4',u'TP7',u'CP3',u'CPz',
          u'CP4',u'TP8',u'FC1',u'FC2',u'FC6',u'P4',u'C5',
          u'C1',u'C2',u'C6',u'P3',u'CP5',u'CP1',u'CP2',u'CP6',u'POz']
        extend = {'description':'extend experiment info','errors':[]}
        
        # информация о названиях файлов с данными
        self.data_train_name = 'data.pkl'
        self.states_train_name = 'states_full.pkl'
        self.data_test_name = 'data.pkl'
        self.states_test_name = 'states_full.pkl'
        
        
        # консруктор полей
        self.resp_name = (info['resp_name'] if 'resp_name' in info else  resp_name)
        self.description = (info['description'] if 'description' in info else  description)
        self.labels_names = (info['labels_names']  if 'labels_names' in info else  labels_names)
        self.frequency = (info['frequency'] if 'frequency' in info else  frequency)
        self.chanels_names = (info['chanels_names'] if 'chanels_names' in info else  chanels_names)
        self.extend = (info['extend'] if 'extend' in info else  extend)
        # информация для обновления структуры каталога
        self.path = path
        self.list_tests = []
        self.threshold = 2
        self.num_tests = 0;
        self.status = False
        
        
        # обновим информацию об испытании
        self.update_info(2)
        
    def getinfo(self):
        """
        получение информации об испытании
        """
        
        print "================================================================="
        print 'Experiment status: ', self.status, '; Num tests: ', self.num_tests
        if(self.extend['errors']):
            print '------------------------------------------------------------------'
            print "Ошибки сборки: "
            for count, item in enumerate(self.extend['errors']):
                print item.ljust(10),
            if count % 1 == 0 and count != 0:
                print
            print '------------------------------------------------------------------'    
        print 'Respondent name: ', self.resp_name
        print 'Description:', self.description
        print 'Labels_names: [', ', '.join([str(x.encode('utf-8')) for x in self.labels_names]),']'
        print 'Frequency:', self.frequency
        print '------------------------------------------------------------------'
        print 'Chanels_names:'
        print '------------------------------------------------------------------'
        for count, item in enumerate(self.chanels_names):
            print item.ljust(10),
            if count % 5 == 0 and count != 0:
                print
        print
        print '------------------------------------------------------------------'
        print 'List tests'
        print '------------------------------------------------------------------'
        for count, item in enumerate(self.list_tests):
            print item.ljust(10),
            if count % 2 == 0 and count != 0:
                print
        print
        
        print '=================================================================='
        
    def checkfiles(self,path,chfiles):
        for x in chfiles:
            flag = []
            # проверить соответствие файла в наборе файлов
            for item in glob.glob(path +"\*"):
                if x in item:
                    flag.append(True)
            
            # если нет ни одного вхождения, то возвращаем False
            if(True in flag):
                continue
            else:
                self.extend['errors'].append(u'не пройдена проверка на наличие всех файлов\n')
                return False
        return True
        
    def update_info(self,threshold):
        """
        обновление информации о структуре каталогов эксперимента
        
        @threshold - пороговое значение кол-ва тестов при котором эксперимент признается удачным
        
        """
    
        if(self.path == False):
            print 'path not set'
        else:
            list_test = []
            os.chdir(self.path)
            
            chfiles = [self.data_test_name,self.states_test_name]
            for idx,file in enumerate(glob.glob("[0-9]*_[0-9]*")):
                
                if(self.checkfiles(self.path + '\\' + file ,chfiles) == True):
                    list_test.append(file)
            
            self.num_tests = len(list_test)
            if(len(list_test) != 0):
                self.list_tests = list_test
               
            chfiles = [self.data_train_name,self.states_train_name]
            if(self.num_tests > threshold) and (self.checkfiles(self.path,chfiles) == True):
                self.status = True
            else:
                self.status = False
            
    
    def save(self,filename = 'exp_info.dat'):
        with open(self.path +'/'+ filename, 'wb') as output:
            pickle.dump(self, output, pickle.HIGHEST_PROTOCOL)