# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 09:51:35 2017

@author: Egor Mikheev
@email: mail@nebesa.me
@package: github/thisroot/eeglab
"""

import pickle, os, glob, sys
import numpy as np

from EEG.info import info_series
from EEG.preprocessing import aligner_exp

class aligner_series:
    def __init__(self,path = '.\\', fileinfo = 'series_info.dat'):
                
        self.fileinfo = fileinfo
        self.path = path
        self.info = self.__loadinfo(self.path, self.fileinfo)
        
        info = info_series(self.path)
        info.save()
        
        
    def __loadinfo(self,path, fileinfo):
        try:
            with open(os.path.join(path, fileinfo), 'rb') as input:   
                data = pickle.load(input)
            return data
        except:
            sys.exit('Object:' + os.path.join(path, fileinfo) +' can\'t load')
            
            
    def align(self,shift=0, mult=500, ignore = False, mode = 'Force', filename = 'exp_data_aligned', saveas = 'data'):
        for idx, item in enumerate(self.info.list_exp):
            aligner = aligner_exp(os.path.join(self.path,item))
            flag = aligner.align(shift,mult)
            
            if(flag == True):
                aligner.save(mode = saveas)
            else:
                self.__delFalseExpInfo(idx)
        return True
        pass
    
    
    def __delFalseExpInfo(self,idx):
        self.info.list_exp.pop(idx)
        #self.info.save()
        #self.info = self.__loadinfo(self.path,self.fileinfo)
        pass
       
        
    def getinfo(self):
        return self.info.getinfo()