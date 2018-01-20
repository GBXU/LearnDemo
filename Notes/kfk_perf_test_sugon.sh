#!/bin/bash
#--------------------------------------------
# author:xugb
# email:xu.gb@outlook.com
#--------------------------------------------
ZPATH=/home/xugb/software/zookeeper/zookeeper-3.4.11
KPATH=/home/xugb/software/kafka/kafka_2.11-1.0.0

JPS="`jps`"
ZooFlag="`echo "$JPS"|grep QuorumPeerMain`"
KfkFlag="`echo "$JPS"|grep Kafka`"

if [ "$ZooFlag" == "" ]
then
  echo "starting up zookeeper"
  cd $ZPATH/bin
  echo "`./zkServer.sh start`"
else
  echo "zookeeper started"
fi

if [ "$KfkFlag" == "" ]
then
  echo "starting up Kafka"
  cd $KPATH/bin
  echo "`nohup ./kafka-server-start.sh -daemon ../config/server.properties >/dev/null 2>&1 &`"
else
  echo "kafka started"
fi
cd $KPATH/bin
TOPICLIST="`./kafka-topics.sh --list --zookeeper localhost:2181`"
TopicFlag="`echo "$TOPICLIST"|grep "test"`"
if [ "$TopicFlag" == "" ]
then
  echo "creating Topic "test""
  cd $KPATH/bin
  echo "`nohup ./kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 3 --partitions 3 --topic "test" >/dev/null 2>&1 &`"
else
  # echo "delete Topic "test""
  # ./kafka-topics.sh --zookeeper localhost:2181 --delete --topic "test" >/dev/null
  # echo "creating Topic "test""
  # echo "`nohup ./kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic test >/dev/null 2>&1 &`"
  echo "Topic "test" is created"
fi

echo "test the producer performance:"
# record size 增加， latency 吞吐num和size的影响
echo "record size -> "
echo "label 1 bytes:"
./kafka-producer-perf-test.sh --num-records 1000000 --record-size 1  --throughput 1000000000 --producer-props bootstrap.servers=node14:9092,node15:9092,node16:9092 --topic "test" |grep "1000000 records sent"
echo "label 64 bytes:"
./kafka-producer-perf-test.sh --num-records 500000000 --record-size 64  --throughput 1000000000 --producer-props bootstrap.servers=node14:9092,node15:9092,node16:9092 --topic "test"
echo "label 128 bytes:"
./kafka-producer-perf-test.sh --num-records 500000000 --record-size 128  --throughput 1000000000 --producer-props bootstrap.servers=node14:9092,node15:9092,node16:9092 --topic "test"
echo "label 256 bytes:"
./kafka-producer-perf-test.sh --num-records 500000000 --record-size 256  --throughput 1000000000 --producer-props bootstrap.servers=node14:9092,node15:9092,node16:9092 --topic "test"
echo "label 512 bytes:"
./kafka-producer-perf-test.sh --num-records 1000000 --record-size 512  --throughput 1000000000 --producer-props bootstrap.servers=node14:9092,node15:9092,node16:9092 --topic "test"
echo "label 1024 bytes:"
./kafka-producer-perf-test.sh --num-records 1000000 --record-size 1024  --throughput 1000000000 --producer-props bootstrap.servers=node14:9092,node15:9092,node16:9092 --topic "test"|grep "50000000 records sent"

# throughput 增加， latency 吞吐num和size的影响
echo "throughput -> "
echo "label throughput 1000000000:"
./kafka-producer-perf-test.sh --num-records 5000000 --record-size 128  --throughput 1000000000 --producer-props bootstrap.servers=node14:9092,node15:9092,node16:9092 --topic "test"
echo "label throughput 100000000:"
./kafka-producer-perf-test.sh --num-records 5000000 --record-size 128  --throughput 100000000 --producer-props bootstrap.servers=node14:9092,node15:9092,node16:9092 --topic "test"
echo "label throughput 10000000:"
./kafka-producer-perf-test.sh --num-records 5000000 --record-size 128  --throughput 10000000 --producer-props bootstrap.servers=node14:9092,node15:9092,node16:9092 --topic "test"
echo "label throughput 1000000:"
./kafka-producer-perf-test.sh --num-records 5000000 --record-size 128  --throughput 1000000 --producer-props bootstrap.servers=node14:9092,node15:9092,node16:9092 --topic "test"
echo "label throughput 100000:"
./kafka-producer-perf-test.sh --num-records 5000000 --record-size 128  --throughput 100000 --producer-props bootstrap.servers=node14:9092,node15:9092,node16:9092 --topic "test"
echo "label throughput 10000:"
./kafka-producer-perf-test.sh --num-records 5000000 --record-size 128  --throughput 10000 --producer-props bootstrap.servers=node14:9092,node15:9092,node16:9092 --topic "test"
# num records 增加， latency 吞吐num和size的影响
echo "num records -> "
echo "label num records 5000:"
./kafka-producer-perf-test.sh --num-records 5000 --record-size 128  --throughput 1000000000 --producer-props bootstrap.servers=node14:9092,node15:9092,node16:9092 --topic "test"
echo "label num records 50000:"
./kafka-producer-perf-test.sh --num-records 50000 --record-size 128  --throughput 1000000000 --producer-props bootstrap.servers=node14:9092,node15:9092,node16:9092 --topic "test"
echo "label num records 500000:"
./kafka-producer-perf-test.sh --num-records 500000 --record-size 128  --throughput 1000000000 --producer-props bootstrap.servers=node14:9092,node15:9092,node16:9092 --topic "test"
echo "label num records 5000000:"
./kafka-producer-perf-test.sh --num-records 5000000 --record-size 128  --throughput 1000000000 --producer-props bootstrap.servers=node14:9092,node15:9092,node16:9092 --topic "test"
echo "label num records 50000000:"
./kafka-producer-perf-test.sh --num-records 50000000 --record-size 128  --throughput 1000000000 --producer-props bootstrap.servers=node14:9092,node15:9092,node16:9092 --topic "test"
echo "label num records 500000000:"
./kafka-producer-perf-test.sh --num-records 500000000 --record-size 128  --throughput 1000000000 --producer-props bootstrap.servers=node14:9092,node15:9092,node16:9092 --topic "test"
# replication factor 增加， latency 吞吐num和size的影响
echo "replication factor -> "
echo "replication factor 1:"
./kafka-producer-perf-test.sh --num-records 50000000 --record-size 128  --throughput 1000000000 --producer-props bootstrap.servers=node14:9092,node15:9092,node16:9092 --topic "test-1-3"
echo "replication factor 2:"
./kafka-producer-perf-test.sh --num-records 50000000 --record-size 128  --throughput 1000000000 --producer-props bootstrap.servers=node14:9092,node15:9092,node16:9092 --topic "test-2-3"
echo "replication factor 3:"
./kafka-producer-perf-test.sh --num-records 50000000 --record-size 128  --throughput 1000000000 --producer-props bootstrap.servers=node14:9092,node15:9092,node16:9092 --topic "test-3-3"
# partition 增加， latency 吞吐num和size的影响
echo "partition -> "
echo "partition 3:"
./kafka-producer-perf-test.sh --num-records 50000000 --record-size 128  --throughput 1000000000 --producer-props bootstrap.servers=node14:9092,node15:9092,node16:9092 --topic "test-3-3"
echo "partition 4:"
./kafka-producer-perf-test.sh --num-records 50000000 --record-size 128  --throughput 1000000000 --producer-props bootstrap.servers=node14:9092,node15:9092,node16:9092 --topic "test-3-4"
echo "partition 5:"
./kafka-producer-perf-test.sh --num-records 50000000 --record-size 128  --throughput 1000000000 --producer-props bootstrap.servers=node14:9092,node15:9092,node16:9092 --topic "test-3-5"



echo "test the consumer performance:"
# messages 增加，性能
echo "messages ->"
echo "messages 5000:"
./kafka-consumer-perf-test.sh --broker-list node14:9092,node15:9092,node16:9092 --messages 5000 --num-fetch-threads 1 --fetch-size 1048576 --threads 10 --topic "test-3-3"
echo "messages 500000:"
./kafka-consumer-perf-test.sh --broker-list node14:9092,node15:9092,node16:9092 --messages 500000 --num-fetch-threads 1 --fetch-size 1048576 --threads 10 --topic "test-3-3"
echo "messages 50000000:"
./kafka-consumer-perf-test.sh --broker-list node14:9092,node15:9092,node16:9092 --messages 50000000 --num-fetch-threads 1 --fetch-size 1048576 --threads 10 --topic "test-3-3"

# num-fetch-threads增加，性能
echo "num-fetch-threads ->"
echo "num-fetch-threads 1:"
./kafka-consumer-perf-test.sh --broker-list node14:9092,node15:9092,node16:9092 --messages 50000000 --num-fetch-threads 1 --fetch-size 1048576 --threads 10 --topic "test-3-3"
echo "num-fetch-threads 2:"
./kafka-consumer-perf-test.sh --broker-list node14:9092,node15:9092,node16:9092 --messages 50000000 --num-fetch-threads 2 --fetch-size 1048576 --threads 10 --topic "test-3-3"
echo "num-fetch-threads 3:"
./kafka-consumer-perf-test.sh --broker-list node14:9092,node15:9092,node16:9092 --messages 50000000 --num-fetch-threads 3 --fetch-size 1048576 --threads 10 --topic "test-3-3"
# fetch-size 增加，性能
echo "fetch-size ->"
echo "fetch-size 32:"
./kafka-consumer-perf-test.sh --broker-list node14:9092,node15:9092,node16:9092 --messages 50000000 --num-fetch-threads 1 --fetch-size 32 --threads 10 --topic "test-3-3"
echo "fetch-size 64:"
./kafka-consumer-perf-test.sh --broker-list node14:9092,node15:9092,node16:9092 --messages 50000000 --num-fetch-threads 1 --fetch-size 64 --threads 10 --topic "test-3-3"
echo "fetch-size 128:"
./kafka-consumer-perf-test.sh --broker-list node14:9092,node15:9092,node16:9092 --messages 50000000 --num-fetch-threads 1 --fetch-size 128 --threads 10 --topic "test-3-3"
echo "fetch-size 1048576:"
./kafka-consumer-perf-test.sh --broker-list node14:9092,node15:9092,node16:9092 --messages 50000000 --num-fetch-threads 1 --fetch-size 1048576 --threads 10 --topic "test-3-3"
# threads 增加，性能
echo "threads ->"
echo "threads 10:"
./kafka-consumer-perf-test.sh --broker-list node14:9092,node15:9092,node16:9092 --messages 50000000 --num-fetch-threads 1 --fetch-size 1048576 --threads 10 --topic "test-3-3"
echo "threads 20:"
./kafka-consumer-perf-test.sh --broker-list node14:9092,node15:9092,node16:9092 --messages 50000000 --num-fetch-threads 1 --fetch-size 1048576 --threads 20 --topic "test-3-3"
echo "threads 30:"
./kafka-consumer-perf-test.sh --broker-list node14:9092,node15:9092,node16:9092 --messages 50000000 --num-fetch-threads 1 --fetch-size 1048576 --threads 30 --topic "test-3-3"
# replication factor 增加， 性能
echo "replication factor -> "
echo "replication factor 1:"
./kafka-consumer-perf-test.sh --broker-list node14:9092,node15:9092,node16:9092 --messages 50000000 --num-fetch-threads 1 --fetch-size 1048576 --threads 10 --topic "test-1-3"
echo "replication factor 2:"
./kafka-consumer-perf-test.sh --broker-list node14:9092,node15:9092,node16:9092 --messages 50000000 --num-fetch-threads 1 --fetch-size 1048576 --threads 10 --topic "test-2-3"
echo "replication factor 3:"
./kafka-consumer-perf-test.sh --broker-list node14:9092,node15:9092,node16:9092 --messages 50000000 --num-fetch-threads 1 --fetch-size 1048576 --threads 10 --topic "test-3-3"

# partition 增加， latency 吞吐num和size的影响
echo "partition -> "
echo "partition 3:"
./kafka-consumer-perf-test.sh --broker-list node14:9092,node15:9092,node16:9092 --messages 50000000 --num-fetch-threads 1 --fetch-size 1048576 --threads 10 --topic "test-3-3"
echo "partition 4:"
./kafka-consumer-perf-test.sh --broker-list node14:9092,node15:9092,node16:9092 --messages 50000000 --num-fetch-threads 1 --fetch-size 1048576 --threads 10 --topic "test-3-4"
echo "partition 5:"
./kafka-consumer-perf-test.sh --broker-list node14:9092,node15:9092,node16:9092 --messages 50000000 --num-fetch-threads 1 --fetch-size 1048576 --threads 10 --topic "test-3-5"

echo "finished $date goodnight"
# 1024bytes = 1 KB, 1048576bytes=1MB
# 在不同节点并行运行脚本？ consumer数
# producer和consumer同时运行？
# partition分布 ？

# ./kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic "test" --from-beginning
