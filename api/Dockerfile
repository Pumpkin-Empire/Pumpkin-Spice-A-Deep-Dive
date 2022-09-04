FROM python:3.9.0-slim-buster
WORKDIR /code
COPY requirements.txt requirements.txt
RUN python3 -m pip install --upgrade pip
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2
RUN pip install -r requirements.txt
COPY .. .
#ARG HOSTNAME="database"
#ARG PORT="5432"
#ARG DBNAME="database"
#ARG UNAME="postgres"
#ARG PWD="docker"
CMD ["python3", "-m", "PumpkinEmpire"]