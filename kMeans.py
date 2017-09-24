# -*- coding: UTF-8 -*-
from numpy import *

def loadDataSet(fileName):
    dataMat = []
    fr = open(fileName)
    for line in fr.readlines():
        curLine = line.strip().split('\t')
        fltLine = map(float,curLine)
        dataMat.append(fltLine)
    return dataMat

def distEclud(vecA,vecB):   #计算欧式距离
    return sqrt(sum(power(vecA-vecB,2)))

def randCent(dataSet,k):
    n = shape(dataSet)[1]
    centroids = mat(zeros((k,n)))
    for j in range(n):
        minJ = min(dataSet[:,j])
        rangeJ = float(max(dataSet[:,j]) - minJ)
        centroids[:,j] = minJ + rangeJ * random.rand(k,1)
    return centroids

def kMeans(dataSet,k,distMeas=distEclud,createCent=randCent):
    m = shape(dataSet)[0]
    clusterAssemt = mat(zeros((m,2)))
    centroids = createCent(dataSet,k)
    clusterChanged = True
    while clusterChanged:
        clusterChanged = False
        for i in range(m):
            minDist = inf
            minIndex = -1
            for j in range(k):
                distJI = distMeas(centroids[j,:],dataSet[i,:])
                if distJI < minDist:
                    minDist = distJI
                    minIndex = j
            if clusterAssemt[i,0] != minIndex:
                clusterChanged = True
            clusterAssemt[i,:] = minIndex,minDist ** 2
        print centroids
        for cent in range(k):
            ptsInClust = dataSet[nonzero(clusterAssemt[:,0].A==cent)[0]]
            centroids[cent,:] = mean(ptsInClust,axis=0)  #axis = 0：压缩行，对各列求均值，返回 1* n 矩阵 axis =1 ：压缩列，对各行求均值，返回 m *1 矩阵
    return centroids,clusterAssemt
