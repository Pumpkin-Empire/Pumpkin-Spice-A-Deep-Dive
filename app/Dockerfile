FROM python:3.9.0-slim-buster
WORKDIR /code
COPY requirements.txt requirements.txt
RUN python3 -m pip install --upgrade pip
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2
RUN pip install -r requirements.txt
COPY .. .
CMD ["python3", "-m", "PumpkinEmpire"]