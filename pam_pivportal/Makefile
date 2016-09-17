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

install:
	sudo cp -f $(TARGET).so /lib/security/
	sudo chown root:root /lib/security/$(TARGET).so
	sudo chmod 500 /lib/security/$(TARGET).so

clean:
	rm -f $(TARGET).o
