#coding=utf-8

import numpy as np


class NormalEqualtion(object):
    def cal_normal_equation(self, X, y):
        #onesmatrix = np.ones([X.shape[0], 1])
        #tmp = X.astype(np.float)
        #Xtmp = np.c_[onesmatrix, tmp]
        pinv_matrix = np.linalg.pinv(np.dot(X.T, X))
        theta = np.dot(np.dot(pinv_matrix, X.T), y)
        return theta
