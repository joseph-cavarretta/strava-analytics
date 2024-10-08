FROM python:3.12.1

WORKDIR /app

ADD requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

ENTRYPOINT ["./docker_entrypoint.sh"]