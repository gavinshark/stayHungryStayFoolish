#!/usr/bin/env python
#-*- coding:utf-8 -*-
import time
import json
import threading
import esDemoData
import random

lock=threading.Lock()

count = 0
iterNum = 100

def RunRaceThreads():
    try:
        #1. create N threads to Do DNS query
        threadsNum = 10
        threadList = list()
        for i in range(0, threadsNum):
            threadList.append(threading.Thread(
                target=subRunRaceThreads
            ))
        
        print('%d threads start' % (threadsNum))

        for thread in threadList:
            thread.start()

        #2. join the N threads results
        for thread in threadList:
            thread.join()
        
        print('all threads ends and count is %d(should be %d if no race)' % (count, (iterNum * threadsNum)))
    except:
        print('fail to RunRaceThreads!')
        return []
    return []

def subRunRaceThreads():
    global lock
    for idx in range(iterNum):
        global count
        lock.acquire()
        currentCount = count
        time.sleep(random.randint(1,1000)*0.001)
        currentCount += 1
        print('current Count is %d' % (currentCount))
        count = currentCount
        lock.release()
    return

if __name__ == '__main__':
    RunRaceThreads()
