# -*- coding: utf-8 -*-
'''
Created on 2013-3-10

@author: hmwv1114
'''
fille = open('data/news.txt','w')

from sgmllib import SGMLParser
import jieba
import encodings

def strQ2B(ustring):
    """把字符串全角转半角"""
    rstring = ""
    for uchar in ustring:
        inside_code=ord(uchar)
        if inside_code==0x3000:
            inside_code=0x0020
        else:
            inside_code-=0xfee0
        if inside_code<0x0020 or inside_code>0x7e:      #转完之后不是半角字符返回原来的字符
            rstring += uchar
        else:
            rstring += unichr(inside_code)
    return rstring

class PageAnalyse(SGMLParser):
    '''
    use SGMLParser to analyse the zhidao page
    '''


    def reset(self):
        '''
        Constructor
        '''
        SGMLParser.reset(self)
        
        self.content = ''
        self.iscontent = False
        self.str = ''
        
    def start_content(self, attrs):
        self.iscontent = True
    
    def end_content(self):
        self.iscontent = False
            
    def handle_data(self, data):
        if self.iscontent:
            str = strQ2B(data.decode('gb18030'))
            #fille.write('<content>' + str + '</content>\n')
            
            t = list(jieba.cut(str, cut_all = False))
            str = ''
            for word in t:
                str += word + ' '
            fille.write(str+'\n')
            
            
pageAnalyse = PageAnalyse()
source = open('data/news_tensite_xml.dat').read()
pageAnalyse.feed(source)

fille.flush()
fille.close()