FROM alpine:3.5
MAINTAINER "Joan Ardiaca Jové"

# Base packages
RUN apk add --no-cache apache2 python3
RUN ln -s /usr/bin/python3.5 /usr/bin/python

# Code
RUN mkdir /var/www/finem_imperii
WORKDIR /var/www/finem_imperii
ADD . .
RUN pip3 install -r requirements.txt

# Application
RUN rm finem_imperii/db.sqlite3 || true
RUN ./db_create.sh
RUN finem_imperii/manage.py collectstatic --no-input

# Apache
RUN rm /etc/apache2/conf.d/languages.conf /etc/apache2/conf.d/userdir.conf /etc/apache2/conf.d/info.conf
RUN cp devops/mod_wsgi.conf devops/finem_imperii_vhost.conf /etc/apache2/conf.d
RUN cp devops/mod_wsgi.so /usr/lib/apache2/mod_wsgi.so
RUN mkdir /run/apache2

CMD devops/alpine_entry.sh
