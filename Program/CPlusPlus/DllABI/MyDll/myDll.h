#pragma once

#if MYDLL_EXPORTS
#define DLL_API	__declspec(dllexport)
#else
#define DLL_API __declspec(dllimport)
#endif

#if MYDLL_EXPORTS
#define CLASS_API __declspec(dllexport)
#else
#define CLASS_API __declspec(dllimport)
#endif



DLL_API int addFunc(int, int);
DLL_API int minusFunc(int, int);

class CLASS_API MyClass {
public:
    int MyFunc();
private:
    int m_i;
};