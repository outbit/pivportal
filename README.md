pivportal
===========

Secure Linux sudo access using a PIV, CAC, SmartCard, or x509 Client Certificate.

[![Build Status](https://secure.travis-ci.org/starboarder2001/pivportal.png?branch=master "ansible-docs latest build")](http://travis-ci.org/starboarder2001/pivportal)
[![PIP Version](https://img.shields.io/pypi/v/pivportal.svg "ansible-docs PyPI version")](https://pypi.python.org/pypi/pivportal)
[![PIP Downloads](https://img.shields.io/pypi/dm/pivportal.svg "ansible-docs PyPI downloads")](https://pypi.python.org/pypi/pivportal)
[![Coverage Status](https://coveralls.io/repos/starboarder2001/pivportal/badge.svg?branch=develop&service=github)](https://coveralls.io/github/starboarder2001/pivportal?branc    h=develop)
[![Gitter IM](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/starboarder2001/pivportal)

![alt tag](https://raw.githubusercontent.com/starboarder2001/pivportal/images/pivportal_web.png)
![alt tag](https://raw.githubusercontent.com/starboarder2001/pivportal/images/pivportal_client.png)

Installing pivportal Server
======

```bash
$ docker pull starboarder2001/pivportal
```

Configuring pivportal Server
======

```bash
docker run -d -p 80:80 -p 442:442 -p 443:443 starboarder2001/pivportal
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

ip - IP Address of the server

port - TCP Port to user to connect to the server

ssl_verify_host - SSL verify server certificate is valid. 0 = false, 1 = true.

```bash
[server]
ip=192.16.0.1
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
