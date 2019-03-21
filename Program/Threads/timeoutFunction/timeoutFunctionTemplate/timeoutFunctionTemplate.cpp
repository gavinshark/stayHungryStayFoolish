#include "stdafx.h"
#include <iostream>
#include <future>
#include <chrono>
#include <windows.h>

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

int AsyncFunction()
{
    fprintf(stderr, "AsyncFunction start\n");
    Sleep(3 * 1000);
    fprintf(stderr, "AsyncFunction end\n");
    return 1;
}

void AsyncTest()
{
    fprintf(stderr, "AsyncTest Begin\n");
    std::future_status status;
    std::future<int> future_test = really_async2(AsyncFunction);
    status = future_test.wait_for(std::chrono::milliseconds(100));
    if (std::future_status::timeout == status)
    {
        fprintf(stderr, "AsyncTest timeout\n");
    }
    else if (std::future_status::ready == status)
    {
        fprintf(stderr, "AsyncTest ready\n");
    }
    else
    {
        fprintf(stderr, "AsyncTest Other Error: %d\n", status);
    }
    fprintf(stderr, "AsyncTest End\n");
}
int main()
{
    int abc = 1;
    while (true) {
        fprintf(stderr, "Main start\n");
        AsyncTest();
        fprintf(stderr, "Main end\n");
    }
    return 0;
}