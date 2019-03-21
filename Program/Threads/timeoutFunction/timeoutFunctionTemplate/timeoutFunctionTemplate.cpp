#include "stdafx.h"
#include <iostream>
#include <future>
#include <chrono>
#include <string>
#include <windows.h>
using namespace std;

std::string current_time() {
    time_t now = time(NULL);
    struct tm tstruct;
    char buf[40];
    localtime_s(&tstruct, &now);
    //format: HH:mm:ss
    strftime(buf, sizeof(buf), "%X", &tstruct);
    return buf;
}

template <typename F, typename... Args>
auto really_async2(F&& f, Args&&... args)
-> std::future<typename std::result_of<F(Args...)>::type>
{
    using _Ret = typename std::result_of<F(Args...)>::type;
    auto _func = std::bind(std::forward<F>(f), std::forward<Args>(args)...);
    std::packaged_task<_Ret()> tsk(std::move(_func));
    auto _fut = tsk.get_future();
    std::thread thd(std::move(tsk));
    thd.detach();
    return _fut;
}

int AsyncFunction(string strInput)
{
    fprintf(stdout, "AsyncFunction start and input string is %s at %s\n", strInput.c_str(), current_time().c_str());
    Sleep(1*1000);
    fprintf(stdout, "AsyncFunction end at %s\n", current_time().c_str());
    return 1;
}

void AsyncTest(string strInput)
{
    fprintf(stdout, "AsyncTest Begin at %s\n", current_time().c_str());
    std::future_status status;
    //std::future<int> future_test = really_async2(AsyncFunction);      // method 1 , but std::result_of<F(Args...)>::type is legacy in C++ 17
    std::packaged_task<int(string)> tsk(AsyncFunction);                 // method 2 
    std::future<int> future_test = tsk.get_future();
    std::thread thd(std::move(tsk), strInput);
    thd.detach();
    status = future_test.wait_for(std::chrono::milliseconds(2*1000));
    if (std::future_status::timeout == status)
    {
        fprintf(stdout, "AsyncTest timeout at %s\n", current_time().c_str());
    }
    else if (std::future_status::ready == status)
    {
        fprintf(stdout, "AsyncTest ready and result is %d at %s\n", future_test.get(), current_time().c_str());
    }
    else
    {
        fprintf(stderr, "AsyncTest Other Error: %d at %s\n", status, current_time().c_str());
    }
    fprintf(stdout, "AsyncTest End at %s\n", current_time().c_str());
}
int main()
{
    int abc = 1;
    string str = "Hello";
    while (true) {
        fprintf(stdout, "Main start at %s\n", current_time().c_str());
        AsyncTest(str);
        fprintf(stdout, "Main end at %s\n", current_time().c_str());
        break;
    }
    while (1) {

    }
    return 0;
}