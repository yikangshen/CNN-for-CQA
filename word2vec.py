# -*- coding: utf-8 -*-
'''
Created on 2014.1.10

@author: Yikang
'''
import gensim.models.word2vec as word2vec


inputtxt = word2vec.Text8Corpus('training_text_yahoo.txt')

model = word2vec.Word2Vec(inputtxt, size=100, window=5, min_count=5, workers=4)

model.save('word_embedding_yahoo_100D')

t = model.most_similar(positive=['apple'], negative = [])
#print model['索尼']
for a,b in t:
    print a
