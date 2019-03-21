#!/usr/bin/env python
#-*- coding:utf-8 -*-

import logging
import os
 
LOG_DIR = './log'

if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)


from logging.handlers import RotatingFileHandler
logger = logging.getLogger("Rotating Log")
logger.setLevel(logging.INFO)
handler = RotatingFileHandler(os.path.join(LOG_DIR, 'dnsQueryFromES.log'), maxBytes=10*1000*1000,
                                  backupCount=300)
formatter = logging.Formatter('%(asctime)-12s [%(levelname)s] %(message)s')  
handler.setFormatter(formatter)
logger.addHandler(handler)


chlr = logging.StreamHandler()
chlr.setFormatter(formatter)
chlr.setLevel('INFO')
logger.addHandler(chlr)