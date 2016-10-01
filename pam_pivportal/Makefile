CC = gcc
LD = ld

CFLAGS = -fPIC -fno-stack-protector -I/usr/include/glib-2.0/ -I/usr/lib64/glib-2.0/include/
LFLAGS = -x --shared -lcurl -lglib-2.0 --build-id

TARGET = pam_pivportal

all: $(TARGET)

$(TARGET).o: $(TARGET).c
	$(CC) $(CFLAGS) -c $(TARGET).c

$(TARGET): $(TARGET).o
	$(LD) $(LFLAGS) -o $(TARGET).so $(TARGET).o

install:
	sudo cp -f $(TARGET).so /usr/lib64/security/ && chown root:root /usr/lib64/security/$(TARGET).so && chmod 755 /usr/lib64/security/$(TARGET).so

test:
	$(CC) -o $(TARGET)_test $(TARGET)_test.c -lpam -lpam_misc -lcurl && ./$(TARGET)_test nobody

rpm:
	scons

dpkg:
	# apt-get install alien
	alien *.x86_64.rpm
	# mkdir -p /usr/lib64/
	# ln -s /lib/x86_64-linux-gnu/security/ /usr/lib64/security

clean:
	rm -f $(TARGET).o $(TARGET)_test $(TARGET).so *.rpm *.spec *.tar.gz
	rm -rf pam_pivportal-*/
	rm -rf rpmtemp/
