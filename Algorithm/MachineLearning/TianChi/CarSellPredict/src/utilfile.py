#!/usr/bin/env python
#-*- coding:utf-8 -*-

from numpy import *
from logger import logger
import csv

SALE_DATE = 'sale_date'
CLASS_ID = 'class_id'
SALE_QUANTITY = 'sale_quantity'
BRAND_ID = 'brand_id'
COMPARTMENT = 'compartment'
TYPE_ID = 'type_id'
LEVEL_ID = 'level_id'
DEPARTMENT_ID = 'department_id'
TR = 'TR'
GEARBOX_TYPE = 'gearbox_type'
DIPLACEMENT = 'displacement'
IF_CHARGEING = 'if_charging'
PRICE_LEVEL = 'price_level'
PRICE = 'price'
DRIVEN_TZYPE_ID = 'driven_type_id'
FUEL_TYPE_ID = 'fuel_type_id'
NEWENERGY_TYPE_ID = 'newenergy_type_id'
EMISSION_STANDARDS_ID = 'emission_standards_id'
IF_MPV_ID = 'if_MPV_id'
IF_LUXURIOUS_ID = 'if_luxurious_id'
POWER = 'power'
CYLINDER_NUMBER = 'cylinder_number'
ENGINE_TORQUE = 'engine_torque'
CAR_LENGTH = 'car_length'
CAR_WIDTH = 'car_width'
CAR_HEIGHT = 'car_height'
TOTAL_QUALITY = 'total_quality'
EQUIPMENT_QUALITY = 'equipment_quality'
RATE_PASSENGER = 'rated_passenger'
WHEELBASE = 'wheelbase'
FRONT_TRACK = 'front_track'
REAR_TRACK = 'rear_track'

PREDICT_IDX_DATE = 0
PREDICT_IDX_CLASS_ID = 1

class utilfile(object):
    training_file = ""
    predict_file = ""
    output_file = ""
    crsval_file = ""
    def __init__(self, training_file, predict_file, output_file, crsval_file):
        self.training_file = training_file
        self.predict_file = predict_file
        self.output_file = output_file
        self.crsval_file = crsval_file

    def readTrainData(self):
        logger.info("readTrainData from %s ", self.training_file)
        train_attri_dict = {}
        try:
            rownum = self.getfilerows(self.training_file)
            csv_file = csv.reader(open(self.training_file))
            irowidx = 0
            trainlabels = ""
            trainX = mat(zeros((rownum-1, 2)))
            trainY = mat(zeros((rownum-1, 1)))
            for row in csv_file:
                if irowidx == 0:
                    trainlabels = row.copy()
                    attridx = 0
                    for idx in range(len(trainlabels)):
                        if trainlabels[idx] != SALE_QUANTITY:
                            train_attri_dict[trainlabels[idx]] = attridx
                            attridx += 1
                else:
                    x,y = self.washData(row, train_attri_dict)
                    trainX[irowidx-1] = x
                    trainY[irowidx-1] = y
                irowidx += 1
            logger.info("TrainX size %d*%d firstdata:%d lastdata:%d", shape(trainX)[0], shape(trainX)[1], trainX[0,0], trainX[-1,-1])
            logger.info("TrainY size %d*%d firstdata:%d lastdata:%d ", shape(trainY)[0], shape(trainY)[1], trainY[0,0], trainY[-1,-1])
            logger.info("trainlabels %s ", ",".join(trainlabels))
        except IOError as err:
            logger.error("IOError in handling %s, error code %d", self.training_file, err.errno)
        return trainX, trainY, train_attri_dict


    def readPredictData(self):
        logger.info("readPredictData from %s ", self.predict_file)
        try:
            rownum = self.getfilerows(self.predict_file)
            csv_file = csv.reader(open(self.predict_file))
            irowidx = 0
            predictlabels = ""
            predictX = zeros((rownum-1, 2))
            for row in csv_file:
                if irowidx == 0:
                    predictlabels = row.copy()
                else:
                    x = array([self.washmonth(row[0]), row[1]])
                    predictX[irowidx-1] = mat(x)
                irowidx += 1
            logger.info("predictX size %d*%d firstdata:%d lastdata:%d", shape(predictX)[0], shape(predictX)[1], predictX[0][0],
                        predictX[-1][-1])
            logger.info("predictlabels %s ", ",".join(predictlabels))
        except IOError as err:
            logger.error("IOError in handling %s, error code %d", self.predict_file, err.errno)
        return predictX, predictlabels


    def writePredictData(self, predictX, predictlabels, predictY):
        csvfile = []
        logger.info("writePredictData to %s ", self.output_file)
        try:
            csvfile = open(self.output_file, 'wt', encoding="UTF8", newline='')
            writer = csv.writer(csvfile, delimiter=",")
            writer.writerow(predictlabels)
            for idx in range(shape(predictX)[0]):
                row = predictX[idx].tolist()
                row[PREDICT_IDX_DATE] = self.recvermonth(row[PREDICT_IDX_DATE])
                for yidx in range(shape(predictY)[1]):
                     row.append(str(predictY[idx, yidx]))
                writer.writerow(row)
            logger.info("PredictData size %d*%d firstdata:%s lastdata:%s", shape(predictY)[0], shape(predictY)[1], str(predictY[0, 0]),
                        str(predictY[-1, -1]))
        except IOError as err:
            logger.error("IOError in handling %s, error code %d", self.output_file, err.errno)

    def washData(self, data, train_attri_dict):
        x = [self.washmonth(data[train_attri_dict[SALE_DATE]]), data[train_attri_dict[CLASS_ID]]]
        y = data[2]
        return x, y


    def washmonth(self, yearmonthinput):
        yearmonthint = round(float(yearmonthinput)) -1 #201500-201511
        year = floor(yearmonthint/100)
        month = yearmonthint - year*100
        monthoutput = (year-2012)*12 + month
        return monthoutput

    def recvermonth(self, monthinput):
        year = floor(int(monthinput)/12)
        month = int(monthinput) - year*12 + 1
        return (year*100 + 201200 + month)

    def getfilerows(self, filename):
        try:
            pfile = open(filename, 'r')
            linenum = len(pfile.readlines())
        except IOError as err:
            logger.error("IOError in handling %s, error code %d", filename, err.errno)
        finally:
            pfile.close()
        return linenum

    def readCrsValData(self):
        logger.info("read Corss Validation Data from %s ", self.crsval_file)
        try:
            rownum = self.getfilerows(self.crsval_file)
            csv_file = csv.reader(open(self.crsval_file))
            irowidx = 0
            crxvallabels = ""
            crxvalX = mat(zeros((rownum - 1, 2)))
            crxvalY = mat(zeros((rownum - 1, 1)))
            for row in csv_file:
                if irowidx == 0:
                    crxvallabels = row.copy()
                else:
                    x = array([self.washmonth(row[0]), row[1]])
                    crxvalX[irowidx - 1, :] = mat([x])
                    crxvalY[irowidx - 1, 0] = int(row[2])
                irowidx += 1
            logger.info("crxvalX size %d*%d firstdata:%d lastdata:%d", shape(crxvalX)[0], shape(crxvalX)[1],
                        crxvalX[0,0], crxvalX[-1,-1])
            logger.info("crxvalY size %d*%d firstdata:%d lastdata:%d", shape(crxvalY)[0], shape(crxvalY)[1],
                        crxvalY[0, 0], crxvalY[-1, -1])
            logger.info("crxvallabels %s ", ",".join(crxvallabels))
        except IOError as err:
            logger.error("IOError in handling %s, error code %d", self.crsval_file, err.errno)
        return crxvalX, crxvallabels, crxvalY

if __name__ == '__main__':
    print('utilFile UT begin')
    utilf = utilfile('../data/raw/[new] yancheng_train_20171226.csv',
                         '../data/raw/yancheng_testA_20171225.csv',
                         '../data/output/predict_result_UT.csv')
    trainX, trainY, trainlabels = utilf.readTrainData()
    #print('trainX', trainX[0:9, :], trainX[-1, :])
    #print('trainY', trainY[0:9, :], trainY[-1, :])
    #print('trainlabels', trainlabels)

    predictX,predictlabels  = utilf.readPredictData()
    #print('predictX', predictX[0:9, :], predictX[-1, :])
    #print('predictlabels', predictlabels)

    predictY = predictX[:,0][:,newaxis]
    utilf.writePredictData(predictX, predictlabels, predictY)

    print('month 201409 wash result is ', utilf.washmonth(201409.0))

    print('utilFile UT end')
