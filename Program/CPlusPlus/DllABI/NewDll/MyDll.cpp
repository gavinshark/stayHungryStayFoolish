// MyDll.cpp : Defines the exported functions for the DLL application.
//

#include "stdafx.h"
#include "myDll.h"


int addFunc(int a, int b) {

    return (a + b);
};

int multiFunc(int a, int b) {

    return (a * b);
};

int minusFunc(int a, int b) {
    return (a - b);
};


int divFunc(int a, int b) {
    return (a / b);
};


int MyClass::MyFunc() {
    int a = 1 + 20;
    return a;
}


int MyClass::additionFunc() {
    int a = 1 + 3;
    return a;
}

int MyClass::MyNewFunc(int i) {
    int a = 1 + i;
    return a;
}
