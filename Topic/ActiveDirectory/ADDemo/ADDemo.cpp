// ADDemo.cpp : Defines the entry point for the console application.
//

//  Add msvcrt.dll to the project.
//  Add activeds.lib to the project.

#include "stdafx.h"
#include <objbase.h>
#include <wchar.h>
#include <activeds.h>
#include <sddl.h>

#include <comdef.h>
#include "ultifunc.h"


//  Entry point for the application.
void wmain(int argc, wchar_t *argv[])
{
    wprintf(L"main func begins.\n");

    wprintf(L"read cfg file(cfg.ini) begins.\n");
    CfgStruct stCfg = { 0 };
    DWORD dwLength = MAX_PATH * 2;
    LPOLESTR pszFilter = new OLECHAR[dwLength];
    wcsncpy_s(pszFilter, dwLength, L"", wcslen(L""));
    stCfg.pszFilter = pszFilter;
    LPOLESTR pszAttriBuffer = new OLECHAR[dwLength];
    wcsncpy_s(pszAttriBuffer, dwLength, L"", wcslen(L""));
    stCfg.pszAttriArr = pszAttriBuffer;
    ReadCfg(stCfg);
    int iRetTimes = stCfg.iCycleTimes;
    if (0 > iRetTimes)
    {
        wprintf(L"read cfg pararm from cfg.ini error, erro code is  %d\n", iRetTimes);
    }
    else
    {
        wprintf(L"cfg pararm is %s Circle Time is %d, Page Enable %d,Page size is %d\n", pszFilter, iRetTimes, stCfg.bPageEnable, stCfg.dwPageSize);
    }
    

    //  Handle the command line arguments.    
    BOOL bReturnVerbose = FALSE;

    wprintf(L"Parse input filter begins.\n");

    for (int i = 1;i < argc;i++)
    {
        if (_wcsicmp(argv[i], L"/V") == 0)
        {
            bReturnVerbose = TRUE;
        }
        else if ((_wcsicmp(argv[i], L"/?") == 0) ||
            (_wcsicmp(argv[i], L"-?") == 0))
        {
            wprintf(L"This application queries for users in the current user domain.\n");
            wprintf(L"Syntax: queryusers [/V][querystring]\n");
            wprintf(L"where /V specifies that all properties for the found users should be returned.\n");
            wprintf(L"querystring is the query criteria in ldap query format.\n");
            wprintf(L"Defaults: If no /V is specified, the query returns only the RDN and DN of the items found.\n");
            wprintf(L"If no querystring is specified, the query returns all users.\n");
            wprintf(L"Example: queryusers (sn=Smith)\n");
            wprintf(L"Returns all users with surname Smith.\n");
            return;
        }
        else
        {
            wcsncpy_s(pszFilter, dwLength - wcslen(pszFilter), argv[i], wcslen(argv[i]));
        }
    }
    wprintf(L"Parse input filter ends.\n");
    if (_wcsicmp(pszFilter, L"") == 0)
        wprintf(L"\nFinding all user objects...\n\n");
    else
        wprintf(L"\nFinding user objects based on query: %s...\n\n attribute is %s\n\n", pszFilter, pszAttriBuffer);

    //  Initialize COM.
    CoInitialize(NULL);
    DWORD dwStartTime = GetTickCount();
    HRESULT hr = S_OK;
    //  Get rootDSE and the current user domain container distinguished name.
    IADs *pObject = NULL;
    IDirectorySearch *pContainerToSearch = NULL;
    LPOLESTR szPath = new OLECHAR[MAX_PATH];
    VARIANT var;
    hr = ADsOpenObject(L"LDAP://rootDSE",
        NULL,
        NULL,
        ADS_SECURE_AUTHENTICATION, // Use Secure Authentication.
        IID_IADs,
        (void**)&pObject);
    if (FAILED(hr))
    {
        wprintf(L"Cannot execute query. Cannot bind to LDAP://rootDSE.\n");
        if (pObject)
            pObject->Release();
        return;
    }
    if (SUCCEEDED(hr))
    {
        hr = pObject->Get(_bstr_t("defaultNamingContext"), &var);
        if (SUCCEEDED(hr))
        {
            //  Build path to the domain container.
            wcsncpy_s(szPath, MAX_PATH, L"LDAP://", wcslen(L"LDAP://"));
            wcsncat_s(szPath, MAX_PATH - wcslen(szPath), var.bstrVal, wcslen(var.bstrVal));
            for (int i = 0; i < iRetTimes ; i++)
            {
                hr = ADsOpenObject(szPath,
                    NULL,
                    NULL,
                    ADS_SECURE_AUTHENTICATION, //  Use Secure Authentication.
                    IID_IDirectorySearch,
                    (void**)&pContainerToSearch
                    );

                if (SUCCEEDED(hr))
                {

                    wprintf(L"\ncall FindUsers Func...\n\n");

                    hr = FindUsers(pContainerToSearch, //  IDirectorySearch pointer to domainDNS container.
                        NULL, //  Return all properties.
                        bReturnVerbose,
                        stCfg
                    );


                    if (SUCCEEDED(hr))
                    {
                        if (S_FALSE == hr)
                            wprintf(L"User object cannot be found.\n");
                    }
                    else if (E_ADS_INVALID_FILTER == hr)
                        wprintf(L"Cannot execute query. Invalid filter was specified.\n");
                    else
                        wprintf(L"Query failed to run. HRESULT: %x\n", hr);
                }
                else
                {
                    wprintf(L"Cannot execute query. Cannot bind to the container.\n");
                }
                if (pContainerToSearch)
                    pContainerToSearch->Release();
            }
        }
        VariantClear(&var);
    }
    if (pObject)
        pObject->Release();

    //  Uninitialize COM.
    DWORD dwEndTime = GetTickCount();

    CoUninitialize();
    delete[] szPath;
    delete[] pszFilter;
    delete[] pszAttriBuffer;

    wprintf(L"Time used : %d ms.\n", dwEndTime-dwStartTime);

    if (iRetTimes != 0)
    {
        wprintf(L"every Time used : %d ms.\n", (dwEndTime - dwStartTime) / iRetTimes);
    }
    

    system("Pause");

    return;

}