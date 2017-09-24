# -*- coding: UTF-8 -*-
from numpy import *

def loadDataSet():
    postingList = [['my','dog','has','flea','problems','help','please'],
                   ['maybe','not','take','him','to','dog','park','stupid'],
                   ['my','dalmation','is','so','cute','I','love','him'],
                   ['stop','posting','stupid','worthless','garbage'],
                   ['mr','licks','ate','steak','how','to','stop','him'],
                   ['quit','buying','worthless','dog','food','stupid']]
    classVec = [0,1,0,1,0,1] #1代表侮辱性文字
    return postingList,classVec

def createVocabList(dataSet):   #集合化 返回所有词语
    vocabSet = set([])
    for document in dataSet:
        vocabSet = vocabSet | set(document)
    return list(vocabSet)

def setOfWords2Vec(vocabList,inputSet):  #向量化
    returnVec = [0] * len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] = 1
        else: print "the word: %s is not in my vocabulary!" % word
    return returnVec

def bagOfWords2VecMN(vocabList,inputSet):
    returnVec = [0] * len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] += 1
    return returnVec

def trainNB0(trainMatrix,trainCategory):
    numTrainDocs = len(trainMatrix)  #矩阵的行数即文档数
    numWords = len(trainMatrix[0])   #词典大小
    pAbusive = sum(trainCategory)/float(numTrainDocs) #概率P(c)
    p0Num = ones(numWords)           #非侮辱性文章词语向量 (拉普拉斯平滑)
    p1Num = ones(numWords)           #侮辱性文章词语向量
    p0Denom = 2.0                    #非侮辱性文章总词数
    p1Denom = 2.0                    #侮辱性文章总词数
    for i in range(numTrainDocs):
        if trainCategory[i] == 1:
            p1Num += trainMatrix[i]
            p1Denom += sum(trainMatrix[i])
        else:
            p0Num += trainMatrix[i]
            p0Denom += sum(trainMatrix[i])
    p1Vect = log(p1Num/p1Denom)     #P(w/c)
    p0Vect = log(p0Num / p0Denom)   #P(w/c)
    return p0Vect,p1Vect,pAbusive

def classifyNB(vec2Classify,p0Vec,p1Vec,pClass1):
    p1 = sum(vec2Classify*p1Vec) + log(pClass1)           #P(wc)
    p0 = sum(vec2Classify*p0Vec) + log(1-pClass1)
    if p1>p0:
        return 1
    else:
        return 0

def testingNB():
    listOPosts,listClasses = loadDataSet()
    myVocabList = createVocabList(listOPosts)   #集合化去重
    trainMat = []
    for postinDoc in listOPosts:
        trainMat.append(setOfWords2Vec(myVocabList,postinDoc))
    p0V,p1V,pAb = trainNB0(array(trainMat),array(listClasses))
    testEntry = ['love','my','dalmation']
    thisDoc = array(setOfWords2Vec(myVocabList,testEntry))
    print testEntry,'classified as: ',classifyNB(thisDoc,p0V,p1V,pAb)
    testEntry = ['stupid', 'garbage']
    thisDoc = array(setOfWords2Vec(myVocabList, testEntry))
    print testEntry, 'classified as: ', classifyNB(thisDoc, p0V, p1V, pAb)

def textParse(bigString):
    import re
    listOfTokens = re.split(r'\w*',bigString)
    return [tok.lower() for tok in listOfTokens if len(tok) > 2]

#垃圾邮件测试
def spamTest():
    docList = []
    classList = []
    fullText = []
    for i in range(1,26):
        wordList = textParse(open('email/spam/%d.txt' % i).read())
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(1)
        wordList = textParse(open('email/ham/%d.txt' % i).read())
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(0)
    vocabList = createVocabList(docList)
    trainingSet = range(50)
    testSet = []
    for i in range(10):                                   #产生10个测试样本
        randIndex = int(random.uniform(0,len(trainingSet)))
        testSet.append(trainingSet[randIndex])
        del(trainingSet[randIndex])
    trainMat = []
    trainClasses = []
    for docIndex in trainingSet:
        trainMat.append(setOfWords2Vec(vocabList,docList[docIndex]))
        trainClasses.append(classList[docIndex])
    p0V,p1V,pSpam = trainNB0(array(trainMat),array(trainClasses))    #训练结果
    errorCount = 0
    for docIndex in testSet:
        wordVector = setOfWords2Vec(vocabList,docList[docIndex])
        if classifyNB(wordVector,p0V,p1V,pSpam) != classList[docIndex]:
            errorCount += 1
    print 'the error rate =',float(errorCount)/len(testSet)


