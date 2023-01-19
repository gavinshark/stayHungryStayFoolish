#include<iostream>
#include<stdio.h>
#include<Winsock2.h>
#include<fstream>

using namespace std;

int main()
{

    WORD wsa = MAKEWORD(2,2);
    //这里声明了winsock的版本2.2
    //1.1版本只支持TCP/IP协议
    //2.0版本支持多协议。
    //2.0版有兼容性
    //任何使用1.1版的源代码、二进制文件、应用程序都可以不加修改地在2.0规范下使用
     WSADATA wsaData;
     //WSADATA结构体中主要包含了系统所支持的Winsock版本信息
     if(WSAStartup(wsa, &wsaData)!=0)
    {
        cout<<"初始化失败"<<endl;   //这进行初始化
        return 0;
    }
    //创建套接字
    SOCKET s_server = socket(AF_INET, SOCK_STREAM, 0);
    //AF_INET   面向网络的  IPV4
    //AF_INET6用于第6版因特网协议（IPv6）寻址
    //SOCK_STREAM   TCP链接   面向链接    SOCK_DGRAM 无连接 UDP
    if(s_server==INVALID_SOCKET) //INVALID_SOCKET是-1 错误标志
    {
        cout<<"socket创建失败"<<endl;
        return 0;
    }
    //这里配置server配置信息
    sockaddr_in server_addr;    //创建sockaddr_in结构体
    server_addr.sin_family = AF_INET;   //IPV4协议
    server_addr.sin_port = htons(8888);     //本地端口8888
    server_addr.sin_addr.S_un.S_addr = INADDR_ANY;   //设置地址 监听本地端口
    //利用bind函数将socket和配置信息绑定
    //bind通常和下面的listen配套使用 处于被动链接中泰
    if   (  bind( s_server,(SOCKADDR *)&server_addr,sizeof(SOCKADDR)) ==SOCKET_ERROR )
    {
        //socket和配置绑定
        cout<<"ERROR bind!!"<<endl;
        WSACleanup();
    }

    if(listen( s_server,5 )<0)
    {
        cout<<"listen failed"<<endl;
    }
    cout<<"listen********************"<<endl;
    sockaddr_in clinet_addr;   //用于获取客户端地址端口信息 用于回传
    SOCKET s_accept;
    //这里定义了一个用于接收的sockaddr_in名字为s_accept。用于接收客户端的地址信息和端口信息，用于回传。
    int len=sizeof(SOCKADDR);
    s_accept = accept(s_server,(SOCKADDR *)&clinet_addr,&len);
    //在这里阻塞 挂起等待
    
    if( s_accept ==SOCKET_ERROR  )  //
    {
        cout<<"connect error"<<endl;
        return 0;
    }
    cout<<"connection is OK;ready to accept"<<endl;
    char recv_buf[200];
    char send_buf[200];
    //两个buff缓冲区，用于缓存接收字符和发送字符。
    while(true)
    {
        memset(recv_buf,0,sizeof(recv_buf));
        int recv_len = 0;
        while (strlen(recv_buf) == 0){
            recv_len = recv(s_accept,recv_buf,sizeof(recv_buf)-1,0);
            //这里 即使链接断开 也能继续监听 服务端不关闭
            if(recv_len<0)
            {
                cout<<"listen********************"<<endl;
                s_accept = accept(s_server,(SOCKADDR *)&clinet_addr,&len);
                //在这里阻塞 挂起等待
                continue;
                if( s_accept ==SOCKET_ERROR  )  //
                {
                    cout<<"connect error"<<endl;
                    return 0;
                }
            }
        }
        cout<<"client message:"<<recv_buf<<endl;

        memset(send_buf,0,sizeof(send_buf));
        cout<<"please input server response:"<<endl;        
        while (strlen(send_buf) == 0 )
        {
            cin.getline(send_buf, sizeof(send_buf)-1);            
        }
        send(s_accept,send_buf,sizeof(send_buf),0);
        cout<<"send success, wait the client response"<<endl;
    }
    closesocket(s_server);
	closesocket(s_accept);
	//释放DLL资源
	WSACleanup();
	return 0;
}

