// MyDll.cpp : Defines the exported functions for the DLL application.
//

#include "stdafx.h"
#include "myDll.h"


DLL_API int addFunc(int a, int b) {
    return (a + b);
};

DLL_API int minusFunc(int a, int b) {
    return (a - b);
};

int MyClass::MyFunc() {
    int a = 1 + 2;
    return a;
}


