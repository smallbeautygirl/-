實作socket連線：

1.server.c:
(1).TCP：require (1.socket() 2.bind() 3.listen() 4.accept() 5.read())build up a TCP server
(2).多個client同時連線:建立thread去服務每個要連線的client
    ex:pthread_t thread; //client thread
       pthread_create(&thread, NULL, run, &argument);
(3).接收檔案:
    (i)接收還沒壓縮前的檔名:read(run_arg.run_fd, decompressed_filename,sizeof(decompressed_filename)); //收原本的檔名
    (ii)接收還沒壓縮前的檔案大小:read(run_arg.run_fd,&original_filesize,sizeof(original_filesize));          //收原本的檔案大小
    (iii)接收壓縮過的檔案大小:read(run_arg.run_fd, &file_size, sizeof(file_size));                        //收壓縮過的檔案大小
    (iv)接收壓縮過的檔案:
        int count = ceil((float)file_size / SIZE); //計算要幾個segment才收的完檔案
    FILE *f;
    f = fopen("out", "wb");

    for (int i = 0; i < count; ++i)
    {
        bzero(buf, sizeof(buf));
        int size = (file_size >= SIZE) ? SIZE : file_size;
        file_size -= SIZE;
        int nbytes = mread(run_arg.run_fd, buf, sizeof(buf));
        if (nbytes < 0)
        {
            perror("read error\n");
            exit(1);
        }
        fwrite(buf, sizeof(char), size, f); //把收到的封包的data存入file
    }
    (v)接收字元出現的頻率:read(run_arg.run_fd, ascii, sizeof(ascii));
2.client.c:
(1)TCP:require (1).socket (2).connect (3).write build up a TCP client
(2)建立void split(char *input, char split_word[3][64])切割出使用者輸入的指令
(3)輸入connect server_ip server_port 建立連線
(4)輸入upload file傳送檔案
(5)輸入bye關閉連線
(6)輸入help得知正確的command
(7)壓縮檔案:
    (i)void huffman(int fd, FILE *file, char *filename):傳入原本的檔案進行壓縮
    (ii)Node *build_tree(int *ascii, Node list[512]):依照檔案裡各個字元出現的頻率建huffman的tree
    (iii)void build_table(Node *root, Encode encode[256], char code, int count):利用huffman tree建立編碼表
(8)傳送檔案:
    (i)傳送還沒壓縮前的檔名:write(fd,split_word[1], sizeof(split_word[1]));          //傳原本的檔名
    (ii)傳送還沒壓縮前的檔案大小:write(fd,&original_file_size,sizeof(original_file_size));//傳原本的檔案大小
    (iii)傳送壓縮過的檔案大小:write(fd, &file_size, sizeof(file_size)); //傳壓縮後的檔案大小
    (iv)傳送壓縮過的檔案:
        for (int i = 0; i < count; ++i)
                    {
                        int size = (file_size >= SIZE) ? SIZE : file_size; //判斷檔案大小是否大於一個segment
                        nbytes = 0;
                        file_size -= SIZE;

                        fread(buf, sizeof(char), size, file);
                        /*write procedure*/
                        if ((nbytes = mwrite(fd, buf, sizeof(buf))) < 0)
                        {
                            perror("write error");
                            exit(1);
                        }
                    }
    (v)傳送字元出現的頻率:
        write(fd, ascii, sizeof(ascii)); //把字元出現頻率傳過去給server

