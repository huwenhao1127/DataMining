#! /usr/local/bin/python3.6
# coding=utf-8

# 作者：huwenhao
# Github主页： https://github.com/huwenhao1127/
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
        print('%-38s%d' % (list(i), round(frequent_itemset[i], 3)))
    return None


# 有每个频繁项集产生强关联规则
def big_rules(frequent_itemset, min_conf=0.8):
    big_rules_list = []
    confidence_list = []
    # 判断每个频繁项能否相互关联，能关联求conf并过滤
    for i in range(len(frequent_itemset)):
        itemset_1 = set(list(frequent_itemset.keys())[i])
        for j in range(1, len(frequent_itemset)):
            itemset_2 = set(list(frequent_itemset.keys())[j])
            if (not itemset_1 & itemset_2) and (frozenset(itemset_1|itemset_2) in frequent_itemset):
                confidence = frequent_itemset[frozenset(itemset_1|itemset_2)]/frequent_itemset[frozenset(itemset_1)]
                if (confidence > min_conf) and ([itemset_1, itemset_2] not in big_rules_list):
                    big_rules_list.append([itemset_1, itemset_2])
                    confidence_list.append(confidence)
    for i in range(len(big_rules_list)):
        print('big rules:%s => %s' % (big_rules_list[i][0], big_rules_list[i][1]), end=' ')
        print('confidence:', confidence_list[i])
    return big_rules_list, confidence_list


# 项（item）：可能包含多个字符串，结构是set，存入项集时转换为frozenset
# frequent_itemset: 频繁项集的集合，频繁项集及对应支持度，结构是字典，key的数据类型为frozenset
# candidate_itemset： 候选项集的集合，候选项集及对应支持度， 结构是字典， key的数据类型为frozenset
def apriori(data_set, min_sup=3):
    frequent_itemset = {}
    candidate_itemset = {}

    # 第一次扫描D，产生候选集
    for i in data_set:
        print(i)
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
    print()
    print_frequent_itemset(frequent_itemset)
    return frequent_itemset


dataset = [['牛奶', '面包', '尿布'], ['面包', '啤酒'], ['面包', '黄油'], ['牛奶', '面包', '啤酒'], ['牛奶', '黄油'], ['面包', '黄油'],
           ['牛奶', '黄油'], ['牛奶', '面包', '黄油', '尿布'], ['牛奶', '面包', '黄油']]

data1 = [['M', 'O', 'N', 'K', 'E', 'Y'],
         ['D', 'O', 'N', 'K', 'E', 'Y'],
         ['M', 'A', 'K', 'E'],
         ['M', 'U', 'C', 'K', 'Y'],
         ['C', 'O', 'O', 'K', 'I', 'E']]
a = apriori(data1)
b, c = big_rules(a)


