# -*- coding: UTF-8 -*-
from numpy import *

def loadDataSet(fileName,delim='\t'):
    fr = open(fileName)
    stringArr = [line.strip().split(delim) for line in fr.readlines()]
    print 'stringArr: ',stringArr
    datArr = [map(float,line) for line in stringArr]
    print 'datArr: ',datArr
    return mat(datArr)

def pca(dataMat,topNfeat=9999999):
    print 'dataMat size: ',shape(dataMat)
    meanVals = mean(dataMat,axis=0) #对各列求均值
    meanRemoved = dataMat - meanVals
    print 'meanRemoved size: ', shape(meanRemoved)
    covMat = cov(meanRemoved,rowvar = 0)
    eigVals,eigVects = linalg.eig(mat(covMat)) #求得协方差矩阵特征值和特征向量
    print 'eigVals: ',eigVals
    print 'eigVects: ', eigVects
    eigValInd = argsort(eigVals)
    print 'before sort eigValInd: ',eigValInd
    eigValInd = eigValInd[:-(topNfeat+1):-1]
    print 'after sort eigValInd: ', eigValInd
    redEigVects = eigVects[:,eigValInd] #保留最上面的N个特征向量
    lowDDatamat = meanRemoved * redEigVects
    print 'redEigVects size: ', shape(redEigVects)
    print 'lowDDatamat size: ', shape(lowDDatamat)
    reconMat = (lowDDatamat * redEigVects.T) + meanVals
    print 'reconMat size: ', shape(reconMat)
    return lowDDatamat,reconMat

import matplotlib
import matplotlib.pyplot as plt
def draw(dataMat,reconMat):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(dataMat[:,0].flatten().A[0],dataMat[:,1].flatten().A[0],marker='^',s=90)
    ax.scatter(reconMat[:,0].flatten().A[0],reconMat[:,1].flatten().A[0],marker='o',s=50,c='red')
    plt.show()

#计算出非NaN值得平均值,将所有NaN替换为该平均值
def replaceNanWithMean():
    datMat = loadDataSet('secom.data',' ')
    numFeat = shape(datMat)[1]
    for i in range(numFeat):
        meanVal = mean(datMat[nonzero(~isnan(datMat[:,i].A))[0],i])
        datMat[nonzero(isnan(datMat[:,i].A))[0],i] = meanVal
    return datMat

