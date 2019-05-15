client.c:

用到的function:
int mwrite(int sockfd, const void *buf, size_t len);
int mread(int sockfd, void *buf, size_t len);
int split(char *input, char split_word[10][100]); //分割指令
void *msgread(void *fd); //一直收訊息

另外建立一個thread一直收訊息

server.c:
用到的function:
void *run(void *all);
int mread(int sockfd, void *buf, size_t len);
int mwrite(int sockfd, const void *buf, size_t len);
bool find(char database[DATABASE_SIZE][100], char name[100]); //看user是否存在
void broadcast(int newfd, char *cli_ip, char username[100], char IsOnline[10]);

用一個database array和storefd array存使用者名字和對應的fd ，且放全域

