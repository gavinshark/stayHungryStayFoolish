#!/usr/bin/env python
#-*- coding:utf-8 -*-
import utilAlgorithm
from numpy import *
from logger import logger
from utilfile import *
from utilconfigration import cfg


class utilAlg_Mean(utilAlgorithm.utilAlgorithm):
    def __init__(self):
        print('utilAlg_Mean __init__', self.__class__.__name__)

    def trainData(self, trainX, trainY, train_attri_dict, crxvalX, crxvalY):
        logger.info("%s trainData", self.__class__.__name__)
        trainCarSell = {}
        num_of_car_month = 0
        for idx in range(shape(trainX)[0]):
            cartype = int(trainX[idx, train_attri_dict[CLASS_ID]])
            month = int(trainX[idx, train_attri_dict[SALE_DATE]])
            if cartype in trainCarSell:
                if month in trainCarSell[cartype]:
                    trainCarSell[cartype][month] += trainY[idx][0]
                else:
                    trainCarSell[cartype][month] = trainY[idx][0]
                    num_of_car_month += 1
            else:
                trainCarSell[cartype] = {}
                trainCarSell[cartype][month] = trainY[idx][0]
                num_of_car_month += 1
        conditionX = zeros((num_of_car_month, 2));sellcountY = zeros((num_of_car_month, 1))
        trainW = {}
        totalsell = 0
        totalcarmonthcnt = 0
        totalcartype_num = 0
        idx_of_car_month = 0
        for cartype, selldict in trainCarSell.items():
            monthnum = 0
            sellsum = 0
            for month, monthsell in selldict.items():
                monthnum += 1
                sellsum += monthsell
                if 1 == cfg.getint("mean_method", "genfile"):
                    conditionX[idx_of_car_month][PREDICT_IDX_CLASS_ID] = cartype
                    conditionX[idx_of_car_month][PREDICT_IDX_DATE] = month
                    sellcountY[idx_of_car_month][0] = monthsell
                    idx_of_car_month += 1
            trainW[cartype] = sellsum/monthnum
            totalsell = totalsell + sellsum
            totalcarmonthcnt = totalcarmonthcnt + monthnum
            totalcartype_num += 1
        trainW[0] = totalsell/totalcarmonthcnt

        if 1 == cfg.getint("mean_method", "genfile"):
            output_file_path = cfg.get("mean_method", "outputfile")
            utilf = utilfile("", "", output_file_path,"")
            callabels = [SALE_DATE, CLASS_ID, SALE_QUANTITY]
            utilf.writePredictData(conditionX, callabels, sellcountY)
        logger.info("total car type num is %d, total car*month is %d" % (totalcartype_num, num_of_car_month))
        return trainW

    def predictData(self, trainW, predictX):
        logger.info("%s predictData", self.__class__.__name__)
        predictY = ones((shape(predictX)[0], 1))*trainW[0]
        for idx in range(shape(predictX)[0]):
            if predictX[idx, PREDICT_IDX_CLASS_ID] in trainW:
                car_idx = predictX[idx, PREDICT_IDX_CLASS_ID]
                predictY[idx, 0] = round(float(trainW[car_idx][0][0]))
            else:
                predictY[idx, 0] = round(trainW[0][0][0])
                logger.info('car type %d is not in trainW, using mean data instead',predictX[idx][train_attri_dict[CLASS_ID]])
        return predictY