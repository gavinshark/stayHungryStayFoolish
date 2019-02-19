#!/usr/bin/env python
#-*- coding:utf-8 -*-
import utilfile
import utilAlgorithmFactory
from logger import logger

class srvpredict(object):
    utilAlgVector = []
    utilfile = []
    def __init__(self, training_file, predict_file, output_file, methodstr="Lineregression;", crsval_file=""):
        logger.debug("%s init training file %s predict file %s output file %s cross validation file %s" %
                     (self.__class__.__name__, training_file, predict_file, output_file, crsval_file))
        self.utilfile = utilfile.utilfile(training_file, predict_file, output_file, crsval_file)
        methodvector = methodstr.split(";")
        for method in methodvector:
            if method.__len__() != 0:
                self.utilAlgVector.append(utilAlgorithmFactory.utilAlgorithmFactory().getAlgotithm(int(method)))

    @staticmethod
    def trainData(utilAlg, trainX, trainY, train_attri_dict, crxvalX, crxvalY):
        print('begin to train Data')
        trainW = utilAlg.trainData(trainX, trainY, train_attri_dict, crxvalX, crxvalY)
        print('end with training Data\r\n')
        return trainW

    @staticmethod
    def crossverify(utilAlg, trainW, verifyX, verifyY):
        print('begin to verify Data')
        #predictY = utilAlg.predictData(trainW, verifyX)
        print('end with verifying Data\r\n')
        return []#predictY

    def selectbestAlgorithm(self, verifyResultdict):
        print('begin to select Algorithm')
        for key, value in verifyResultdict.items():
            print('end with selecting Algorithm')
            return self.utilAlgVector[0], value['trainW']
        print('end with selecting Algorithm')
        return []

    def predictData(self, bestalgorithm, trainW, predictX):
        print('begin to predict data')
        predictY = bestalgorithm.predictData(trainW, predictX)
        print('end with predicting  data')
        return predictY

    def train_predict(self):
        #train
        trainX, trainY, train_attri_dict = self.utilfile.readTrainData()
        crxvalX, crxlabels, crxvalY = self.utilfile.readCrsValData()
        verifyX = trainX.copy()
        verfyY = trainY.copy()
        #cross verify
        verifyresultdict = {}
        for utilAlg in self.utilAlgVector:
            trainW = self.trainData(utilAlg, trainX, trainY, train_attri_dict, crxvalX, crxvalY)
            verifyresult = self.crossverify(utilAlg, trainW, verifyX, verfyY)
            verifyresultdict[utilAlg.__class__.__name__] = {}
            verifyresultdict[utilAlg.__class__.__name__]['trainW'] = trainW
            verifyresultdict[utilAlg.__class__.__name__]['verifyresult'] = verifyresult
        bestalgorithm, trainW = self.selectbestAlgorithm(verifyresultdict)
        #predict
        predictX, predictXlabels = self.utilfile.readPredictData()
        predictY = self.predictData(bestalgorithm, trainW, predictX)
        #write data
        self.utilfile.writePredictData(predictX, predictXlabels, predictY)

if __name__ == '__main__':
    srvpred = srvpredict("..\\data\\[new] yancheng_train_20171226.csv",
                                    "..\\data\\yancheng_testA_20171225.csv",
                                    "..\\data\\predict_result.csv",
                                    "2;")
    srvpred.train_predict()