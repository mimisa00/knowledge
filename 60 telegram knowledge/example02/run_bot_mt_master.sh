#!/bin/bash
# Master 機器啟動腳本

ap_name=mt_master

##################
#                #
# docker trigger #
#                #
##################
if docker ps -a | grep ${ap_name}$; then
  docker rm -f ${ap_name}
fi

mkdir -p /opt/mt-script/mt-bot-service/queue
mkdir -p /opt/mt-script/mt-bot-service/results
mkdir -p /opt/mt-script/mt-bot-service/history

docker run -d \
 --name $ap_name  \
 --restart always \
 -e TELEGRAM_TOKEN="abc:efg"                                                     \
 -e ALLOWED_CHAT_IDS="-1234567890"                                               \
 -e ALLOWED_USERS="0123456789","9876543210"                                      \
 -v /opt/mt-script/mt-bot-service/host_list.txt:/opt/mt-script/host_list.txt     \
 -v /opt/mt-script/mt-bot-service/queue:/opt/mt-script/queue                     \
 -v /opt/mt-script/mt-bot-service/results:/opt/mt-script/results                 \
 -v /opt/mt-script/mt-bot-service/history:/opt/mt-script/history                 \
 -v /opt/mt-script/mt-bot-service/master_bot.py:/app/master_bot.py               \
mt-bot-service python3 master_bot.py


