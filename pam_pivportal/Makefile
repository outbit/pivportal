CC = gcc
LD = ld

CFLAGS = -fPIC -fno-stack-protector
LFLAGS = -x --shared

TARGET = pam_pivportal

all: $(TARGET)

$(TARGET).o: $(TARGET).c
	$(CC) $(CFLAGS) -c $(TARGET).c

$(TARGET): $(TARGET).o
	$(LD) $(LFLAGS) -o $(TARGET).so $(TARGET).o

clean:
	rm $(TARGET).o
