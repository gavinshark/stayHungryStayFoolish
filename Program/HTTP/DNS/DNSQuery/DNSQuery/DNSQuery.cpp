// DNSQuery.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <stdio.h>
#include <vector>
#include <string>
#include "ws2tcpip.h"
#include <windns.h>
#include <Windows.h>
#include <iostream>
using namespace std;

#pragma comment(lib, "Dnsapi.lib")
#pragma comment(lib, "Ws2_32.lib")

#define MAX_IP_STRING_LENGTH (128)

typedef struct _DNS_RESULT {
    wstring strType;
    wstring strDNSValue;
}DNS_RESULT;

typedef vector<DNS_RESULT> VDNSRESULT;

int getDNSVector(const wstring & strHostName, VDNSRESULT & vDNSResult) {
    int ret = 0;
    vDNSResult.clear();

    PDNS_RECORD pDnsRecord = NULL;
    DNS_STATUS iDNSTATUS = DnsQuery_W(
        strHostName.c_str(), DNS_TYPE_ALL, DNS_QUERY_STANDARD, NULL, &pDnsRecord, NULL);//DNS_TYPE_ALL,DNS_TYPE_ANY,DNS_TYPE_A, DNS_TYPE_AAAA, DNS_TYPE_CNAME
    
    PDNS_RECORD pTempRecord = pDnsRecord;
    TCHAR szTmp[MAX_IP_STRING_LENGTH] = {_T('0')};
    while (pTempRecord != NULL)
    {
        DNS_RESULT dnsResult;
        switch (pTempRecord->wType)
        {
        case DNS_TYPE_A:
            dnsResult.strType = L"IPV4";
            InetNtopW(AF_INET, &pTempRecord->Data.A.IpAddress, szTmp, sizeof(szTmp));            
            dnsResult.strDNSValue = szTmp;
            break;
        case DNS_TYPE_AAAA:
            dnsResult.strType = L"IPV6";
            InetNtopW(AF_INET6, &pTempRecord->Data.AAAA.Ip6Address, szTmp, sizeof(szTmp));
            //wsprintf(szTmp, L"0x%032x", pTempRecord->Data.AAAA.Ip6Address);
            dnsResult.strDNSValue = szTmp;
            break;
        case DNS_TYPE_CNAME:
            dnsResult.strType = L"CNAME";
            wsprintf(szTmp, L"%s", pTempRecord->Data.CNAME.pNameHost);
            dnsResult.strDNSValue = szTmp;
            break;
        default:
            wsprintf(szTmp, L"%d", pTempRecord->wType);
            dnsResult.strType = szTmp;
            dnsResult.strDNSValue = L"";
            break;
        }
        
        vDNSResult.push_back(dnsResult);

        pTempRecord = pTempRecord->pNext;
    }

    DnsRecordListFree(pDnsRecord, DnsFreeRecordList);

    return ret;
}


void displayDNSVector(const VDNSRESULT & vDNSResult) {
    wcout << L"the DNS result is :\n";
    for each (DNS_RESULT dnsResult in vDNSResult)
    {
        wcout << L"wType: "<<dnsResult.strType <<L" and Resolved Address:"<< dnsResult.strDNSValue<<endl;
    }
}


int main(int argc, char **argv)
{
    wstring strHostName;
    VDNSRESULT vDNSResult;
    while (true) {
        wcout << L"\nPlease input the HostName"<<endl;
        wcin >> strHostName;
        if (0 == getDNSVector(strHostName, vDNSResult))
        {
            displayDNSVector(vDNSResult);
        }
    }
    return 0;
}

