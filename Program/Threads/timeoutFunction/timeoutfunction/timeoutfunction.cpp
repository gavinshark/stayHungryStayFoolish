// timeoutfunction.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <future>
#include <thread>
#include <chrono>
#include <ctime>
#include "windows.h"
#include <iostream>
#include <string>
#include <time.h>
using namespace std::chrono;
using namespace std;

#define WAIT_FOR_TIME_OUT (1000*1)
#define DELAY_FUNC_DELAY_TIME (1000*4)

std::string current_time() {
    time_t now = time(NULL);
    struct tm tstruct;
    char buf[40];
    localtime_s(&tstruct, &now);
    //format: HH:mm:ss
    strftime(buf, sizeof(buf), "%X", &tstruct);
    return buf;
}

int delayfunc(int input) {
    std::cout << "delayfunc in  => "<< current_time() <<endl;
    Sleep(DELAY_FUNC_DELAY_TIME);
    std::cout << "delayfunc out  => " << current_time() << endl;
    return 12;
}

future<int> future_Query;
int callDelayFunc() {
    std::cout << "callDelayFunc: in =>" << current_time() << endl;

    future_status status;
    future_Query = async(std::launch::async, delayfunc, 10);

    status = future_Query.wait_for(chrono::milliseconds(WAIT_FOR_TIME_OUT));

    if (future_status::timeout == status) {
        std::cout << "callDelayFunc: timeout =>"<< current_time() << endl;
    }
    else if (future_status::ready == status) {
        std::cout << "callDelayFunc: OK =>" << current_time() << endl;
    }
    else {  //future_status::deferred
        std::cout << "callDelayFunc: deferred =>" << current_time() << endl;
    }

    std::cout << "callDelayFunc: out =>" << current_time() << endl;
    return 10;
}


int main()
{
    std::cout << "main: callDelayFunc begin =>" << current_time() << endl;
    callDelayFunc();
    std::cout << "main: callDelayFunc end =>" << current_time() << endl;
    return 0;
}

