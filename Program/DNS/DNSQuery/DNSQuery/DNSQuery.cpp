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
#include <future>
#include <thread>
#include <chrono>
#include <ctime>
using namespace std;

#pragma comment(lib, "Dnsapi.lib")
#pragma comment(lib, "Ws2_32.lib")

#define MAX_IP_STRING_LENGTH (128)
#define MAX_TIMEOUT_MILLI_SECONDS (1000)

typedef struct _DNS_RESULT {
    wstring strType;
    wstring strDNSValue;
}DNS_RESULT;

typedef vector<DNS_RESULT> VDNSRESULT;

int getDNSVector(const wstring & strHostName, VDNSRESULT & vDNSResult) {
    int ret = 0;
    vDNSResult.clear();

    wcout << "start to query DNS for "<< strHostName << endl;

    PDNS_RECORD pDnsRecord = NULL;
    DNS_STATUS iDNSTATUS = DnsQuery_W(
        strHostName.c_str(), DNS_TYPE_ANY, DNS_QUERY_STANDARD, NULL, &pDnsRecord, NULL);//DNS_TYPE_ALL,DNS_TYPE_ANY,DNS_TYPE_A, DNS_TYPE_AAAA, DNS_TYPE_CNAME
    ret = iDNSTATUS;
    if (DNS_RCODE_NOERROR == iDNSTATUS)
    {
        PDNS_RECORD pTempRecord = pDnsRecord;
        TCHAR szTmp[MAX_IP_STRING_LENGTH] = { _T('0') };
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
    }
    else
    {
        wprintf(L"DNS Query error, error code is %d\n", iDNSTATUS);
    }

    DnsRecordListFree(pDnsRecord, DnsFreeRecordList);

    wcout << "End with querying DNS for " << strHostName << " with "<< vDNSResult.size() << " records"<< endl;

    return ret;
}


void displayDNSVector(const VDNSRESULT & vDNSResult) {
    wcout << L"the DNS result is"<<endl;
    for each (DNS_RESULT dnsResult in vDNSResult)
    {
        wcout << L"wType: " << dnsResult.strType << L" and Resolved Address:" << dnsResult.strDNSValue << endl;
    }
}


int handleDNSQuery(const wstring strHostName) {
    VDNSRESULT vDNSResult;
    clock_t beignTime = clock();
    int iRet = getDNSVector(strHostName, vDNSResult);
    clock_t endTime = clock();
    wcout<< L"Time used(ms): " << (endTime - beignTime)<< endl;
    if (0 == iRet)
    {
        displayDNSVector(vDNSResult);
    }
    return iRet;
}

int main(int argc, char **argv)
{
    wstring strHostName;
    while (true) {
        wcout << L"\nPlease input the HostName" << endl;
        wcin >> strHostName;

        wcout << L"waiting..." << endl;
        future_status status;

        future<int> future_DNSQuery = async(handleDNSQuery, strHostName);
            
        status = future_DNSQuery.wait_for(chrono::milliseconds(MAX_TIMEOUT_MILLI_SECONDS));
        if (future_status::deferred == status) {
            wcout << L"deferred" << endl;
        }
        else if (future_status::timeout == status) {
            wcout << L"timeout" << endl;
        }
        else  if (future_status::ready == status) {
            wcout << L"finished with retCode:"<< future_DNSQuery.get() << endl;
        }
    }
    return 0;
}

