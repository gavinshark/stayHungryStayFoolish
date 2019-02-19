#pragma once

#include "stdafx.h"
#include <objbase.h>
#include <wchar.h>
#include <activeds.h>
#include <sddl.h>

#include <Winldap.h>
#pragma comment (lib, "Wldap32.lib")


#include <comdef.h>

typedef struct _CfgStruct
{
    int iCycleTimes;
    DWORD dwPageSize;
    bool bPageEnable;
    LPOLESTR pszFilter;
    LPOLESTR pszAttriArr;
}CfgStruct;

HRESULT FindUsers(IDirectorySearch *pContainerToSearch,  //  IDirectorySearch pointer to the container to search.
    LPOLESTR *pszPropertiesToReturn, //  Properties to return for user objects found.
                                     //  NULL returns all set properties.
    BOOL bIsVerbose, //  TRUE indicates that display all properties for the found objects.
    CfgStruct stcfg
);

int ReadCfg(CfgStruct & stCfg);
void freesplitArr(LPOLESTR pstroutPut[], DWORD dwlength);
DWORD splitString(LPOLESTR pstrinput, LPOLESTR **pstroutPut);
void DisplayQueryResult(ADS_SEARCH_COLUMN &col, const LPOLESTR pszColumn, VARIANT &varDate);
