# -*- coding: UTF-8 -*-
from numpy import *
import urllib
import json
import matplotlib

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

def biKmeans(dataSet,k,distMeas=distEclud):
    m = shape(dataSet)[0]
    clusterAssment = mat(zeros((m,2)))
    centroid0 = mean(dataSet,axis=0).tolist()[0] #得到两个元素的列表
    centList = [centroid0]
    for j in range(m):
        clusterAssment[j,1] = distMeas(mat(centroid0),dataSet[j,:])**2
    while(len(centList) < k): #当簇数目小于K时
        lowestSSE = inf
        for i in range(len(centList)): #对于每一个簇
            ptsInCurrCluster = dataSet[nonzero(clusterAssment[:,0].A==i)[0],:]
            centroidMat,splitClustAss = kMeans(ptsInCurrCluster,2,distMeas)
            sseSplit = sum(splitClustAss[:,1])
            sseNotSplit = sum(clusterAssment[nonzero(clusterAssment[:,0].A!=i)[0],1])
            print "sseSplit,and notSplit: ",sseSplit,sseNotSplit
            if(sseSplit + sseNotSplit) < lowestSSE:
                bestCentToSplit = i
                bestNewCents = centroidMat
                bestClustAss = splitClustAss.copy() #索引加误差
                lowestSSE = sseSplit + sseNotSplit
        bestClustAss[nonzero(bestClustAss[:,0].A == 1)[0],0] = len(centList) #更新簇的分配结果 索引
        bestClustAss[nonzero(bestClustAss[:,0].A == 0)[0],0] = bestCentToSplit
        print 'the bestCentToSplit is: ',bestCentToSplit
        print 'the len of bestClustAss is: ',len(bestClustAss)
        #centList[bestCentToSplit] = bestNewCents[0,:] #修改分配结果
        #centList.append(bestNewCents[1,:]) #添加新的质心
        centList[bestCentToSplit] = bestNewCents[0, :].tolist()[0]  # replace a centroid with two best centroids
        centList.append(bestNewCents[1, :].tolist()[0])
        clusterAssment[nonzero(clusterAssment[:,0].A == bestCentToSplit)[0],:] = bestClustAss
    return mat(centList),clusterAssment

def geoGrab(stAddress,city):
    apiStem = 'http://where.yahooapis.com/geocode?'
    params = {}
    params['flag'] = 'J'
    params['appid'] = 'dj0yJmk9MkpORFhQcHpmQk1TJmQ9WVdrOVdsVjFObGhhTldjbWNHbzlNQS0tJnM9Y29uc3VtZXJzZWNyZXQmeD1lNA--'
    params['location'] = '%s %s' % (stAddress,city)
    url_params = urllib.urlencode(params)
    yahooApi = apiStem + url_params
    print yahooApi
    c = urllib.urlopen(yahooApi)
    return json.loads(c.read())

from time import sleep
def massPlaceFind(fileName):
    fw = open('places.txt', 'w')
    for line in open(fileName).readlines():
        line = line.strip()
        lineArr = line.split('\t')
        retDict = geoGrab(lineArr[1], lineArr[2])
        if retDict['ResultSet']['Error'] == 0:
            lat = float(retDict['ResultSet']['Results'][0]['latitude'])
            lng = float(retDict['ResultSet']['Results'][0]['longitude'])
            print "%s\t%f\t%f" % (lineArr[0], lat, lng)
            fw.write('%s\t%f\t%f\n' % (line, lat, lng))
        else: print "error fetching"
        sleep(1)
    fw.close()

#球面距离公式
def distSLC(vecA,vecB):
    a = sin(vecA[0,1]*pi/180) * sin(vecB[0,1]*pi/180)
    b = cos(vecA[0,1]*pi/180) * cos(vecB[0,1]*pi/180) * cos(pi * (vecB[0,0]-vecA[0,0])/180)
    return arccos(a+b)*6371.0

import matplotlib.pyplot as plt
def clusterClubs1(numClust=5):
    datList = []
    for line in open('places.txt').readlines():
        lineArr = line.split('\t')
        datList.append([float(lineArr[4]),float(lineArr[3])])
        datMat = mat(datList)
        myCentroids,clustAssing = biKmeans(datMat,numClust,distMeas=distSLC)
        fig = plt.figure()
        rect = [0.1,0.1,0.8,0.8]
        scatterMarkers = ['s','o','^','8','p','d','v','h','>','<']  #标记类型列表
        axprops = dict(xticks=[],yticks=[])
        ax0 = fig.add_axes(rect,label='ax0',**axprops)
        imgP = plt.imread('Protland.png')
        ax0.imshow(imgP)
        ax1 = fig.add_axes(rect,label='ax1',frameon=False)
        for i in range(numClust):
            ptsInCurrCluster = datMat[nonzero(clustAssing[:,0].A==i)[0],:]
            markerStyle = scatterMarkers[i % len(scatterMarkers)] #循环使用列表中的标记
            ax1.scatter(ptsInCurrCluster[:,0].flatten().A[0],myCentroids[:,1].flatten().A[0],marker='+',s=300)
            plt.show()

import matplotlib.pyplot as plt
def clusterClubs(numClust=5):
    datList = []
    for line in open('places.txt').readlines():
        lineArr = line.split('\t')
        datList.append([float(lineArr[4]), float(lineArr[3])])
    datMat = mat(datList)
    myCentroids, clustAssing = biKmeans(datMat, numClust, distMeas=distSLC)
    fig = plt.figure()
    rect=[0.1,0.1,0.8,0.8]
    scatterMarkers=['s', 'o', '^', '8', 'p', \
                    'd', 'v', 'h', '>', '<']
    axprops = dict(xticks=[], yticks=[])
    ax0=fig.add_axes(rect, label='ax0', **axprops)
    imgP = plt.imread('Portland.png')
    ax0.imshow(imgP)
    ax1=fig.add_axes(rect, label='ax1', frameon=False)
    for i in range(numClust):
        ptsInCurrCluster = datMat[nonzero(clustAssing[:,0].A==i)[0],:]
        markerStyle = scatterMarkers[i % len(scatterMarkers)]
        ax1.scatter(ptsInCurrCluster[:,0].flatten().A[0], ptsInCurrCluster[:,1].flatten().A[0], marker=markerStyle, s=90)
    ax1.scatter(myCentroids[:,0].flatten().A[0], myCentroids[:,1].flatten().A[0], marker='+', s=300)
    plt.show()
