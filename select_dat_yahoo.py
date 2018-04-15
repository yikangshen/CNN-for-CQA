# -*- coding: utf-8 -*-
'''
Created on 2014.1.25

@author: Yikang
'''
import shelve
import gensim.models.word2vec as word2vec
import nltk

stemmer = nltk.stem.lancaster.LancasterStemmer()

db = shelve.open('yahoo/travel_70142.dat')

fille = open('training_text_yahoo_travel.txt','w')

model = word2vec.Word2Vec.load('word_embedding_yahoo_100D')
        
print 'start'
    
table = db['Table']
table50 = []
qa50 = {}
n = 0
for index in table:
    n += 1
    print n

    question, answer = db[index]
    
    tquestion = []
    tquestion1 = []
    for i in range(len(question)):
        question[i] = stemmer.stem(question[i])
        fille.write(question[i] + ' ')
        try:
            tquestion.append(model[question[i].encode('utf-8')])
            tquestion1.append(question[i].encode('utf-8'))
        except:
            pass
    question = tquestion1
    if (len(question) == 0) or (len(question) > 50):
        continue
    
    tanswer = []
    tanswer1 = []
    for j in range(len(answer)):
        answer[j] = stemmer.stem(answer[j])
        fille.write(answer[j] + ' ')
        try:
            tanswer.append(model[answer[j].encode('utf-8')])
            tanswer1.append(answer[j].encode('utf-8'))
        except:
            pass
    answer = tanswer1
    if (len(answer) == 0) or (len(answer) > 50):
        continue
    
    table50.append(index)
    qa50[index] = (question, answer)

print len(table50)

newdb = shelve.open('database_yahoo_50.dat')    
newdb['Table'] = table50
newdb['qa'] = qa50
newdb.close()

db.close()