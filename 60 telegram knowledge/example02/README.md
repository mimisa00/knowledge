## 用途
此 example 是透過 telegram bot listening 將要派送的任務，送到各個主機共享的 nfs 目錄，再由各個主機自行認領任務進行作業

## 背景說明
1. 需進行特定例維護作業
2. 登入工作主機作業程序繁瑣 vpn > host auth login > account switch role
3. 同時需要維護多台主機
4. 主機與主機間網路無法互通
5. 主機之間有可以 nfs 可以共享目錄
6. 主機能夠探訪 http

## Structure
```
example02/
├── Dockerfile            # 運作 telegram bot app image build file
├── README.md             # Project documentation
├── host_list.txt         # 要維護的主機列表 : 主機 hostname 需依照特定格式設定名稱 xxx-ap xxx-proxy
├── history/              # 工作記錄留存目錄 : 當 master 確認此次任務皆己完成時，會將 reslut 的所有人容打包送到此目錄下留存備查
├── master_bot.py         # Python application : 驅動 bot 產生 telegram chat panel 及接收指令，接收到指令會將任務派送到共享目錄
├── queue/                # 派送工作任務目錄 : worker 主機會於此目錄認領自己的工作
├── results/              # 派送工作任務目錄 : worker 主機工作完成後會將自己的工作從 queue 目錄轉移到 results 目錄暫時存放
├── run_bot_mt_master.sh  # 啟用容器環境驅動 master_boy.py 
├── run_bot_mt_worker.sh  # Python application : 直接於 host 主機驅動 worker_agent.py 
└── worker_agent.py       # 輪詢 queue 目錄確認是否有維護工作待處理
```

##  Getting Started
### Prerequisites
- Docker
- Python3

### 1. Clone the example02
### 2. Set Up the Environment (Master for telegram bot listening)
```bash
docker build -t mt-bot-service .
# edit run_bot_mt_master.sh type your telegram bot token and chat id and user id
# edit host_list.txt
sh run_bot_mt_master.sh
```
### 3. Set Up the Environment (Woker for reciver Mission)
```
sh run_bot_mt_worker.sh.sh
```

### 啟動後與 telegram 顯示如下
<img width="459" height="555" alt="image" src="https://github.com/user-attachments/assets/01272846-81e0-4155-8d32-19d711923261" />


### 備註
此 example 的工作目錄實務可能不同每個人所需要的環境，故請注意此點並調整之
