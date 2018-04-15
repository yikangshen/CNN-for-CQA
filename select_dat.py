# -*- coding: utf-8 -*-
'''
Created on 2014.1.25

@author: Yikang
'''
import shelve
import gensim.models.word2vec as word2vec
import jieba
from com.util.tranfer_word_vect import tranfer_dict_vect
from com.util.ZhidaoDiscussion import ZhidaoDiscussion

db = shelve.open('database_zhidao_196879_selected_2014_01_23_2/database_zhidao_196879_selected.dat')

model = word2vec.Word2Vec.load('word_embedding_zhidao_100D')
        
print 'start'

lq = 0
la = 0
    
exclu_table = []
pageGroupList = db['pageGroupList']
for pageGroup in pageGroupList:
    try:
        pageGroup.tag = pageGroup.tag.decode('gb2312')
    except:
        pass
    if pageGroup.tag == '游戏':
        exclu_table = pageGroup.Table
'''
table = []
for pageGroup in pageGroupList:
    if pageGroup.tag == '资源共享':
        continue
    for index in pageGroup.Table:
        table.append(index)
'''   
table = db['Table']
table50 = []
qa = {}
word_dict = {}
words = []
nword = 0
n = 0

newdb = shelve.open('database_30_50_games.dat')
newdb['pageGroupList'] = pageGroupList

for index in table:
    if not(index in exclu_table):
        continue
    n += 1
    print n
    
    article = db[index]
    question = list(jieba.cut(article.question[0][1], cut_all=False))
    tquestion = []
    tquestion1 = []
    for i in range(len(question)):
        try:
            tquestion.append(model[question[i].encode('utf-8')])
            tquestion1.append(question[i].encode('utf-8'))
        except:
            pass
    question = tquestion1
    lq += len(question)
        
    answer = []
    try:
        answer = list(jieba.cut(article.answer[0][1]))
    except:
        continue
    tanswer = []
    tanswer1 = []
    for j in range(len(answer)):
        try:
            tanswer.append(model[answer[j].encode('utf-8')])
            tanswer1.append(answer[j].encode('utf-8'))
        except:
            pass
    answer = tanswer1
    la += len(answer)
    
    word_vect = tranfer_dict_vect(question+answer)
    for word in word_vect.keys():
        if word_dict.has_key(word):
            word_dict[word][0] += 1
            word_dict[word][1] += word_vect[word]
        else:
            word_dict[word] = [1, word_vect[word]]
        nword += word_vect[word]
    
    if (len(question) == 0) or (len(answer) == 0):
        continue
    if (len(question) > 30) or (len(answer) > 50):
        continue
    table50.append(index)
    qa[index] = (question,answer)
    words.extend(question)
    words.extend(answer)

print lq/n, la/n
print len(table50)
TestTable = table50[len(table50)-len(table50)/11:len(table50)]

narticle = len(table)    
for word in word_dict:
    word_dict[word][1] = float(word_dict[word][1]) / nword

newdb['Table'] = table50[0:len(table50)-len(table50)/11]
newdb['TestTable'] = TestTable
newdb['qa'] = qa
newdb['word_dict'] = word_dict

n = 0
translation = {}
word_count1 = {}
word_count2 = {}
for index in table50:
    if index in TestTable:
        continue
    n += 1
    print n
        
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

newdb['translation'] = translation

newdb.close()
db.close()