# -*- coding: utf-8 -*-
'''
Created on 2013-3-13

@author: hmwv1114
'''
import shelve
from com.util.PageGroup import PageGroup
import time
import shutil
from datetime import date
import os

def classupcast(categories, category):
    for a,b,c,d in categories:
        if b == category:
            if d == 1:
                return category
            else:
                for aa,bb,cc,dd in categories:
                    if aa == c:
                        return classupcast(categories, bb)
    return 'None'

if __name__ == '__main__':
    
    db2 = shelve.open('categories.dat','c')
    categories = db2['categories']
    db2.close()
    
    origine = 'database_yahoo'
    
    newFolderName = origine + '_' + date.today().strftime("%Y_%m_%d")
    i = 0
    while os.path.isdir( newFolderName ):
        i = i + 1
        newFolderName = origine + '_' + date.today().strftime("%Y_%m_%d") + '_' + str(i)
    print(newFolderName)
    if os.path.isdir( newFolderName ):
        print(newFolderName," Exists already ")
    else:
        os.mkdir( newFolderName )
        print(newFolderName," Create OK ")
    
    shutil.copy('data/' + origine + '.dat', newFolderName+'\\' + origine + '.dat')
    
    os.chdir(newFolderName)
    
    try:
        #create new database
        db = shelve.open(origine+'.dat', 'c') 
        questionTable = db['Table']
        
        if db.has_key('pageGroupList'):
            pageGroupList = db['pageGroupList']
        else:
            pageGroupList = []
            db['pageGroupList'] = pageGroupList
            
        if db.has_key('pageGroupPoints'):
            pageGroupPoints = db['pageGroupPoints']
        else:
            pageGroupPoints = []
            db['pageGroupPoints'] = pageGroupPoints
        startTime = time.ctime()
        i = 0
        
        questions = {}
        for index in questionTable:
            questions[index] = db[index]
        
        for index in questionTable:
            print str(i) + ' ' + index + ' start at ' + time.ctime()
            
            if index in pageGroupPoints:
                i += 1
                continue
            
            relatedGroup = []
            page = db[index]
            flag = False
            page.classinfo[1] = classupcast(categories, page.classinfo[1])
            '''
            if page.classinfo[1] == '资源共享':
                continue
            '''
            for pageGroup in pageGroupList:
                if pageGroup.tag == page.classinfo[1]:
                    pageGroup.addNewPoint(index, questions)
                    flag = True
                    break
                    
            if not flag:
                pageGroup = PageGroup()
                pageGroup.tag = page.classinfo[1]
                print pageGroup.tag
                pageGroup.addNewPoint(index, questions)
                pageGroupList.append(pageGroup)
                
            pageGroupPoints.append(index)
            
            print 'Nombre de Group: ' + str(len(pageGroupList))
                    
            i += 1
            
        time.sleep(3)
        db['pageGroupPoints']= pageGroupPoints
        time.sleep(3)
        db['pageGroupList'] = pageGroupList
        time.sleep(3)
        db.sync()
    
        endTime = time.ctime()
            
        resultFile = open(origine+'_similarity_result.txt','w')
        resultFile.write(origine + '\n')
        resultFile.write(startTime + '\n')
        resultFile.write(endTime + '\n')
        resultFile.write('Nombre de Space: ' + str(len(pageGroupList)) + '\n')
        groupSize = {}
        for pageGroup in pageGroupList:
            if groupSize.has_key(pageGroup.nombreDeArticle):
                groupSize[pageGroup.nombreDeArticle] += 1
            else:
                groupSize[pageGroup.nombreDeArticle] = 1
            resultFile.write(pageGroup.tag + ': ' + str(pageGroup.nombreDeArticle) + '\n')
        resultFile.write(str(groupSize) + '\n')
        resultFile.flush()
        resultFile.close()
    finally:
        db.close()
        
    print 'tout fini'