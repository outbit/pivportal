Building
=====

```bash
$ docker build -t starboarder2001/pivportal .
```

Running
=====

```bash
$ docker run -d -p 80:80 -p 442:442 -p 443:443 starboarder2001/pivportal
```

Use Bash Shell To Customize Running Container
======

```bash
docker exec -i -t da426841d88f /bin/bash
```

In the running docker instance, you are required to:

- Copy x509 PEM CA and intermediate certificates in /etc/ssl/private/pivportalCA.crt.
- Edit /etc/pivportal-server.conf and add the Designated Names you authorize to use the application. The file includes examples.

In the running docker instance, it is recomended to:

- Copy the CRL (certificate revokation list) to /etc/ssl/private/pivportal.crl and uncomment the line in /etc/apache2/sites-enabled/httpd-pivportal.conf.
- Copy your valid SSL public certificate to /etc/ssl/private/pivportal.crt.
- Copy your valid SSL private certificate to /etc/ssl/private/pivportal.key.

Be Careful, Shortcuts for Testing and Development. The below commands will stop all docker containers, remove all docker containers, and remove all docker images.
======

```bash
for img in $(docker ps|awk '{print $1}'|grep -v CONT); do docker stop $img; done
for img in $(docker ps -a|awk '{print $1}'|grep -v CONT); do docker rm $img; done
for img in $(docker images|grep -v debian|grep -v IMAGE|awk '{print $3}'); do docker rmi $img; done
```