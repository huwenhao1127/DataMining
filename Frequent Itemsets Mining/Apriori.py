#! /usr/local/bin/python3.6
# coding=utf-8

# 作者：huwenhao
# Github主页： https://github.com/huwenhao1127/

import numpy as np
import os

np.set_printoptions(threshold=np.inf)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


def loadData():
    data = [['M', 'O', 'N', 'K', 'E', 'Y'],
             ['D', 'O', 'N', 'K', 'E', 'Y'],
             ['M', 'A', 'K', 'E'],
             ['M', 'U', 'C', 'K', 'Y'],
             ['C', 'O', 'O', 'K', 'I', 'E']]
    dataset = [['牛奶', '面包', '尿布'], ['面包', '啤酒'], ['面包', '黄油'], ['牛奶', '面包', '啤酒'], ['牛奶', '黄油'], ['面包', '黄油'],
               ['牛奶', '黄油'], ['牛奶', '面包', '黄油', '尿布'], ['牛奶', '面包', '黄油']]
    return data


def CkCount(Ck, dataSet):
    for kItems in Ck.keys():
        for thing in dataSet:
            if set(thing) | set(kItems) == set(thing):
                Ck[kItems] += 1


def selfJoining(Lk):
    Ck = {}
    for i in range(len(Lk)):
        Lk[i] = sorted(Lk[i])
    for i in range(len(Lk)):
        for j in range(i+1, len(Lk)):
            if Lk[i][:-1] == Lk[j][:-1]:
                set1 = set(Lk[i])
                set2 = set(Lk[j])
                Fk_1 = frozenset(set1 | set2)
                Ck[Fk_1] = 0
    return Ck


def pruning(Ck, Lk):
    for kItems in Ck.keys():
        for i in range(len(kItems)):
            temp = list(kItems)
            temp.pop(i)
            if temp not in Lk:
                del Ck[kItems]


def calBigRules(frequentItems, confMin, dataNum):
    bigRules = []
    confidences = []
    keys = list(frequentItems.keys())
    for i in range(len(frequentItems)):
        for j in range(len(frequentItems)):
            if i is not j:
                temp = frozenset(set(keys[i]) | set(keys[j]))
                if (temp in frequentItems) and (not (set(keys[i]) & set(keys[j]))):
                    conf = frequentItems[temp]/frequentItems[keys[i]]
                    sup = frequentItems[temp]/dataNum
                    if conf >= confMin:
                        bigRules.append([keys[i], keys[j]])
                        confidences.append([sup, conf])
    return bigRules, confidences


def apriori(dataSet, supMin, confMin):
    frequentItem = {}
    C1 = {}
    dataNum = len(dataSet)
    supCountMin = supMin * len(dataSet)
    for thing in dataSet:
        temp = set(thing)
        for item in temp:
            if item not in C1:
                C1[item] = 1
            else:
                C1[item] += 1
    L1 = []
    for item in C1.keys():
        if C1[item] >= supCountMin:
            L1.append([item])
            frequentItem[frozenset({item})] = C1[item]
    Lk_1 = L1
    while True:
        Ck = selfJoining(Lk_1)
        if len(Ck) == 0:
            break
        CkCount(Ck, dataSet)
        Lk_1.clear()
        for items in Ck.keys():
            if Ck[items] >= supCountMin:
                Lk_1.append(list(items))
                frequentItem.update({items: Ck[items]})
    bigRule, confidence = calBigRules(frequentItem, confMin, dataNum)
    return frequentItem, bigRule, confidence


def allPrint(frequentItem, bigRule, confidence):
    print('-----------------frequent itemset-----------------')
    for itemset in frequentItem:
        print(list(itemset), ':', frequentItem[itemset])
    print('--------------------big rules---------------------')
    for i in range(len(confidence)):
        print(list(bigRule[i][0]), '=>', list(bigRule[i][1]), '[support=', confidence[i][0], ',',
              'confidence=', confidence[i][1], ']')


if __name__ == '__main__':
    myData = loadData()
    f, br, con = apriori(myData, 0.6, 0.8)
    allPrint(f, br, con)
