FROM python:3.8-slim-buster
RUN apt-get update
 
WORKDIR /src
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
ENV DASH_DEBUG_MODE True

EXPOSE 8050

CMD [ "python3", "src/dash/app.py"]