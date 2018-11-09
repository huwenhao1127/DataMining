#! /usr/local/bin/python3.6
# coding=utf-8

import numpy as np
import os

np.set_printoptions(threshold=np.inf)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


# FP树的结点类
class treeNode:
    def __init__(self, nameValue, numOccur, parentNode):
        self.name = nameValue
        self.count = numOccur
        self.parent = parentNode
        self.nodeLink = None
        self.children = {}

    def inc(self, numOccur):
        self.count += numOccur

    def display(self, ind=1):
        print(' '*ind, self.name, ':', self.count)
        for child in self.children.values():
            child.display(ind+1)


def load_data():
    dataset = [['牛奶', '面包', '尿布'], ['面包', '啤酒'], ['面包', '黄油'], ['牛奶', '面包', '啤酒'], ['牛奶', '黄油'], ['面包', '黄油'],
               ['牛奶', '黄油'], ['牛奶', '面包', '黄油', '尿布'], ['牛奶', '面包', '黄油']]
    data = [['r', 'z', 'h', 'j', 'p'],
            ['z', 'y', 'x', 'w', 'v', 'u', 't', 's'],
            ['z'],
            ['r', 'x', 'n', 'o', 's'],
            ['y', 'r', 'x', 'z', 'q', 't', 'p'],
            ['y', 'z', 'x', 'e', 'q', 's', 't', 'm']]
    retDict = {}
    for trans in data:
        if frozenset(trans) not in retDict:
            retDict[frozenset(trans)] = 1
        else:
            retDict[frozenset(trans)] += 1
    return retDict


# 将一个事务更新到树上
def update_tree(trans, retTree, count, headerTable):
    # 添加一个结点到树上
    if trans[0] in retTree.children:
        retTree.children[trans[0]].inc(count)
    else:
        retTree.children[trans[0]] = treeNode(trans[0], count, retTree)

    # 给结点添加指针
    if headerTable[trans[0]][1] is None:
        headerTable[trans[0]][1] = retTree.children[trans[0]]
    else:
        update_node_link(headerTable[trans[0]][1], retTree.children[trans[0]])

    # 递归，将整个事务添加到树上
    if len(trans) > 1:
        update_tree(trans[1:], retTree.children[trans[0]], count, headerTable)


def update_node_link(node, targetNode):
    while node.nodeLink != None:
        node = node.nodeLink
    node.nodeLink = targetNode


def creat_tree(data, min_sup=3):
    header_lable = {}
    for trans in data:
        for item in trans:
            if item not in header_lable:
                header_lable.update({item: [1, None]})
            else:
                header_lable[item][0] += 1

    for item in list(header_lable.keys()):
        if header_lable[item][0] < min_sup:
            del(header_lable[item])

    # 对头表排序
    header_lable = header_lable.items()
    header_lable = dict(sorted(header_lable, key=lambda x: x[1][0], reverse=True))

    # 根据排序后的频度，为每个事务排序
    count_trans = {}
    reTree = treeNode('Null', 1, None)
    for trans, count in data.items():
        for item in trans:
            if item in header_lable:
                num = header_lable[item][0]
                count_trans.update({item: num})
        count_trans = count_trans.items()
        count_trans = dict(sorted(count_trans, key=lambda x:x[1], reverse=True))
        ordered_trans = list(count_trans.keys())
        count_trans.clear()

        # 将排好队的事务添加至树中
        if len(ordered_trans) > 0:
            update_tree(ordered_trans, reTree, count, header_lable)
    reTree.display()
    return header_lable


creat_tree(load_data())
