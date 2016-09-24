pam_pivportal
==================


Build
====

```bash
$ make
```

Install
====

Debian
$ sudo apt-get install -y libpam0g-dev libcurl4-openssl-dev glib2-devel

Redhat / CentOS
$ sudo yum install pam-devel libcurl-devel glib2-devel

```bash
$ make install
```

Example /etc/pam.d/sudo file:

```bash
auth required pam_pivportal.so
account include system-auth
password include system-auth
session optional pam_keyinit.so revoke
session required pam_limits.so
```

Example /etc/pivportal.conf:

ip - IP Address of the server
port - TCP Port to user to connect to the server
ssl_verify_host - SSL verify server certificate is valid

```bash
[server]
ip=192.16.0.1
port=442
ssl_verify_host=0
```