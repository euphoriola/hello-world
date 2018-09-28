OBJS = main.o \

SRC = main.c \


MY_C_FLAG = -Wall -o -g

helloworld:$(OBJS)
	gcc $(OBJS) -o helloworld -g

main.o: $(SRC)
	gcc $(MY_C_FLAG) -c main.c -o main.o


clean:
	rm -rf *.o helloworld
