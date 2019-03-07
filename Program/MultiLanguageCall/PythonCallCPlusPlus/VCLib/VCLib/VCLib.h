#pragma once
// The following ifdef block is the standard way of creating macros which make exporting 
// from a DLL simpler. All files within this DLL are compiled with the EXPORT_DLL_EXPORT
// symbol defined on the command line. this symbol should not be defined on any project
// that uses this DLL. This way any other project whose source files include this file see 
// EXPORT_DLL_API functions as being imported from a DLL, whereas this DLL sees symbols
// defined with this macro as being exported.
#ifndef EXPORT_DLL_EXPORT
#define EXPORT_DLL_API	extern "C" __declspec(dllimport) 
#else
#define EXPORT_DLL_API	extern "C" __declspec(dllexport) 
#endif

//1. C style function call
EXPORT_DLL_API int add(int a, int b);

//2. class export
class CFoo {
public:
    int multiply(int a, int b);
private:
    int m_ia;
};

EXPORT_DLL_API CFoo* CFoo_new();
EXPORT_DLL_API int CFoo_multiply(CFoo*pFoo, int a, int b);
EXPORT_DLL_API void CFoo_delele(CFoo*pFoo);
