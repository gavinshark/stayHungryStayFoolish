#ifndef _CSAPP_H
#define _CSAPP_H

#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <winsock2.h>
#pragma comment(lib, "ws2_32.lib")

#include <stdio.h>
#include <windows.h>
#include <string.h>
#include <stdlib.h>
#include <ws2tcpip.h>

#define MAXLINE 2048
#define MAXBUF  10240
#define LISTENQ 1024

#define S_ISREG(m) (((m) & 0170000) == (0100000)) 
#define S_ISDIR(m) (((m) & 0170000) == (0040000))

int open_listenfd(char *port);


#define RIO_BUFFERSIZE 8192
typedef struct{
	int rio_fd;
	int rio_cnt;
	char *rio_bufptr;
	char rio_buf[RIO_BUFFERSIZE];
}rio_t;

typedef struct sockaddr SA;
typedef unsigned int ssize_t;

ssize_t rio_readn(int fd, void *usrbuf, size_t n);
ssize_t rio_writen(int fd, void *usrbuf, size_t n);
void rio_readinitb(rio_t *rp, int fd);
ssize_t rio_readnb(rio_t *rp, void *usrbuf, size_t n);
ssize_t rio_readlineb(rio_t *rp, void *usrbuf, size_t maxlen);

#endif