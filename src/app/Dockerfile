FROM python:3.8.16-slim-buster

WORKDIR /app

COPY . /app

RUN pip3 install flask 

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]