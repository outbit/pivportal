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
  nginx \
  python-pip
RUN pip install -U pip
RUN pip install -U setuptools

# pivportal application user and group
RUN groupadd -r pivportal && useradd -r -g pivportal pivportal

# pivportal-api install latest stable
RUN pip install -U pivportal

# SSL Cert
RUN openssl req -new -nodes -x509 -subj "/C=US/ST=Oregon/L=Portland/O=IT/CN=testhost" -days 3650 -keyout /etc/ssl/certs/pivportal.key -out /etc/ssl/certs/pivportal.crt -extensions v3_ca || true
RUN chown pivportal: /etc/ssl/certs/pivportal*
RUN chmod 440 /etc/ssl/certs/pivportal*

# Log file
RUN touch /var/log/pivportal.log && chmod 755 /var/log/pivportal.log && chown pivportal: /var/log/pivportal.log

# Entry Point
COPY ./docker-entrypoint.sh /sbin/
RUN chmod 755 /sbin/docker-entrypoint.sh
ENTRYPOINT ["/sbin/docker-entrypoint.sh"]
