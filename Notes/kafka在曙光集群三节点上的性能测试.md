# kafka在曙光集群三节点上的性能测试
标签（空格分隔）： kafka 实验测试
---

## 主要参数

### 环境
三个节点，每个节点有1个`broker`。
曙光集群单节点

|CPU| mem | disk | Ethernet|
|:-:|:-:|:-:|:-:|
|Intel(R) Xeon(R) CPU E5-2650 v4 @ 2.20GHz with 12 cores *48|62.6GB|12000GB|56000Mb/s 1000Mb/s|

### 创建主题的相关参数

| 参数 | 值   |  影响  |
| ---:| ----:  | :----:  |
| `topic`|    test    |  无  |
| `replication factor`  | 3 |   -    |
| `partition`|   3   |  并行效果    |

### 测试的相关参数

| 参数 | 值   |  影响  |
| ---:| ----:  | :----:  |
| `num records`|    500000    |  - |
| `record size`  | 3000 |   -    |
| `throughput`|   1000   |  -    |

## 实验思路
1 创建多个topic，每个topic的partition不同，replication factor不同
2 numrecords，record size,throughput等变化。

producer情况：

|单节点broker数|topic备份数|topic分区|producer数|num records|record size|throughput限制|影响|
|:---:|:----:|:----:|:----:|:----:|:----:|
|    |    |   |  |    |    |   | -  |

consumer情况：

|单节点broker数|topic备份数|topic分区|consumer数|message总量|num-fetch-threads|fetch-size|threads|影响|
|:---:|:----:|:----:|:----:|:---:|:----:|:----:|:----:|:----:|
|    |    |    |    |    |    |    |    | -  |

## 实验运行情况

### kfk\_perf\_test\_local
本地 单机

|编号|单节点broker数|replication|partition|producer数|num records|record size(bytes)|throughput限制|records/sec(MB/s)|latency(ms)|
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
|001| 1   |  1  |  1 | 1 |  1000000  |  4096  | 1000000000  | 21143(82.59)|288.22|
|002| 1   |  1  |  1 | 1 |  1000000  |  2048  | 1000000000  | 51361(100.31)|273.01 |
|003| 1   |  1  |  1 | 1 |  1000000  |  1024 | 1000000000  | 85171(83.18)|339.67|

|编号|原始数据|
|:---:|:---:|
|001|1000000 records sent, 21143.437077 records/sec (82.59 MB/sec), 288.22 ms avg latency, 2351.00 ms max latency, 209 ms 50th, 760 ms 95th, 1414 ms 99th, 2159 ms 99.9th.|
|002|1000000 records sent, 51361.068310 records/sec (100.31 MB/sec), 273.01 ms avg latency, 1104.00 ms max latency, 210 ms 50th, 608 ms 95th, 852 ms 99th, 1082 ms 99.9th.|
|003|1000000 records sent, 85171.620816 records/sec (83.18 MB/sec), 339.67 ms avg latency, 943.00 ms max latency, 241 ms 50th, 659 ms 95th, 881 ms 99th, 936 ms 99.9th.|

### kfk\_perf\_test\_sugon
