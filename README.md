pivportal
===========

Secure Linux sudo access using a PIV card.

Installing
======

```bash
$ docker pull starboarder2001/pivportal
```

PAM Configuration on Linux Client
======

/etc/pam.d/sudo

```bash
auth sufficient pam_pivportal.so
account sufficient pam_pivportal.so
```

Usage
======

```bash
docker run -d -p 80:80 -p 442:442 -p 443:443 starboarder2001/pivportal
```

Connect using a web browser to the pivportal server.

The first login you will be prompted to provide the root CA certificates, CRL url, and a list of serial numbers.
