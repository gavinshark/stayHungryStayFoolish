#!/usr/bin/env python
#coding=utf-8

from matplotlib import pyplot
from matplotlib import cm
from mpl_toolkits.mplot3d import axes3d
import numpy

class plotData(object):
    filename = ''
    matrixfile = []
    X = []
    y = []
    def __init__(self):
        filename = ''

    def __init__(self, filename):
        self.filename = filename
        if(self.filename != ''):
            self.matrixfile = numpy.loadtxt(self.filename, dtype=numpy.str, delimiter=',')
            self.X = self.matrixfile[:, 0].astype(numpy.float)
            self.y = self.matrixfile[:, 1].astype(numpy.float)

    def plottxtfunc(self):
        self.plotDataFunc(self.X, self.y, True)

    def plotDataFunc(self, X, y, isShow):
        print('Plotting Orignal Data Begin...')
        pyplot.figure(1)
        pyplot.plot(X,y,'rx')
        pyplot.xlabel('Profit in $10,000s')
        pyplot.ylabel('Population of City in 10,000s')
        if isShow:
            pyplot.show()
        print('Plotting Orignal Data End...')

    def plotthetafunc(self, theta):
        self.plotDataFunc(self.X, self.y, False)
        onesmatrix = numpy.ones([self.X.shape[0], 1])
        Xmatrix = numpy.c_[onesmatrix, self.X]
        yest = numpy.dot(Xmatrix, theta)
        self.plotstraitline(self.X, yest, False)

    def plotstraitline(self, X, y, isNew=True):
        if isNew:
            pyplot.figure(1)
        pyplot.plot(X, y)
        pyplot.show()

    def plotsurf(self, X, y, z):
        fig = pyplot.figure()
        ax = fig.add_subplot(111, projection="3d")
        X, y = numpy.meshgrid(X,y)
        surf = ax.plot_surface(X,y,z,cmap=cm.coolwarm)
        fig.colorbar(surf,shrink=0.6, aspect=10)
        pyplot.show()

    def plotcontour(self,X,y,z,theta):
        fig = pyplot.figure()
        v = numpy.logspace(-2, 3, num=20)
        CS = pyplot.contour(X,y,z,v)
        pyplot.plot(theta[0], theta[1], 'rx')
        pyplot.show()








