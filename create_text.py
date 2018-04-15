# -*- coding: utf-8 -*-
'''
Created on 2014.1.10

@author: Yikang
'''
import shelve
import jieba 
import re
import DBModule.DBhelper as DBhelper

text = open('training_text_all_word1.txt','w')

database_name = 'data\database_zhidao_438078_unselected.dat'
#database_name = 'data\database_zhidao_1000.dat'
db = shelve.open(database_name, 'c')

accepted_chars = re.compile(ur"[\u4E00-\u9FA5]+")
    
table = db['Table']

i = 0
string = ''
for index in table:
    i += 1
    print i
    article = db[index]
    segList = list(jieba.cut(article.strip(), cut_all = False))
    for word in segList:
        #if accepted_chars.match(word):
        string += word + ' '
    string += '\n'
    if i % 500 == 0:
        text.write(string)
        string = ''
        
db.close()
        
db2 = DBhelper.DBHelper()
categories = db2.selectAllClass()
string = ''
for a,b,c,d in categories:
    questions = db2.selectAllQuestionWithClassAlike(b)
    print questions

text.write(string)    
text.flush()
text.close()