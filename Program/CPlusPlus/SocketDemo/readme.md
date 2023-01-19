## how-to-read
程序说明：https://blog.csdn.net/weixin_43134135/article/details/92080605

## how-to-build
编译环境准备：https://zhuanlan.zhihu.com/p/77645306
编译：
g++ src/server/server.cpp -o release/server.exe -lwsock32
g++ src/client/client.cpp -o release/client.exe -lwsock32

## how-to-run
先在一个cmd或terminal运行server：release/server.exe
再在另一个cmd或terminal运行client：release/client.exe
注：
1. 半双工系统
2. 输入不超过200字符的英文
3. 是否允许访问网络：允许
4. 监听8888端口，注意端口冲突