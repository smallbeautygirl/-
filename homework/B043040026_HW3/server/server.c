#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h> //Internet Protocol family, ex: sin_family, sin_port, ..., ect
#include <netdb.h>
#include <arpa/inet.h>
#include <pthread.h>
#include <math.h>
#include <string.h>
#include <stdbool.h>
#include <time.h>
/*require (1.socket() 2.bind() 3.listen() 4.accept() 5.read())build up a TCP server */
#define SIZE 512         //buffer size
#define DATABASE_SIZE 10 //database size
#define FD_NUMBER 10     //fd number
/*因為pthread規定它裡面的自己的function只能傳一個argument，所以先把要傳的變數包成一個structer*/
struct run_argument
{
    struct sockaddr_in run_cli;
    int run_fd;
};

void *run(void *all);
int mread(int sockfd, void *buf, size_t len);
int mwrite(int sockfd, const void *buf, size_t len);
bool find(char database[DATABASE_SIZE][100], char name[100]); //看user是否存在
void broadcast(int newfd, char *cli_ip, char username[100], char IsOnline[10]);

char database[DATABASE_SIZE][100] = {'\0'}; //initialize the database
int storefd[FD_NUMBER] = {-1, -1, -1, -1, -1, -1, -1, -1, -1, -1};
char off_lineMessage[10][100] = {'\0'};
int main(int argc, char **argv)
{
    int fd;                 /* socket descriptor returned by socket()*/
    int newfd;              /* returned by accept() */
    struct sockaddr_in srv; //used by bind()
    struct sockaddr_in cli; //used by accept()
    //struct ifreq ifr;//used by get server ip
    char buf[SIZE];            //used by read()
    int cli_len = sizeof(cli); //used by accept()
    int nbytes;                //used by read()
    int server_port = atoi(argv[1]);

    if (argc != 2)
    {
        fprintf(stderr, "[error] usage: ./Server [port]\n");
        exit(1);
    }

    fd = socket(AF_INET, SOCK_STREAM, 0);
    /*socket procedure*/
    if (fd < 0)
    {
        //AF_INET是指用IPv4 , SOCK_STREAM select the TCP protocol
        perror("socket error");
        exit(1); //非正常運行檔至退出程序
    }

    /*bind procedure*/
    /* create the socket */
    srv.sin_family = AF_INET;          /* use the Internet address family */
    srv.sin_port = htons(server_port); /* bind socket ‘fd’ to server port */
    /* bind: a client may connect to any of my addresses */
    srv.sin_addr.s_addr = htonl(INADDR_ANY);
    if (bind(fd, (struct sockaddr *)&srv, sizeof(srv)) < 0)
    {
        perror("bind error");
        exit(1);
    }

    /*listen procedure*/
    if (listen(fd, 5) > 0)
    { //"5" specifies the maximum number of connections that kernel should queue for this socket .
        perror("listen error");
        exit(1);
    }
    while (1)
    {
        /*accept procedure*/
        newfd = accept(fd, (struct sockaddr *)&cli, &cli_len);
        if (newfd < 0)
        {
            perror("accept error");
            exit(1);
        }

        /* create a thread to handle client requst */
        struct run_argument argument = {.run_cli = cli, .run_fd = newfd};
        pthread_t thread; //client thread
        pthread_create(&thread, NULL, run, &argument);
    }

    return 0;
}

void *run(void *all)
{
    struct run_argument run_arg = *(struct run_argument *)all;
    struct sockaddr_in cli = run_arg.run_cli;
    char *cli_ip = inet_ntoa(cli.sin_addr); //將 network address 由 struct in_addr 轉換為句號與數字組成的字串格式
    int cli_port = ntohs(cli.sin_port);
    char username[100] = {'\0'};
    char IsOnline[10] = {"on-line"};
    int fdindex = 0;
    char *wday[] = {"Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"};
    time_t timep;
    struct tm *p;
    time(&timep);
    p = localtime(&timep); /*取得當地時間*/

    setbuf(stdout, NULL);                              //因為 printf 其實只是把東西放到 buffer 當中而不會立刻顯示，而預設的 stdout 是 line buffered，所以只有當遇到 '\n' 才會清空 buffer 把內容印出來
    mread(run_arg.run_fd, username, sizeof(username)); //讀username
    printf("A client (name : %s) \"%s\" has connected via port num %d using SOCK_STREAM(TCP)\n", username, cli_ip, cli_port);

    //把newfd 放入 fd list中 也把username放入database中(username對應到fd)
    for (int i = 0; i < DATABASE_SIZE; ++i)
    {
        if (strcmp(username, database[i]) == 0)
        {
            if (storefd[i] == -1)
            {
                storefd[i] = run_arg.run_fd;
                fdindex = i;
            }
            break;
        }
        else
        {
            if (strcmp(database[i], "") == 0)
            {
                if (storefd[i] == -1)
                {
                    storefd[i] = run_arg.run_fd;
                    fdindex = i;
                }
                strcpy(database[i], username);
                break;
            }
        }
    }

    if (strcmp(off_lineMessage[fdindex], "") != 0)
    {
        mwrite(storefd[fdindex], off_lineMessage[fdindex], sizeof(off_lineMessage[fdindex]));
        strcpy(off_lineMessage[fdindex], "");
    }
    broadcast(run_arg.run_fd, cli_ip, username, IsOnline); //告訴大家你上線了
    while (1)
    {
        int howmanypeople = 0;
        char othername[10][100] = {'\0'}; //store the ones who the user want to send to
        char message[100] = {'\0'};
        char usernotfind[100] = {'\0'};
        int IsClosefd = 0;
        char from[100] = {""};
        char timerecord[100] = {""}; //紀錄現在時間

        IsClosefd = mread(run_arg.run_fd, &howmanypeople, sizeof(howmanypeople)); //收要傳訊息給幾個人
        if (IsClosefd == 0)
        {
            strcpy(IsOnline, "off-line");
            storefd[fdindex] = -1;
            broadcast(run_arg.run_fd, cli_ip, username, IsOnline); //告訴大家你下線了
            pthread_exit(NULL);
        }
        for (int i = 0; i < howmanypeople; ++i)
        {
            mread(run_arg.run_fd, othername[i], sizeof(othername[i])); //收每個人的名字
            printf("receiver: %s \n", othername[i]);
            if (find(database, othername[i]) == 0)
            {
                sprintf(usernotfind, "<User %s does not exist.>", othername[i]);
                mwrite(storefd[fdindex], usernotfind, sizeof(usernotfind));
                printf("%s\n", usernotfind);
                strcpy(othername[i], "");
            }
        }

        mread(run_arg.run_fd, message, sizeof(message));
        printf("message: %s\n", message);
        sprintf(timerecord, "%d %d %d %s %d:%d:%d", (1900 + p->tm_year), (1 + p->tm_mon), p->tm_mday, wday[p->tm_wday], p->tm_hour, p->tm_min, p->tm_sec);
        sprintf(from, "    message sent by \"%s\" at %s", username, timerecord);

        for (int i = 0; i < howmanypeople; ++i)
        {
            char useroffline[100] = {'\0'};
            for (int j = 0; j < FD_NUMBER; ++j)
            {
                if ((strcmp(othername[i], "") != 0) && (strcmp(othername[i], database[j]) == 0)) //若在database找到這個人
                {
                    strcat(message, from);
                    if (storefd[j] == -1) //若對方離線了
                    {
                        strcpy(off_lineMessage[j], message); //先把訊息暫存起來
                        sprintf(useroffline, "<User %s is off-line. The message will be passed when he comes back.>", othername[i]);
                        mwrite(run_arg.run_fd, useroffline, sizeof(useroffline));
                    }
                    else //對方在線上
                    {
                        mwrite(storefd[j], message, sizeof(message));
                        break;
                    }
                }
            }
        }
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

bool find(char database[DATABASE_SIZE][100], char name[100])
{ //看user是否存在
    for (int i = 0; i < DATABASE_SIZE; i++)
    {
        if (strcmp(database[i], name) == 0)
        {
            return true;
        }
    }
    return false;
}

void broadcast(int newfd, char *cli_ip, char username[100], char IsOnline[10])
{
    char message[100] = {'\0'};
    sprintf(message, "<User %s is %s, IP address: %s.>", username, IsOnline, cli_ip);
    for (int i = 0; i < FD_NUMBER; ++i)
    {
        if ((storefd[i] != -1) && (storefd[i] != newfd))
        {
            mwrite(storefd[i], message, sizeof(message));
        }
    }
}