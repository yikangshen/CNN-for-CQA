# -*- coding: utf-8 -*-
'''
Created on 2013��11��14��

@author: Yikang
'''

def decode(s):
    try:
        s = s.decode('utf-8')
    except:
        s = s.decode('gb2312')

def encode(s):
    try:
        s = s.encode('utf-8')
    except:
        print 'encode wrong'