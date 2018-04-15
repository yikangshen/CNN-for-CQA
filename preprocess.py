# -*- coding: utf-8 -*-
'''
Created on 2014.1.25

@author: Yikang
'''

import shelve
from com.util.tranfer_word_vect import tranfer_dict_vect

db = shelve.open('database_30_50.dat')    
table = db['Table']
qa = db['qa']

translation = {}
word_count1 = {}
word_count2 = {}
n=0
for index in table:
    n+=1
    print n
    if n > 90000:
        break
    q,a = qa[index]
    qq = tranfer_dict_vect(q).keys()
    aa = tranfer_dict_vect(a).keys()
    for word0 in qq:
        for word1 in aa:
            if translation.has_key(word0):
                if translation[word0].has_key(word1):
                    translation[word0][word1] += 1.0
                else:
                    translation[word0][word1] = 1.0
            else:
                translation[word0] = {}
                translation[word0][word1] = 1.0
                
    for word in qq:
        if word_count1.has_key(word):
            word_count1[word] += 1
        else:
            word_count1[word] = 1
    for word in aa:
        if word_count2.has_key(word):
            word_count2[word] += 1
        else:
            word_count2[word] = 1
            
for word in translation.keys():
    for w in translation[word].keys():
        translation[word][w] = 0.5*(float(translation[word][w]) / word_count1[word])+0.5*(float(translation[word][w]) / word_count2[w])
    translation[word][word] = 1.0
                
db['translation'] = translation

word_dict = {}
nword = 0
n = 0
for index in table:
    n += 1
    print n
    
    q,a = qa[index]
    word_vect = tranfer_dict_vect(q+a)
    for word in word_vect.keys():
        if word_dict.has_key(word):
            word_dict[word][0] += 1
            word_dict[word][1] += word_vect[word]
        else:
            word_dict[word] = [1, word_vect[word]]
        nword += word_vect[word]

narticle = len(table)    
for word in word_dict:
    word_dict[word][1] = float(word_dict[word][1]) / nword
    
db['word_dict'] = word_dict

db.close()