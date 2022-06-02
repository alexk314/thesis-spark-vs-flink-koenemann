#!/bin/bash

echo "build new Jar..."
sbt clean package

echo "remove Old jar file..."
rm -f ../../Environments/FlinkEnv/flink-1.14.4/my_apps/flink-word-count_2.12-1.0.jar
rm -f ../../Environments/FlinkEnv/my_apps/flink-word-count_2.12-1.0.jar

echo "copy new .jar file..."
cp target/scala-2.12/flink-word-count_2.12-1.0.jar ../../Environments/FlinkEnv/flink-1.14.4/my_apps/flink-word-count_2.12-1.0.jar
cp target/scala-2.12/flink-word-count_2.12-1.0.jar ../../Environments/FlinkEnv/my_apps/flink-word-count_2.12-1.0.jar

echo "finished compiling and copying process!"