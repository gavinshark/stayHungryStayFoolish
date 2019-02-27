#include "csapp.h"

int main(){
	char *buf, *p;
	char arg1[MAXLINE]={'\0'}, arg2[MAXLINE]={'\0'}, content[MAXBUF]={'\0'};
	int n1 = 0, n2 = 0;
	
	if((buf = getenv("QUERY_STRING")) != NULL){
		p = strchr(buf, '&');
		*p = '\0';
		strcpy(arg1, buf);
		strcpy(arg2, p+1);
		n1 = atoi(arg1);
		n2 = atoi(arg2);		
	}
	
	sprintf(content, "QUERY_STRING=%s", buf);
	sprintf(content, "Welcome to add.com: ");
	sprintf(content, "%s<p>The Internet addition portal.</p>\r\n", content);
	sprintf(content, "%s<p>The answer is: %d + %d = %d</p>\r\n", content, n1, n2, n1+n2);
	
	printf("Connection: close\r\n");
	printf("Content-length: %d\r\n", (int)strlen(content));
	printf("Content-type: text/html\r\n\r\n");
	printf("%s", content);
	fflush(stdout);
	
	exit(0);
}