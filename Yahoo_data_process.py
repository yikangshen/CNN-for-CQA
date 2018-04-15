# -*- coding: utf-8 -*-
'''
Created on 2014.1.27

@author: Yikang
'''
from sgmllib import SGMLParser
from com.util.ZhidaoDiscussion import ZhidaoDiscussion
import shelve
import re

db = shelve.open('data/database_yahoo.dat')
if db.has_key('Table'):
    table = db['Table']
else:
    table = []
if db.has_key('count'):
    count = db['count']
else:
    count = 0

class PageAnalyse(SGMLParser):
    '''
    use SGMLParser to analyse the zhidao page
    '''


    def reset(self):
        '''
        Constructor
        '''
        SGMLParser.reset(self)
        
        self.isTitle = False
        self.isName = False
        self.isQuestion = False
        self.isAnswer = False
        self.tempText = ['','']
        self.discussion = None
        self.ok = False
        self.inDocument = False
        self.isCat = False
        self.isUri = False
        self.index = ''
        self.count = 0
        
    def start_uri(self, attrs):
        self.isUri = True
    
    def end_uri(self):
        self.isUri = False
        
    def start_document(self, attrs):
        self.discussion = ZhidaoDiscussion()
        self.inDocument = True
    
    def end_document(self):
        self.count += 1
        self.inDocument = False
        if not self.index in table:
            db[self.index] = self.discussion
            table.append(self.index)
        print self.count,len(table)
        
    def start_subject(self, attrs):
        self.isTitle = True
    
    def end_subject(self):
        self.isTitle = False
        
    def start_content(self, attrs):
        self.isQuestion = True
    
    def end_content(self):
        self.isQuestion = False
        self.tempText[1] = re.sub('<br />&#xa;','\n',self.tempText[1])
        self.discussion.add_question(self.tempText[0], self.tempText[1])
        self.tempText = ['','']
        
    def start_bestanswer(self, attrs):
        self.discussion.bestAnswer = True
        self.isAnswer = True
    
    def end_bestanswer(self):
        self.isAnswer = False
        self.tempText[1] = re.sub('<br />&#xa;','\n',self.tempText[1])
        self.discussion.add_answer(self.tempText[0], self.tempText[1])
        self.tempText = ['','']
        
    def start_answer_item(self, attrs):
        self.isAnswer = True
    
    def end_answer_item(self):
        self.isAnswer = False
        self.tempText[1] = re.sub('<br />&#xa;','\n',self.tempText[1])
        self.discussion.add_answer(self.tempText[0], self.tempText[1])
        self.tempText = ['','']
        
    def start_cat(self, attrs):
        self.isCat = True
        
    def end_cat(self):
        self.isCat = False 
        
    def start_maincat(self, attrs):
        self.isCat = True
        
    def end_maincat(self):
        self.isCat = False
            
    def handle_data(self, data):
        if self.isTitle:
            self.tempText[1] = self.tempText[1] + data + '\n'
        if self.isName:
            self.tempText[0] = data
        if self.isAnswer:
            self.tempText[1] = self.tempText[1] + data
        if self.isQuestion:
            self.tempText[1] = self.tempText[1] + data
        if self.isCat:
            self.discussion.classinfo.append(data)
        if self.isUri:
            self.index = data
            
pageAnalyse = PageAnalyse()

fille = open('data/FullOct2007.xml.part1')

i = 0
while i < count:
    s = fille.read(1000000000)
    i += 1    

s = fille.read(1000000000)

pageAnalyse.feed(s)
'''
try:
    pageAnalyse.feed(s)
except:
    pass
'''
count += 1
db['Table'] = table
db['count'] = count
db.sync()
fille.close()

db['Table'] = table
db.close()