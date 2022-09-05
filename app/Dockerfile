FROM python:3.9.0-slim-buster
WORKDIR /app
COPY requirements.txt requirements.txt
RUN python3 -m pip install --upgrade pip
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2
RUN pip install -r requirements.txt
COPY .. .
ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
