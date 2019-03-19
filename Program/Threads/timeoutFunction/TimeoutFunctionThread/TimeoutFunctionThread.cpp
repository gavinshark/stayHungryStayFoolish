#include "stdafx.h"
#include <iostream>
#include "process.h"
#include <string>
#include <time.h>
#include <memory>
#include <map>
#include <random>
#include <cmath>
#include "windows.h"
using namespace std;

#define ERROR_TIME_OUT (-1)
#define ERROR_SUCCESS  (0)
#define ERROR_RETCODE  (3)
#define ERROR_ERROR (1)

#define WAIT_FOR_TIME_OUT (200)
#define DELAY_FUNC_DELAY_TIME (50)

std::string current_time() {
    time_t now = time(NULL);
    struct tm tstruct;
    char buf[40];
    localtime_s(&tstruct, &now);
    //format: HH:mm:ss
    strftime(buf, sizeof(buf), "%X", &tstruct);
    return buf;
}

class CTimeOutParam {
public:
    CTimeOutParam(HANDLE handle, string strInput):m_handle(handle), m_string(strInput), m_iRetCode(ERROR_SUCCESS) { }
    ~CTimeOutParam() {
        CloseHandle(m_handle); 
        std::cout << "close handle at:" << current_time() << endl;
    }
    int getRetCode() { return m_iRetCode; }
    void setRetCode(int iRetCode) { m_iRetCode = iRetCode; }
    HANDLE getHandle() { return m_handle; }
    string getString() { return m_string; }
private:
    HANDLE m_handle;
    string m_string;
    int m_iRetCode;
};

UINT _stdcall busyworkFunc(LPVOID pParam) {
    std::random_device r;
    std::default_random_engine e1(r());
    std::uniform_int_distribution<int> uniform_dist(1, 6);
    int mean = uniform_dist(e1);
    if (NULL != pParam)
    {
        std::shared_ptr<CTimeOutParam> pShare = *((std::shared_ptr<CTimeOutParam> *)pParam);
        std::cout << "busyworkFunc: pShare use count is:" << pShare.use_count() << endl;
        std::cout << "busyworkFunc: work with "<<pShare->getString() <<" starts at:" << current_time() << endl;
        Sleep(mean*DELAY_FUNC_DELAY_TIME);
        ::SetEvent(pShare->getHandle());
        pShare->setRetCode(ERROR_RETCODE);
        std::cout << "busyworkFunc: ends at:" << current_time() << endl;
        std::cout << "busyworkFunc: pShare use count is:" << pShare.use_count() << endl;
        return ERROR_SUCCESS;
    }
    else {
        return ERROR_ERROR;
    }
}


int timoutReturnFunc(int timoutInterval, string strParam) {
    int iRet = ERROR_SUCCESS;
    unsigned int uiThreadId = 0;
    HANDLE hEvent = ::CreateEvent(NULL, FALSE, FALSE, NULL);
    std::shared_ptr<CTimeOutParam> pShare(new CTimeOutParam(hEvent, strParam));
    std::cout << "timoutReturnFunc: pShare use count is:" << pShare.use_count()<< endl;
    HANDLE hThread = (HANDLE)_beginthreadex(NULL, 0, busyworkFunc, (void *)&pShare, 0, &uiThreadId);
    DWORD dwResult = ::WaitForSingleObject(hEvent, WAIT_FOR_TIME_OUT);
    CloseHandle(hThread);
    if (WAIT_OBJECT_0 == dwResult)
    {
        iRet = pShare->getRetCode();
    } 
    else if (WAIT_TIMEOUT == dwResult)
    {
        iRet = ERROR_TIME_OUT;
    } 
    else
    {
        iRet = ERROR_ERROR;
    }
    return iRet;
}

int main()
{
    bool timedout = false;
    int retValue = 10;
    int timoutInterval = WAIT_FOR_TIME_OUT;
    string strParam = "Hello main";
    while (true) {
        std::cout << endl;
        std::cout << "Main: call function at:" << current_time() << endl;
        retValue = timoutReturnFunc(timoutInterval, strParam);
        if (ERROR_TIME_OUT == retValue)
        {
            std::cout << "Main: Time out at:" << current_time() << endl;
        }
        else {
            std::cout << "Main: retValue is:" << retValue << " at " << current_time() << endl;
        }
    }

    while(1){}

    return 0;
}