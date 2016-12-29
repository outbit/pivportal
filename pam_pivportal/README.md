pam_pivportal
==================

Build and Installation
====

Debian

```bash
$ sudo apt-get install -y libpam0g-dev libcurl4-openssl-dev glib2.0
$ make && make install
```

Redhat / CentOS

```bash
$ sudo yum install pam-devel libcurl-devel glib2-devel
$ make && make install
```

Configuration
====

Example /etc/pam.d/sudo file:

```bash
auth required pam_pivportal.so
account include system-auth
password include system-auth
session optional pam_keyinit.so revoke
session required pam_limits.so
```

Example /etc/pivportal.conf:

ip - IP Address of the server. Default is 127.0.0.1.

port - TCP Port to user to connect to the server. Default is 442.

client_ssl_cert - Client SSL certificate used by the pam_pivportal module to authenticate to the pivportal server. Default is /etc/ssl/certs/pivportalClient.pem.

ssl_verify_host - SSL verify server certificate is valid. 0 = false, 1 = true. Default is false.

```bash
[server]
ip=192.16.0.1
port=442
client_ssl_cert=/etc/ssl/certs/pivportalClient.pem
ssl_verify_host=0
```