all: clean server

server: server.o
	gcc -o server server.o -pthread -lm
server.o:
	gcc -c server.c
clean:
	rm -f *.o server
