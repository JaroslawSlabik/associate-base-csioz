FROM ubuntu:16.04

#Install packages
RUN apt-get update && apt-get upgrade
RUN apt-get --yes --force-yes install python3 g++ python3-pip python3-django postgresql postgresql-contrib libpq-dev
RUN pip3 install --upgrade pip
RUN pip3 install psycopg2 django==1.8


#Configure postgresql
USER postgres
RUN /etc/init.d/postgresql start && psql --command "CREATE USER docker WITH SUPERUSER PASSWORD 'docker';" && createdb -O docker docker
RUN echo "host all  all    0.0.0.0/0  md5" >> /etc/postgresql/9.5/main/pg_hba.conf
RUN echo "listen_addresses='*'" >> /etc/postgresql/9.5/main/postgresql.conf
EXPOSE 5432
EXPOSE 8000
CMD ["/usr/lib/postgresql/9.5/bin/postgres", "-D", "/var/lib/postgresql/9.5/main", "-c", "config_file=/etc/postgresql/9.5/main/postgresql.conf"]

