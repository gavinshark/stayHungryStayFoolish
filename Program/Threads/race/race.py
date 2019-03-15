#!/usr/bin/env python
#-*- coding:utf-8 -*-
import time
import json
import threading
import esDemoData
import random

lock=threading.Lock()

def DNSQuery(hostName):
    time.sleep(random.randint(1,1000)*0.001)
    delayTime = random.randint(1,1000)
    retCode = random.randint(1,10)
    return (delayTime, retCode)


'''
esQueriedResult : [element0, element1, ...]
element format:{"_id": "H_ft2mgB0knGCje4J7uD",
               "_source": {
                    "reason": ["www.baidu.com"],
                    "level": "No",
                    "timestamp": "2019-02-11T05:00:02Z",
                    ...
                },
                ...
}
'''
#query DNS record by N threads
def batchQueryDNS(esQueriedResult):
    try:
        #1. create N threads to Do DNS query
        count = len(esQueriedResult)        
        idxlist = range(0, count)
        threadsNum = 10
        threadList = list()
        for i in range(0, threadsNum):
            threadList.append(threading.Thread(
                target=subBatchQueryDNS, args=(esQueriedResult, idxlist[i::threadsNum])
            ))
        
        print('%d threads start to query job for %d urls' % (threadsNum, count))

        for thread in threadList:
            thread.start()

        #2. join the N threads results
        for thread in threadList:
            thread.join()
        
        print('%d DNS queries finished' % count)
        return esQueriedResult
    except:
        print('fail to batchQueryDNS Error!')
        return []
    return []

def subBatchQueryDNS(esQueriedResult, indexList):
    #global lock
    for idx in indexList:
        #lock.acquire()
        element = esQueriedResult[idx]
        #lock.release()
        url = element['_source']['url'][0]
        print('start to query DNS for %d:%s threadid is:%d' % (idx, url, threading.current_thread().ident))
        hostName = url
        (delayTime, retCode) = DNSQuery(hostName)
        element['DNSQuery_Delay'] = delayTime
        element['DNSQuery_retCode'] = retCode
        #lock.acquire()
        esQueriedResult[idx] = element
        #lock.release()
        print('DNS queried result (Delay:%d,retCode:%d) for %d:%s threadid is:%d' % (delayTime,retCode,idx,hostName,threading.current_thread().ident))
    return

if __name__ == '__main__':
    while 1:
        analyzeResult = batchQueryDNS(esDemoData.demoData)  
        #with open('dnsQueryWrapperResult.log', "w") as f:
        #    f.write(json.dumps(analyzeResult, indent=4))
        for item in analyzeResult:
            if (not ('DNSQuery_retCode' in item)) or ((not 'DNSQuery_Delay' in item)):
                with open('dnsQueryWrapperResulterror.log', "w") as f:
                    f.write(json.dumps(item, indent=4))
