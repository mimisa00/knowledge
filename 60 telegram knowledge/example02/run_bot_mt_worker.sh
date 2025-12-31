#!/bin/bash

# 自動取得當前主機的 Hostname
CUR_HOSTNAME=$(hostname)

# 檔案路徑設定，加上 Hostname 避免共享目錄衝突
APP_NAME="worker_agent.py"
LOG_FILE="/opt/mt-script/mt-bot-service/log/worker_${CUR_HOSTNAME}.log"
PID_FILE="/opt/mt-script/mt-bot-service/pid/worker_${CUR_HOSTNAME}.pid"
APP_PATH="/opt/mt-script/mt-bot-service/worker_agent.py"

start() {
    # 檢查是否已有該主機的 PID 檔案且進程真的在跑
    if [ -f $PID_FILE ] && kill -0 $(cat $PID_FILE) 2>/dev/null; then
        echo "主機 [$CUR_HOSTNAME] 的 Worker 已經在運行中 (PID: $(cat $PID_FILE))"
    else
        echo "正在啟動主機 [$CUR_HOSTNAME] 的 Worker Agent..."
        # 確保在 /opt/mt-script/mt-bot-service 目錄下執行
        cd /opt/mt-script/mt-bot-service
        nohup python3 $APP_PATH > $LOG_FILE 2>&1 &
        echo $! > $PID_FILE
        echo "Worker 已啟動，日誌位於 $LOG_FILE"
    fi
}

stop() {
    if [ -f $PID_FILE ]; then
        PID=$(cat $PID_FILE)
        echo "正在停止主機 [$CUR_HOSTNAME] 的 Worker Agent (PID: $PID)..."
        kill $PID
        rm $PID_FILE
        echo "Worker 已停止。"
    else
        echo "找不到主機 [$CUR_HOSTNAME] 運行中的 Worker。"
    fi
}

status() {
    if [ -f $PID_FILE ] && kill -0 $(cat $PID_FILE) 2>/dev/null; then
        echo "主機 [$CUR_HOSTNAME] Worker 狀態：運行中 (PID: $(cat $PID_FILE))"
    else
        echo "主機 [$CUR_HOSTNAME] Worker 狀態：未啟動。"
        # 如果檔案存在但進程不在，順便清理
        [ -f $PID_FILE ] && rm $PID_FILE
    fi
}

case "$1" in
    start) start ;;
    stop) stop ;;
    status) status ;;
    restart) stop; start ;;
    *) echo "使用方式: $0 {start|stop|status|restart}" ;;
esac
