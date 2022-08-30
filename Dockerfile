FROM postgres
ENV POSTGRES_PASSWORD docker
ENV POSTGRES_DB pumpkinempire
FROM python:3.9.0
WORKDIR //Users/nick/Python/PycharmProjects/Pumpkin-Spice-A-Deep-Dive
COPY requirements.txt requirements.txt
RUN python3 -m pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . .
CMD ["python3", "-m", "PumpkinEmpire"]