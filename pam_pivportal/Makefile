CC = gcc
CPP = g++
LD = ld

CFLAGS = -fPIC -fno-stack-protector -I/usr/include/glib-2.0/ -I/usr/lib64/glib-2.0/include/ -I/usr/lib/x86_64-linux-gnu/glib-2.0/include/
LFLAGS = -x --shared -lcurl -lglib-2.0 --build-id

TARGET = pam_pivportal

all: $(TARGET)

$(TARGET).o: $(TARGET).c
	$(CC) $(CFLAGS) -c $(TARGET).c

$(TARGET): $(TARGET).o
	$(LD) $(LFLAGS) -o $(TARGET).so $(TARGET).o

install:
	sudo cp -f $(TARGET).so /usr/lib64/security/ && chown root:root /usr/lib64/security/$(TARGET).so && chmod 755 /usr/lib64/security/$(TARGET).so

$(TARGET)_test: $(TARGET).c $(TARGET)_test.c
	# yum install gtest gtest-devel gcc gcc-c++
	# apt-get install -y libgtest-dev gcc c++
	$(CPP) -lcurl -lglib-2.0 -lgtest -o $(TARGET)_test -I/usr/include/glib-2.0/ -I/usr/lib64/glib-2.0/include/ -I/usr/lib/x86_64-linux-gnu/glib-2.0/include/ $(TARGET)_test.c $(TARGET).c

test: $(TARGET)_test
	./$(TARGET)_test

rpm:
	scons

dpkg:
	# apt-get install alien
	# mkdir -p /usr/lib64/ && ln -s /lib/x86_64-linux-gnu/security/ /usr/lib64/security
	alien *.x86_64.rpm

clean:
	rm -f $(TARGET).o $(TARGET)_test $(TARGET).so *.rpm *.spec *.tar.gz
	rm -rf pam_pivportal-*/
	rm -rf rpmtemp/
