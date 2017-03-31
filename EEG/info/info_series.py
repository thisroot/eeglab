# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 09:51:35 2017

@author: Egor Mikheev
@email: mail@nebesa.me
@package: github/thisroot/eeglab
"""
import pickle, os, glob, sys

class info_series():
    
    def __init__(self,path = False, info = {}) :
        
        # поля по умолчанию
        exp_name = 'name'
        description = 'description'
        labels_names = []
        frequency = False
        chanels_names = []
        extend = {'description':'extend experiment info'}
        
        # информация о названиях файлов с данными
        self.data_train_name = 'states_full.pkl'
        self.states_train_name = 'data.pkl'
        
        #информация о конфиг файлах
        self.exp_conf_file_name = 'exp_info.dat'
        self.series_conf_file_name = 'series_info.dat'
        
        
        # конструктор полей
        self.path = path
        
        self.exp_name = (info['exp_name'] if 'exp_name' in info else  exp_name)
        self.description = (info['description'] if 'description' in info else  description)
        self.labels_names = (info['labels_names']  if 'labels_names' in info else  labels_names)
        self.frequency = (info['frequency'] if 'frequency' in info else  frequency)
        self.chanels_names = (info['chanels_names'] if 'chanels_names' in info else  chanels_names)
        self.extend = (info['extend'] if 'extend' in info else  extend)
        
        # получение данных вложенных каталогов
        

        # обновим информацию об испытаниях
        self.update_info()
                
    def update_info(self,method = 'onlyread'):
        """
        обновление информации о структуре каталогов эксперимента
        
        @method - метод по которому будет производится сбор информации
            
            onread -      только чтение данных экспериментов 
            rewrite -     сканирование каталогов и генерация новых данных для 
                          них в случае если данные отсутствуют
        """
        
        if(self.path == False):
            print 'path not set'
        else:
            list_exp = []
            
            os.chdir(self.path)
            for idx,file in enumerate(glob.glob("*_*_*")):
                list_exp.append(file)
            
            self.num_exp = len(list_exp)
            if(len(list_exp) == 0):
                    print 'Experiments not found'
                    return False
            self.list_exp = list_exp
            self.exp_info = dict.fromkeys(list_exp, False)
            
            for item in self.list_exp:
                ## загрузка файла
                data = self.load_info_exp(item)
                if(method == 'onlyread'):
                    if(data != False):
                        self.exp_info[item] = data
                if(method == 'rewrite'):
                    # здесь надо реализовать функцию перезаписи объектов, в случае если в них отсутствует файл info.dat
                    # стоит подумать о том, какими инициализирующими значениями заполнять каждый из наборов
                    # возможно перед этим стоит заполнить данный класс общими данными
                    print 'перезапись'
                
                
            # заполняем агрегированными данными
            # инициализируем счетчики
            self.num_exp = 0
            self.num_exp_success = 0
            self.num_tests = 0
            self.num_tests_success = 0
            self.resp_names = []
            
            for item in self.exp_info:
                self.num_exp =  self.num_exp + 1
                self.num_tests = self.num_tests + self.exp_info[item].num_tests
                self.resp_names.append(self.exp_info[item].resp_name)
                
                if(self.exp_info[item].status == True):
                    self.num_exp_success = self.num_exp_success + 1
                    self.num_tests_success = self.num_tests_success + self.exp_info[item].num_tests
            # Основные данные эксперимента
                self.labels_names = self.exp_info[item].labels_names
                self.frequency = self.exp_info[item].frequency
                self.chanels_names = self.exp_info[item].chanels_names
                self.data_train_name = self.exp_info[item].data_train_name
                self.states_train_name = self.exp_info[item].states_train_name
            self.resp_names = set(self.resp_names)
            
    def getinfo(self):
        """
        получение информации о серии экспериментов
        """
        print "================================================================="
        print 'Name series of experiments: ', self.exp_name
        print 'Description:', self.description
        print 'Count experiments:', self.num_exp, 'Successed:', self.num_exp_success
        print 'Num test', self.num_tests, 'Num tests among sucessed', self.num_tests_success
    
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
        print '-------------------------------------------------------------------'
        print 'Unique respondents'
        print '-------------------------------------------------------------------'
        for count, item in enumerate(self.resp_names):
            print item.ljust(10),
            if count % 3 == 0 and count != 0:
                print
        print
        print '------------------------------------------------------------------'
        print 'List experiments'
        print '------------------------------------------------------------------'
        for count, item in enumerate(self.list_exp):
            
            print item.ljust(10),
            if count % 2 == 0 and count != 0:
                print
        print
        
        print '=================================================================='
     
    def load_info_exp(self,name,filename = 'exp_info.dat'):
        try:
            with open(os.path.join(self.path + name,filename), 'rb') as input:   
                data = pickle.load(input)
        except:
            sys.exit('object can\'t load')
             
        return data
    
    def save(self,filename = 'series_info.dat'):
        with open(os.path.join(self.path,filename), 'wb') as output:
            pickle.dump(self, output, pickle.HIGHEST_PROTOCOL)