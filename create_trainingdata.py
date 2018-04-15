# -*- coding: utf-8 -*-
'''
Created on 2014.1.12

@author: Yikang
'''
import gensim.models.word2vec as word2vec
import shelve
import numpy

model = word2vec.Word2Vec.load('word_embedding_zhidao_100D')
database_name = 'database_30_50_games.dat'
db = shelve.open(database_name, 'c')

table = db['Table']
qa = db['qa']

l = 0
n = 0
ny = 0
nn = 0
x = []
y = []
pre_answer = None
for index in table:
    question, answer = qa[index]
    l += 1
        
    matrix0 = []
    for j in range(30):
        t = []
        for k in range(50):
            #print [question[j%len(question)], answer[k%len(answer)]]
            t.append([model.similarity(question[j%len(question)], answer[k%len(answer)])])
        matrix0.append(t)
        
    matrix0 = numpy.array(matrix0,dtype=numpy.float32)
    matrix0 = matrix0.transpose(2,0,1)
    
    for i in range(9):
        if l+i >= len(table):
            break
        t, answer = qa[table[l+i]]
        
        matrix1 = []
        for j in range(30):
            t = []
            for k in range(50):
                t.append([model.similarity(question[j%len(question)], answer[k%len(answer)])])
            matrix1.append(t)
                
        matrix1 = numpy.array(matrix1,dtype=numpy.float32)
        matrix1 = matrix1.transpose(2,0,1)

        x.append(matrix1.flatten())
        y.append(0)
        nn += 1
        
        x.append(matrix0.flatten())
        y.append(1)
        ny += 1
        
        n += 1
        print n
    if n >= 90000:
        break
    
db.close()

n = len(x)/2
print n,ny,nn
fille = shelve.open('training_data_30_50_1_9_games.dat','c')
'''
fille['train_set'] = (x[0:n/4*3*2],y[0:n/4*3*2])
fille['valid_set'] = (x[n/4*3*2:n/8*7*2],y[n/4*3*2:n/8*7*2])
fille['test_set'] = (x[n/8*7*2:n*2],y[n/8*7*2:n*2])
'''
fille['train_set1'] = (x[0:n/10*5*2],y[0:n/10*5*2])
fille['train_set2'] = (x[n/10*5*2:n/10*9*2],y[n/10*5*2:n/10*9*2])
fille['valid_set'] = (x[n/10*9*2:n*2],y[n/10*9*2:n*2])
fille.sync()
fille.close()
                