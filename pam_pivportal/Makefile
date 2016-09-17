CC = gcc
LD = ld

CFLAGS = -fPIC -fno-stack-protector
LFLAGS = -x --shared -lcurl

TARGET = pam_pivportal

all: $(TARGET)

$(TARGET).o: $(TARGET).c
	$(CC) $(CFLAGS) -c $(TARGET).c

$(TARGET): $(TARGET).o
	$(LD) $(LFLAGS) -o $(TARGET).so $(TARGET).o

install:
	sudo cp -f $(TARGET).so /usr/lib64/security/
	sudo chown root:root /usr/lib64/security/$(TARGET).so
	sudo chmod 755 /usr/lib64/security/$(TARGET).so

test:
	$(CC) -o $(TARGET)_test $(TARGET)_test.c -lpam -lpam_misc -lcurl
	./$(TARGET)_test

clean:
	rm -f $(TARGET).o
	rm -f $(TARGET)_test
	rm -f $(TARGET).so
