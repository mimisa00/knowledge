#!/bin/bash
#############
#           #
# run nginx #
#           #
#############
ap_name="http"
fd_name="/home/project"

#######################################
#                                     #
# 如果系統運作中，要重建容器前需檢測  #
# proxy 內容是否正確，若內容不正確，  #
# 則取消重啟                          #
#                                     #
#######################################
if docker ps | grep " ${ap_name}$"; then
  
  docker cp $fd_name/$ap_name/conf/default.conf $ap_name:/tmp/default.conf
  docker cp $fd_name/$ap_name/conf/proxy.conf   $ap_name:/tmp/proxy.conf
  docker cp $fd_name/$ap_name/conf/nginx.conf   $ap_name:/tmp/nginx.conf
  docker exec $ap_name bash -c "cat /tmp/default.conf > /etc/nginx/conf.d/default.conf"
  docker exec $ap_name bash -c "cat /tmp/proxy.conf   > /etc/nginx/proxy.conf"
  docker exec $ap_name bash -c "cat /tmp/nginx.conf   > /etc/nginx/nginx.conf"
  
  docker exec $ap_name bash -c "nginx -t ;echo \$? > /tmp/$ap_name-conf-check.log"
  docker cp $ap_name:/tmp/$ap_name-conf-check.log /tmp/$ap_name-conf-check.log
  proxy_result=$(cat /tmp/$ap_name-conf-check.log)

  if [ ! $proxy_result == '0' ]
  then
    echo "nginx conf file verify faild... check that!!"
    exit 1
  fi
  docker exec $ap_name bash -c "nginx -s reload"
  exit 0
fi

##################
#                #
# 關閉容器並重建 #
#                #
##################
if docker ps -a | grep " ${ap_name}$"; then
  docker rm -f $ap_name
fi

docker run -itd -p 80:80 -p 443:443 \
--restart=always --log-opt max-size=10m --log-opt max-file=10 \
--net=docker \
--ulimit nofile=102400:102400 \
--ulimit nproc=102400:102400 \
-v $fd_name/$ap_name/conf/nginx.conf:/etc/nginx/nginx.conf \
-v $fd_name/$ap_name/conf/default.conf:/etc/nginx/conf.d/default.conf \
-v $fd_name/$ap_name/conf/proxy.conf:/etc/nginx/proxy.conf \
-v $fd_name/$ap_name/conf/pswd/:/etc/nginx/pswd/:ro \
-v $fd_name/$ap_name/conf/ssl/:/etc/nginx/ssl/:ro \
-v $fd_name/$ap_name/content:/usr/share/nginx/html:ro \
-v $fd_name/$ap_name/logs:/var/log/nginx \
-v /etc/localtime:/etc/localtime:ro \
--name $ap_name \
nginx:1.16.1


############################
#                          #
# run nginx log logrotate  #
#                          #
############################
# 產生 logrotate 檔案
cat << EOF > /etc/logrotate.d/${ap_name}
$fd_name/${ap_name}/logs/*.log {
    daily
    dateext
    missingok
    rotate 90
    notifempty
    compress
    create 640 root root
    delaycompress
    sharedscripts
    postrotate
        /usr/bin/docker exec ${ap_name} bash -c 'nginx -s reload'
    endscript
}
EOF

#設定log滾動排程
sed -i "/logrotate.d\/${ap_name};/d" /var/spool/cron/root 2> /dev/null
echo "0 0 * * * /usr/sbin/logrotate -f /etc/logrotate.d/${ap_name}; > $fd_name/${ap_name}/logs/access.log; > $fd_name/${ap_name}/logs/error.log;" >> /var/spool/cron/root
systemctl restart crond
