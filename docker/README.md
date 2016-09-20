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

Bash Shell
======

```bash
docker exec -i -t da426841d88f /bin/bash
```

Be Careful, Cleanup docker images
======

```bash
for img in $(docker ps|awk '{print $1}'|grep -v CONT); do docker stop $img; done
for img in $(docker ps -a|awk '{print $1}'|grep -v CONT); do docker rm $img; done
for img in $(docker images|grep -v debian|grep -v IMAGE|awk '{print $3}'); do docker rmi $img; done
```