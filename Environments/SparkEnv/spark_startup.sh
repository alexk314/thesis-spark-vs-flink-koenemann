#!/bin/bash

export SPARK_HOME=/spark
export SPARK_MASTER_HOST=${SPARK_MASTER_HOST:-$(hostname)} #TODO: Check what this does...

. "/spark/sbin/spark-config.sh"

. "/spark/bin/load-spark-env.sh"

# When the spark work_load is master run class org.apache.spark.deploy.master.Master
if [ "$SPARK_WORKLOAD" == "master" ];
then

export SPARK_MASTER_HOST=$(hostname)

echo "Startup master Node... Name of SPARK_MASTER_HOST: $SPARK_MASTER_HOST"

# TODO: Check settings of Master Deploy adress
cd /spark/bin && ./spark-class org.apache.spark.deploy.master.Master --ip "$SPARK_MASTER_HOST" --port $SPARK_MASTER_PORT --webui-port "$SPARK_MASTER_WEBUI_PORT" >> "$SPARK_MASTER_LOG"

elif [ "$SPARK_WORKLOAD" == "worker" ];
then
echo "startup worker Node..."
cd /spark/bin && ./spark-class org.apache.spark.deploy.worker.Worker --webui-port "$SPARK_WORKER_WEBUI_PORT" "$SPARK_MASTER" >> "$SPARK_WORKER_LOG"

#TODO: CHeck what this does...
elif [ "$SPARK_WORKLOAD" == "submit" ];
then
    echo "SPARK SUBMIT"
else
    echo "Undefined Workload Type $SPARK_WORKLOAD, must specify: master, worker, submit"
fi