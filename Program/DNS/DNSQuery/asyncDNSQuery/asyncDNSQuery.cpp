// asyncDNSQuery.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include "asyncDNSHandler.h"


int main()
{
    wstring strHostName;
    while (true) {
        wcout << L"\nPlease input the HostName" << endl;
        wcin >> strHostName;

        wcout << L"waiting..." << endl;

        handleDNSQuery(strHostName);
    }
    return 0;
}

