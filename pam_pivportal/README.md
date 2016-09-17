pam_pivportal
==================


Build
====

```bash
$ make
```

Install
====

```bash
$ make install
```

Example /etc/pam.d/sudo file.

```bash
auth sufficient pam_pivportal.so
account sufficient pam_pivportal.so
```