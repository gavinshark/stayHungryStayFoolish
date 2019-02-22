// singlelon.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"

#include <windows.h>
#include <stdio.h>
#include <process.h>


CRITICAL_SECTION criticalSection;

class Singleton {
public:
    static Singleton * instance();
    void displayVisitTimes() { wprintf(L"VisitTimes=%d\n", ullsVisitTimes); };
    void increaseVisitTimes() {
        InterlockedIncrement(&ullsVisitTimes);                   //to avoid multi-assemble orders in different threads 
    }
private:
    static Singleton* volatile psInstance;                       //to avoid reg in different threads
    static unsigned long long volatile ullsVisitTimes;           //to avoid reg in different threads
    int x;
    Singleton() :x(5) {};
};

Singleton* volatile Singleton::psInstance = NULL;
unsigned long long volatile Singleton::ullsVisitTimes = 0;

Singleton* Singleton::instance() {
    if (NULL == psInstance) {
        EnterCriticalSection(&criticalSection);
        if (NULL == psInstance) {
            wprintf(L"Time to create an object for singleton.\n");
            Singleton* volatile pTemp = new Singleton;            //to avoid malloc and initialization gap in singleton
            psInstance = pTemp;
        }
        LeaveCriticalSection(&criticalSection);
    }
    return psInstance;
}

unsigned __stdcall ThreadFunc(void* pArguments) {
    DWORD idx = (DWORD)pArguments;
    wprintf(L"This is the %d th Thread\n", idx);
    Singleton::instance()->increaseVisitTimes();
    Singleton::instance()->displayVisitTimes();
    return 0;
}


int main()
{
    if (!InitializeCriticalSectionAndSpinCount(&criticalSection, 0x00000400))
    {
        return -1;
    }

    //...
    HANDLE hzthread[5];
    int idx = 0;
    for (idx = 0; idx < sizeof(hzthread) / sizeof(HANDLE); idx++) {
        hzthread[idx] = (HANDLE)_beginthreadex(NULL, 0, &ThreadFunc, (void *)idx, NULL, 0);
    }

    WaitForMultipleObjects(sizeof(hzthread) / sizeof(HANDLE), hzthread, TRUE, INFINITE);

    wprintf(L"All threads finished.\n");

    for (idx = 0; idx < sizeof(hzthread) / sizeof(HANDLE); idx++)
    {
        CloseHandle(hzthread[idx]);
    }
    //

    DeleteCriticalSection(&criticalSection);

    while (true)
    {

    }

    return 0;
}

