# -*- coding: utf-8 -*-
'''
Created on 2013.10.31

@author: Yikang
'''
import shelve

import numpy

import theano
import theano.tensor as T

from mlp import MLP
from com.util.logistic_sgd import LogisticRegression
from com.util.ANNs import HiddenLayer
from convolutional_mlp import LeNetConvPoolLayer

import gensim.models.word2vec as word2vec

from com.util.tranfer_word_vect import tranfer_dict_vect

Narticle = 196879

def create_cf_logistic(n_in, n_out):  
    params_DB = shelve.open('params_logistic.dat')
    best_params = params_DB['params']
    params_DB.close()
    
    x = T.vector('x')
    
    classifier = LogisticRegression(input=x, n_in=n_in, n_out=n_out)
    
    #print best_params[0].get_value()
    
    inc = T.matrix('inc')
    setvalue = theano.function([inc], classifier.W, updates=[(classifier.W, inc)])
    setvalue(best_params[0])
    
    inc = T.vector('inc')
    setvalue = theano.function([inc], classifier.b, updates=[(classifier.b, inc)])
    setvalue(best_params[1])
    
    #print classifier.params[0].get_value()
    #print classifier.logRegressionLayer.W.get_value()
    
    vect = T.vector('vect')
    cf = theano.function(inputs=[vect],
            outputs=classifier.p_y_given_x,
            givens={x: vect})
    
    return cf

def create_cf_mlp(n_in, n_out):
    params_DB = shelve.open('params_mlp.dat')
    best_params = params_DB['params_mlp']
    params_DB.close()
    
    x = T.vector('x')
    
    rng = numpy.random.RandomState(1234)
    
    classifier = MLP(rng=rng, input=x, n_in=n_in,
                     n_hidden=500, n_out=n_out)
    
    #print best_params[0].get_value()
    
    inc = T.matrix('inc')
    setvalue = theano.function([inc], classifier.params[0], updates=[(classifier.params[0], inc)])
    setvalue(best_params[0])
    
    inc = T.vector('inc')
    setvalue = theano.function([inc], classifier.params[1], updates=[(classifier.params[1], inc)])
    setvalue(best_params[1])
    
    inc = T.matrix('inc')
    setvalue = theano.function([inc], classifier.params[2], updates=[(classifier.params[2], inc)])
    setvalue(best_params[2])
    
    inc = T.vector('inc')
    setvalue = theano.function([inc], classifier.params[3], updates=[(classifier.params[3], inc)])
    setvalue(best_params[3])
    
    #print classifier.params[0].get_value()
    #print classifier.logRegressionLayer.W.get_value()
    
    vect = T.vector('vect')
    cf = theano.function(inputs=[vect],
            outputs=classifier.logRegressionLayer.p_y_given_x,
            givens={x: vect})
    
    return cf

def create_cf_cnn(n_in, n_out, nkerns=[20, 50]):
    params_DB = shelve.open('params_cnn.dat')
    best_params = params_DB['params']
    params_DB.close()
      
    x = T.vector('x')
    
    rng = numpy.random.RandomState(1234)
    
    # Reshape matrix of rasterized images of shape (batch_size,28*28)
    # to a 4D tensor, compatible with our LeNetConvPoolLayer
    layer0_input = x.reshape((1, 1, 30, 50))

    # Construct the first convolutional pooling layer:
    # filtering reduces the image size to (28-5+1,28-5+1)=(24,24)
    # maxpooling reduces this further to (24/2,24/2) = (12,12)
    # 4D output tensor is thus of shape (batch_size,nkerns[0],12,12)
    layer0 = LeNetConvPoolLayer(rng, input=layer0_input,
            image_shape=(1, 1, 30, 50),
            filter_shape=(nkerns[0], 1, 5, 5), poolsize=(2, 2))

    # Construct the second convolutional pooling layer
    # filtering reduces the image size to (12-5+1,12-5+1)=(8,8)
    # maxpooling reduces this further to (8/2,8/2) = (4,4)
    # 4D output tensor is thus of shape (nkerns[0],nkerns[1],4,4)
    layer1 = LeNetConvPoolLayer(rng, input=layer0.output,
            image_shape=(1, nkerns[0], 13, 23),
            filter_shape=(nkerns[1], nkerns[0], 5, 5), poolsize=(2, 2))

    # the HiddenLayer being fully-connected, it operates on 2D matrices of
    # shape (batch_size,num_pixels) (i.e matrix of rasterized images).
    # This will generate a matrix of shape (20,32*4*4) = (20,512)
    layer2_input = layer1.output.flatten(2)

    # construct a fully-connected sigmoidal layer
    layer2 = HiddenLayer(rng, input=layer2_input, n_in=nkerns[1] * 4 * 9,
                         n_out=500, activation=T.tanh)

    # classify the values of the fully-connected sigmoidal layer
    layer3 = LogisticRegression(input=layer2.output, n_in=500, n_out=2)
    
    params = layer3.params + layer2.params + layer1.params + layer0.params
    
    #print best_params[0].get_value()
    
    for i in range(len(best_params)):
        try:
            inc = T.vector('inc')
            setvalue = theano.function([inc], params[i], updates=[(params[i], inc)])
            setvalue(best_params[i])
        except:
            try:
                inc = T.matrix('inc')
                setvalue = theano.function([inc], params[i], updates=[(params[i], inc)])
                setvalue(best_params[i])
            except:
                inc = T.tensor4('inc')
                setvalue = theano.function([inc], params[i], updates=[(params[i], inc)])
                setvalue(best_params[i])
    
    #print classifier.params[0].get_value()
    #print classifier.logRegressionLayer.W.get_value()
    
    vect = T.vector('vect')
    cf = theano.function(inputs=[vect],
            outputs=layer3.p_y_given_x,
            givens={x: vect})
    
    return cf

def sum(matrix):
    return numpy.sum(matrix)

def VSM(question, answer, word_dict, translation):  
    q = tranfer_dict_vect(question)
    d = tranfer_dict_vect(answer)
     
    wq = {}
    Wq = 0.0
    for word in q.keys():
        if word_dict.has_key(word):
            wq[word] = numpy.log(1+Narticle/float(word_dict[word][0]))
            Wq += wq[word]*wq[word]
    Wq = numpy.sqrt(Wq)
    
    wd = {}
    Wd = 0
    for word in d.keys():
        wd[word] = 1 + numpy.log(d[word])
        Wd += wd[word]*wd[word]
    Wd = numpy.sqrt(Wd)
    
    s = 0.0
    for word in wq.keys():
        if word in wd.keys():
            s += wq[word]*wd[word]
    
    s = s / Wq / Wd
    
    return s

def Okapi(question, answer, word_dict, translation):  
    q = tranfer_dict_vect(question)
    d = tranfer_dict_vect(answer)
    k1 = 1.2
    b = 0.75
         
    wq = {}
    for word in q.keys():
        if word_dict.has_key(word):
            wq[word] = numpy.log((Narticle-word_dict[word][0]+0.5)/(word_dict[word][0]+0.5))*q[word]
    
    wd = {}
    Kd = k1*((1-b)+b*len(question)*27)
    for word in d.keys():
        wd[word] = (k1+1)*d[word]/(Kd+d[word])
    
    s = 0.0
    for word in wq.keys():
        if word in wd.keys():
            s += wq[word]*wd[word]
    
    return s

def LM(question, answer, word_dict, translation):
    q = tranfer_dict_vect(question)
    d = tranfer_dict_vect(answer)
    Pd = {}
    Pc = {}
    lbd = 0.2
    s = 1.0
    for word in q.keys():
        if word in d.keys():
            Pd[word] = float(d[word])/len(answer)
        else:
            Pd[word] = 0
        if word_dict.has_key(word):
            Pc[word] = word_dict[word][1]
        else:
            Pc[word] = 1.0 / 80000.0
        
        s *= (1-lbd)*Pd[word] + lbd*Pc[word]
    return s

def TM(question, answer, word_dict, translation):
    q = tranfer_dict_vect(question)
    d = tranfer_dict_vect(answer)
    Pd = {}
    Pc = {}
    lbd = 0.2
    s = 1.0
    for word in q.keys():
        Pd[word] = 0
        
        for w in d.keys():
            #if translation[word].has_key(w):
                #Pd[word] += translation[word][w] * float(d[w])/len(answer)
            t = translation.similarity(word, w)
            if t > 0:
                Pd[word] += t * float(d[w])/len(answer)
        
        if word_dict.has_key(word):
            Pc[word] = word_dict[word][1]
        else:
            Pc[word] = 1.0 / 80000.0
        
        s *= (1-lbd)*Pd[word] + lbd*Pc[word]
    return s 

def TLM(question, answer, word_dict, translation):
    q = tranfer_dict_vect(question)
    d = tranfer_dict_vect(answer)
    Pd = {}
    Pc = {}
    lbd = 0.2
    beta = 0.8
    s = 1.0
    for word in q.keys():
        Pd[word] = 0
        
        for w in d.keys():
            #if translation[word].has_key(w):
                #Pd[word] += translation[word][w] * float(d[w])/len(answer)
            t = translation.similarity(word, w)
            if t > 0:
                Pd[word] += t * float(d[w])/len(answer)
            
        if word in d.keys():
            Pd[word] = Pd[word] * beta + (1-beta) * float(d[word])/len(answer)
        else:
            Pd[word] = Pd[word] * beta
            
        if word_dict.has_key(word):
            Pc[word] = word_dict[word][1]
        else:
            Pc[word] = 1.0 / 80000.0
        
        s *= (1-lbd)*Pd[word] + lbd*Pc[word]
    return s 

if __name__ == '__main__':
    db = shelve.open('database_30_50.dat')

    model = word2vec.Word2Vec.load('word_embedding_zhidao_100D')
    
    cf = create_cf_cnn(1*30*50, 2)
    
    word_dict = db['word_dict']
    translation = db['translation']
    pageGroupList = db['pageGroupList']
        
    print 'start'
    '''
    testTable = db['TestTable']
    table = []
    for pageGroup in pageGroupList:
        for index in pageGroup.Table:
            if index in testTable:
                table.append(index)
    '''
    table = db['TestTable']
    qa50 = db['qa']
    print(len(table))
    k0 = 0
    n = 0
    l = 0
    nDCG6 = 0.0
    groups = {}
    for pageGroup in pageGroupList:
        groups[pageGroup.tag] = numpy.array([0,0,0], dtype=numpy.float32)
        
    while (n < len(table)) and (n < 1000):
        l += 1
        index = table[l-1]
        
        question, answer = qa50[index]
        answer_quality = numpy.zeros(6)
        
        matrix = []
        for j in range(30):
            t = []
            for k in range(50):
                #t.append(numpy.abs(question[j%len(question)]-answer[k%len(answer)]))
                t.append([numpy.abs(model.similarity(question[j%len(question)], answer[k%len(answer)]))])
            matrix.append(t)
            
        matrix = numpy.array(matrix,dtype=numpy.float32)
        matrix = matrix.transpose(2,0,1).flatten()
        answer_quality[0] = cf(matrix)[0][1]
        #answer_quality[0] = sum(matrix)
        
        #answer_quality[0] = Okapi(question,answer,word_dict,model)
        
        for i in range(5):
            #print l, i
            if l+i+1 < len(table):
                t, answer = qa50[table[l+i]]
            else:
                t, answer = qa50[table[l-i-2]]
            
            matrix = []
            for j in range(30):
                t = []
                for k in range(50):
                    #t.append(numpy.abs(question[j%len(question)]-answer[k%len(answer)]))
                    t.append([numpy.abs(model.similarity(question[j%len(question)], answer[k%len(answer)]))])
                matrix.append(t)
                
            matrix = numpy.array(matrix,dtype=numpy.float32)
            matrix = matrix.transpose(2,0,1).flatten()
            answer_quality[i+1] = cf(matrix)[0][1]
            #answer_quality[i+1] = sum(matrix)
            
            #answer_quality[i+1] = Okapi(question,answer,word_dict,model)
        
        print answer_quality
        n += 1
        print n
        #c = numpy.argmax(answer_quality)
        c = 0
        for i in range(5):
            if answer_quality[i+1] >= answer_quality[0]:
                c += 1
        if c == 0:
            k0 += 1
            nDCG6 += 1
        else:
            nDCG6 += 1 / numpy.log2(c+1)
            
        for pageGroup in pageGroupList:
            if index in pageGroup.Table:
                if c == 0:
                    groups[pageGroup.tag] += [1,1,1]
                else:
                    groups[pageGroup.tag] += [1,0,1 / numpy.log2(c+1)]
    
    print float(k0) / n,n
    print nDCG6/n
    for pageGroup in pageGroupList:
        print pageGroup.tag
        if groups[pageGroup.tag][0] > 0:
            groups[pageGroup.tag][1] /= groups[pageGroup.tag][0]
            groups[pageGroup.tag][2] /= groups[pageGroup.tag][0]
            print groups[pageGroup.tag]
    db.close()