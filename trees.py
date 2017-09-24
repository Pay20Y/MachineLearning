# -*- coding: UTF-8 -*-
from math import log
import operator

#calculate Shonnon#
def calcShannonEnt(dataSet):
    numEntries = len(dataSet)
    labelCounts = {}
    for featVec in dataSet:
        currentLabel = featVec[-1]
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1
    shannonEnt = 0.0
    for key in labelCounts:
        prob = float(labelCounts[key])/numEntries
        shannonEnt -= prob * log(prob,2)
    return shannonEnt

def createDataSet():
    dataSet = [[1,1,'yes'],
               [1,1,'yes'],
               [1,0,'no'],
               [0,1,'no'],
               [0,1,'no']]
    labels = ['no surfacing','flippers']
    return dataSet,labels

def splitDataSet(dataSet,axis,value):   #待划分的数据集，划分数据集的特征，需要返回的特征的值
    retDataSet = []
    for featVec in dataSet:
        if featVec[axis] == value:
            reducedFeatVec = featVec[:axis]
            reducedFeatVec.extend(featVec[axis+1:])
            retDataSet.append(reducedFeatVec)
    return retDataSet

def chooseBestFeatureToSplit(dataSet):
    numFeatrues = len(dataSet[0]) - 1
    baseEntropy = calcShannonEnt(dataSet)  #原始香农熵
    bestInfoGain = 0.0
    bestFeature = -1
    for i in range(numFeatrues):
        featList = [example[i] for example in dataSet]
        uniqueVals = set(featList)
        newEntropy = 0.0
        for value in uniqueVals:
            subDataSet = splitDataSet(dataSet,i,value)
            prob = len(subDataSet)/float(len(dataSet))
            newEntropy += prob*calcShannonEnt(subDataSet) #加权计算该种划分方式的信息熵
        infoGain = baseEntropy - newEntropy
        if(infoGain > bestInfoGain):
            bestInfoGain = infoGain
            bestFeatrue = i
    return bestFeatrue

def majorityCnt(classList):
    classCount = {}
    for vote in classList:
        if vote not in classCount.keyss(): classCount[vote] = 0
        classCount[vote] += 1
    sportedClassCount = sorted(classCount.iteritems(),key=operator.itemgetter(1),reverse=True)
    return sportedClassCount[0][0]

def createTree(dataSet,labels):
    classList = [example[-1] for example in dataSet]
    if classList.count(classList[0]) == len(classList): #类别相同时停止划分
        return classList[0]
    if len(dataSet[0]) == 1:                            #遍历完所有特征时返回出现次数最多的类别
        return majorityCnt(classList)
    bestFeat = chooseBestFeatureToSplit(dataSet)
    bestFeatLabel = labels[bestFeat]                     #所以转换成文字版
    myTree = {bestFeatLabel:{}}
    del(labels[bestFeat])                                #删除引用
    featValues = [example[bestFeat] for example in dataSet]
    uniqueVals = set(featValues)
    for value in uniqueVals:
        subLabels = labels[:]
        myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet,bestFeat,value),subLabels)
    return myTree

def classify(inputTree,featLabels,testVec):
    firstStr = inputTree.keys()[0] #根节点
    secondDict = inputTree[firstStr]
    featIndex = featLabels.index(firstStr)  #将标签字符串转换成索引
    for key in secondDict.keys():
        if testVec[featIndex] == key:
            if type(secondDict[key]).__name__ == 'dict':
                classLabel = classify(secondDict[key],featLabels,testVec)
            else: classLabel = secondDict[key]
    return classLabel

def retrieveTree(i):
    listOfTrees =[{'no surfacing':{0:'no',1:{'flippers':{0:'no',1:'yes'}}}},{'no surfacing':{0:'no',1:{'flippers':{0:{'head':{0:'no',1:'yes'}},1:'no'}}}}]
    return listOfTrees[i]

#存储树结构#
def storeTree(inputTree,filename):
    import pickle
    fw = open(filename,'w')
    pickle.dump(inputTree,fw)
    fw.close()

def grabTree(filename):
    import pickle
    fr = open(filename)
    return pickle.load(fr)

