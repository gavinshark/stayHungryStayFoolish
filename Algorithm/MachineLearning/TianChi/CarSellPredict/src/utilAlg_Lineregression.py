#!/usr/bin/env python
#-*- coding:utf-8 -*-
import utilAlgorithm
from logger import logger
from utilfile import *
from utilconfigration import cfg
from numpy import *
import os

class utilAlg_Lineregression(utilAlgorithm.utilAlgorithm):
    def __init__(self):
        print('__init__', self.__class__.__name__)

    def trainData(self, trainX, trainY,train_attri_dict, crxvalX, crxvalY):
        logger.info("%s trainData", self.__class__.__name__)
        mediumfile_path = cfg.get("mean_method", "outputfile")
        if not os.path.exists(mediumfile_path):
            logger.error("medium file %s lost ", mediumfile_path)
            return []
        utilf = utilfile(mediumfile_path, "", "","")
        trainX, trainY, trainlabels = utilf.readTrainData()
        #car_type;month;sellamount
        trainW = {}
        car_type_set = set(trainX[:, train_attri_dict[CLASS_ID]].flatten().A[0].tolist())
        predictX_mid = zeros((len(car_type_set), 2))
        preidct_aws_len = 1
        method_id = cfg.getint("linear_regression", "method")
        if 2 == method_id:
            preidct_aws_len = 3
        predictk_mid = zeros((len(car_type_set), preidct_aws_len))
        car_idx = 0
        for car_type in car_type_set:
            car_num_idx_array = nonzero(trainX[:, train_attri_dict[CLASS_ID]] == car_type)
            trainX_car = trainX[car_num_idx_array[0], train_attri_dict[SALE_DATE]].copy().reshape(
                (shape(car_num_idx_array)[1], -1))  # month
            trainY_car = trainY[car_num_idx_array[0], 0].copy().reshape((shape(car_num_idx_array)[1], -1))
            print('\n\nbegin to train %dth car_id:%d' % (car_idx,car_type))
            ws_car = []
            if 0 == method_id: #direct linear
                ws_car = self.cal_ws_of_linear(trainX_car, trainY_car)
            elif 1 == method_id or  2 == method_id:#metric linear
                car_num_idx_array_crx = nonzero(crxvalX[:, PREDICT_IDX_CLASS_ID] == car_type)
                calvalX_car = crxvalX[car_num_idx_array_crx[0], PREDICT_IDX_DATE].copy().reshape(
                    (shape(car_num_idx_array_crx)[1], -1))  # month
                calvalY_car = crxvalY[car_num_idx_array_crx[0], 0].copy().reshape((shape(car_num_idx_array_crx)[1], -1))
                bmonthcos = 2 == cfg.getint("linear_regression", "method")
                ws_car = self.cal_ws_of_mretic_linear(trainX_car, trainY_car, calvalX_car, calvalY_car, bmonthcos)
                predictX_mid[car_idx][PREDICT_IDX_CLASS_ID] = car_type
                predictX_mid[car_idx][PREDICT_IDX_DATE] = calvalX_car[0,0]
                predictk_mid[car_idx][0] = ws_car["k"]
                if bmonthcos:
                    predictk_mid[car_idx][1] = ws_car["theta"]
                    predictk_mid[car_idx][2] = ws_car["height"]
            car_idx += 1
            trainW[car_type] = ws_car
        if 1 == cfg.getint("linear_regression", "genfile") & 2 == cfg.getint("linear_regression", "method"):
            output_file_path = cfg.get("linear_regression", "outputfile")
            utilf = utilfile("", "", output_file_path,"")
            callabels = [SALE_DATE, CLASS_ID, "train_k"]
            if bmonthcos:
                callabels = [SALE_DATE, CLASS_ID, "train_k", "train_theta", "train_height"]
            utilf.writePredictData(predictX_mid, callabels, predictk_mid)
        return trainW

    def predictData(self, trainW, predictX):
        logger.info("%s predictData ", self.__class__.__name__)
        trainY = zeros((shape(predictX)[0], 1))
        method_id = cfg.getint("linear_regression", "method")

        for idx in range(0, shape(trainY)[0]):
            print("car_id is %d", car_id)
            xMat = predictX[idx, 0]
            car_id = predictX[idx, 1]
            if 0 == method_id:
                trainY[idx, 0] = self.cal_predict_result_of_linear(trainW[car_id], mat(xMat))
            elif 1 == method_id or 2 == method_id:
                trainY[idx, 0] = self.cal_predict_result_of_linear_metric(trainW[car_id], mat(xMat), 2 == method_id)
        return trainY

    def cal_ws_of_linear(self, xMatin, yMat, lam = 0):
        xMat = column_stack((ones((shape(xMatin)[0], 1)), xMatin))
        xTx = xMat.T * xMat
        denom = xTx + eye(shape(xMat)[1]) * lam
        if linalg.det(denom) == 0.0:
            logger.error("This is singular, cannot do inverse")
            return []
        ws = denom.I * (xMat.T * yMat)
        return ws

    def cal_predict_result_of_linear(self, ws, xMatin):
        xMat = mat(ones((shape(xMatin)[0]+1, 1))) #2*1
        xMat[1:(shape(xMatin)[0]+1)] = xMatin
        y = ws.T*xMat
        return round(y[0,0])

    def cal_predict_result_of_linear_metric(self, wsk, xMatin, bmonthcos):
        xMat = mat(ones((shape(xMatin)[0]+1, 1))) #2*1
        xMat[1:(shape(xMatin)[0]+1)] = xMatin
        xMat = xMat.T
        min_ws = wsk["ws"]
        min_k = wsk["k"]
        min_theta = wsk["theta"]
        min_height = wsk["height"]
        xMatTrain = wsk["xMat"].copy()
        yMatTrain = wsk["yMat"].copy()
        m = shape(xMatTrain)[0]  # m
        weights = mat(eye(m))
        for j in range(m):
            diffMat = xMat - xMatTrain[j, :]
            weights[j, j] = exp(diffMat * diffMat.T / (-2 * (min_k ** 2)))  #1*1
        xTx = xMatTrain.T * (weights * xMatTrain)  # 2*2
        if linalg.det(xTx) != 0.0:
            ws = xTx.I * (xMatTrain.T * (weights * yMatTrain))  # 2*1
            print("ws is ", ws)
            y = (xMat * ws)[0, 0]  # 1*1
        else:
            y = 0
        if bmonthcos:
            y = y*self.calmonthcos(xMatin[0,0], min_theta, min_height)
        if y < 0:
            y = 0
        y = round(y)
        print('predict answer is %d' % y)
        return y

    def cal_ws_of_mretic_linear(self, xMatin, yMatin, calvalX, calvalY, bmonthcos):
        m = shape(xMatin)[0]#m
        xMat = column_stack((ones((m, 1)), xMatin))#m*2
        yMat = zeros(shape(yMatin))
        calvalXMat = column_stack((ones((1, 1)), calvalX))#1*2
        weights = mat(eye(m))
        min_theta = 0
        theta_arr = [0]
        if bmonthcos:
            theta_arr_length = 12
            theta_arr = [3]
            for idx in range(theta_arr_length):
                theta_arr.append(2 * pi * idx / theta_arr_length)
        k_arr = [0.1, 0.3, 1, 2, 3, 5, 10, 20, 30, 100]
        min_ws = []
        min_val = Inf
        min_y =0
        min_k = k_arr[0]
        height_arr = [0]
        if bmonthcos:
            height_arr = [1.1, 2.1, 10.1]
        min_height = height_arr[0]
        for height in height_arr:
            for theta in theta_arr:
                for idx in range(m):
                    if bmonthcos:
                        yMat[idx, 0] = yMatin[idx, 0]/self.calmonthcos(xMatin[idx,0], theta, height)
                    else:
                        yMat[idx, 0] = yMatin[idx, 0]
                cosmonthpredict = self.calmonthcos(calvalX, theta, height)
                for k in k_arr:
                    for j in range(m):
                        diffMat = calvalXMat - xMat[j,:]
                        weights[j, j] = exp(diffMat * diffMat.T/(-2*(k**2)))#m*m
                    xTx = xMat.T * (weights * xMat)#2*2
                    if linalg.det(xTx) != 0.0:
                        ws = xTx.I * (xMat.T * (weights * yMat))#2*1
                        yHat = calvalXMat * ws#1*1
                        if bmonthcos:
                            yHat = yHat*cosmonthpredict
                        if (abs(calvalY-yHat)) < min_val:
                            min_val = abs(calvalY-yHat)
                            min_ws = ws
                            min_k = k
                            min_theta = theta
                            min_height = height
                            min_y = yHat
                            min_y_mat = yMat.copy()
        print('bcos is %d min_k is %f min_theta is %f min_height is %f min_val is %f(real:%d predict:%f)\n'
              % (bmonthcos, min_k, min_theta, min_height, min_val, calvalY, min_y))
        print('min_ws is', min_ws)
        return {"ws":min_ws, "k":min_k, "theta":min_theta, "height":min_height, "xMat":xMat, "yMat":min_y_mat}


    def calmonthcos(self, month, theta, height):
        theta_month = (2 * pi * month / 12) + float(theta)
        cos_theta = cos(theta_month)
        cos_theta+= height
        #cos_theta = 2
        #print('cos of month:%d cos_theta:%f (height is %f, theta is %f)' %
        #      (month, cos_theta, height, theta))
        return cos_theta