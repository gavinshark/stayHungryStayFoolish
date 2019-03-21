#!/usr/bin/env python
#-*- coding:utf-8 -*-
from logger import logger

def subFunc(divider):
    a = 10
    try:
        a = 1/divider
    except Exception as err:
            logger.error('exception happened in subFunc')
            logger.exception(err)
    else:
        a =1
    a = 100/divider
    return a

def mainFunc(divider):
    try:            
        subFunc(divider)
        b = 10/divider        
    except Exception as err:
        logger.error('exception happened in mainFunc')
        logger.exception(err)
    return

if __name__ == '__main__':
    divider = 0
    mainFunc(divider)
    print('I am fine. Thank you , and you?')

