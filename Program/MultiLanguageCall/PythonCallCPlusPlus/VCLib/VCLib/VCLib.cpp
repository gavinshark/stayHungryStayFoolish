// VCLib.cpp : Defines the exported functions for the DLL application.
//

#include "stdafx.h"
#include "stdio.h"
#include "VCLib.h"
// must use release version and x64

int add(int a, int b) {
    return (a + b);
}

//2. class export
int CFoo:: multiply(int a, int b) {
        return (a * b);
    }

CFoo* CFoo_new() { wprintf(L"constructor is called.\n");return new CFoo; }
int CFoo_multiply(CFoo*pFoo, int a, int b) { return pFoo->multiply(a, b); }
void CFoo_delele(CFoo*pFoo) { wprintf(L"de-constructor is called.\n");delete pFoo; }
