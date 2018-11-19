#! /usr/local/bin/python3.6
# coding=utf-8

# 作者：huwenhao
# Github主页： https://github.com/huwenhao1127/
import numpy as np
import os
import matplotlib.pyplot as plt
from numpy import random

np.set_printoptions(threshold=np.inf)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

dataDict = '/Users/huwenhao/Github/DataMining/Cluster/two_cluster.txt'


def getData():
    data = []
    a = random.uniform(-2, 2, 200)
    datax = []
    datay = []
    f = open(dataDict, 'w')
    for i in range(0, 100, 2):
        datax.extend([1+a[i], 5+a[i+100]])
        datay.extend([1+a[i+1], 5+a[i+101]])
    data.append(datax)
    data.append(datay)
    f.write(str(datax).strip('[').strip(']')+'\n'+str(datay).strip('[').strip(']'))
    f.close()


def loadData():
    f = open(dataDict, 'r')
    data = f.read().split('\n')
    datax = data[0].split(',')
    datax = [float(i) for i in datax]
    datay = data[1].split(',')
    datay = [float(i) for i in datay]
    return datax, datay


def plotData(datax, datay):
    plt.figure(1)
    plt.scatter(datax, datay, s=10)
    plt.show()


x, y = loadData()
plotData(x, y)
