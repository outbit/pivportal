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
	sudo cp -f $(TARGET).so /usr/lib64/security/
	sudo chown root:root /usr/lib64/security/$(TARGET).so
	sudo chmod 755 /usr/lib64/security/$(TARGET).so

clean:
	rm -f $(TARGET).o
