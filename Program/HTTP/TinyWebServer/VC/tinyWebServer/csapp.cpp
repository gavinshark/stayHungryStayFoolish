#include "StdAfx.h"
#include "csapp.h"

int open_listenfd(char *port){
	struct addrinfo hints, *listp, *p;
	int listenfd, optval=1;
	DWORD dwRetval = 0;

	WSADATA wsaData;
	int iResult = WSAStartup(MAKEWORD(2, 2), &wsaData);
	if (iResult != 0) {
		printf("WSAStartup failed: %d\n", iResult);
		return -1;
	}
	memset(&hints, 0, sizeof(struct addrinfo));
	hints.ai_socktype = SOCK_STREAM;
	hints.ai_flags = AI_PASSIVE | AI_ADDRCONFIG;
	hints.ai_flags |= AI_NUMERICSERV;
	dwRetval = getaddrinfo(NULL, port, &hints, &listp);
	if ( dwRetval != 0 ) {
		printf("getaddrinfo failed with error: %d\n", dwRetval);
		WSACleanup();
		return -1;
	}
	
	for(p=listp; p; p=p->ai_next){
		if (p->ai_family != AF_INET) // add this line to accept IPV4 only
		{
		    continue;
		}
		if ((listenfd = socket(p->ai_family, p->ai_socktype, p->ai_protocol)) < 0) continue;

		setsockopt(listenfd, SOL_SOCKET, SO_REUSEADDR, (const char *)&optval, sizeof(int));

		if(bind(listenfd, p->ai_addr, p->ai_addrlen) == 0) 
		{
			printf("Server Configuration:\nai_family=%d, ai_addr=%d, ai_protocol=%d\n\n", p->ai_family, p->ai_addr, p->ai_protocol);
			break;
		}

		WSACleanup();
	}

	freeaddrinfo(listp);
	if(!p) return -1;

	if(listen(listenfd, LISTENQ) < 0){
		WSACleanup();
		return -1;
	}

	return listenfd;
}

ssize_t rio_readn(int fd, void *usrbuf, size_t n) 
{
	size_t nleft = n; 
	ssize_t nread;
	char *bufp = (char *)usrbuf;

	while (nleft > 0) {
		if ((nread = recv(fd, bufp, nleft, 0)) < 0) {
			if (WSAGetLastError() == WSAEINTR)  
				nread = 0;
			else
				return -1;      
		} 
		else if (nread == 0) 
			break;              
		nleft -= nread; 
		bufp += nread;  
	}
	//返回实际读取的字符数
	return (n - nleft);         /* return >= 0 */
}

ssize_t rio_writen(int fd, void *usrbuf, size_t n) 
{
	size_t nleft = n;
	ssize_t nwritten;
	char *bufp = (char *)usrbuf;

	while (nleft > 0) {
		if ((nwritten = send(fd, bufp, nleft, 0)) <= 0) {
			if (WSAGetLastError() == WSAEINTR)  
				nwritten = 0;    
			else
				return -1;       
		}
		nleft -= nwritten;
		bufp += nwritten;
	}
	return n;
}

void rio_readinitb(rio_t *rp, int fd) 
{
	rp->rio_fd = fd;  
	rp->rio_cnt = 0;  
	rp->rio_bufptr = rp->rio_buf;
}

static ssize_t rio_read(rio_t *rp, char *usrbuf, size_t n)
{
	int cnt;

	while (rp->rio_cnt <= 0) {
		rp->rio_cnt = recv(rp->rio_fd, rp->rio_buf, 
			sizeof(rp->rio_buf), 0);
		if (rp->rio_cnt < 0) {
			if (WSAGetLastError() == WSAEINTR) /* Interrupted by sig handler return */
				return -1;
		}
		else if (rp->rio_cnt == 0)  /* EOF */
			return 0;
		else 
			rp->rio_bufptr = rp->rio_buf; /* Reset buffer ptr */
	}

	/* Copy min(n, rp->rio_cnt) bytes from internal buf to user buf */
	cnt = n;          
	if (rp->rio_cnt < n)   
		cnt = rp->rio_cnt;
	memcpy(usrbuf, rp->rio_bufptr, cnt);
	rp->rio_bufptr += cnt;
	rp->rio_cnt -= cnt;
	return cnt;
}

ssize_t rio_readnb(rio_t *rp, void *usrbuf, size_t n) 
{
	size_t nleft = n;
	ssize_t nread;
	char *bufp = (char *)usrbuf;

	while (nleft > 0) {
		if ((nread = rio_read(rp, bufp, nleft)) < 0) 
			return -1;          /* errno set by read() */ 
		else if (nread == 0)
			break;              /* EOF */
		nleft -= nread;
		bufp += nread;
	}
	return (n - nleft);         /* return >= 0 */
}

ssize_t rio_readlineb(rio_t *rp, void *usrbuf, size_t maxlen) 
{
	int n, rc;
	char c, *bufp = (char *)usrbuf;

	for (n = 1; n < maxlen; n++) { 
		if ((rc = rio_read(rp, &c, 1)) == 1) {
			*bufp++ = c;
			if (c == '\n') {
				n++;
				break;
			}
		} else if (rc == 0) {
			if (n == 1)
				return 0; //reach EOF when first time reading
			else
				break;    //reach EOF after reading some characters
		} else
			return -1;    /* Error */
	}
	*bufp = 0;
	return n-1;
}