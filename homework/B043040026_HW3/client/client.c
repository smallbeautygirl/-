#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <netinet/in.h> //Internet Protocol family, ex: sin_family, sin_port, ..., ect
#include <sys/socket.h>
#include <arpa/inet.h> //for inet_addr()
#include <math.h>
#include <unistd.h> //write(.)
#define SIZE 512

/*require (1.socket() 2.connect() 3.write())build up a TCP client*/
int mwrite(int sockfd, const void *buf, size_t len);
void split(char *input, char split_word[3][64]);

int main(void){
    struct sockaddr_in srv;
    struct sockaddr_in cli;
    int nbytes=0;
    int fd = -1;
    int server_port = 0;
    char* server_ip = NULL;

    while(1){
        char input[64]={'\0'};//the user's input
        char split_word[4][64]={'\0'};

        printf("$");
        fgets(input,64,stdin);
        split(input,split_word);

        if(strcmp(split_word[0],"connect")==0){
            fd = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP); //AF_INET是指用IPv4 , SOCK_STREAM select the TCP protocol
            /*socket procedure*/
            if (fd < 0)
            {
                perror("socket error");
                exit(1); //非正常運行檔至退出程序
            }

            server_ip = split_word[1];
            server_port = atoi(split_word[2]);
            /*connect procedure*/
            /* connect: use the Internet address family */
            srv.sin_family = AF_INET;
            /* connect: socket ‘fd’ to port */
            srv.sin_port = htons(server_port);
            /* connect: connect to IP address */
            srv.sin_addr.s_addr = inet_addr(server_ip); //inet_addr() 是將有.的ip轉為二進位
            if (connect(fd, (struct sockaddr *)&srv, sizeof(srv)) < 0)
            {
                perror("connect error");
                exit(1);
            }

            printf("The server with IP \"%s\" has accepted your connection\n", split_word[1]);
        }
        else if(strcmp(split_word[0],"chat")==0){
            if(fd == -1){
                printf("Please connect first\n");
            }
            else{
                write(fd,split_word[3],sizeof(split_word[3]));//傳使用者名稱
                
            }

        }
    }
    return 0;
}

int mwrite(int sockfd, const void *buf, size_t len)
{
    int nbytes = 0;
    int size = len;

    while ((nbytes = write(sockfd, buf, len)) > 0)
    {
        buf += nbytes;
        len -= nbytes;
    }
    if (nbytes < 0)
    {
        return -1; /* fail to read */
    }
    else if (len == 0)
    {
        return size; /* success to read all data */
    }
    else if (len != 0)
    {
        return 0; /* socket is closed, read 0 bytes. */
    }
}

void split(char *input, char split_word[4][64])
{
    int i = 0, j = 0, k = 0;
    // remove the end of line '\n' charactor
    input[strlen(input) - 1] = '\0';
    while (input[i] != '\0')
    {
        if (input[i] != ' ')
        {
            split_word[j][k] = input[i];
            k++;
        }
        else
        {
            k = 0;
            j++;
        }
        i++;
    }
}