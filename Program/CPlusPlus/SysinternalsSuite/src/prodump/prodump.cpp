// prodump.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include "windows.h"

//using procdump.exe -ma PID -t -e -f -o dump_path 
//to get crash dump automatically

int main()
{
    int i = 0;
    int idx = 0;
    while (++idx)
    {
        Sleep(1000);
        wprintf(L"idx = %d, and the proc will crash at 10\n", idx);
        if (idx == 10)
        {
            int j = 12 / i;
            wprintf(L"crash here and j=%d\n", j);
        }
    }
    return 0;
}

