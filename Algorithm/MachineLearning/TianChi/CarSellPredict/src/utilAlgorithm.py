#!/usr/bin/env python
#-*- coding:utf-8 -*-
from logger import logger

class utilAlgorithm():
    def __init__(self):
        logger.debug("%s init",self.__class__.__name__)

    def trainData(self, trainX, trainY, train_attri_dict, crxvalX, crxvalY):
        logger.error("error call with base algorithm")
        return []

    def predictData(self, trainW, predictX):
        logger.error("error call with base algorithm")
        return []

if __name__ == '__main__':
    print("%s UT beign" % (__file__))
