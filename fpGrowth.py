# -*- coding: UTF-8 -*-
from numpy import *

class treeNode:
    def __init__(self,nameValue,numOccur,parentNode):
        self.name = nameValue
        self.count = numOccur
        self.nodeLink = None
        self.parent = parentNode
        self.children = {}
    def inc(self,numOccur):
        self.count += numOccur
    def disp(self,ind=1):
        print ' '*ind,self.name, ' ',self.count
        for child in self.children.values():
            child.disp(ind+1)

def createTree(dataSet,minSup=1):
    headerTable = {} #头指针表
    #第一次遍历开始 扫描数据集并统计每个元素项出现的频度
    for trans in dataSet:
        for item in trans: #单独的字母
            headerTable[item] = headerTable.get(item,0) + dataSet[trans]
    for k in headerTable.keys():
        if headerTable[k] < minSup: #删除项集大小为1的非频繁项集,根据apriori原则,包含该非频繁项集的项集都不可能是频繁项集
            del(headerTable[k])
    freqItemSet = set(headerTable.keys())
    if len(freqItemSet) == 0: return None,None #如果没有元素项满足要求则退出
    for k in headerTable:
        headerTable[k] = [headerTable[k],None] #扩展以便可以保存计数值及指向每种类型第一个元素项的指针
    retTree = treeNode('Null Set',1,None) #建立根节点
    #第二次循环开始
    for tranSet,count in dataSet.items():
        localD = {}
        for item in tranSet:
            if item in freqItemSet:
                localD[item] = headerTable[item][0]
        if len(localD) > 0:
            orderedItems = [v[0] for v in sorted(localD.items(),key=lambda p:p[1],reverse=True)] #根据全局频率对每个事务中的元素排序
            updateTree(orderedItems,retTree,headerTable,count)
    return retTree,headerTable

#items一行记录,inTree FP树的树根,headerTable出现的频繁项集,count这行记录出现的次数
def updateTree(items,inTree,headerTable,count):
    if items[0] in inTree.children:  #如果出现了这个节点,就把这个节点的计数增加
        inTree.children[items[0]].inc(count)
    else:  #否则就创建新的节点
        inTree.children[items[0]] = treeNode(items[0],count,inTree)
        if headerTable[items[0]][1] == None:
            headerTable[items[0]][1] = inTree.children[items[0]]
        else:
            updateHeader(headerTable[items[0]][1],inTree.children[items[0]])
    if len(items) > 1:  #如果要插入字典树的词条还有,那就继续插入剩下的
        updateTree(items[1::],inTree.children[items[0]],headerTable,count) #注意根节点的变化

def updateHeader(nodeToTest,targetNode):
    while (nodeToTest.nodeLink != None):
        nodeToTest = nodeToTest.nodeLink
    nodeToTest.nodeLink = targetNode

def loadSimpDat():
    simpDat = [['r','z','h','j','p'],
               ['z','y','x','w','v','u','t','s'],
               ['z'],
               ['r','x','n','o','s'],
               ['y','r','x','z','q','t','p'],
               ['y','z','x','e','q','s','t','m']]
    return simpDat
def createInitSet(dataSet):
    retDict = {}
    for trans in dataSet:
        retDict[frozenset(trans)] = 1
    return retDict
#至此FP树已经建造完成

#发现以给定元素项结尾的所有路径的函数
def ascendTree(leafNode,prefixPath):
    if leafNode.parent != None:
        prefixPath.append(leafNode.name)
        ascendTree(leafNode.parent,prefixPath)

def findPrefixPath (basePat,treeNode):
    condPats = {}
    while treeNode != None:
        prefixPath = []
        ascendTree(treeNode,prefixPath)
        if len(prefixPath) > 1:
            condPats[frozenset(prefixPath[1:])] = treeNode.count
        treeNode = treeNode.nodeLink
    return condPats

#inTree和headerTable是由createTree()函数生成的数据集的FP树
#minSup表示最小支持度
#preFix请传入一个空集合（set([])），将在函数中用于保存当前前缀
#freqItemList请传入一个空列表（[]），将用来储存生成的频繁项集
def mineTree(inTree,headerTable,minSup,preFix,freqItemList):
    bigL = [v[0] for v in sorted(headerTable.items(),key=lambda p:p[1])]
    for basePat in bigL:
        print 'now the basePat is: ',basePat
        newFreqSet = preFix.copy()
        newFreqSet.add(basePat)
        freqItemList.append(newFreqSet)
        condPattBases = findPrefixPath(basePat,headerTable[basePat][1])
        print 'condPattBases: ',condPattBases
        myCondTree,myHead = createTree(condPattBases,minSup)
        if myHead != None:
            print 'conditional tree for: ',newFreqSet
            myCondTree.disp(1)
            mineTree(myCondTree,myHead,minSup,newFreqSet,freqItemList)
