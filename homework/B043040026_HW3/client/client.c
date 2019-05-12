#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <netinet/in.h> //Internet Protocol family, ex: sin_family, sin_port, ..., ect
#include <sys/socket.h>
#include <arpa/inet.h> //for inet_addr()
#include <pthread.h>
#include <math.h>
#include <unistd.h> //write(.)
#define SIZE 512

/*require (1.socket() 2.connect() 3.write())build up a TCP client*/
int mwrite(int sockfd, const void *buf, size_t len);
int mread(int sockfd, void *buf, size_t len);
int split(char *input, char split_word[10][100]);
void *msgread(void *fd); //一直收訊息

int main(void)
{
    struct sockaddr_in srv;
    struct sockaddr_in cli;
    int nbytes = 0;
    int fd = -1;
    int server_port = 0;
    char *server_ip = NULL;

    while (1)
    {
        char input[64] = {'\0'}; //the user's input
        char split_word[10][100] = {'\0'};
        int countword = 0; //count how many words the user enter
        int IsWrongChat = 0;
        printf("$ ");
        fgets(input, 64, stdin);
        countword = split(input, split_word);

        if (strcmp(split_word[0], "connect") == 0)
        {
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
            mwrite(fd, split_word[3], sizeof(split_word[3])); //傳user name

            pthread_t thread; //read message thread
            pthread_create(&thread, NULL, msgread, &fd);
        }
        else if (strcmp(split_word[0], "chat") == 0)
        {
            if (countword < 3)
            {
                printf("Please enter othername and message!!\n");
                IsWrongChat = 1;
            }
            if (fd == -1)
            {
                printf("Please connect first\n");
            }
            else
            {
                if (IsWrongChat == 0)
                {
                    int howmanypeople = countword - 2;                 //要傳訊息給幾個人
                    mwrite(fd, &howmanypeople, sizeof(howmanypeople)); //傳要傳訊息給幾個人
                    for (int i = 1; i <= howmanypeople; ++i)
                    {
                        mwrite(fd, split_word[i], sizeof(split_word[i])); //傳每個要收的人的名字
                        //printf("%s\n", split_word[i]);
                    }
                    mwrite(fd, split_word[countword - 1], sizeof(split_word[countword - 1])); //傳訊息
                    //printf("%s\n", split_word[countword - 1]);
                }
            }
        }
        else if (strcmp(split_word[0], "bye") == 0)
        {
            printf("Goodbye.\n");
            close(fd);
            break;
        }
        else if (strcmp(split_word[0], "help") == 0)
        {
            printf("You can enter three commands to do something\n");
            printf("1. [connect server_ip server_port yourname]:connect to server\n");
            printf("2. [chat othername*n message]:chat to oyhers(you can chat to one ore more others)\n");
            printf("3. [bye]:close the connection\n");
        }
        else
        {
            printf("please enter correct command!!! or you can enter \"help\" to see correct commands\n");
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

int mread(int sockfd, void *buf, size_t len)
{
    int nbytes = 0;
    int size = len;

    while ((nbytes = read(sockfd, buf, len)) > 0)
    {
        buf += nbytes;
        len -= nbytes;
    }
    if (nbytes < 0)
        return -1; /* fail to read */
    else if (len == 0)
        return size; /* success to read all data */
    else if (len != 0)
        return 0; /* socket is closed, read 0 bytes. */
}

int split(char *input, char split_word[10][100])
{
    int i = 0, j = 0, k = 0;
    int count = 1;
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
            count++;
        }
        i++;
    }
    return count;
}

void *msgread(void *fd)
{
    int socket_fd = *(int *)fd;
    char message[100] = {'\0'};
    while (1)
    {
        setbuf(stdout, NULL); //因為 printf 其實只是把東西放到 buffer 當中而不會立刻顯示，而預設的 stdout 是 line buffered，所以只有當遇到 '\n' 才會清空 buffer 把內容印出來
        mread(socket_fd, message, sizeof(message));
        printf("\r%s\n$ ", message);
    }
}