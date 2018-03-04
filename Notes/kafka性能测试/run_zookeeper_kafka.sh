#!/bin/bash
#--------------------------------------------
# author:gb.xu
# email:gb.xu@outlook.com
#--------------------------------------------

ZPATH=/home/ubuntu/app/zookeeper/zookeeper-3.4.11
KPATH=/home/ubuntu/app/kafka/kafka_2.11-1.0.0

JPS="`jps`"
ZooFlag="`echo "$JPS"|grep QuorumPeerMain`"
KfkFlag="`echo "$JPS"|grep Kafka`"

if [ "$ZooFlag" == "" ]
then
  echo "starting up zookeeper"
  cd $ZPATH/bin
  echo "`./zkServer.sh start`"
else
  ZooErrorCheck="`./app/zookeeper/zookeeper-3.4.11/bin/zkServer.sh status`"
  ZooError="`echo "$ZooErrorCheck"|grep Error`"
  if ["$ZooError" == ""]; then
    echo "zookeeper started"
  else
    echo "`./app/zookeeper/zookeeper-3.4.11/bin/zkServer.sh restart`"
    echo "zookeeper started"
  fi
fi

if [ "$KfkFlag" == "" ]
then
  echo "starting up Kafka"
  cd $KPATH/bin
  echo "`nohup ./kafka-server-start.sh -daemon ../config/server.properties >/dev/null 2>&1 &`"
else
  echo "kafka started"
fi
