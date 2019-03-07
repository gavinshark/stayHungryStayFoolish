// VCLib.cpp : Defines the exported functions for the DLL application.
//

#include "stdafx.h"
#include "stdio.h"
// must use release version and x64
#define EXPORT_DLL_API	extern "C" __declspec(dllexport)

//1. C style function call
EXPORT_DLL_API int add(int a, int b);

int add(int a, int b) {
    return (a + b);
}

//2. class export
class CFoo;
class CFoo {
public:
    int multiply(int a, int b) {
        return (a * b);
    }
private:
    int m_ia;
};

EXPORT_DLL_API CFoo* CFoo_new() { wprintf(L"constructor is called.\n");return new CFoo; }
EXPORT_DLL_API int CFoo_multiply(CFoo*pFoo, int a, int b) { return pFoo->multiply(a, b); }
EXPORT_DLL_API void CFoo_delele(CFoo*pFoo) { wprintf(L"de-constructor is called.\n");delete pFoo; }
