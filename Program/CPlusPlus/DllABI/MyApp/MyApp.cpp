// MyApp.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include "windows.h"
#include "../MyDll/myDll.h"


int main()
{

    int a = addFunc(1, 2);
    wprintf(L"add 1 and 2 is :%d\n", a);


    int b = minusFunc(33, 11);
    wprintf(L"minus 33 to 11 is :%d\n", b);

    MyClass myObject;
    MyClass * pMyObject = &myObject;
    wprintf(L"myObject: myFunction: %d\n", pMyObject->MyFunc());

    system("pause");
    
    return 0;
}

