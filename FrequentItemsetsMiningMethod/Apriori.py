#! /usr/local/bin/python3.6
# coding=utf-8

import numpy as np
import os

np.set_printoptions(threshold=np.inf)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


# 找出Cki的所有长度为k-1的子集，判断是否在Lk中,不在Lk中则需要pruning，返回True
def is_pruning(Cki, Lk):
    C = frozenset(Cki)
    L = list(Lk)
    for i in range(len(C)):
        temp = list(C)
        temp.pop(i)
        temp = frozenset(temp)
        if temp not in L:
            return True
    return False


# 迭代求解C
def iteration(Ck, frequent_itemset, min_sup, data_set):
    # 删除
    for i in frozenset(Ck.keys()):
        if Ck[i] < min_sup:
            Ck.pop(i)

    # 生成频繁项集Lk
    Lk = list(Ck.keys())
    frequent_itemset.update(Ck)

    # 生成候选项集C
    # self-joining ,python list真的强大。。可以将字符串sort,sort完再转回set使用逻辑运算
    Ck.clear()

    len_Lk = len(Lk)
    for i in range(len_Lk):
        for j in range(1,len_Lk):
            L1 = list(Lk[i])
            L2 = list(Lk[j])
            L1.sort()
            L2.sort()
            if (L1[:-2] == L2[:-2]) & (L1 != L2):
                Cki = set(L1) | set(L2)
                # pruning
                if not is_pruning(Cki, Lk):
                    CKi = frozenset(Cki)
                    Ck[CKi] = 0

    # 扫描D，对C的每一项计数
    for i in Ck:
        item = list(i)
        for j in data_set:
            if set(item) & set(j) == set(item):
                Ck[i] += 1
    return Ck


def print_frequent_itemset(frequent_itemset):
    print('frequent_itemset', ' '*20, 'support')
    print('-'*60)
    for i in frequent_itemset:
        print('%-38s%.3f' % (list(i), round(frequent_itemset[i], 3)))
    return None


# 项（item）：可能包含多个字符串，结构是set，存入项集时转换为frozenset
# frequent_itemset: 总的频繁项集，频繁项的集合及对应支持度，结构是字典，key的结构为set->frozenset
# candidate_itemset： 候选项集，候选项的集合及对应支持度， 结构是字典， key的结构为set->frozenset
def apriori(data_set, min_sup=2):
    frequent_itemset = {}
    candidate_itemset = {}

    # 第一次扫描D，产生候选集
    for i in data_set:
        for j in i:
            j = frozenset({j})
            if j not in candidate_itemset:
                candidate_itemset[j] = 1
            else:
                candidate_itemset[j] += 1
    # 开始迭代：删除->生成L->自链接->枝剪->产生C->计数
    k = 0
    while candidate_itemset:
        candidate_itemset = iteration(candidate_itemset,frequent_itemset, min_sup, data_set)
        k += 1
        print('\r', '迭代次数：%d' % k, end=' ')
    for i in frequent_itemset:
        frequent_itemset[i] = frequent_itemset[i]/len(data_set)
    print()
    print_frequent_itemset(frequent_itemset)
    return frequent_itemset


dataset = [['牛奶', '面包', '尿布'], ['面包', '啤酒'], ['面包', '黄油'], ['牛奶', '面包', '啤酒'], ['牛奶', '黄油'], ['面包', '黄油'],
           ['牛奶', '黄油'], ['牛奶', '面包', '黄油', '尿布'], ['牛奶', '面包', '黄油']]
apriori(dataset)


