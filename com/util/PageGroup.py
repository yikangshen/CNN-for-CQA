# -*- coding: utf-8 -*-
'''
Created on 2013-8-30

@author: hmwv1114
'''

class PageGroup:
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
        self.Table = []
        self.nombreDeArticle = 0
        self.tag = ''
        
    def addNewPoint(self, index, questions = None):
        if len(self.Table) == 0:
            self.Table.append(index)
            self.nombreDeArticle = 1
        else:
            if (index in self.Table):
                return
            
            #add to table
            self.Table.append(index)
            self.nombreDeArticle = len(self.Table)