#include "stdafx.h"
#include "csapp.h"

#define CGI_BIN "cgi-bin.exe"

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
	char hostname[MAXLINE]={'\0'}, port[MAXLINE]={'\0'};
	socklen_t clientlen;
	struct sockaddr_storage clientaddr;
	memset(&clientaddr, 0, sizeof(sockaddr_storage));

	/*check command-line args*/
	if (argc != 2)
	{
		fprintf(stderr, "usage: %s <port>\n", argv[0]);
		exit(1);
	}

	listenfd = open_listenfd(argv[1]);
	fprintf(stdout, "start to listen at port: %s\n", argv[1]);

	while (1)
	{
		clientlen = sizeof(clientaddr);
		connfd = accept(listenfd, (SA *)&clientaddr, &clientlen);
		getnameinfo((SA *)&clientaddr, clientlen, hostname, MAXLINE, port, MAXLINE, 0);
		printf("Accepted connection from (%s, %s)\n", hostname, port);
		doit(connfd);
		closesocket(connfd);
	}
	WSACleanup();

	while(TRUE){}
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
	if (strcmp(method, "GET"))
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
		if (!(S_ISREG(sbuf.st_mode)))// || !(S_IRUSR & sbuf.st_mode))
		{
			clienterror(fd, method, "403", "Forbidden", "Tiny could not read this file");
			return;
		}
		serve_static(fd, filename, sbuf.st_size);
	}
	else
	{
		/*Serve dynamic content*/
		if (!(S_ISREG(sbuf.st_mode)))// || !(S_IXUSR & sbuf.st_mode)))
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
	sprintf(buf, "Content-length: %d\r\n\r\n", (int)strlen(body));
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
		ptr = strstr(uri, "?");
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
	FILE * srcfd;
	char srcp[MAXBUF], filetype[MAXLINE], buf[MAXBUF];

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
	srcfd = fopen(filename, "r");
	fread(srcp, 1, sizeof(srcp)-1, srcfd);
	fclose(srcfd);
	rio_writen(fd, srcp, filesize);
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

	
	//1. create pipe to redirect child stdout
	SECURITY_ATTRIBUTES saAttr = {0};
	saAttr.nLength = sizeof(SECURITY_ATTRIBUTES);
	saAttr.bInheritHandle = TRUE;
	saAttr.lpSecurityDescriptor = NULL;

	HANDLE childOut_Read, childOut_Write;
	BOOL bret = CreatePipe(&childOut_Read, &childOut_Write, &saAttr, 0);
	if (FALSE == bret)
	{
		wprintf(L"create pipe failed and the Error Code is %d", GetLastError());
	}
	bret = SetHandleInformation(childOut_Read, HANDLE_FLAG_INHERIT, 0);
	if (FALSE == bret)
	{
		wprintf(L"SetHandleInformation failed and the Error Code is %d", GetLastError());
	}

	STARTUPINFOA si ={sizeof(si)};
	ZeroMemory(&si, sizeof(STARTUPINFOA));
	si.cb = sizeof(STARTUPINFOA);
	si.hStdError = childOut_Write;
	si.hStdOutput = childOut_Write;
	si.dwFlags |= STARTF_USESTDHANDLES;
	//2. use environment variable as input parameters to child process
	char szEnv[MAXBUF];
	sprintf(szEnv,"QUERY_STRING=%s", cgiargs);
	/*
	Note that an ANSI environment block is terminated by two zero bytes: one for the last string, one more to terminate the block.
	A Unicode environment block is terminated by four zero bytes: two for the last string, two more to terminate the block.
	*/
	size_t sT= strlen(szEnv);
	szEnv[sT+1] = '\0';


	PROCESS_INFORMATION pi;    
	ZeroMemory(&pi, sizeof(pi));
	char szCmdLine[MAXLINE] = {'\0'};
	sprintf(szCmdLine, "%s", CGI_BIN);
	bret = CreateProcessA(NULL,
		szCmdLine,
		NULL,
		NULL,
		TRUE,
		0,
		(void *)szEnv,
		NULL,
		&si,
		&pi
		);
	if (!bret)
	{
		wprintf(L"CreateProcess Failed and Get Last Error is %d", GetLastError());
	}
	//3.send the child response to web
	CloseHandle(childOut_Write);
	/*Return first part of HTTP response*/
	sprintf(buf, "HTTP/1.0 200 OK\r\n");
	rio_writen(fd, buf, strlen(buf));
	sprintf(buf, "Server: Tiny Web Server\r\n");
	rio_writen(fd, buf, strlen(buf));

	while (TRUE)
	{
		char szBuffer[MAXBUF] = {'\0'};
		DWORD BytesRead = 0;
		int flag = ReadFile(childOut_Read, szBuffer, MAXBUF, &BytesRead, NULL);
		if (!flag || (0 == BytesRead))
		{
			break;
		}
		rio_writen(fd, szBuffer, BytesRead);
	}
	//4.close handle
	WaitForSingleObject(pi.hProcess, INFINITE);
	CloseHandle ( pi.hProcess );
	CloseHandle ( pi.hThread );
}