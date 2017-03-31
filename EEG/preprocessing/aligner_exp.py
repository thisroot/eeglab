# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 09:51:35 2017

@author: Egor Mikheev
@email: mail@nebesa.me
@package: github/thisroot/eeglab
"""

import pickle, os, glob, sys
import numpy as np
from EEG.info import info_exp

class aligner_exp:
    def __init__(self,path = '.\\', fileinfo = 'exp_info.dat'):
        
        self.__aligned = False
        self.status = True
        self.fileinfo = fileinfo
        self.path = path
        self.info = self.__loadinfo(path, self.fileinfo)
        self.__loaddata()
        pass
    
    def __loadinfo(self,path, fileinfo):
        try:
            with open(os.path.join(path, fileinfo), 'rb') as input:   
                data = pickle.load(input)
            return data
        except:
            sys.exit('Object:' + os.path.join(path, fileinfo) +' can\'t load')
            
    def __loaddata(self):
        if(self.info.status == True):
                self.data = {'data_train':False,'states_train':False,'tests':[]}
                # загружаем тренировочные данные
                self.data['states_train'] = self.__loadfile(os.path.join(self.path,self.info.states_train_name))
                self.data['data_train'] = self.__loadfile(os.path.join(self.path,self.info.data_train_name))
                
                # загружаем тестовые данные
                for item in self.info.list_tests:
                    tests = {'states_test':'', 'data_test':''}
                    tests['states_test'] = self.__loadfile(os.path.join(self.path, item, self.info.states_test_name))
                    tests['data_test'] = self.__loadfile(os.path.join(self.path, item, self.info.data_test_name))
                    self.data['tests'].append(tests)
        else:
            self.status = False
                
    
    def align(self,shift=0,mult=500,ignore = False):
        
        if(self.status != False):
            if(self.__aligned == False):
                # вычисляем границы аквтивностей
                self.data['states_train'], items = self.__gettimegrid(self.data['states_train'])
                self.data.update(items)
                
                # выравниваем активности трейнов
                self.data['data_train'], self.data['start'], self.data['stop'], self.data['time'] = self.__redef_epoch(self.data['data_train'], self.data['states_train'],self.data['time'],shift,mult)
                
                
                for idx,item in enumerate(self.data['tests']):
                    states, items = self.__gettimegrid(self.data['tests'][idx]['states_test'])
                    
                    if(len(items['start']) > 1):
                        self.data['tests'][idx]['states_test'] = states
                        self.data['tests'][idx].update(items)
                    else:
                        print idx,'---', len(items['start']), items['start']
                        
                    # выравниваем активности тестов
                    self.data['tests'][idx]['data_test'], self.data['tests'][idx]['start'], self.data['tests'][idx]['stop'], self.data['tests'][idx]['time'] = self.__redef_epoch(self.data['tests'][idx]['data_test'], self.data['tests'][idx]['states_test'],self.data['tests'][idx]['time'],shift,mult)
                    
            else:
                print "Данные уже выравнены"
            
            
            self.__aligned = True;
            self.info.labels_names[0] = u'удалено'
            self.info.aligned = True
            self.info.save()
            return True
        else:
            return False
        
            
            # сохраняем дамп с данными
        
        pass
    
        
    def __gettimegrid(self,states):
        
        
        items = {}
        
        try:
            #Добавляем нули в начало и конец массива
            xa = np.hstack([[0],states[0],[0]])
            # Получаем массив единиц и нулей, единициы для ненулевых значений и нулей для остальных
            xa1 =(xa!=0) + 0
            # Получение разницы между последовательными значениями out[n] = a[n+1] - a[n]
            xadf = np.diff(xa1)
            # Найдем start и stop+1 индексы and thus the lengths of "islands" of non-zeros
            items['start'] = np.where(xadf==1)[0]
            items['stop'] = np.where(xadf==-1)[0]
            items['time'] = items['stop'] - items['start'] # длительности событий
            items['num_activities'] = items['start'].shape[0]
            
            
            return states[0,items['start']], items
        except:
            return False,items
        
    
    def __redef_epoch(self,data,events,time,shift = 0,mult = 500, ignore = False):
        # shift - отсекаем начало периода (переходный период активности)
        # mult - кратность отсекания
        new_data = []
        new_start = [] 
        new_stop = []
        new_time = []
        ep_len = time.min() - (time.min()%mult)
        start = 0;
        
        i = 0
        for event in range(1, len(events)+1):
            if ignore is True and events[event-1] == ignore:
                pass
            else:
                new_data.append(data[:, start + shift:start + ep_len])
                new_start.append(i)
                i = i + ep_len - shift
                new_stop.append(i)
                new_time.append(ep_len - shift)
                start +=time[event-1]
        return new_data, new_start, new_stop, new_time
    
    def getinfo(self):
        """
        получение информации об испытании
        """
        
        print "================================================================="
        print 'Experiment status: ', self.info.status, '; Num tests: ', self.info.num_tests
        print 'Align status: ', self.__aligned
        if(self.info.extend['errors']):
            print '------------------------------------------------------------------'
            print "Ошибки сборки: "
            for count, item in enumerate(self.info.extend['errors']):
                print item.ljust(10),
            if count % 1 == 0 and count != 0:
                print
            print '------------------------------------------------------------------'    
        
        if(self.status != False):
            print 'Respondent name: ', self.info.resp_name
            print 'Description:', self.info.description
            print 'Labels_names: [', ', '.join([str(x.encode('utf-8')) for x in self.info.labels_names]),']'
            print 'Frequency:', self.info.frequency
            print 'Count train activities: ',  self.data['num_activities']
            print 'Count tests activities:', '[', ', '.join([str(x['num_activities']) for x in self.data['tests']]),']'
            print 'Time of activity:', self.data['time'][0]
            
            print '------------------------------------------------------------------'
            print 'Chanels_names:'
            print '------------------------------------------------------------------'
            for count, item in enumerate(self.info.chanels_names):
                print item.ljust(10),
                if count % 5 == 0 and count != 0:
                    print
            print
            print '------------------------------------------------------------------'
            print 'List tests'
            print '------------------------------------------------------------------'
            for count, item in enumerate(self.info.list_tests):
                print item.ljust(10),
                if count % 2 == 0 and count != 0:
                    print
            print
            
            print '=================================================================='
        
                
      
    def __loadfile(self,pathload):
        with open(pathload, 'rb') as input_load:
            data_load = pickle.load(input_load)
        return data_load
    
    def save(self,filename = 'exp_data_aligned',mode = 'class'):
        if(mode == 'data'):
            with open(os.path.join(self.path,filename + '.dat'), 'wb') as output:
                pickle.dump(self.data, output, pickle.HIGHEST_PROTOCOL)
        elif(mode == 'class'):
            with open(os.path.join(self.path,filename + '.cls'), 'wb') as output:
                pickle.dump(self, output, pickle.HIGHEST_PROTOCOL)
        

    pass