#!/usr/bin/env python
#coding=utf-8

import numpy

class warm_up(object):
    ranklength = 0
    def __init__(self, ranklength):
        self.ranklength = ranklength

    def func(self):
        print('Running warmUpExercise ... ')
        print('5x5 Identity Matrix: ')
        self.martixgen()
        print('martixgen completed.')
        print('Ending warmUpExercise ... ')

    def martixgen(self):
        matrixA = numpy.eye(self.ranklength)
        print(matrixA)

