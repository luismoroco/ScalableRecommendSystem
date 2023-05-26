FROM python:3.8.16-slim-buster

WORKDIR /app

COPY requeriments.txt /app 

RUN pip3 install -r requeriments.txt --no-cache-dir

COPY . /app

CMD [ "python3", "main.py" ]