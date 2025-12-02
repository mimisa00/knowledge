#!/bin/bash

ap_name=__replace_apn__
ap_port=__replace_port__
ap_paths=__replace_ap_path__

##########################
#                        #
# pinpoint trigger       #
#                        ################
# agentId   值不重覆(max length 24)     #
# agentName 人類辨識                    #
#########################################
host_name=`hostname`
sed -i "s#replace_pinpoint_apname#${ap_name}#g"       /home/fusion-ap/$ap_name/bin/setenv.sh
agent_name=${host_name}-${ap_name}
agent_name_sha1=$(echo -n "${agent_name}"|sha1sum|cut -d ' ' -f1)
agent_id=$(echo ${agent_name_sha1:0:24})
sed -i "s#replace_pinpoint_agentname#${agent_name}#g" /home/fusion-ap/$ap_name/bin/setenv.sh
sed -i "s#replace_pinpoint_agentid#${agent_id}#g"     /home/fusion-ap/$ap_name/bin/setenv.sh

##################
#                #
# docker volumme #
#                #
##################
if ! docker volume ls | grep -q "__replace_nfs_volname__$"
then
  docker volume create                          \
  --driver local                                \
  -o type=nfs                                   \
  -o o=addr="__replace_nfs_host__,rw,nfsvers=3" \
  -o device=:__replace_nfs_source__             \
  __replace_nfs_volname__
fi

##################
#                #
# docker trigger #
#                #
##################
IMAGE_TAG="e1-nexus.iwerp.net:8083/werptom:3"
IMAGE_PATH="/home/core/template/werptom_3"
###### 檢查 image 是否存在，若不存在則 build ######
if ! docker image inspect "$IMAGE_TAG" >/dev/null 2>&1; then
  echo "[INFO] Image $IMAGE_TAG 不存在，開始 build ..."
  
  if [ ! -f "$IMAGE_PATH/Dockerfile" ]; then
    echo "[ERROR] 找不到 Dockerfile: $IMAGE_PATH/Dockerfile"
    exit 1
  fi

  docker build -t "$IMAGE_TAG" "$IMAGE_PATH"
  if [ $? -ne 0 ]; then
    echo "[ERROR] Build image 失敗"
    exit 1
  fi

  echo "[INFO] Image $IMAGE_TAG 建立完成"
else
  echo "[INFO] Image $IMAGE_TAG 已存在，略過 build"
fi

# 檢查 container 是否存在
if docker ps -a | grep ${ap_name}$; then
  docker rm -f ${ap_name}
  
fi

# remove app fold
rm -rf  /home/fusion-ap/$ap_name/webapps/{__replace_ap_path__,tmp}

# 取得主機ip
export HOST_IP=$(hostname -I | awk '{print $1}')

# 檢查 catalina.properties 是否存在
# 這一段 處理主要是為了從 werptom:2 版本過渡到 werptom:3 版進行的相關處理，因為整個重建工作目錄所花用時間太多，故若透過部署方式即自動更新會比較理想
CATALINA_FILE="/home/fusion-ap/$ap_name/conf/catalina.properties"
CATALINA_TEMPLATE="/home/core/template/tomcat/conf/catalina.properties"
# 若是目錄，直接砍掉（避免爛掉的空目錄占位置）
if [ -d "$CATALINA_FILE" ]; then
    echo "[WARN] $CATALINA_FILE 是目錄，將刪除以避免異常..."
    rm -rf "$CATALINA_FILE"
fi
if [ ! -f "$CATALINA_FILE" ]; then
    echo "[INFO] $CATALINA_FILE 不存在，從 template 複製中..."
    mkdir -p "/home/fusion-ap/$ap_name/conf"
    cp "$CATALINA_TEMPLATE" "$CATALINA_FILE" || {
        echo "[ERROR] 無法複製 catalina.properties"
        exit 1
    }
    echo "[INFO] 已成功複製 catalina.properties"
else
    echo "[INFO] $CATALINA_FILE 已存在，略過複製"
fi

# start container
#--restart=__replace_restart__
docker run --name $ap_name -d -it               \
--net=docker                                    \
--restart=always                                \
--log-opt max-size=1m                           \
--log-opt max-file=2                            \
--sysctl net.core.somaxconn=65535               \
--ulimit nofile=102400:102400                   \
--ulimit nproc=102400:102400                    \
-p $ap_port:8080                                \
-v /home/fusion-ap/$ap_name/bin/setenv.sh:/tomcat/bin/setenv.sh                        \
-v /home/fusion-ap/$ap_name/lib/__replace_mari_cli__:/tomcat/lib/__replace_mari_cli__  \
-v /home/fusion-ap/$ap_name/conf/context.xml:/tomcat/conf/context.xml                  \
-v /home/fusion-ap/$ap_name/conf/server.xml:/tomcat/conf/server.xml                    \
-v /home/fusion-ap/$ap_name/conf/tomcat-users.xml:/tomcat/conf/tomcat-users.xml        \
-v /home/fusion-ap/$ap_name/conf/catalina.properties:/tomcat/conf/catalina.properties  \
-v /home/fusion-ap/$ap_name/webapps/:/tomcat/webapps/                                  \
-v /home/fusion-ap/$ap_name/logs/:/tomcat/logs/                                        \
-v /home/fusion-ap/config/:/srv/fusion/config/                                         \
-v /home/fusion-ap/pinpoint-agent-2.5.2/:/opt/pinpoint-agent/                          \
-v __replace_nfs_volname__:/srv/fusion/attachment/                                     \
-e HOST_IP=$HOST_IP                                                                    \
"$IMAGE_TAG"

# 探針偵測
