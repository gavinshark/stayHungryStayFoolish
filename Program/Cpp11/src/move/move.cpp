// move.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <iostream>
#include <utility>

int i = 101, j = 101;

int foo() { return i; }
int&& bar() { return std::move(i); }
void set(int&& k) { k = 102; }
int main()
{
    foo();
    std::cout << i << std::endl;
    set(bar());
    std::cout << i << std::endl;
}

