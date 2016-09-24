pivportal
==================


Install
====

```bash
$ pip install pivportal
```

Running
====

```bash
$ pivportal -p 8088 -l 127.0.0.1
```

Config
====

Example /etc/pivportal-server.conf:

authorized_users - List of authorized user DN's and mapping to the unix username
listen_address - Listen IP Address
port - TCP Port to run service on

```bash
---
authorized_users: {"dn1": "user1", "dn2": "user2"}
listen_address: 127.0.0.1
port: 8088
```