FROM python:latest

WORKDIR /app

ADD requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

ENTRYPOINT ["./docker_entrypoint.sh"]