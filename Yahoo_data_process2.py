# -*- coding: utf-8 -*-
'''
Created on 2014.1.27

@author: Yikang
'''
from sgmllib import SGMLParser
import shelve
import re
import nltk
from nltk.tokenize import wordpunct_tokenize

#tokenizer = RegexpTokenizer('\w+|\$[\d\.]+|\S+')

dbs = {}

tf = open('training_text_yahoo2.txt','w')

stemmer = nltk.stem.porter.PorterStemmer()

def text_process(s):
    ss = re.sub('<br />&#xa;','\n',s)
    tt = wordpunct_tokenize(ss)
    t = []
    for word in tt:
        if (word != '.') and (word != ',') and (word != ':') and (word != '"') and (word != '(') and (word != ')') and (word != ';') and (word != '\''):
            t.append(stemmer.stem(word))
        
    for word in t:
        tf.write(word + ' ')
    tf.write('\n')
    
    return t

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
        self.isQuestion = False
        self.isAnswer = False
        self.isCat = False
        self.isUri = False
        self.isSubCat = False
        self.question = []
        self.answer = []
        self.tempText = ''
        self.category = ''
        self.index = ''
        self.subCat = ''
        self.count = 0
        
    def start_uri(self, attrs):
        self.isUri = True
    
    def end_uri(self):
        self.isUri = False
        
    def start_document(self, attrs):
        self.isTitle = False
        self.isQuestion = False
        self.isAnswer = False
        self.isCat = False
        self.isUri = False
        self.isSubCat = False
        self.question = []
        self.answer = []
        self.tempText = ''
        self.category = ''
        self.index = ''
        self.subCat = ''
    
    def end_document(self):
        self.count += 1
        #print self.count
        
        if self.category != 'travel':
            return
        
        if not dbs.has_key(self.subCat):
            dbs[self.subCat] = shelve.open('yahoo/' + self.subCat+'.dat')
        
        db = dbs[self.subCat]
        if db.has_key('Table'):
            table = db['Table']
        else:
            table = []
        
        #print self.question
        #print self.answer
        if not (self.index in table):
            table.append(self.index)
            db[self.index] = (self.question, self.answer)
            db['Table'] = table
            dbs[self.category] = db
        else:
            print 'same!'
            print db[self.index]
            print (self.question, self.answer)
        print self.count,len(table)
        
    def start_subject(self, attrs):
        self.tempText = ''
        self.isTitle = True
    
    def end_subject(self):
        self.isTitle = False
        self.question = text_process(self.tempText)
        
    def start_content(self, attrs):
        self.tempText = ''
        self.isQuestion = True
    
    def end_content(self):
        self.isQuestion = False
        self.question += text_process(self.tempText)
        
    def start_bestanswer(self, attrs):
        self.tempText = ''
        self.isAnswer = True
    
    def end_bestanswer(self):
        self.isAnswer = False
        self.answer = text_process(self.tempText)
        
    def start_maincat(self, attrs):
        self.isCat = True
        
    def end_maincat(self):
        self.isCat = False
        
    def start_subcat(self, attrs):
        self.isSubCat = True
        
    def end_subcat(self):
        self.isSubCat = False
            
    def handle_data(self, data):
        if self.isTitle:
            self.tempText = self.tempText + data.lower()
        if self.isAnswer:
            self.tempText = self.tempText + data.lower()
        if self.isQuestion:
            self.tempText = self.tempText + data.lower()
        if self.isCat:
            self.category = data.lower()
        if self.isUri:
            self.index = data.lower()
        if self.isSubCat:
            self.subCat = data.lower()
            
pageAnalyse = PageAnalyse()

fille = open('data/FullOct2007.xml.part2','r')

s = fille.read(100000000)
pageAnalyse.feed(s)
while s != '':
    try:
        pageAnalyse.feed(s)
    except:
        pass
    s = fille.read(100000000)
    for db in dbs:
        dbs[db].sync()

fille.close()

for db in dbs:
    dbs[db].close()