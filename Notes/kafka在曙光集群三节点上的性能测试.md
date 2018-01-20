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
|001| 1   |  1  |  1 | 1 |  1000000  |  512 | 1000000000  | 296823(1.13)|19.29|
|002| 1   |  1  |  1 | 1 |  1000000  |  512 | 1000000000  | 474383(3.62)|17.20|
|003| 1   |  1  |  1 | 1 |  1000000  |  512 | 1000000000  | 483792(7.38)|12.99|
|004| 1   |  1  |  1 | 1 |  1000000  |  512 | 1000000000  | 271002(8.27)|587.22|
|005| 1   |  1  |  1 | 1 |  1000000  |  512 | 1000000000  | 301204(18.38)|672.97|
|006| 1   |  1  |  1 | 1 |  1000000  |  512 | 1000000000  | 207856(25.37)|811.35|
|007| 1   |  1  |  1 | 1 |  1000000  |  512 | 1000000000  | 121817(29.74)|887.94|
|008| 1   |  1  |  1 | 1 |  1000000  |  512 | 1000000000  | 64985(31.73)|924.36|
|009| 1   |  1  |  1 | 1 |  1000000  |  1024 | 1000000000  | 85171(83.18)|339.67|
|010| 1   |  1  |  1 | 1 |  1000000  |  2048  | 1000000000  | 51361(100.31)|273.01 |
|011| 1   |  1  |  1 | 1 |  1000000  |  4096  | 1000000000  | 21143(82.59)|288.22|




|编号|原始数据|
|:---:|:---:|
|001|1000000 records sent, 296823.983378 records/sec (1.13 MB/sec), 19.29 ms avg latency, 161.00 ms max latency, 14 ms 50th, 56 ms 95th, 77 ms 99th, 81 ms 99.9th.|
|002|1000000 records sent, 474383.301708 records/sec (3.62 MB/sec), 17.20 ms avg latency, 151.00 ms max latency, 10 ms 50th, 53 ms 95th, 83 ms 99th, 90 ms 99.9th.|
|003|1000000 records sent, 483792.936623 records/sec (7.38 MB/sec), 12.99 ms avg latency, 154.00 ms max latency, 10 ms 50th, 34 ms 95th, 48 ms 99th, 63 ms 99.9th.|
|004|1000000 records sent, 271002.710027 records/sec (8.27 MB/sec), 587.22 ms avg latency, 1193.00 ms max latency, 642 ms 50th, 1093 ms 95th, 1162 ms 99th, 1193 ms 99.9th.|
|005|1000000 records sent, 301204.819277 records/sec (18.38 MB/sec), 672.97 ms avg latency, 998.00 ms max latency, 754 ms 50th, 982 ms 95th, 994 ms 99th, 998 ms 99.9th.|
|006|1000000 records sent, 207856.994388 records/sec (25.37 MB/sec), 811.35 ms avg latency, 1205.00 ms max latency, 796 ms 50th, 1180 ms 95th, 1199 ms 99th, 1203 ms 99.9th.|
|007|1000000 records sent, 121817.517359 records/sec (29.74 MB/sec), 887.94 ms avg latency, 1243.00 ms max latency, 862 ms 50th, 1192 ms 95th, 1233 ms 99th, 1241 ms 99.9th.|
|008|1000000 records sent, 64985.703145 records/sec (31.73 MB/sec), 924.36 ms avg latency, 2252.00 ms max latency, 754 ms 50th, 1807 ms 95th, 2138 ms 99th, 2240 ms 99.9th.|
|009|1000000 records sent, 85171.620816 records/sec (83.18 MB/sec), 339.67 ms avg latency, 943.00 ms max latency, 241 ms 50th, 659 ms 95th, 881 ms 99th, 936 ms 99.9th.|
|010|1000000 records sent, 51361.068310 records/sec (100.31 MB/sec), 273.01 ms avg latency, 1104.00 ms max latency, 210 ms 50th, 608 ms 95th, 852 ms 99th, 1082 ms 99.9th.|
|011|1000000 records sent, 21143.437077 records/sec (82.59 MB/sec), 288.22 ms avg latency, 2351.00 ms max latency, 209 ms 50th, 760 ms 95th, 1414 ms 99th, 2159 ms 99.9th.|


### kfk\_perf\_test\_sugon
