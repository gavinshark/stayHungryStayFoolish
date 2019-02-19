#!/usr/bin/env python
#-*- coding:utf-8 -*-
import utilAlgorithm
import utilAlg_Lineregression
import utilAlg_Mean

LINE_REGRESSON = 1
MEAN = 2


class utilAlgorithmFactory(object):
    def getAlgotithm(self, algorithm_id):
        if algorithm_id == LINE_REGRESSON:
            return utilAlg_Lineregression.utilAlg_Lineregression()
        if algorithm_id == MEAN:
            return utilAlg_Mean.utilAlg_Mean()
        else:
            return utilAlgorithm.utilAlgorithm()




