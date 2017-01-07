#!/bin/bash

/sbin/setup-initial-client-certs.sh

service redis-server start
service apache2 start

su - pivportal -c "pivportal"

sleep infinity
