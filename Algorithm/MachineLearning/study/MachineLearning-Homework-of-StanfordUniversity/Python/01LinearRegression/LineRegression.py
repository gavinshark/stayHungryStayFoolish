#!/usr/bin/env python
#coding=utf-8

from warmup import warm_up
from plotData import plotData
from gradientDescent import gradientDescent
from gradientDescent import computeCost
import numpy
from normal_equaltion import NormalEqualtion


def warmup():
    stwarmup =warm_up(5)
    stwarmup.func()

def plotdatafunc(theta):
    stplot = plotData('ex1data1.txt')
    #stplot.plottxtfunc()
    stplot.plotthetafunc(theta)

def gradientdescentfunc(X, y):
    theta = numpy.zeros([2,1])
    #
    stgradientDescent = gradientDescent(X, y, 1500, 0.01, theta)
    stgradientDescent.printcomputeCost()
    thetagradient = stgradientDescent.cal_gradient()
    print('gradient result:')
    print(thetagradient)
    plotdatafunc(thetagradient)
    print('For population = 35,000, we predict a profit of')
    print(numpy.dot(numpy.matrix([[1,3.5]]), thetagradient)[0][0]*10000)
    print('For population = 70,000, we predict a profit of')
    print(numpy.dot(numpy.matrix([[1,7]]), thetagradient)[0][0]*10000)
    return thetagradient


def plot_J_func(X, y, theta):
    theta0_vals = numpy.arange(-10, 10, 0.2)
    theta1_vals = numpy.arange(-1, 4, 0.05)
    J_vals = numpy.zeros((theta0_vals.size, theta1_vals.size))
    for i in range(theta0_vals.size):
        for j in range(theta1_vals.size):
            t = numpy.matrix([theta0_vals[i], theta1_vals[j]])
            J_vals[i][j] = computeCost(X,y,t.T)

    J_vals = J_vals.T
    stplot = plotData('')
    stplot.plotsurf(theta0_vals, theta1_vals, J_vals)
    stplot.plotcontour(theta0_vals, theta1_vals, J_vals,theta)



def normalequalfunc(X, y):
    stnormalequation = NormalEqualtion()
    thetanormal = stnormalequation.cal_normal_equation(X, y)
    print('normal result:')
    print(thetanormal)

def load_data(filename):
    matrixfile = numpy.loadtxt(filename, dtype=numpy.str, delimiter=',')
    X = matrixfile[:, 0].astype(numpy.float)
    onesmatrix = numpy.ones([X.shape[0], 1])
    tmp = X.astype(numpy.float)
    X = numpy.c_[onesmatrix, tmp]
    y = matrixfile[:, 1].astype(numpy.float)
    y = y[:, numpy.newaxis]
    return (X, y)

def ex1():
    #warmup()
    #plotData()
    (X, y) = load_data('ex1data1.txt')
    theta = gradientdescentfunc(X, y)
    normalequalfunc(X, y)
    plot_J_func(X, y, theta)

if __name__ == '__main__':
    ex1()