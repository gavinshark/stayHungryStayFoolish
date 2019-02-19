#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <sys/socket.h>
#include <netdb.h>
#include <stdio.h>
#include <sys/mman.h>
#include <unistd.h>
#include <sys/errno.h>
#include <string.h>
#include <stdlib.h>
//int open_clientfd(char *hostname, char *port);

#define MAXLINE 2048
#define MAXBUF  10240
#define LISTENQ 1024

int open_listenfd(char *port);

extern char **environ; 

#define RIO_BUFFERSIZE 8192
typedef struct{
    int rio_fd;
    int rio_cnt;
    char *rio_bufptr;
    char rio_buf[RIO_BUFFERSIZE];
}rio_t;

typedef struct sockaddr SA;