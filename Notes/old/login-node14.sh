#!/bin/bash
#--------------------------------------------
# author：xugb
# email:xu.gb@outlook.com
#--------------------------------------------
net="`ping -c 2 baidu.com|grep received`"
if [ ${net:35:1} == 0 ]
then
    net_flag=true
else
    net_flag=false
fi

welcome="today: `date` \nnet is $net_flag"
echo -e $welcome

if [ $net_flag == true ]
then
    ssh -p 60014 xugb@node14
else
    echo "check your network please."
fi
