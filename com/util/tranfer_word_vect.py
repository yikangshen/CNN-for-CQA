'''
Created on 2013.11.3

@author: Yikang
'''
import jieba
import numpy
import theano

def tranfer_vect(words, word_list):
    vect = numpy.zeros(len(word_list), dtype=theano.config.floatX)
    for i in xrange(len(word_list)):
        if (words.has_key(word_list[i])):
            vect[i] = words[word_list[i]]
    return vect

def tranfer_dict_vect(segList):
    x = {}
    for word in segList:
        if x.has_key(word):
            x[word] = x[word] + 1
        else:
            x[word] = 1
    return x

def tranfer_dict_vect100(question):
    segList = list(jieba.cut(question, cut_all = False))
    x = {}
    p = 100 / (float)(len(segList))
    for word in segList:
        if x.has_key(word):
            x[word] = x[word] + p
        else:
            x[word] = p