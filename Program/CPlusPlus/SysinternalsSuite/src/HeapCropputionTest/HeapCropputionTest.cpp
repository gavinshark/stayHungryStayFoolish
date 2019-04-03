// HeapCropputionTest.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include "windows.h"

//!heap -s -v in windbg

//gflag enable page heap & heap checking
//"!gflag /p" in windbg to verify if page heap is open 
//  Current NtGlobalFlag contents: 0x02000000
//    hpa - Place heap allocations at ends of pages



int main()
{
    TCHAR *szTemp = (TCHAR*)calloc(5, sizeof(TCHAR));

    wsprintf(szTemp, _T("1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890"));
    
    int i = 2;
    Sleep(10);
    int j = 0;
    scanf_s("%d", &j);
    wprintf(L"func and i=%d j=%d\n", i, j);

    wprintf(L"skip corruption and i=%d!\n", i);
    wprintf(L"szTemp:%s\n", szTemp);
    //free(szTemp);

    return 0;
}

