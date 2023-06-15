FROM python:3.11.4-slim

WORKDIR /

COPY . .

RUN apt-get update

RUN apt-get install -y supervisor

RUN pip install -r requirements.txt --no-cache-dir

ENTRYPOINT ["supervisord","-c","./service_script.conf"]
