#!/bin/bash

openssl req -newkey rsa:4096 -keyform PEM -keyout pivPortalCA.key -x509 -days 3650 -outform PEM -out pivPortalCA.cer
openssl genrsa -out pivPortal.key 4096
openssl req -new -key pivPortal.key -out server.req -sha256
openssl x509 -req -in pivPortal.req -CA pivPortalCA.cer -CAkey pivPortalCA.key -set_serial 100 -extensions server -days 1460 -outform PEM -out pivPortal.cer -sha256
rm -f pivPortal.req

openssl genrsa -out pivPortalClient.key 4096
openssl req -new -key pivPortalClient.key -out pivPortalClient.req
openssl x509 -req -in pivPortalClient.req -CA pivPortalCA.cer -CAkey pivPortalCA.key -set_serial 101 -extensions client -days 365 -outform PEM -out pivPortalClient.cer
openssl pkcs12 -export -inkey pivPortalClient.key -in pivPortalClient.cer -out pivPortalClient.p12
#rm -f pivPortalClient.key pivPortalClient.cer pivPortalClient.req

echo "Import the .p12 file in your browser. Default challenge password for example certs is password."
