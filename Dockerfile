FROM postgres:14

COPY ./db-init/*.sql /docker-entrypoint-initdb.d/

ENV POSTGRES_USER=sqlchallenge
ENV POSTGRES_PASSWORD=sqlchallenge
ENV POSTGRES_DB=sqlchallenge

EXPOSE 5432
