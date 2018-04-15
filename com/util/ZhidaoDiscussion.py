'''
Created on 2013-3-11

@author: hmwv1114
'''

import jieba
from com.util.Article import Article

class ZhidaoDiscussion(Article):
    '''
    this is a class who storage question and answers in one page
    '''


    def __init__(self):
        '''
        Constructor
        '''
        Article.__init__(self)
        self.question = []
        self.answer = []
        self.classinfo = []
        self.bestAnswer = False
        self.answerNumber = 0
        
        
    def add_question(self, questioner, question):   
        self.question.append([questioner, question])
        segList = jieba.cut(question, cut_all = False)
        for word in segList:
            if word in self.wordVect:
                self.wordVect[word] = self.wordVect[word] + 1
            else:
                self.wordVect[word] = 1
            self.totalWord += 1
        
    def add_answer(self, answerer, answer):
        self.answer.append([answerer, answer])
        self.answerNumber = self.answerNumber + 1
        segList = jieba.cut(answer, cut_all = False)
        for word in segList:
            if word in self.wordVect:
                self.wordVect[word] = self.wordVect[word] + 1
            else:
                self.wordVect[word] = 1
            self.totalWord += 1
        
    def strip(self):
        string = str(self.index) + '\n' + 'question' + '\n'
        for s in self.classinfo:
            string = string + s + ' '
        string = string + '\n'
        string = string + '<questionner>' + self.question[0][0] + '</questionner>' + '\n' + '<question>' + self.question[0][1] + '</question>\n'
        string = string + 'answer' + '\n'
        for k,v in self.answer:
            string = string + '<answerer>' + k + '</answerer>\n' + '<answer>' + v + '</answer>' + '\n'
            
        return string