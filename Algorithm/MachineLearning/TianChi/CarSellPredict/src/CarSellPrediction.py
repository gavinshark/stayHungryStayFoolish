#!/usr/bin/env python
#-*- coding:utf-8 -*-
import srvpredict
from logger import logger
from utilconfigration import cfg


if __name__ == '__main__':
    logger.info('Car Sell Prediction Begin!')
    srvpred = srvpredict.srvpredict(cfg.get("data", "trainfile"),
                         cfg.get("data", "predictfile"),
                         cfg.get("data", "outputfile"),
                         cfg.get("method", "methods"),
                         cfg.get("data", "crsval_file"))
    srvpred.train_predict()
    logger.info('Car Sell Prediction End!')
