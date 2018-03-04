# 解读
# kafka performance tet on the GPU cluster

the points:
* easy to get good throughput in MB/sec if messages are large
*

## Producer Throughput
### Single producer thread, no replication
MB/sec not include the overhead  => 1 gigabit NIC is enough
* linear disk I/O
* batch together

### Single producer thread, 3x asynchronous replication

### Single producer thread, 3x synchronous replication
acks -1无确认 0 leader确认 1 follower确认
replicas 影响write整体能力，不影响client性能 本质就多了consumer取数据而已

### Three producers, 3x async replication
1.0Gbps=1024Mbps=128MB/s 因此NIC饱和。要通过每个machine跑一个producer而不能进程
是否是 全双工双绞线网络 上下传不影响

2,024,032/(786,980×3) = 0.857
### Producer Throughput Versus Stored Data
这个实验啥说明总数据很大的时候 系统还是很稳定 ，不会因为要写到磁盘而影响
其他messages system 在memory的时候效果好，但是stored data时候波动很大

## Consumer Throughput
replicas不会影响consumer
acks 不影响 only read fully acknowledged messages
### Single Consumer
测试是真实IO 但是实际上一般都是pageache中完成，因此kafka的consumer和replication都是cheap的
### Three Consumers
几乎是linear scaling 很好的效果啊
2,615,968/(940,521×3) = 0.927
### Producer and Consumer
replicas其实就啥做同样的事情
这时候看的是 consumer的throughput，这是producer的实际上限。
几乎和producer一样，因为consumer is cheap
## Effect of Message Size
smaller messages are the harder problems - overhead
两张图
size越大 reconds/s 越少
size越大 MB/s 越大 直到NIC限制 100MB/s 这儿我的理解 应该要acks为1 才能用NIC限制zookeeper和kafka在同一台machine的环境
## End-to-end Latency
有测试函数
看了下 应该是要写另外的代码来调用了

reference:

[配置参数解释](https://www.cnblogs.com/yinchengzhe/p/5111635.html)，
[commands](https://gist.github.com/jkreps/c7ddb4041ef62a900e6c)，
[tutorial](https://engineering.linkedin.com/kafka/benchmarking-apache-kafka-2-million-writes-second-three-cheap-machines)


```shell
# benchmark commands
Producer

Setup
bin/kafka-topics.sh --zookeeper esv4-hcl197.grid.linkedin.com:2181 --create --topic test-rep-one --partitions 6 --replication-factor 1
bin/kafka-topics.sh --zookeeper esv4-hcl197.grid.linkedin.com:2181 --create --topic test --partitions 6 --replication-factor 3

Single thread, no replication

bin/kafka-run-class.sh org.apache.kafka.clients.tools.ProducerPerformance test7 50000000 100 -1 acks=1 bootstrap.servers=esv4-hcl198.grid.linkedin.com:9092 buffer.memory=67108864 batch.size=8196

Single-thread, async 3x replication

bin/kafktopics.sh --zookeeper esv4-hcl197.grid.linkedin.com:2181 --create --topic test --partitions 6 --replication-factor 3
bin/kafka-run-class.sh org.apache.kafka.clients.tools.ProducerPerformance test6 50000000 100 -1 acks=1 bootstrap.servers=esv4-hcl198.grid.linkedin.com:9092 buffer.memory=67108864 batch.size=8196

Single-thread, sync 3x replication

bin/kafka-run-class.sh org.apache.kafka.clients.tools.ProducerPerformance test 50000000 100 -1 acks=-1 bootstrap.servers=esv4-hcl198.grid.linkedin.com:9092 buffer.memory=67108864 batch.size=64000

Three Producers, 3x async replication
bin/kafka-run-class.sh org.apache.kafka.clients.tools.ProducerPerformance test 50000000 100 -1 acks=1 bootstrap.servers=esv4-hcl198.grid.linkedin.com:9092 buffer.memory=67108864 batch.size=8196

Throughput Versus Stored Data

bin/kafka-run-class.sh org.apache.kafka.clients.tools.ProducerPerformance test 50000000000 100 -1 acks=1 bootstrap.servers=esv4-hcl198.grid.linkedin.com:9092 buffer.memory=67108864 batch.size=8196

Effect of message size

for i in 10 100 1000 10000 100000;
do
echo ""
echo $i
bin/kafka-run-class.sh org.apache.kafka.clients.tools.ProducerPerformance test $((1000*1024*1024/$i)) $i -1 acks=1 bootstrap.servers=esv4-hcl198.grid.linkedin.com:9092 buffer.memory=67108864 batch.size=128000
done;

Consumer
Consumer throughput

bin/kafka-consumer-perf-test.sh --zookeeper esv4-hcl197.grid.linkedin.com:2181 --messages 50000000 --topic test --threads 1

3 Consumers

On three servers, run:
bin/kafka-consumer-perf-test.sh --zookeeper esv4-hcl197.grid.linkedin.com:2181 --messages 50000000 --topic test --threads 1

End-to-end Latency

bin/kafka-run-class.sh kafka.tools.TestEndToEndLatency esv4-hcl198.grid.linkedin.com:9092 esv4-hcl197.grid.linkedin.com:2181 test 5000

Producer and consumer

bin/kafka-run-class.sh org.apache.kafka.clients.tools.ProducerPerformance test 50000000 100 -1 acks=1 bootstrap.servers=esv4-hcl198.grid.linkedin.com:9092 buffer.memory=67108864 batch.size=8196

bin/kafka-consumer-perf-test.sh --zookeeper esv4-hcl197.grid.linkedin.com:2181 --messages 50000000 --topic test --threads 1
```
