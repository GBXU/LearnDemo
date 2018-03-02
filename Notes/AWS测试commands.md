# kafka-producer-perf-test.sh
./kafka-producer-perf-test.sh
--topic TOPIC
--num-records 500000000
--throughput 50000000000
--producer-props
  bootstrap.servers=node1:9092,node2:9092,node3:9092
  acks=0
  compression.type=[none, gzip, snappy, or lz4]
--record-size 128
## 需要备份

受NIC影响， 三台机器都运行一个producer
## 不需要备份
三台机器都运行若干个producer
