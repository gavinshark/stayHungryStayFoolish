#include "csapp.h"


void doit(int fd);
void read_requesthdrs(rio_t *rp);
int parse_uri(char *uri, char *filename, char *cgiargs);
void serve_static(int fd, char *filename, int filesize);
void get_filetype(char *filename, char *filetype);
void serve_dynamic(int fd, char *filename, char *cgiargs);
void clienterror(int fd, char *cause, char *errnum, char *shortmsg, char *longmsg);

int main(int argc, char **argv)
{
	int listenfd, connfd;
	char hostname[MAXLINE], port[MAXLINE];
	socklen_t clientlen;
	struct sockaddr_storage clientaddr;

	/*check command-line args*/
	if (argc != 2)
	{
		fprintf(stderr, "usage: %s <port>\n", argv[0]);
		exit(1);
	}

	listenfd = open_listenfd(argv[1]);
	while (1)
	{
		clientlen = sizeof(clientaddr);
		connfd = accept(listenfd, (SA *)&clientaddr, &clientlen);
		getnameinfo((SA *)&clientaddr, clientlen, hostname, MAXLINE, port, MAXLINE, 0);
		printf("Accepted connection from (%s, %s)\n", hostname, port);
		doit(connfd);
		close(connfd);
	}
}

void doit(int fd)
{
	int is_static;
	struct stat sbuf;
	char buf[MAXLINE], method[MAXLINE], uri[MAXLINE], version[MAXLINE];
	char filename[MAXLINE], cgiargs[MAXLINE];
	rio_t rio;

	rio_readinitb(&rio, fd);
	rio_readlineb(&rio, buf, MAXLINE);
	printf("Request headers:\n");
	printf("%s", buf);
	sscanf(buf, "%s %s %s", method, uri, version);
	if (strcasecmp(method, "GET"))
	{
		clienterror(fd, method, "501", "Not implemented", "Tiny does not implement this method");
		return;
	}
	read_requesthdrs(&rio);

	/*Parse URI from GET request*/
	is_static = parse_uri(uri, filename, cgiargs);
	if (stat(filename, &sbuf) < 0)
	{
		clienterror(fd, filename, "404", "Not found", "Tiny could not find this file");
		return;
	}

	if (is_static)
	{
		/*Serve static content*/
		if (!(S_ISREG(sbuf.st_mode)) || !(S_IRUSR & sbuf.st_mode))
		{
			clienterror(fd, method, "403", "Forbidden", "Tiny could not read this file");
			return;
		}
		serve_static(fd, filename, sbuf.st_size);
	}
	else
	{
		/*Serve dynamic content*/
		if (!(S_ISREG(sbuf.st_mode) || !(S_IXUSR & sbuf.st_mode)))
		{
			clienterror(fd, method, "403", "Forbidden", "Tiny could not run the CGI program");
			return;
		}
		serve_dynamic(fd, filename, cgiargs);
	}
}

void clienterror(int fd, char * cause, char * errnum, char * shortmsg, char * longmsg){
	char buf[MAXLINE], body[MAXLINE];

	/*Build the HTTP response body*/
	sprintf(body, "<html><title>Tiny Error</title>");
	sprintf(body, "%s<body bgcolor=""ffffff""\r\n", body);
	sprintf(body, "%s%s: %s\r\n", body, errnum, shortmsg);
	sprintf(body, "%s<p>%s: %s\r\n", body, longmsg, cause);
	sprintf(body, "%s<hr><em>The Tiny Web Server </em>\r\n", body);

	/*Print the HTTP response*/
	sprintf(buf, "HTTP/1.0 %s %s\r\n", errnum, shortmsg);
	rio_writen(fd, buf, strlen(buf));
	sprintf(buf, "Content-type: text/html\r\n");
	rio_writen(fd, buf, strlen(buf));
	sprintf(buf, "Contetn-length: %d\r\n\r\n", (int)strlen(body));
	rio_writen(fd, buf, strlen(buf));
	rio_writen(fd, body, strlen(body));
}

void read_requesthdrs(rio_t *rp){
	char buf[MAXLINE];

	rio_readlineb(rp, buf, MAXLINE);
	printf("%s", buf);
	while(strcmp(buf, "\r\n")){
		rio_readlineb(rp, buf, MAXLINE);
		printf("%s", buf);
	}
	return;
}

int parse_uri(char * uri, char * filename, char * cgiargs){
	char *ptr;

	if(!strstr(uri, "cgi-bin")){
		strcpy(cgiargs, "");
		strcpy(filename, ".");
		strcat(filename, uri);
		if(uri[strlen(uri)-1] == '/'){
			strcat(filename, "home.html");
		}
		return 1;
	}
	else{
		/*Dynamic content*/
		ptr = index(uri, '?');
		if(ptr){
			strcpy(cgiargs, ptr+1);
			*ptr = '\0';
		}
		else
		{
			strcpy(cgiargs, "");
		}
		strcpy(filename, ".");
		strcat(filename, uri);
		return 0;		
	}
}


void serve_static(int fd, char * filename, int filesize){
	int srcfd;
	char *srcp, filetype[MAXLINE], buf[MAXBUF];

	/*Send response headers to client*/
	get_filetype(filename, filetype);
	sprintf(buf, "HTTP/1.0 200 OK\r\n");
	sprintf(buf, "%sServer: Tiny Web Server\r\n", buf);
	sprintf(buf, "%sConnection: close\r\n", buf);
	sprintf(buf, "%sContent-length: %d\r\n", buf, filesize);
	sprintf(buf, "%sContent-type: %s\r\n\r\n", buf, filetype);
	rio_writen(fd, buf, strlen(buf));
	printf("Response headers:\n");
	printf("%s", buf);

	/*Send response body to client*/
	srcfd = open(filename, O_RDONLY, 0);
	srcp = mmap(0, filesize, PROT_READ, MAP_PRIVATE, srcfd, 0);
	close(srcfd);
	rio_writen(fd, srcp, filesize);
	munmap(srcp, filesize);
}

void get_filetype(char *filename, char *filetype){
	if(strstr(filename, ".html")){
		strcpy(filetype, "text/html");
	}else if(strstr(filename, ".gif")){
		strcpy(filetype, "image/gif");
	}else if(strstr(filename, ".png")){
		strcpy(filetype, "image/png");
	}else if(strstr(filename, ".jpg")){
		strcpy(filetype, "image/jpeg");
	}else{
		strcpy(filetype, "text/plain");
	}
}

void serve_dynamic(int fd, char * filename, char * cgiargs){
	char buf[MAXLINE], *emptylist[] = {NULL};

	/*Return first part of HTTP response*/
	sprintf(buf, "HTTP/1.0 200 OK\r\n");
	rio_writen(fd, buf, strlen(buf));
	sprintf(buf, "Server: Tiny Web Server\r\n");
	rio_writen(fd, buf, strlen(buf));

	if(fork() == 0){
		setenv("QUERY_STRING", cgiargs, 1);
		dup2(fd, STDOUT_FILENO);
		execve(filename, emptylist, environ);
	}
	wait(NULL);
}