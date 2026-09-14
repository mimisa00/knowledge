# 實用工具

## 如何接回舊 session 接續作業 (原本 session 仍在作業中)
```
##################################################
#
# 如果是透過 opencode serve or opencode web 啟動
#
##################################################
# 連接 Server 並自動接回上一次 Session
opencode attach http://localhost:4096 -c
# 連接 Server 並指定特定 Session ID
opencode attach http://localhost:4096 -s <SESSION_ID>

###############################
#
# 透過 CLI 旗標重開歷史 Session
#
###############################
# 接回最後一次運作的 Session
opencode -c # or opencode --continue
# 接回指定的 Session
opencode -s <SESSION_ID>
# 或
opencode --session <SESSION_ID>

###############################
#
# 在 TUI 介面中即時切換 Session
#
###############################
/sessions  # 選取目標 Session 即可繼續輸出 (需稍微等一下)
```


## opencode 即時權限審批
##### 當 opencode 在 pc 或 server 背景作業，可透過 telegram 遠端操作 session 進行即時審批，且需注意資安問題，透過 npx 啟動 bot server 時不要使用預設密碼
```
# 啟動本地 OpenCode API
opencode serve

# 啟動 bot server
# 依提示輸入 Bot Token 與 User ID 及即完成設定
npx @grinev/opencode-telegram-bot
 
# 一切設定完畢後，即可開始在 telegram 跟 bot 進行對話
# /projects 選擇運作專案
# /sessions 撰擇主對話
```



## 透過 MCP 觸發 playwright 時截圖中文字顯示異常
##### 如果 opencode 運作在 Rocky Linux Base 環境，預設無中文語系字體，故造成截圖時中文字部份呈現方塊或消失的狀況，必須直接在 Rocky Linux 系統中安裝中文字型與語系包
```
# 1. 安裝繁體中文語系包
sudo dnf install -y langpacks-zh_TW glibc-langpack-zh

# 2. 安裝 Google 官方的開源中文字型（Noto CJK，包含黑體與明體）
sudo dnf install -y google-noto-cjk-fonts google-noto-sans-cjk-ttc-fonts

# 3. 重新整理系統的字型快取
sudo fc-cache -fv
```
##### 除此之外 opencode.jsonc 也需設定環境參數，讓 playwright 時載入系統的中文語系資訊
```
  "mcp": {
    "playwright": {
      "type": "local",
      "command": [
        "npx",
        "-y",
        "@playwright/mcp@latest",
        "--isolated",
        "--headless",
        "--caps=tabs,storage",
        "--output-dir=.where_dir_your_want"
      ],
      "enabled": true,
      "env": {
        // 1. 強制讓 Playwright 啟動的 Chromium 使用中文語系
        "LANGUAGE": "zh_TW.UTF-8",
        "LANG": "zh_TW.UTF-8",
        "LC_ALL": "zh_TW.UTF-8"
      }
    },
```
