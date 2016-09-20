pivportal
===========

Secure Linux sudo access using a PIV card.

[![Build Status](https://secure.travis-ci.org/starboarder2001/pivportal.png?branch=master "ansible-docs latest build")](http://travis-ci.org/starboarder2001/pivportal)
[![PIP Version](https://img.shields.io/pypi/v/pivportal.svg "ansible-docs PyPI version")](https://pypi.python.org/pypi/pivportal)
[![PIP Downloads](https://img.shields.io/pypi/dm/pivportal.svg "ansible-docs PyPI downloads")](https://pypi.python.org/pypi/pivportal)
[![Coverage Status](https://coveralls.io/repos/starboarder2001/pivportal/badge.svg?branch=develop&service=github)](https://coveralls.io/github/starboarder2001/pivportal?branc    h=develop)
[![Gitter IM](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/starboarder2001/pivportal)

Installing
======

```bash
$ docker pull starboarder2001/pivportal
```

PAM Configuration on Linux Client
======

/etc/pam.d/sudo

```bash
auth required pam_pivportal.so
account include system-auth
password include system-auth
session optional pam_keyinit.so revoke
session required pam_limits.so
```

Usage
======

```bash
docker run -d -p 80:80 -p 442:442 -p 443:443 starboarder2001/pivportal
```

In the running docker instance, you are required to:

- Copy CA and intermediate certificates (in x509 PEM format) in /etc/ssl/private/pivportalCA.crt.
- Edit /etc/pivportal-server.conf and add the Designated Names you authorize to use the application. The file includes examples.

In the running docker instance, it is recommended to:

- Copy the CRL (certificate revokation list) to /etc/ssl/private/pivportal.crl
- Copy your valid SSL public certificate to /etc/ssl/private/pivportal.crt
- Copy your valid SSL private certificate to /etc/ssl/private/pivportal.key

Connect using a web browser to the pivportal server.
