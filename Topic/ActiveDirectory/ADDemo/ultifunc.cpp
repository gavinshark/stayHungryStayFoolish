#include "stdafx.h"
#include "ultifunc.h"
#include "Winbase.h"

int ReadCfg(CfgStruct & stCfg)
{
    OLECHAR szCfgFileName[MAX_PATH] = L"./cfg.ini";
    OLECHAR szAppName[MAX_PATH] = L"cfg";
    
    stCfg.iCycleTimes = ::GetPrivateProfileInt(szAppName, _T("CycleTime"), 1, (LPCWSTR)szCfgFileName);
    //wprintf(L"read cfg pararm from %s-%s iCycleTimes is  %d errorCode is %d\n", szCfgFileName, szAppName, stCfg.iCycleTimes, GetLastError());
    stCfg.dwPageSize = ::GetPrivateProfileInt(szAppName, _T("PageSize"), 0, szCfgFileName);
    //wprintf(L"read cfg pararm from %s-%s PageSize is  %d errorCode is %d\n", szCfgFileName, szAppName, stCfg.dwPageSize, GetLastError());
    stCfg.bPageEnable = ::GetPrivateProfileInt(szAppName, _T("PageEnable"), 1, szCfgFileName) != 0;

    ::GetPrivateProfileString(szAppName, _T("Filter"), _T("(name=*)"), stCfg.pszFilter, MAX_PATH * 2-1,szCfgFileName);
    //wprintf(L"read cfg pararm from %s-%s Filter is  %s errorCode is %d\n", szCfgFileName, szAppName, stCfg.pszFilter, GetLastError());
    ::GetPrivateProfileString(szAppName, _T("Arr"), _T("name|objectGUID"), stCfg.pszAttriArr, MAX_PATH * 2-1,szCfgFileName);
    //wprintf(L"read cfg pararm from %s-%s Attribute Array is  %s errorCode is %d\n", szCfgFileName, szAppName, stCfg.pszAttriArr, GetLastError());

    return 0;
}


DWORD splitString(LPOLESTR pstrinput, LPOLESTR ** ppstroutPut)
{
    //1.count "|"
    DWORD splitcnt = 0;
    LPOLESTR pstrtmp = pstrinput;
    while (_T('\0') != (*pstrtmp))
    {
        if (_T('|') == (*pstrtmp))
        {
            splitcnt++;
        }
        pstrtmp++;
    }
    splitcnt++;
    //wprintf(L"splitString: %d attris\n\n", splitcnt);
    //2.new and copy
    LPOLESTR *pstroutPut = new LPOLESTR[splitcnt];
    if (NULL == pstroutPut)
    {
        return -1;
    }
    //wprintf(L"splitString: %d-attr array newed at %x\n\n", splitcnt, pstroutPut);
    pstrtmp = pstrinput;
    LPOLESTR pstrend = pstrinput + 1;
    DWORD dwseclength = 0;
    DWORD dwscidx = 0;
    while (true)
    {
        while (_T('|') != (*pstrend) && _T('\0') != (*pstrend))
        {
            pstrend++;
        }
        dwseclength = DWORD(pstrend - pstrtmp + 1);
        pstroutPut[dwscidx] = new OLECHAR[dwseclength];
        pstroutPut[dwscidx][dwseclength - 1] = _T('\0');
        //wprintf(L"pstrtmp is %s and dwseclength is %d pstroutPut[dwscidx] is %x\n", pstrtmp, dwseclength, pstroutPut[dwscidx]);
        wcsncpy_s((LPOLESTR)(pstroutPut[dwscidx]), dwseclength, pstrtmp, dwseclength - 1);
        //wprintf(L"splitString: %d-attr %s is spited\n\n", dwscidx, pstroutPut[dwscidx]);
        dwscidx++;
        if (_T('\0') == (*pstrend))
        {
            break;
        }
        pstrend++;
        pstrtmp = pstrend;
    }
    *ppstroutPut = pstroutPut;
    return splitcnt;
}

void freesplitArr(LPOLESTR pstroutPut[], DWORD dwlength)
{
    for (DWORD i = 0; i < dwlength; i++)
    {
        LPOLESTR pstroutPuttmp = pstroutPut[i];
        delete[] pstroutPuttmp;
    }
    delete[] pstroutPut;
}


void DisplayQueryResult(ADS_SEARCH_COLUMN &col, const LPOLESTR pszColumn, VARIANT &varDate)
{
    LPOLESTR pszBool = NULL;
    DWORD dwBool = 0;
    PSID pObjectSID = NULL;
    LPOLESTR szSID = NULL;
    LPOLESTR szDSGUID = new WCHAR[39];
    LPGUID pObjectGUID = NULL;
    FILETIME filetime;
    SYSTEMTIME systemtime;
    DATE date;

    LARGE_INTEGER liValue;

    DWORD x = 0L;

    wprintf(L"%s\n", col.pszAttrName);
    switch (col.dwADsType)
    {
    case ADSTYPE_DN_STRING:
        for (x = 0; x < col.dwNumValues; x++)
        {
            wprintf(L"  %s\r\n", col.pADsValues[x].DNString);
        }
        break;
    case ADSTYPE_CASE_EXACT_STRING:
    case ADSTYPE_CASE_IGNORE_STRING:
    case ADSTYPE_PRINTABLE_STRING:
    case ADSTYPE_NUMERIC_STRING:
    case ADSTYPE_TYPEDNAME:
    case ADSTYPE_FAXNUMBER:
    case ADSTYPE_PATH:
        for (x = 0; x < col.dwNumValues; x++)
        {
            wprintf(L"  %s\r\n", col.pADsValues[x].CaseIgnoreString);
        }
        break;
    case ADSTYPE_BOOLEAN:
        for (x = 0; x < col.dwNumValues; x++)
        {
            dwBool = col.pADsValues[x].Boolean;
            pszBool = dwBool ? L"TRUE" : L"FALSE";
            wprintf(L"  %s\r\n", pszBool);
        }
        break;
    case ADSTYPE_INTEGER:
        for (x = 0; x < col.dwNumValues; x++)
        {
            wprintf(L"  %d\r\n", col.pADsValues[x].Integer);
        }
        break;
    case ADSTYPE_OCTET_STRING:
        if (_wcsicmp(col.pszAttrName, L"objectSID") == 0)
        {
            for (x = 0; x < col.dwNumValues; x++)
            {
                pObjectSID = (PSID)(col.pADsValues[x].OctetString.lpValue);
                //  Convert SID to string.
                ConvertSidToStringSid(pObjectSID, &szSID);
                wprintf(L"  %s\r\n", szSID);
                LocalFree(szSID);
            }
        }
        else if ((_wcsicmp(col.pszAttrName, L"objectGUID") == 0))
        {
            for (x = 0; x < col.dwNumValues; x++)
            {
                //  Cast to LPGUID.
                pObjectGUID = (LPGUID)(col.pADsValues[x].OctetString.lpValue);
                //  Convert GUID to string.
                ::StringFromGUID2(*pObjectGUID, szDSGUID, 39);
                //  Print the GUID.
                wprintf(L"  %s\r\n", szDSGUID);
            }
        }
        else
            wprintf(L"  Value of type Octet String. No Conversion.");
        break;
    case ADSTYPE_UTC_TIME:
        for (x = 0; x < col.dwNumValues; x++)
        {
            systemtime = col.pADsValues[x].UTCTime;
            if (SystemTimeToVariantTime(&systemtime,
                &date) != 0)
            {
                //  Pack in variant.vt.
                varDate.vt = VT_DATE;
                varDate.date = date;
                VariantChangeType(&varDate, &varDate, VARIANT_NOVALUEPROP, VT_BSTR);
                wprintf(L"  %s\r\n", varDate.bstrVal);
                VariantClear(&varDate);
            }
            else
                wprintf(L"%s  Could not convert UTC-Time.\n", pszColumn);
        }
        break;
    case ADSTYPE_LARGE_INTEGER:
        for (x = 0; x < col.dwNumValues; x++)
        {
            liValue = col.pADsValues[x].LargeInteger;
            filetime.dwLowDateTime = liValue.LowPart;
            filetime.dwHighDateTime = liValue.HighPart;
            if ((filetime.dwHighDateTime == 0) && (filetime.dwLowDateTime == 0))
            {
                wprintf(L"  No value set.\n");
            }
            else
            {
                //  Verify properties of type LargeInteger that represent time.
                //  If TRUE, then convert to variant time.
                if ((0 == wcscmp(L"accountExpires", col.pszAttrName)) |
                    (0 == wcscmp(L"badPasswordTime", col.pszAttrName)) ||
                    (0 == wcscmp(L"lastLogon", col.pszAttrName)) ||
                    (0 == wcscmp(L"lastLogoff", col.pszAttrName)) ||
                    (0 == wcscmp(L"lockoutTime", col.pszAttrName)) ||
                    (0 == wcscmp(L"pwdLastSet", col.pszAttrName))
                    )
                {
                    //  Handle special case for Never Expires where low part is -1.
                    if (filetime.dwLowDateTime == -1)
                    {
                        wprintf(L"  Never Expires.\n");
                    }
                    else
                    {
                        if (FileTimeToLocalFileTime(&filetime, &filetime) != 0)
                        {
                            if (FileTimeToSystemTime(&filetime,
                                &systemtime) != 0)
                            {
                                if (SystemTimeToVariantTime(&systemtime,
                                    &date) != 0)
                                {
                                    //  Pack in variant.vt.
                                    varDate.vt = VT_DATE;
                                    varDate.date = date;
                                    VariantChangeType(&varDate, &varDate, VARIANT_NOVALUEPROP, VT_BSTR);
                                    wprintf(L"  %s\r\n", varDate.bstrVal);
                                    VariantClear(&varDate);
                                }
                                else
                                {
                                    wprintf(L"  FileTimeToVariantTime failed\n");
                                }
                            }
                            else
                            {
                                wprintf(L"  FileTimeToSystemTime failed\n");
                            }

                        }
                        else
                        {
                            wprintf(L"  FileTimeToLocalFileTime failed\n");
                        }
                    }
                }
                else
                {
                    //  Print the LargeInteger.
                    wprintf(L"  high: %d low: %d\r\n", filetime.dwHighDateTime, filetime.dwLowDateTime);
                }
            }
        }
        break;
    case ADSTYPE_NT_SECURITY_DESCRIPTOR:
        for (x = 0; x < col.dwNumValues; x++)
        {
            wprintf(L"  Security descriptor.\n");
        }
        break;
    default:
        wprintf(L"Unknown type %d.\n", col.dwADsType);
    }
    delete[] szDSGUID;
}


HRESULT FindUsers(IDirectorySearch *pContainerToSearch,  //  IDirectorySearch pointer to the container to search.
    LPOLESTR *pszPropertiesToReturn, //  Properties to return for user objects found.
                                     //  NULL returns all set properties.
    BOOL bIsVerbose, //  TRUE indicates that display all properties for the found objects.
                     //  FALSE indicates that only the RDN.
    CfgStruct stcfg
)
{

    /////////////////////////////

    if (!pContainerToSearch)
        return E_POINTER;
    DWORD dwLength = MAX_PATH * 2;
    // Create search filter.
    LPOLESTR pszSearchFilter = new OLECHAR[dwLength];

    //  Add the filter.
    swprintf_s(pszSearchFilter, dwLength, L"(&(objectClass=user)(objectCategory=person)%s)", stcfg.pszFilter);
    //swprintf_s(pszSearchFilter, dwLength, L"(&(objectClass=user)(objectCategory=person)(|(memberOf:1.2.840.113556.1.4.1941:=cn=TopGroup,DC=smexdvp,DC=com)(memberOf:1.2.840.113556.1.4.1941:=cn=BRPGroup,cn=users,DC=smexdvp,DC=com)))");        
    //  Specify subtree search.
    ADS_SEARCHPREF_INFO SearchPrefs[2];
    SearchPrefs[0].dwSearchPref = ADS_SEARCHPREF_SEARCH_SCOPE;
    SearchPrefs[0].vValue.dwType = ADSTYPE_INTEGER;
    SearchPrefs[0].vValue.Integer = ADS_SCOPE_SUBTREE;
    
    SearchPrefs[1].dwSearchPref = ADS_SEARCHPREF_PAGESIZE;
    SearchPrefs[1].vValue.dwType = ADSTYPE_INTEGER;
    SearchPrefs[1].vValue.Integer = stcfg.dwPageSize;
    DWORD dwNumPrefs = (stcfg.bPageEnable) ? 2 : 1;
    

    //  COL for iterations.
    LPOLESTR pszColumn = NULL;
    ADS_SEARCH_COLUMN col;
    HRESULT hr = S_OK;

    //  Interface Pointers
    IADs  *pObj = NULL;
    IADs  * pIADs = NULL;

    //  Search handle.
    ADS_SEARCH_HANDLE hSearch = NULL;

    //  Set search preference.
    hr = pContainerToSearch->SetSearchPreference(SearchPrefs, dwNumPrefs);
    if (FAILED(hr))
        return hr;


    LPOLESTR *pszPropertyList = NULL;
    //LPOLESTR pszNonVerboseList[] = { L"name",L"distinguishedName" };
    LPOLESTR *pszNonVerboseList = NULL;
    wprintf(L"call split func to split %s \n", stcfg.pszAttriArr);
    DWORD dwAttriNum = splitString(stcfg.pszAttriArr, &pszNonVerboseList);
    wprintf(L"query %d attr, which are --------------------\n", dwAttriNum);
    for (DWORD idx = 0; idx < dwAttriNum; idx++)
    {
        wprintf(L"%s\t", pszNonVerboseList[idx]);
    }
    wprintf(L"\n");

    //LPOLESTR szAttriValue = new OLECHAR[MAX_PATH];
    //LPOLESTR szDN = new OLECHAR[MAX_PATH];
    VARIANT varDate;
    VariantInit(&varDate);

    int iCount = 0;


    wprintf(L"-------ExecuteSearch start------------\n");

    if (!bIsVerbose)
    {
        //  Return non-verbose list properties only.
        hr = pContainerToSearch->ExecuteSearch(pszSearchFilter,
            pszNonVerboseList,
            dwAttriNum,
            &hSearch
        );
    }
    else
    {
        if (!pszPropertiesToReturn)
        {
            //  Return all properties.
            hr = pContainerToSearch->ExecuteSearch(pszSearchFilter,
                NULL,
                (DWORD)-1,
                &hSearch
            );
        }
        else
        {
            //  Specified subset.
            pszPropertyList = pszPropertiesToReturn;
            //  Return specified properties.
            hr = pContainerToSearch->ExecuteSearch(pszSearchFilter,
                pszPropertyList,
                sizeof(pszPropertyList) / sizeof(LPOLESTR),
                &hSearch
            );
        }
    }
    wprintf(L"-------ExecuteSearch done------------\n");
    if (SUCCEEDED(hr))
    {
        //  Call IDirectorySearch::GetNextRow() to retrieve the next data row.
        hr = pContainerToSearch->GetFirstRow(hSearch);
        if (SUCCEEDED(hr))
        {
            while (hr != S_ADS_NOMORE_ROWS)
            {
                //  Keep track of count.
                iCount++;
                if (bIsVerbose)
                    wprintf(L"----------------------------\n");
                //  Loop through the array of passed column names,
                //  print the data for each column.
                wprintf(L"---------iCount=%d-------------------\n", iCount);
                while (pContainerToSearch->GetNextColumnName(hSearch, &pszColumn) != S_ADS_NOMORE_COLUMNS)
                {
                    hr = pContainerToSearch->GetColumn(hSearch, pszColumn, &col);
                    if (SUCCEEDED(hr))
                    {
                        //  Print the data for the column and free the column.
                        if (bIsVerbose)
                        {
                            //  Get the data for this column.
                            DisplayQueryResult(col, pszColumn, varDate);
                        }
                        else
                        {

                            //  Verbose handles only the two single-valued attributes: cn and ldapdisplayname,
                            //  so this is a special case.
                            //wcscpy_s(szAttriValue, MAX_PATH-1, col.pADsValues->CaseIgnoreString);
                            DisplayQueryResult(col, pszColumn, varDate);

                            //if (0 == wcscmp(L"distinguishedName", pszColumn))
                            //{
                            //    wcscpy_s(szDN, MAX_PATH-1, col.pADsValues->CaseIgnoreString);
                            //}

                        }
                        pContainerToSearch->FreeColumn(&col);
                    }
                    FreeADsMem(pszColumn);
                }
                //if (!bIsVerbose)
                //    wprintf(L"%s\n  DN: %s\n\n", szName, szDN);
                //  Get the next row.
                hr = pContainerToSearch->GetNextRow(hSearch);
                wprintf(L"-------------GetNextRow---------------------\n");
            }

        }
        //  Close the search handle to cleanup.
        pContainerToSearch->CloseSearchHandle(hSearch);
    }
    if (SUCCEEDED(hr) && 0 == iCount)
        hr = S_FALSE;


    //delete[] szAttriValue;
    //delete[] szDN;

    delete[] pszSearchFilter;
    freesplitArr(pszNonVerboseList, dwAttriNum);
    return hr;
}