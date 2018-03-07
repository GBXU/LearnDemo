m4.2xlarge
(26 ECU,
  8 vCPU, 2.4 GHz, Intel Xeon E5-2676v3,
  32 GiB 内存,
  仅限于 EBS)

最大带宽 (Mbps) 1000
最大吞吐量 (MB/s，128 KB I/O) 125
参考[文档](https://docs.aws.amazon.com/zh_cn/AWSEC2/latest/UserGuide/ebs-ec2-config.html)
---

1 producer 1consumer  test-1-3-50mil
producer

| | | |  ||id|
|---:|---:|---:|---:|---:|---:|---:|
|50000000 records sent, |499575.360943 records/sec |(60.98 MB/sec), |0.36 ms avg latency, |138 max latency.|node1|

consumer

|start.time, |end.time, |data.consumed.in.MB, |MB.sec, |data.consumed.in.nMsg, |nMsg.sec, |rebalance.time.ms, |fetch.time.ms, |fetch.MB.sec, |fetch.nMsg.sec|id|
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
|2018-03-04 14:11:34:479, |2018-03-04 14:12:51:968, |6103.5156, |78.7662, |50000000, |645252.8746, |68, |77421, |78.8354, |645819.6097|node2|
---


2 producer 1consumer  test-1-3-50mil-004
producer

| | | | | ||id|
|---:|---:|---:|---:|---:|---:|---:|
|50000000 records sent, |468033.323973 records/sec |(57.13 MB/sec), |0.95 ms avg latency, |168.00 ms max latency, |0 ms 50th, 5 ms 95th, 10 ms 99th, 33 ms 99.9th.|node1|
|50000000 records sent, |461816.972697 records/sec |(56.37 MB/sec), |0.91 ms avg latency, |201.00 ms max latency, |0 ms 50th, 4 ms 95th, 10 ms 99th, 74 ms 99.9th.|node3|
consumer

|start.time, |end.time, |data.consumed.in.MB, |MB.sec, |data.consumed.in.nMsg, |nMsg.sec, |rebalance.time.ms, |fetch.time.ms, |fetch.MB.sec, |fetch.nMsg.sec|id|
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
|2018-03-04 15:49:57:442, |2018-03-04 15:50:52:589, |6103.5415, |110.6777, |50000212, |906671.4780, |64, |55083, |110.8063, |907724.9242|node2|
---

3 producer 1consumer  test-1-3-50mil-005
producer

| | | | | ||id |
|---:|---:|---:|---:|---:|---:|---:|
|50000000 records sent, |416184.586188 records/sec |(50.80 MB/sec), |2.46 ms avg latency, |159.00 ms max latency, |1 ms 50th, 11 ms 95th, 24 ms 99th, 52 ms 99.9th.|node1|
|50000000 records sent, |418053.209813 records/sec |(51.03 MB/sec), |2.20 ms avg latency, |159.00 ms max latency, |1 ms 50th, 10 ms 95th, 19 ms 99th, 39 ms 99.9th.|node3|
|50000000 records sent, |413760.002648 records/sec |(50.51 MB/sec), |1.86 ms avg latency, |157.00 ms max latency, |0 ms 50th, 9 ms 95th, 16 ms 99th, 34 ms 99.9th.|node2|

|start.time, |end.time, |data.consumed.in.MB, |MB.sec, |data.consumed.in.nMsg, |nMsg.sec, |rebalance.time.ms, |fetch.time.ms, |fetch.MB.sec, |fetch.nMsg.sec|id|
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
|2018-03-04 15:57:46:310, |2018-03-04 15:58:29:516, |6103.5684, |141.2667, |50000432, |1157256.6773, |55, |43151, |141.4467, |1158731.7096|node2|
---


4 producer 1consumer  test-1-3-50mil-006
producer

| | | | | ||id |
|---:|---:|---:|---:|---:|---:|---:|
|50000000 records sent, |362355.601293 records/sec |(44.23 MB/sec), |4.49 ms avg latency, |150.00 ms max latency, |2 ms 50th, 18 ms 95th, 36 ms 99th, 61 ms 99.9th.|node1|
|50000000 records sent, |365566.555047 records/sec |(44.62 MB/sec), |4.36 ms avg latency, |265.00 ms max latency, |1 ms 50th, 17 ms 95th, 48 ms 99th, 67 ms 99.9th.|node1|
|50000000 records sent, |392449.275931 records/sec |(47.91 MB/sec), |10.16 ms avg latency, |268.00 ms max latency, |2 ms 50th, 50 ms 95th, 151 ms 99th, 244 ms 99.9th.|node3|
|50000000 records sent, |378486.809735 records/sec |(46.20 MB/sec), |15.63 ms avg latency, |415.00 ms max latency, |3 ms 50th, 62 ms 95th, 317 ms 99th, 384 ms 99.9th.|node2|

|start.time, |end.time, |data.consumed.in.MB, |MB.sec, |data.consumed.in.nMsg, |nMsg.sec, |rebalance.time.ms, |fetch.time.ms, |fetch.MB.sec, |fetch.nMsg.sec|id|
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
|2018-03-04 16:25:58:059, |2018-03-04 16:26:45:523,| 6103.5267, |128.5928, |50000091, |1053431.8852, |89, |47375, |128.8343, |1055410.8918|node2|
---


5 producer 1consumer  test-1-3-50mil-007
producer

| | | | | ||id |
|---:|---:|---:|---:|---:|---:|---:|
|50000000 records sent, |244498.777506 records/sec |(29.85 MB/sec), |7.58 ms avg latency, |408.00 ms max latency, |2 ms 50th, 32 ms 95th, 78 ms 99th, 307 ms 99.9th.|node1|
|50000000 records sent, |244171.623351 records/sec |(29.81 MB/sec), |7.17 ms avg latency, |363.00 ms max latency, |1 ms 50th, 32 ms 95th, 74 ms 99th, 223 ms 99.9th.|node1|
|50000000 records sent, |347381.438715 records/sec |(42.40 MB/sec), |12.48 ms avg latency, |386.00 ms max latency, |6 ms 50th, 46 ms 95th, 103 ms 99th, 269 ms 99.9th.|node3|
|50000000 records sent, |340541.460923 records/sec |(41.57 MB/sec), |17.75 ms avg latency, |829.00 ms max latency, |6 ms 50th, 62 ms 95th, 154 ms 99th, 686 ms 99.9th.|node3|
|50000000 records sent, |371650.499870 records/sec |(45.37 MB/sec), |10.32 ms avg latency, |341.00 ms max latency, |4 ms 50th, 41 ms 95th, 89 ms 99th, 208 ms 99.9th.|node2|


|start.time, |end.time, |data.consumed.in.MB, |MB.sec, |data.consumed.in.nMsg, |nMsg.sec, |rebalance.time.ms, |fetch.time.ms, |fetch.MB.sec, |fetch.nMsg.sec|id|
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
|2018-03-04 16:53:43:342, |2018-03-04 16:56:13:979,| 18310.5511, |121.5541, |150000035, |995771.5236, |677, |149960, |122.1029, |1000266.9712|node2|
---
