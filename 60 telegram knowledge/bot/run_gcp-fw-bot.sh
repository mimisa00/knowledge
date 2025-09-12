#!/bin/bash

ap_name=gcp-fw-bot

##################
#                #
# docker trigger #
#                #
##################
if docker ps -a | grep ${ap_name}$; then
  docker rm -f ${ap_name}
  docker rmi $ap_name:latest
fi

docker build -t ${ap_name}:latest /home/fusion-ap/${ap_name}/
docker run -d \
  --name ${ap_name} \
  --restart=always --log-opt max-size=10m --log-opt max-file=10 \
  -e TELEGRAM_TOKEN="6395609***:***" \
  -e API_URL="https://fw-trigger-whitelist-"****.asia-east1.run.app" \
  -e API_AUTH="Bearer ***" \
  -e ALLOWED_CHAT_IDS="****" \
  -e ALLOWED_USERS="123","456" \
  -v /home/fusion-ap/${ap_name}/coms.txt:/app/coms.txt \
  -v /home/fusion-ap/${ap_name}/bot.py:/app/bot.py \
  -v /home/fusion-ap/${ap_name}/fw.log:/app/fw.log \
  ${ap_name}:latest

