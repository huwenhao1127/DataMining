#! /usr/local/bin/python3.6
# coding=utf-8

# 作者：huwenhao
# Github主页： https://github.com/huwenhao1127/
import numpy as np
np.set_printoptions(threshold=np.inf)
import treePlotter


def loadDataSet1():
    attributeSet = ['色泽', '根蒂', '敲击', '纹理', '脐部', '触感']
    dataSet = [
        # 1
        ['青绿', '蜷缩', '浊响', '清晰', '凹陷', '硬滑', '好瓜'],
        # 2
        ['乌黑', '蜷缩', '沉闷', '清晰', '凹陷', '硬滑', '好瓜'],
        # 3
        ['乌黑', '蜷缩', '浊响', '清晰', '凹陷', '硬滑', '好瓜'],
        # 4
        ['青绿', '蜷缩', '沉闷', '清晰', '凹陷', '硬滑', '好瓜'],
        # 5
        ['浅白', '蜷缩', '浊响', '清晰', '凹陷', '硬滑', '好瓜'],
        # 6
        ['青绿', '稍蜷', '浊响', '清晰', '稍凹', '软粘', '好瓜'],
        # 7
        ['乌黑', '稍蜷', '浊响', '稍糊', '稍凹', '软粘', '好瓜'],
        # 8
        ['乌黑', '稍蜷', '浊响', '清晰', '稍凹', '硬滑', '好瓜'],

        # ----------------------------------------------------
        # 9
        ['乌黑', '稍蜷', '沉闷', '稍糊', '稍凹', '硬滑', '坏瓜'],
        # 10
        ['青绿', '硬挺', '清脆', '清晰', '平坦', '软粘', '坏瓜'],
        # 11
        ['浅白', '硬挺', '清脆', '模糊', '平坦', '硬滑', '坏瓜'],
        # 12
        ['浅白', '蜷缩', '浊响', '模糊', '平坦', '软粘', '坏瓜'],
        # 13
        ['青绿', '稍蜷', '浊响', '稍糊', '凹陷', '硬滑', '坏瓜'],
        # 14
        ['浅白', '稍蜷', '沉闷', '稍糊', '凹陷', '硬滑', '坏瓜'],
        # 15
        ['乌黑', '稍蜷', '浊响', '清晰', '稍凹', '软粘', '坏瓜'],
        # 16
        ['浅白', '蜷缩', '浊响', '模糊', '平坦', '硬滑', '坏瓜'],
        # 17
        ['青绿', '蜷缩', '沉闷', '稍糊', '稍凹', '硬滑', '坏瓜']
    ]
    return dataSet, attributeSet


def loadDataSet2():
    attributeSet = ['no surfacing', 'flippers']
    dataSet = [[1, 1, 'yes'],
               [1, 1, 'yes'],
               [1, 0, 'no'],
               [0, 1, 'no'],
               [0, 1, 'no']]
    return dataSet, attributeSet


def calEnt(dataSet):
    countClass = {}
    for data in dataSet:
        if data[-1] not in countClass:
            countClass[data[-1]] = 1
        else:
            countClass[data[-1]] += 1
    Entropy = 0
    for classfication in countClass.keys():
        prob = float(countClass[classfication]/len(dataSet))
        Entropy -= prob * np.log2(prob)
    return Entropy


def splitDataSet(dataSet, attribute, value):
    subDataSet = []
    for data in dataSet:
        if data[attribute] == value:
            subData = data[:attribute]
            subData.extend(data[attribute+1:])
            subDataSet.append(subData)
    return subDataSet


# ID3
def getBestAttribute(dataSet):
    bestAttribute = None
    valueSet = set()
    maxGain = -1
    entData = calEnt(dataSet)
    for attribute in range(len(dataSet[0])-1):
        attributeValueSet = set([data[attribute] for data in dataSet])
        entSubData = 0
        for attributeValue in attributeValueSet:
            subDataSet = splitDataSet(dataSet, attribute, attributeValue)
            weight = float(len(subDataSet)/len(dataSet))
            entSubData += weight * calEnt(subDataSet)
        gain = entData - entSubData
        if gain > maxGain:
            maxGain = gain
            bestAttribute = attribute
            valueSet = attributeValueSet
    return bestAttribute, valueSet


def getMajorityClass(dataSet):
    classCount = {}
    for data in dataSet:
        if data[-1] not in classCount:
            classCount[data[-1]] = 1
        else:
            classCount[data[-1]] += 1
    classCount = classCount.items()
    classCount = sorted(classCount, key=lambda x:x[1], reverse=True)
    majorityClass = classCount[0][0]
    return majorityClass


def treeGenerate(dataSet, attributes):
    classList = set([data[-1] for data in dataSet])
    # 全部是一类
    if len(classList) == 1:
        return list(classList)[0]
    # 遍历完所有属性,并且还有多类,返回出现次数最多的类
    if len(attributes) == 0:
        return getMajorityClass(dataSet)
    index, attributeValueset = getBestAttribute(dataSet)
    bestAttribute = attributes[index]
    del (attributes[index])
    # 创建结点
    tree = {bestAttribute: {}}
    # 递归生成分枝
    for value in attributeValueset:
        subAttributes = attributes[:]
        tree[bestAttribute][value] = treeGenerate(splitDataSet(dataSet, index, value),
                                                  subAttributes)
    return tree


myData, myLable = loadDataSet1()
a = treeGenerate(myData, myLable)
treePlotter.createPlot(a)
