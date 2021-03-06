
# -*- coding: UTF-8 -*-

from numpy import *
import operator

def createDataSet() :
    group = array ([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
    labels = ['A','A','B','B']
    return group, labels

def classify0(inX, dataSet, labels, k):
    dataSetSize = dataSet.shape[0]
    #计算距离#
    diffMat = tile(inX, (dataSetSize,1)) - dataSet  #tile使inX沿各维度重复
    sqDiffMat = diffMat**2
    sqDistances = sqDiffMat.sum(axis=1)  #axis=1即矩阵每行相加
    distances = sqDistances**0.5
    sortedDisIndicies = distances.argsort(); #排序序号
    classCount = {}
    for i in range(k):
        voteIlabel = labels[sortedDisIndicies[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel,0) + 1
    sortedClassCount = sorted(classCount.iteritems(),
                              key=operator.itemgetter(1),reverse=True)
    return sortedClassCount[0][0]

def file2matrix(filename):
    fr = open(filename)
    arrayOLines = fr.readlines()
    numberOfLines = len(arrayOLines)
    returnMat = zeros((numberOfLines,3)) #生成NumPy矩阵
    classLabelVector = []
    index = 0
    for line in arrayOLines:
        line = line.strip() #默认删除空白符
        listFromLine = line.split('\t')
        returnMat[index,:] = listFromLine[0:3]
        classLabelVector.append(int(listFromLine[-1])) #-1索引最后一列
        index += 1
    return returnMat,classLabelVector

def autoNorm(dataSet):
    minVals = dataSet.min(0) #min(0)在列中返回最小值，max同理
    maxVals = dataSet.max(0)
    ranges = maxVals - minVals
    normDataSet = zeros(shape(dataSet))
    m = dataSet.shape[0]     #shape[0]返回行数，shape[1]返回列数
    normDataSet = dataSet - tile(minVals,(m,1))
    normDataSet = normDataSet/tile(ranges,(m,1))
    return normDataSet,ranges,minVals

def datingClassTest():
    hoRatio = 0.10 #测试样本数比例
    datingDataMat,datingLabels = file2matrix('datingTestSet2.txt')
    normMat,ranges,minVals = autoNorm(datingDataMat)
    m = normMat.shape[0]
    numTestVecs = int(m*hoRatio)
    errorCount = 0.0
    for i in range(numTestVecs) :
        classifierResult = classify0(normMat[i, :], normMat[numTestVecs:m, :], datingLabels[numTestVecs:m], 3)
        print "the classifier came back with: %d, the real answer is: %d" % (classifierResult, datingLabels[i])
        if (classifierResult != datingLabels[i]): errorCount += 1.0
    print "the total error rate is: %f" % (errorCount / float(numTestVecs))
    print errorCount

def classifyPerson():
    resultList = ['not at all','in small does','in large doses']
    percentTats = float(raw_input("percentage of time spent playing games?"))
    ffMiles = float(raw_input("flier miles ?"))
    iceCream = float(raw_input("liters of icecream?"))
    datingDataMat,datingLabels = file2matrix('datingTestSet2.txt')
    normMat,ranges,minVals = autoNorm(datingDataMat)
    inArr = array([ffMiles,percentTats,iceCream])
    classifierResult = classify0((inArr - minVals)/ranges,normMat,datingLabels,3)
    print "like this guy",resultList[classifierResult-1]