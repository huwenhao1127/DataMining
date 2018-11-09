#! /usr/local/bin/python3.6
# coding=utf-8

# 作者：huwenhao
# Github主页： https://github.com/huwenhao1127/
import numpy as np
import scipy.fftpack as fft

np.set_printoptions(threshold=np.inf)


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
    print('base：', P)

    # Compute new data
    Y = P*X
    return Y


a = np.array([[1, 1, 1, 1, 0, 0, 0, 0],
              [1, 1, 1, 1, 0, 0, 0, 0],
              [1, 1, 1, 1, 0, 0, 0, 0],
              [1, 1, 1, 1, 0, 0, 0, 0],
              [1, 1, 1, 1, 0, 0, 0, 0],
              [1, 1, 1, 1, 0, 0, 0, 0],
              [1, 1, 1, 1, 0, 0, 0, 0],
              [1, 1, 1, 1, 0, 0, 0, 0]])

b = np.array([[1, 0, 1, 0, 1, 0, 1, 0],
              [0, 1, 0, 1, 0, 1, 0, 1],
              [1, 0, 1, 0, 1, 0, 1, 0],
              [0, 1, 0, 1, 0, 1, 0, 1],
              [1, 0, 1, 0, 1, 0, 1, 0],
              [0, 1, 0, 1, 0, 1, 0, 1],
              [1, 0, 1, 0, 1, 0, 1, 0],
              [0, 1, 0, 1, 0, 1, 0, 1]])


dct = lambda x: fft.dct(x, norm='ortho')
idct = lambda x: fft.idct(x, norm='ortho')

c = dct(b)
d = idct(c)

print(c)
print(d)

