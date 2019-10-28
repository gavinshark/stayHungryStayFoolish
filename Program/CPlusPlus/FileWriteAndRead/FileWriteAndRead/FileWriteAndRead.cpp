// FileWriteAndRead.cpp : 定义控制台应用程序的入口点。
//
#include "StdAfx.h"
#include <iostream>
#include <fstream>
#include <string>

void stopUntilEnter(){
	while (getchar() != '\n')
	{
	}
}

int _tmain()
{
	std::wstring filename = L"test.txt";
	std::wfstream s(filename, std::ios_base::in | std::ios_base::out);
	if(!s.is_open()){
		std::wcout << L"failed to open" << filename << std::endl;
	} else {
		//s.seekp(0);		
		std::wstring str;
		std::wcout<<"skip space"<<std::endl;
		while (!s.eof())
		{
			stopUntilEnter();
			s >> str;
			std::wcout << "read result: " << str <<std::endl;
		}

		if(false){
			s.clear();
			s.seekp(std::ios::beg);
			std::wcout<<"Do not skip space"<<std::endl;
			const int LINE_LENGTH = 100;
			wchar_t cstr[LINE_LENGTH];
			while (s.getline(cstr,LINE_LENGTH-1))
			{
				std::wcout << "read result: " << cstr <<std::endl;
			}
		}
	}

	system("pause");
	
	return 0;
}

