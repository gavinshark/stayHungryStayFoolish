#!/usr/bin/env python
#coding=utf-8

from matplotlib import pyplot
import numpy


def computeCost(X, y, theta):
    dotresult = numpy.dot(X, theta)
    costArray = dotresult - y
    cost = numpy.dot(costArray.T, costArray)[0][0] / 2 / y.size
    return cost

class gradientDescent(object):
    filename = ''
    iternum = 0
    alpha = 0
    theta = []
    X = []
    y = []
    J = []
    def __init__(self,X, y, iternum,alpha,theta):
        self.X = X
        self.y = y
        self.iternum = iternum
        self.alpha = alpha
        self.theta = theta
        #self.loadData()

    #def loadData(self):
    #    onesmatrix = numpy.ones([self.X.shape[0], 1])
    #    tmp = self.X.astype(numpy.float)
    #    self.X = numpy.c_[onesmatrix, tmp]
    #    self.y = self.y.astype(numpy.float)
    #    self.y = self.y[:, numpy.newaxis]

    def cal_gradient(self):
        print('cal_gradient begin')
        JHistory = numpy.zeros((self.iternum, 1))
        thetaest = self.theta
        for i in range(0, self.iternum-1):
            weight = numpy.dot(self.X.T, numpy.dot(self.X,thetaest)-self.y)
            thetaest = thetaest - self.alpha/self.y.size*weight
            JHistory[i] = computeCost(self.X, self.y, thetaest)
        print('cal_gradient end')
        return thetaest

    def printcomputeCost(self):
        cost = computeCost(self.X, self.y, self.theta)
        print("orignal cost = ", cost)

    def featureNormalize(self, X):
        mu = numpy.mean(X).T
        sigma = numpy.std(X, axis=0)
        diag_mu = numpy.diag(mu)
        diag_sigma = numpy.diag(numpy.ones(sigma.shape)/numpy.linalg.inv(sigma))
        size_x = X.shape
        ones_matrix = numpy.ones(size_x)
        X = numpy.dot(X-numpy.dot(ones_matrix, diag_mu), diag_sigma)
        return X, mu, sigma