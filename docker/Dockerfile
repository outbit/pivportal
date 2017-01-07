FROM debian:stable
MAINTAINER David Whiteside <david@davidwhiteside.com>

# pivportal-api dependencies
RUN apt-get update && apt-get install -y python \
  python-setuptools \
  python-dev \
  build-essential \
  libffi-dev \
  openssl \
  libssl-dev \
  apache2 \
  redis-server \
  python-pip
RUN pip install -U pip
RUN pip install -U setuptools

# pivportal application user and group
RUN groupadd -r pivportal && useradd -r -g pivportal pivportal

# pivportal-api install latest stable
RUN pip install -U pivportal

# Apache
RUN a2enmod ssl
RUN a2enmod proxy_http
RUN a2enmod headers
COPY ./ports.conf /etc/apache2/
COPY ./httpd-pivportal.conf /etc/apache2/sites-enabled/
RUN chown root: /etc/apache2/sites-enabled/httpd-pivportal.conf && chmod 755 /etc/apache2/sites-enabled/httpd-pivportal.conf

# SSL Server Cert
RUN openssl req -new -nodes -x509 -subj "/C=US/ST=Oregon/L=Portland/O=IT/CN=testhost" -days 3650 -keyout /etc/ssl/private/pivportal.key -out /etc/ssl/private/pivportal.crt -extensions v3_ca || true
RUN chown pivportal: /etc/ssl/private/pivportal* && chmod 440 /etc/ssl/private/pivportal*

# Log file
RUN touch /var/log/pivportal.log && chmod 755 /var/log/pivportal.log && chown pivportal: /var/log/pivportal.log

# Config file for pivportal
COPY ./pivportal-server.conf /etc/
RUN chown pivportal: /etc/pivportal-server.conf && chmod 440 /etc/pivportal-server.conf

# Entry Point
COPY ./setup-initial-client-certs.sh /sbin/
COPY ./docker-entrypoint.sh /sbin/
RUN chmod 755 /sbin/docker-entrypoint.sh /sbin/setup-initial-client-certs.sh
RUN chown root: /sbin/docker-entrypoint.sh /sbin/setup-initial-client-certs.sh
ENTRYPOINT ["/sbin/docker-entrypoint.sh"]
