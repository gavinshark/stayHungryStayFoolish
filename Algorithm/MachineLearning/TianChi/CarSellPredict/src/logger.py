#!/usr/bin/env python
# -*- coding:utf-8 -*-

import logging
import logging.handlers
from utilconfigration import cfg

LOG_FILE = '..\\log\\logger.log'
handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1024 * 1024, backupCount=5)
fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'

formatter = logging.Formatter(fmt)
handler.setFormatter(formatter)

logger = logging.getLogger('logger')
logger.addHandler(handler)
logger.setLevel(cfg.getint("log","loglevel"))

if __name__ == '__main__':
    logger.info('first info message')
    logger.debug('first debug message')
