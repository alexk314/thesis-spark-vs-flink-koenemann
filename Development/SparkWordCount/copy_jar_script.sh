#!/bin/bash

echo "build new Jar..."
sbt clean package

echo "remove Old jar file..."
rm -f ../../Environments/SparkEnv/apps/spark-word-count_2.12-1.0.jar

echo "copy new .jar file..."
cp target/scala-2.12/spark-word-count_2.12-1.0.jar ../../Environments/SparkEnv/apps/spark-word-count_2.12-1.0.jar