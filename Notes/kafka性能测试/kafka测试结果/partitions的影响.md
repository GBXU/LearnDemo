
---

1 producer 1consumer  test-1-1-50mil-002
producer

| | | | | ||
|---:|---:|---:|---:|---:|---:|---:|
|50000000 records sent, |375099.401341 records/sec |(45.79 MB/sec), |1.12 ms avg latency, |123.00 ms max latency|, 1 ms 50th, 4 ms 95th, 5 ms 99th, 16 ms 99.9th.|

consumer

|start.time, |end.time, |data.consumed.in.MB, |MB.sec, |data.consumed.in.nMsg, |nMsg.sec, |rebalance.time.ms, |fetch.time.ms, |fetch.MB.sec, |fetch.nMsg.sec|
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
|2018-03-04 14:27:56:087, |2018-03-04 14:29:49:036, |6103.5156, |54.0378, |50000000, |442677.6687, |16, |112933, |54.0455, |442740.3859|
---

1 producer 1consumer  test-1-2-50mil-008
producer

| | | | | ||
|---:|---:|---:|---:|---:|---:|---:|
|50000000 records sent, |475127.096498 records/sec |(58.00 MB/sec), |1.79 ms avg latency, |148.00 ms max latency, |0 ms 50th, 5 ms 95th, 10 ms 99th, 84 ms 99.9th.
|

consumer

|start.time, |end.time, |data.consumed.in.MB, |MB.sec, |data.consumed.in.nMsg, |nMsg.sec, |rebalance.time.ms, |fetch.time.ms, |fetch.MB.sec, |fetch.nMsg.sec|
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
|2018-03-06 07:30:31:023, |2018-03-06 07:32:16:124,| 6103.5156, |58.0729, |50000000, |475732.8665, |59,| 105042, |58.1055, |476000.0762|
---

1 producer 1consumer  test-1-3-50mil
producer

| | | | | |
|---:|---:|---:|---:|---:|---:|
|50000000 records sent, |499575.360943 records/sec |(60.98 MB/sec), |0.36 ms avg latency, |138 max latency.|

consumer

|start.time, |end.time, |data.consumed.in.MB, |MB.sec, |data.consumed.in.nMsg, |nMsg.sec, |rebalance.time.ms, |fetch.time.ms, |fetch.MB.sec, |fetch.nMsg.sec|
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
|2018-03-04 14:11:34:479, |2018-03-04 14:12:51:968, |6103.5156, |78.7662, |50000000, |645252.8746, |68, |77421, |78.8354, |645819.6097|
---

1 producer 1consumer  test-1-4-50mil
producer

| | | | | |
|---:|---:|---:|---:|---:|---:|
|50000000 records sent, |519032.937830 records/sec |(63.36 MB/sec), |0.38 ms avg latency, |142.00 ms max latency, |0 ms 50th, 1 ms 95th, 4 ms 99th, 15 ms 99.9th.|

consumer

|start.time, |end.time, |data.consumed.in.MB, |MB.sec, |data.consumed.in.nMsg, |nMsg.sec, |rebalance.time.ms, |fetch.time.ms, |fetch.MB.sec, |fetch.nMsg.sec|
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
|2018-03-06 07:38:29:250, |2018-03-06 07:39:59:701,| 6103.5156, |67.4787, |50000000, |552785.4861, |44, |90407, 67.5115, |553054.5201|
---

1 producer 1consumer  test-1-5-50mil-003
producer

| | | | | ||
|---:|---:|---:|---:|---:|---:|---:|
|50000000 records sent, |496770.988574 records/sec |(60.64 MB/sec), |0.38 ms avg latency, |150.00 ms max latency, |0 ms 50th, 2 ms 95th, 8 ms 99th, 36 ms 99.9th.|

consumer

|start.time, |end.time, |data.consumed.in.MB, |MB.sec, |data.consumed.in.nMsg, |nMsg.sec, |rebalance.time.ms, |fetch.time.ms, |fetch.MB.sec, |fetch.nMsg.sec|
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
|2018-03-04 14:35:21:499, |2018-03-04 14:36:55:047, |6103.5156, |65.2447, |50000000, |534484.9703, |15, |93533, |65.2552, |534570.6863|
---

1 producer 1consumer  test-1-6-50mil-003
producer

| | | | | ||
|---:|---:|---:|---:|---:|---:|---:|
|50000000 records sent, |529818.166405 records/sec |(64.68 MB/sec), |0.34 ms avg latency, |136.00 ms max latency, |0 ms 50th, 1 ms 95th, 5 ms 99th, 22 ms 99.9th. |

consumer

|start.time, |end.time, |data.consumed.in.MB, |MB.sec, |data.consumed.in.nMsg, |nMsg.sec, |rebalance.time.ms, |fetch.time.ms, |fetch.MB.sec, |fetch.nMsg.sec|
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
|2018-03-06 07:43:36:927, |2018-03-06 07:45:06:077,| 6103.5156, |68.4634, |50000000, |560852.4958, |20, |89130, |68.4788, |560978.3462 |
---
试验发现partitions 3最优
