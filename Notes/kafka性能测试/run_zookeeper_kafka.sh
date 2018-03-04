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
  cd $ZPATH/bin
  echo "`./zkServer.sh start >/dev/null 2>&1`"
  echo "zookeeper started 1"
else
  cd $ZPATH/bin
  ZooErrorCheck="`./zkServer.sh status`"
  ZooError="`echo "$ZooErrorCheck"|grep Error`"
  if ["$ZooError" == ""]
  then
    echo "zookeeper started 2"
  else
    echo "`./zkServer.sh restart >/dev/null 2>&1`"
    echo "zookeeper started 3"
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
