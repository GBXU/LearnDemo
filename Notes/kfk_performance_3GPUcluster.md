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
[!配置参数解释](https://www.cnblogs.com/yinchengzhe/p/5111635.html)
[!commands](https://gist.github.com/jkreps/c7ddb4041ef62a900e6c)
[!tutorial](https://engineering.linkedin.com/kafka/benchmarking-apache-kafka-2-million-writes-second-three-cheap-machines)
