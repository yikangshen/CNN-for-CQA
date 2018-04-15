# -*- coding: utf-8 -*-
'''
Created on 2013.11.14

@author: Yikang
'''

import numpy
import shelve

import theano
import theano.tensor as T

import scipy.sparse as sp

def load_data(database_name, start, end):
    def tranfer_data(x, word_list):
        row = []
        col = []
        data = []
        for i in xrange(len(x)):
            print i
            words = x[i]
            for j in xrange(len(word_list)):
                if (words.has_key(word_list[j])):
                    row.append(i)
                    col.append(j)
                    data.append(words[word_list[j]] / 100.0)
        x_sparse = sp.csr_matrix((data,(row,col)), shape=(len(x),len(word_list)), 
                                 dtype=theano.config.floatX).toarray()
        return x_sparse
        
    def shared_dataset(data_xy, word_list, borrow=True):
        data_x, data_y = data_xy
        data_x = tranfer_data(data_x, word_list)
        shared_x = theano.shared(data_x,
                                 borrow=borrow)
        shared_y = theano.shared(numpy.asarray(data_y,
                                               dtype=theano.config.floatX),
                                 borrow=borrow)
        return shared_x, T.cast(shared_y, 'int32')

    #f = open(database_name, 'rb')
    #x, y, word_list, categories = cPickle.load(f)
    
    db = shelve.open(database_name, 'c')
    x = db['x']
    y = db['y']
    x = x[start:end]
    y = y[start:end]
    word_list = db['word_list']
    categories = db['categories']
    db.close()
    
    remove_word = []
    twords = {}
    for xx in x:
        for word in xx.keys():
            twords[word] = 1
    for word in word_list:
        if not twords.has_key(word):
            remove_word.append(word)
    for word in remove_word:
        word_list.remove(word)
    print len(word_list)
    
    train_set = (x[0 : (int)(len(x) - len(x)/4)], y[0 : (int)(len(x) - len(x)/4)])
    valid_set = (x[(int)(len(x) - len(x)/4) : int(len(x) - len(x)/8)], 
                 y[(int)(len(x) - len(x)/4) : int(len(x) - len(x)/8)])
    test_set = (x[int(len(x) - len(x)/8) : len(x)], y[int(len(x) - len(x)/8) : len(x)])
    
    test_set_x, test_set_y = shared_dataset(test_set, word_list)
    valid_set_x, valid_set_y = shared_dataset(valid_set, word_list)
    train_set_x, train_set_y = shared_dataset(train_set, word_list)

    rval = [(train_set_x, train_set_y), (valid_set_x, valid_set_y),
            (test_set_x, test_set_y)]
    return (rval, word_list, categories)