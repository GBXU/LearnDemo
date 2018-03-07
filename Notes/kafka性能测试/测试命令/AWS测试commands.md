# kafka-producer-perf-test.sh


思路：node1 生产， node2 消费
猜测：
线程增加，吞吐量增加
增加broker的个数，吞吐量增加

分区数越多，单线程生产者吞吐率越小。
备份数越多，吞吐率越低
异常产生数据比同步产生数据吞吐率高近3倍
批处理大小
消息长度
数据压缩


## 需要备份
受NIC影响， 三台机器都运行一个producer即可


## 不需要备份

### 主题
./kafka-topics.sh \
--create --zookeeper \
localhost:2181 \
--replication-factor 1 \
--partitions 6 \
--topic "test-1-6-50mil-010"

### 三台机器都运行1个producer
./kafka-producer-perf-test.sh \
--topic "test-1-6-50mil-010" \
--num-records 50000000 \
--record-size 128 \
--throughput 50000000 \
--producer-props \
bootstrap.servers=node1:9092,node2:9092,node3:9092 \
acks=0 \
compression.type=none

### 一台机器运行consumer
./kafka-consumer-perf-test.sh \
--broker-list node1:9092,node2:9092,node3:9092 \
--messages 150000000 \
--num-fetch-threads 1 \
--fetch-size 1048576 \
--threads 10 \
--topic "test-1-6-50mil-010"



########

8 bytes overhead for timestamp
compression throughput大 latency也大
compression最好增加user thread
