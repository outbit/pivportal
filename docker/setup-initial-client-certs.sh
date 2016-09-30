#!/bin/bash

# Only Run On First Start
if [ ! -f /etc/ssl/private/pivportalClientCA.key ]; then

# SSL CA Certificate For Client Cert
openssl genrsa -out /etc/ssl/private/pivportalClientCA.key 4096
openssl req -new -x509 -subj "/C=US/ST=Oregon/L=Portland/O=IT/CN=pivportalclientCA" -days 3650 -key /etc/ssl/private/pivportalClientCA.key -out /etc/ssl/private/pivportalClientCA.crt

# SSL Create the Client Key and CSR
openssl genrsa -out /etc/ssl/private/pivportalClient.key 1024
openssl req -new -subj "/C=US/ST=Oregon/L=Portland/O=IT/CN=pivportalclient" -key /etc/ssl/private/pivportalClient.key -out /etc/ssl/private/pivportalClient.csr

# SSL Sign the client certificate with our CA cert.
openssl x509 -req -days 3650 -in /etc/ssl/private/pivportalClient.csr -CA /etc/ssl/private/pivportalClientCA.crt -CAkey /etc/ssl/private/pivportalClientCA.key -set_serial 01 -out /etc/ssl/private/pivportalClient.crt
cat /etc/ssl/private/pivportalClient.key /etc/ssl/private/pivportalClient.crt > /etc/ssl/private/pivportalClient.pem

fi
