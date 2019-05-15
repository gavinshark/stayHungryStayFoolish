// CSLock.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <windows.h>
#include <process.h>

HANDLE mutex1;
HANDLE mutex2;


unsigned __stdcall thread1(LPVOID lp) {

    WaitForSingleObject(mutex1, INFINITE);    
    wprintf(L"thread 1, Entered mutex1\n");

    Sleep(1000);

    wprintf(L"thread 1, try to enter mutex2\n");
    WaitForSingleObject(mutex2, INFINITE);

    wprintf(L"thread1, all mutex got!\n");

    ReleaseMutex(mutex2);
    ReleaseMutex(mutex1);

    return 0;
}


unsigned __stdcall thread2(LPVOID lp) {

    WaitForSingleObject(mutex2, INFINITE);
    wprintf(L"thread 2, Entered mutex2\n");

    Sleep(1000);

    wprintf(L"thread 2, try to enter mutex1\n");
    WaitForSingleObject(mutex1, INFINITE);

    wprintf(L"thread2, all mutex got!\n");

    ReleaseMutex(mutex1);
    ReleaseMutex(mutex2);

    return 0;
}

int main()
{

    mutex1 = CreateMutex(NULL, false, L"MYMUTEX1");
    mutex2 = CreateMutex(NULL, false, L"MYMUTEX2");

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

    CloseHandle(mutex1);
    CloseHandle(mutex2);

    return 0;
}
