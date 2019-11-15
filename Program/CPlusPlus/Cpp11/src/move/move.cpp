// move.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <iostream>
#include <utility>

int i = 101, j = 101;

int foo() { return i; }
int&& bar() { return std::move(i); }
void set(int&& k) { k = 102; }


class A {
public:
    A() {
        std::cout << "A()" << std::endl;
    }

    A(int j) {
        std::cout << "A("<< j <<")" << std::endl;
        m_i = j;
    }

    ~A() {
        m_i = 0;
    }

    A(const A & a) {
        std::cout << "A(const A & a)" << std::endl;
        m_i = a.m_i;
    }

    void display() {
        std::cout << m_i << std::endl;
    }

    A(A && a) {
        std::cout << "A(A && a)" << std::endl;
        m_i = a.m_i;
        a.m_i = 0;
    }

private:
    int m_i;
};

A Get() {
    std::cout << "A Get()" << std::endl;
    return A(0);
}


int main()
{
#if 0
    foo();
    std::cout << i << std::endl;
    set(bar());
    std::cout << i << std::endl;
#endif

#if 0
    A a(123);
    std::cout << "a.display()" << std::endl;
    a.display();
    A b(std::move(a));
    std::cout << "b.display()" << std::endl;
    b.display();
    std::cout << "a.display()" << std::endl;
    a.display();
#endif

#if 0
    //complier optimization
    A a(A(13));
    a.display();
    A aa(Get());
    aa.display();
#endif
}

