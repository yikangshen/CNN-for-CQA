'''
Created on 2013-3-20

@author: hmwv1114
'''

import jieba
from com.util.Article import Article

class BaikeArticle(Article):
    '''
    this is a class who storage Baidu Baike in one page
    '''


    def __init__(self):
        '''
        Constructor
        '''
        Article.__init__(self)
        self.text = ""
        self.openTag = []
        
    def AddText(self, text):
        self.text += text
        segList = jieba.cut(text, cut_all = False)
        for word in segList:
            if word in self.wordVect:
                self.wordVect[word] = self.wordVect[word] + 1
            else:
                self.wordVect[word] = 1
        #self.totalWord += len(segList)
        
    def strip(self):
        ss = ''
        for s in self.openTag:
            ss += s + ' '
        return '<article>' + self.text + '</article>\n' + ss