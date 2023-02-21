#include<iostream>
#include<stdio.h>
#include<Winsock2.h>
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
        cout<<"WSAStartup failed"<<endl;   //这进行初始化
        return 0;
    }
    SOCKET s_server = socket(AF_INET, SOCK_STREAM, 0);
    if(s_server==INVALID_SOCKET)
    {
        cout<<"socket init failed"<<endl;
        return 0;
    }
    sockaddr_in server_addr;
    server_addr.sin_family = AF_INET;   //IPV4协议
    server_addr.sin_port = htons(8888);     //服务器端口
    //这里有改动 写网络地址
    server_addr.sin_addr.S_un.S_addr = inet_addr("127.0.0.1");
    if (connect(s_server, (SOCKADDR *)&server_addr, sizeof(SOCKADDR)) == SOCKET_ERROR) {
		cout << "server connnet fail!!" << endl;
		WSACleanup();
		return 0;
	}
	else {
		cout << "server connected!!" << endl;
	}
    char send_buf[200];
    char accept_buf[200];
    int iResult = 0;
    while(true)
    {
        cout<<"input client message:"<<endl;
        memset(send_buf,0,sizeof(send_buf));
        while (strlen(send_buf) == 0 )
        {
            cin.getline(send_buf, sizeof(send_buf)-1);            
        }        
        
        int res_len = send(s_server,send_buf,sizeof(send_buf),0);
        if(res_len<0)
        {
            cout<<"error"<<endl;
        }
        cout<<"send success, wait the server response"<<endl;
        memset(accept_buf,0,sizeof(accept_buf));
        //while (strlen(accept_buf) == 0)
        {
            iResult = recv(s_server, accept_buf, sizeof(accept_buf)-1, 0);
        }        
        cout<<"server response:"<<accept_buf<<endl;
    }

    closesocket(s_server);
	//释放DLL资源
	WSACleanup();
	return 0;
}

