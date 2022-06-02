FROM openjdk:8-alpine
RUN apk --update add wget tar bash vim
RUN wget https://dlcdn.apache.org/spark/spark-3.2.1/spark-3.2.1-bin-hadoop3.2.tgz
RUN tar -xzf spark-3.2.1-bin-hadoop3.2.tgz && \
      mv spark-3.2.1-bin-hadoop3.2 /spark && \
      rm spark-3.2.1-bin-hadoop3.2.tgz

# Copy startup scripts:
COPY spark_startup.sh /

# Shared Settings:
ENV SPARK_LOG_DIR /opt/spark/logs

# Settings Master:
ENV SPARK_MASTER_PORT 7077
ENV SPARK_MASTER_WEBUI_PORT 8080
ENV SPARK_MASTER_LOG /opt/spark/logs/spark-master.out

# Settings Worker:
ENV SPARK_WORKER_WEBUI_PORT 8080
ENV SPARK_WORKER_PORT 7000
ENV SPARK_WORKER_LOG /opt/spark/logs/spark-worker.out
#TODO: Check why no data is written into log file

RUN mkdir -p $SPARK_LOG_DIR && \
touch $SPARK_MASTER_LOG && \
touch $SPARK_WORKER_LOG && \
ln -sf /dev/stdout $SPARK_MASTER_LOG && \
ln -sf /dev/stdout $SPARK_WORKER_LOG

# Modify hosts file and add hostnames:
#RUN echo "192.168.178.26 SparkMaster" >> etc/hosts && wget http://SparkMaster

EXPOSE 6066 7077 7000 8080 37663 36609 
#TODO: Probably delete 37x und 36x ports

CMD ["/bin/bash", "/spark_startup.sh"]
