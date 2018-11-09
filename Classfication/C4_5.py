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


# C4.5
def getBestAttribute(dataSet, labels):
    metricValueList = []
    entData = calEnt(dataSet)
    for attribute in range(len(dataSet[0])-1):
        attributeValueSet = set([data[attribute] for data in dataSet])
        entSubData = 0
        # 每一个属性对应有一个"固有值"，属性取值数越多，"固有值"越大。
        intrinsicValue = 0
        for attributeValue in attributeValueSet:
            subDataSet = splitDataSet(dataSet, attribute, attributeValue)
            weight = float(len(subDataSet)/len(dataSet))
            entSubData += weight * calEnt(subDataSet)
            intrinsicValue -= weight * np.log2(weight)
        # 与ID3的主要区别在于引入了gainRation作为度量
        gain = entData - entSubData
        # 防止某一属性的"固有值"为0产生溢出
        if intrinsicValue == 0:
            gainRation = 0
        else:
            gainRation = float(gain/intrinsicValue)
        metricValueList.append([attribute, gain, gainRation, attributeValueSet])
    # 从信息增益高于平均水平的属性中选增益率高的
    gainList = np.array([example[1] for example in metricValueList])
    averageGain = gainList.mean()
    tempList = []
    for i in range(len(metricValueList)):
        if metricValueList[i][1] > averageGain:
            tempList.append(metricValueList[i])
    sorted(tempList, key=lambda x: x[2], reverse=True)
    bestAttribute = tempList[0][0]
    bestAttributeValueSet = tempList[0][3]
    return bestAttribute, bestAttributeValueSet


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


def treeGenerate(dataSet, Labels):
    attributes = Labels[:]
    classList = set([data[-1] for data in dataSet])
    # 全部是一类
    if len(classList) == 1:
        return list(classList)[0]
    # 遍历完所有属性,并且还有多类,返回出现次数最多的类
    if len(attributes) == 0:
        return getMajorityClass(dataSet)

    index, attributeValueset = getBestAttribute(dataSet, attributes)
    bestAttribute = attributes[index]
    del(attributes[index])
    # 创建结点
    tree = {bestAttribute: {}}
    # 递归生成分枝
    for value in attributeValueset:
        subAttributes = attributes[:]
        tree[bestAttribute][value] = treeGenerate(splitDataSet(dataSet, index, value),
                                                  subAttributes)
    return tree


def classify(inputTree, testDataSet, labels):
    classLabel = None
    firstStr = list(inputTree.keys())[0]
    secondDict = inputTree[firstStr]
    attributeIndex = labels.index(firstStr)
    for key in secondDict.keys():
        if testDataSet[attributeIndex] == key:
            if type(secondDict[key]).__name__ == 'dict':
                classLabel = classify(secondDict[key], testDataSet, labels)
            else:
                classLabel = secondDict[key]
    return classLabel


myData, myLable = loadDataSet1()
a = treeGenerate(myData, myLable)
testData = ['青绿', '蜷缩', '沉闷', '稍糊', '稍凹', '硬滑']
b = classify(a, testData, myLable)
print(b)
treePlotter.createPlot(a)
