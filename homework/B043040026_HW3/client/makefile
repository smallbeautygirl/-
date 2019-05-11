all: clean client

client: client.o
	gcc -o client client.o -pthread -lm
client.o: 
	gcc -c client.c
clean:
	rm -f *.o client
