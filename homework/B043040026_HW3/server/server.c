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
/*require (1.socket() 2.bind() 3.listen() 4.accept() 5.read())build up a TCP server */

/*因為pthread規定它裡面的自己的function只能傳一個argument，所以先把要傳的變數包成一個structer*/
struct run_argument
{
    struct sockaddr_in run_cli;
    int run_fd;
};

void *run(void *all);

#define SIZE 512//buffer size

int main(int argc,char **argv){
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

void *run(void *all){
   struct run_argument run_arg = *(struct run_argument *)all;
    struct sockaddr_in cli = run_arg.run_cli;
    char *cli_ip = inet_ntoa(cli.sin_addr); //將 network address 由 struct in_addr 轉換為句號與數字組成的字串格式
    int cli_port = ntohs(cli.sin_port);
    printf("A client \"%s\" has connected via port num %d using SOCK_STREAM(TCP)\n", cli_ip, cli_port);
    printf("111");
    // read(run_arg.run_fd,username,20);//收使用者名稱
    // printf("1111");
    // printf("%s",username);
    //database = fopen("database","a");
    //fwrite(cli_ip, sizeof(char), sizeof(cli_ip), database);
    //fclose(database);
    //while(1){
        
        // unsigned char buf[SIZE]={'\0'};//要用成unsigned不然傳過去的資料會錯誤
        
        
        // FILE * database = NULL;
        // database = fopen("database","r");
        // //char temp = '\0';
        // char *temp_name=NULL;
        // while(fgets(temp_name,20,database)!= NULL){
        //     if(strcmp(temp_name,username)==0){
        //         printf("%s",cli_ip);
        //         break;
        //     }
        //     //fwrite(cli_ip, sizeof(char), sizeof(cli_ip), database);
        // }
        // fclose(database);
    //}
}