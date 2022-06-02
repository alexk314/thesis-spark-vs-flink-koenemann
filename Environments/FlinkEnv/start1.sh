#!/bin/bash
./bin/flink run -p 1 -c WordCount my_apps/flink-word-count_2.12-1.0.jar 9000
