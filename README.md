# Thesis Spark vs. Flink on heterogeneous hardware
## Documenation
See thesis_spark_vs_flink.pdf

## Cluster UI Flink
### Master UI Overview:
http://192.168.178.56:8081/

## Start Flink Application on JobManager Node:
- Open Shell on Master:
```bash
docker exec -it jobmanager /bin/sh
```
- Start own WordStream creator to send words and Flink App to consume (cluster needs to be started first):
```bash
python3 /Development/WordStreamCreator/word_stream_creator.py
./bin/flink run -c WordCount my_apps/flink-word-count_2.12-1.0.jar --9001 
```
- Start own Batch Application to process BatchWordCount on Flink cluster:
```bash
./bin/flink run -c WordCountBatch my_apps/flink-word-count_2.12-1.0.jar --stdout --input input_data/50MiB 
```
- Execute Batch processing of multiple experiements in jobmanager container:
```bash
sh start.sh
```
- View Result from APP:
```bash
tail log/flink-*-taskexecutor-*.out
```

## Setup Flink Cluster:
### Start local:
- Go to folder: Environments/FlinkEnv/bin
```bash
sh jobmanager.sh start-foreground
```
### Start docker:
- Go to folder: Environments/FlinkEnv/
```bash
docker-compose up 
```

# SPARK
## Cluster UI Spark
### Master UI Overview:
http://192.168.178.56:8080/
### Master UI Jobs
http://192.168.178.56:4040/jobs

## Start Spark Application on Master Node:
- Open Shell on Master:
```bash
docker exec -it spark-master bash
```
- Test application from Spark, replace MasterURL and number of tasks:
```bash
spark/bin/spark-submit --class org.apache.spark.examples.SparkPi   --master  spark://$(hostname):7077    --num-executors 1     --driver-memory 1g     --executor-memory 1g     --executor-cores 1     spark/examples/jars/spark-examples*.jar 100
```
## Start own Wordcount application
```bash
spark/bin/spark-submit --class WordCount --master spark://$(hostname):7077 --num-executors 1 /apps/spark-word-count_2.12-1.0.jar 1000 6
```
## Setup Spark Cluster:
### Build Docker Image worker:
```bash
sudo docker build -t pipi/spark:latest .
```
### Start Master:
- Go to folder: Environments/SparkEnv/
```bash
docker-compose up spark-master
```
### Start Worker
```bash
docker-compose up spark-worker-surface
```
