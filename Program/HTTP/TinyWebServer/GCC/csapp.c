#include "csapp.h"

int open_listenfd(char *port){
    struct addrinfo hints, *listp, *p;
    int listenfd, optval=1;

    memset(&hints, 0, sizeof(struct addrinfo));
    hints.ai_socktype = SOCK_STREAM;
    hints.ai_flags = AI_PASSIVE | AI_ADDRCONFIG;
    hints.ai_flags |= AI_NUMERICSERV;
    getaddrinfo(NULL, port, &hints, &listp);

    for(p=listp; p; p=p->ai_next){
        if ((listenfd = socket(p->ai_family, p->ai_socktype, p->ai_protocol)) < 0) continue;

        setsockopt(listenfd, SOL_SOCKET, SO_REUSEADDR, (const void *)&optval, sizeof(int));

        if(bind(listenfd, p->ai_addr, p->ai_addrlen) == 0) break;

        close(listenfd);
    }

    freeaddrinfo(listp);
    if(!p) return -1;

    if(listen(listenfd, LISTENQ) < 0){
        close(listenfd);
        return -1;
    }

    return listenfd;
}

ssize_t rio_readn(int fd, void *usrbuf, size_t n) 
{
    size_t nleft = n; //剩下未读字符数
    ssize_t nread;
    char *bufp = usrbuf;

    while (nleft > 0) {
    if ((nread = read(fd, bufp, nleft)) < 0) {
        if (errno == EINTR)  //被信号处理函数中断
        nread = 0;      //本次读到0个字符，再次读取
        else
        return -1;      //出错，errno由read设置
    } 
    else if (nread == 0) //读取到EOF
        break;              
    nleft -= nread; //剩下的字符数减去本次读到的字符数
    bufp += nread;  //缓冲区指针向右移动
    }
    //返回实际读取的字符数
    return (n - nleft);         /* return >= 0 */
}

ssize_t rio_writen(int fd, void *usrbuf, size_t n) 
{
    size_t nleft = n;
    ssize_t nwritten;
    char *bufp = usrbuf;

    while (nleft > 0) {
    if ((nwritten = write(fd, bufp, nleft)) <= 0) {
        if (errno == EINTR)  
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

    while (rp->rio_cnt <= 0) {  //缓冲区为空，调用read填充
    rp->rio_cnt = read(rp->rio_fd, rp->rio_buf, 
               sizeof(rp->rio_buf));
    if (rp->rio_cnt < 0) {
        if (errno != EINTR) /* Interrupted by sig handler return */
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
    char *bufp = usrbuf;
    
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
    char c, *bufp = usrbuf;

    for (n = 1; n < maxlen; n++) { 
        if ((rc = rio_read(rp, &c, 1)) == 1) {
        *bufp++ = c;
        if (c == '\n') {
                n++;
            break;
            }
    } else if (rc == 0) {
        if (n == 1)
        return 0; //第一次读取就到了EOF
        else
        break;    //读了一些数据后遇到EOF
    } else
        return -1;    /* Error */
    }
    *bufp = 0;
    return n-1;
}