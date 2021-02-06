pivportal
===========

Secure Linux sudo access using a PIV (HSPD-12), CAC, SmartCard, or x509 Client Certificate.

[![Build Status](https://secure.travis-ci.org/outbit/pivportal.png?branch=master "ansible-docs latest build")](http://travis-ci.org/outbit/pivportal)
[![PIP Version](https://img.shields.io/pypi/v/pivportal.svg "ansible-docs PyPI version")](https://pypi.python.org/pypi/pivportal)
[![Coverage Status](https://coveralls.io/repos/outbit/pivportal/badge.svg?branch=develop&service=github)](https://coveralls.io/github/outbit/pivportal?branch=develop)
[![Gitter IM](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/outbit/pivportal)

![alt tag](https://raw.githubusercontent.com/outbit/pivportal/images/pivportal_web.png)
![alt tag](https://raw.githubusercontent.com/outbit/pivportal/images/pivportal_client.png)

Installing pivportal Server
======

```bash
$ docker pull outbit/pivportal
```

Configuring pivportal Server
======

```bash
docker run -d -p 80:80 -p 442:442 -p 443:443 outbit/pivportal
```

In the running docker instance, **you are required to**:

- Copy CA and intermediate certificates (in x509 PEM format) in /etc/ssl/private/pivportalCA.crt.
- Edit /etc/pivportal-server.conf and add the Designated Names you authorize to use the application. The file includes examples.

In the running docker instance, **it is recommended to**:

- Copy the CRL (certificate revokation list) to /etc/ssl/private/pivportal.crl and uncomment the line in /etc/apache2/sites-enabled/httpd-pivportal.conf.
- Copy your valid SSL public certificate to /etc/ssl/private/pivportal.crt.
- Copy your valid SSL private certificate to /etc/ssl/private/pivportal.key.

Connect using a web browser to the pivportal server.

PAM Configuration on Linux Client
======

- Build and Install pam_pivportal.so.
- Copy /etc/ssl/private/pivportalClient.pem from the docker container to /etc/ssl/certs/pivportalClient.pem on each Linux Client.

Example /etc/pam.d/sudo file:

```bash
auth required pam_pivportal.so
account include system-auth
password include system-auth
session optional pam_keyinit.so revoke
session required pam_limits.so
```

Example /etc/pivportal.conf:

hosts - Hostname or IP Address of the server. Default is 127.0.0.1.

port - TCP Port for pam_pivportal to authenticate to the server. Default is 442.

client_ssl_cert - Client SSL certificate used by the pam_pivportal module to authenticate to the pivportal server. Default is /etc/ssl/certs/pivportalClient.pem.

ssl_verify_host - SSL verify server certificate is valid. 0 = false, 1 = true. Default is false.

```bash
[server]
hosts=192.16.0.1;192.168.0.2
port=442
client_ssl_cert=/etc/ssl/certs/pivportalClient.pem
ssl_verify_host=0
```

License
======

pivportal is released under the [MIT License](LICENSE.md).


Author
======

David Whiteside (<david@davidwhiteside.com>)
