// exception.cpp : 定义控制台应用程序的入口点。
//

#include "stdafx.h"
#include "string"
#include <iostream>
using namespace std;

class MyException{
public:
	MyException(){}

	MyException(char * str){
		msg = str;
	}

	MyException(MyException & rhs){
		msg = rhs.msg;
	}
	
	string msg;
};


class MyClass{
public:
	MyClass(){ wcout<<L"MyClass construct!!"<<endl;}
	~MyClass(){wcout<<L"MyClass deConstruct!"<<endl;}
	void display(){ wcout<<L"this is MyClass"<<endl;}
};


/*
MyClass construct!!
MyClass deConstruct!
my exception is caught
main function end
*/
int _tmain(int argc, _TCHAR* argv[])
{
	try
	{
		MyClass a;
		throw MyException("my exception");
		cout<<"hello my main"<<endl;
		a.display();
	}
	catch (MyException& e)
	{
		cout<< e.msg <<" is caught"<<endl;
	}

	wcout<<L"main function end"<<endl;

	string a;
	cin>>a;

	return 0;
}

