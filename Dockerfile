FROM bitnami/spark:3.3 

COPY requeriments.txt . 

RUN pip3 install -r requeriments.txt --no-cache-dir
