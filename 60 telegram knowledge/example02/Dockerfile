# 使用輕量級 Python 3.9
FROM python:3.9-slim

# 設定工作目錄
WORKDIR /app

# 安裝基本系統套件 (如果執行 sh 需要額外工具可以在此加入)
RUN apt-get update && apt-get install -y --no-install-recommends \
    procps \
    && rm -rf /var/lib/apt/lists/*

# 安裝 Telegram Bot 必要的 Python 套件
# 這裡使用 v13.x 版本，因為它的同步架構更適合簡單的腳本控制
RUN pip install --no-cache-dir python-telegram-bot==13.15

# 將程式碼複製進容器
COPY master_bot.py .

# 預設不設定 ENTRYPOINT，由 run_docker.sh 來決定啟動哪個程式
