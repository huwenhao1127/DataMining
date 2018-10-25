#! /usr/local/bin/python3.6
# coding=utf-8

import numpy as np
import os

np.set_printoptions(threshold=np.inf)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


# PCA（principal component analysis）
# data: raw data
# K: new dimensions
def pca(data, k):
    X = np.asmatrix(data)
    RawDim, NumData = data.shape[0], data.shape[1]

    # Make X a mean-normalized m*n data matrix
    for i in range(RawDim):
        X[i] = X[i] - X[i].mean()

    # Compute symmetric matrix of X
    C = X*X.T*(1/NumData)

    # Compute eigenvectors and eigenvalues of C
    eigenvalue, eigenvector = np.linalg.eig(C)
    eigenvector = eigenvector.T
    print('eigenvalue：', eigenvalue)
    print('eigenvector：', eigenvector)

    # Find P, sort eigenvalue
    SortEigenvalue = np.sort(eigenvalue)
    P = np.zeros((k, RawDim))
    for i in range(k):
        value = SortEigenvalue[RawDim-1-i]
        index = np.argwhere(eigenvalue == value)
        P[i] = eigenvector[index]
    print('base：',P)

    # Compute new data
    Y = P*X
    return Y
