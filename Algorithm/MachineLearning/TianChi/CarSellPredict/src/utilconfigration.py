#!/usr/bin/env python
#-*- coding:utf-8 -*-

import configparser
CFG_FILE = '..\\cfg\\cfg.ini'
cfg = configparser.RawConfigParser()
cfg.read(CFG_FILE)


if __name__ == '__main__':
    print('loglvel is %d' % cfg.getint('log', 'loglevel'))