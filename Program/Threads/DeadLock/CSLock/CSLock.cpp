// CSLock.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <windows.h>
#include <process.h>

CRITICAL_SECTION cs1;
CRITICAL_SECTION cs2;


unsigned __stdcall thread1(LPVOID lp) {

    EnterCriticalSection(&cs1);
    wprintf(L"thread 1, Entered cs1\n");
    
    Sleep(1000);
    
    wprintf(L"thread 1, try to enter cs2\n");
    EnterCriticalSection(&cs2);

    wprintf(L"thread1, all cs got!\n");

    LeaveCriticalSection(&cs2);
    LeaveCriticalSection(&cs1);

    return 0;
}


unsigned __stdcall thread2(LPVOID lp) {

    EnterCriticalSection(&cs2);
    wprintf(L"thread 2, Entered cs2\n");

    Sleep(1000);

    wprintf(L"thread 2, try to enter cs1\n");
    EnterCriticalSection(&cs1);

    wprintf(L"thread2, all cs got!\n");

    LeaveCriticalSection(&cs1);
    LeaveCriticalSection(&cs2);
    return 0;
}

int main()
{

    InitializeCriticalSection(&cs1);
    InitializeCriticalSection(&cs2);
        
    HANDLE hThread1 = (HANDLE)_beginthreadex(
        NULL, 0, thread1, NULL, 0, 0
    );
    HANDLE hThread2 = (HANDLE)_beginthreadex(
        NULL, 0, thread2, NULL, 0, 0
    );

    WaitForSingleObject(hThread1, INFINITE);
    WaitForSingleObject(hThread2, INFINITE);


    CloseHandle(hThread1);
    CloseHandle(hThread2);

    return 0;
}
