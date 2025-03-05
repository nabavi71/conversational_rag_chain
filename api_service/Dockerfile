FROM python:3.10

RUN apt-get update && apt-get -y install netcat-traditional && apt-get clean

RUN apt-get -y install nano
RUN apt-get -y install netbase

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app
COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["/usr/local/bin/python3.10", "/app/main.py"]