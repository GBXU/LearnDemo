# kafka

## 介绍
Kafka的[github](https://github.com/apache/kafka)和[官网](http://kafka.apache.org/)。
## 搭建
### 配置zookeeper 2181
zookeeper的配置要求参考[这处文档](https://zookeeper.apache.org/doc/current/zookeeperAdmin.html#sc_maintenance)

搭建主要参考[这篇教程](https://www.cnblogs.com/luotianshuai/p/5206662.html)。

### 配置kafka 9092
搭建主要参考[这篇教程](https://www.cnblogs.com/luotianshuai/p/5206662.html)及官方[tutorial](https://kafka.apache.org/quickstart)。

### 搭建出现的error及解决
* 出现warning

  查了[资料](https://www.cnblogs.com/subendong/p/7786547.html)发现没有配置下面这句`listeners = PLAINTEXT://node1:9092`
* 出现error

  查了[资料](http://blog.csdn.net/getyouwant/article/details/79000524)发现这是因为配置文件中的PLAINTEXT跟你请求的内容不同。举例来说，我在配置文件里配置的`listeners=PLAINTEXT://10.127.96.151:9092`，但是我想测试的时候请求的是`./kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic topic1 --from-beginning`

  正确的应该是`./kafka-console-consumer.sh --bootstrap-server 10.127.96.151:9092 --topic topic1 --from-beginning` ，或者都更改node14

* topics创建出错
  为主题生产/消费消息时，用node14，node15都可以，但是node16时候报`test1=LEADER_NOT_AVAILABLE`错误，此时`Leader: 14	Replicas: 16,14,15	Isr: 14,15`
  但是改成node14 node15 却没有问题，原因肯定在node16上
  查配置文件，发现所有node的`zoo.cfg`中 server把`node16`写成`ndoe16`,改正。

* 仍然接不上node16
  把所有zookeeper和kafka关闭，先启动所有zookeeper发现正常，再启动kafka的node16，查看主题没问题，producer发现有问题，根据error信息，是接不上node16，再启动node14，查看主题没问题，producer出现error是`no route to host`。检查`sudo firewall-cmd --state`  果然node16防火墙还在，而node14 node15都关了

  关闭防火墙
  `sudo systemctl stop firewalld.service`
  `sudo systemctl disable firewalld.service`
  参考[这里](http://blog.csdn.net/doctor_who2004/article/details/39567289)



## 运行
### 启动
* 启动zookeeper：所以节点
```shell
./zkServer.sh start
./zkServer.sh status
./zkServer.sh restart
```
* 启动kafka：所以节点
```shell
nohup ./kafka-server-start.sh -daemon ../config/server.properties >/dev/null 2>&1 &
./kafka-server-stop.sh
```
* jps：jps命令可以查看当前java进程

### 基本操作
* 新建主题:创建的时候replication不能超过broker，partition无所谓
```shell
./kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 3 --partitions 3 --topic test
```
* 查看主题
```shell
./kafka-topics.sh --list --zookeeper node14:2181
```
* 主题详情
```shell
./kafka-topics.sh --describe --zookeeper node14:2181 --topic test
```
* 创建发布者
```shell
./kafka-console-producer.sh --broker-list node14:9092 --topic test
```
* 创建消费者
```shell
./kafka-console-consumer.sh --bootstrap-server node14:9092 --topic test --from-beginning
```
* 删除主题：删除topic需要另外配置，可以参考[这篇帖子](http://blog.csdn.net/u010003835/article/details/53071882)。
```shell
./kafka-topics.sh --zookeeper node1:2181,node2:2181,node3:2181 --delete --topic "test"
```


***以上操作都运行成功，则搭建完成了。***

---

## 自带shell脚本测试
* 教程

  [官方测试教程](https://engineering.linkedin.com/kafka/benchmarking-apache-kafka-2-million-writes-second-three-cheap-machines)提供了kafka 0.8的测试思路。

  还参考以下资料：

  * http://blog.csdn.net/luoww1/article/details/70839727
  * http://blog.csdn.net/luoww1/article/details/70839727
  * http://blog.csdn.net/u013970991/article/details/52061794
  * https://www.cnblogs.com/xiaodf/p/6023531.html 【\*】

* 测试中可能需要调整jvm大小
>配置kafka /config/server.properties 文件
本地 KAFKA_HEAP_OPT="-Xmx2G"
sogon KAFKA_HEAP_OPT="-Xmx30G"


### producer
* 根据[这封邮件](https://mail-archives.apache.org/mod_mbox/kafka-users/201601.mbox/%3CCAE1jLMMb=NnRRfY9aynNNwy5uwffi8xKfr9TrtvBqG2J50exAQ@mail.gmail.com%3E)，得知kafka 0.9之后，不支持thread的配置，而需要multi process来运行。
* 在AWS测试，出现存储不够的问题，重新买机器,8g变为16g，再跑。可以`df -h`查看目前存储情况。要考虑`50000000*128/1024/1024/1024 = 5.96 G`每次测试产生的数据量。

### consumer

---
## java client
java client代码可以参考:
* http://blog.csdn.net/xj626852095/article/details/51711076
* http://orchome.com/303

### java client project出现的error及解决
* maven配置java client project以为更方便，没想到它的maven缺少了个log4j的jar包，运行出错又没有说是这个包的问题。在国外论坛看到别人说创建java project把包一个个放进去可以用，才发现有warning提示这个log4j。目前还不清楚maven的解决方案。
* terminal运行出错

  `javac -cp .:/libs/* src/com/exam/main/Main.java`
  `java -cp .:/libs/* bin/com/exam/main/Main`
