# 透過 GCP Vertex AI 啟用 Claude Code 

### 官方說明
https://docs.claude.com/zh-TW/docs/claude-code/google-vertex-ai

#### 前置作業 - 先到 GCP 平台啟用 Vertex AI 提供的 Claude Model
<img width="1883" height="906" alt="image" src="https://github.com/user-attachments/assets/560b8cb0-4565-4e49-9227-f95b16b86c12" />

#### 選擇 Anthropic
<img width="1912" height="904" alt="image" src="https://github.com/user-attachments/assets/21f558d9-24d1-4aa1-a9f5-851f7207ac74" />

#### 選擇啟用模型
<img width="1898" height="895" alt="image" src="https://github.com/user-attachments/assets/227395d1-ea76-4024-be3e-d9b64451584b" />
<img width="1556" height="892" alt="image" src="https://github.com/user-attachments/assets/62c7f6b1-c5ba-4526-b0bd-6b3d2bf53a59" />

#### 如果 Vertex API 尚未啟用會提示需要先啟用 Vertex API 
<img width="1667" height="863" alt="image" src="https://github.com/user-attachments/assets/2cca4a5b-ee72-41eb-85ba-1b73b59c3ac3" />

#### 填寫必要資訊 - 此頁面資料主要是 google 要將客戶資訊分享給 Anthropic，除了要取得客戶同意以外，也有利之後的帳務作業
<img width="622" height="907" alt="image" src="https://github.com/user-attachments/assets/2eb2a133-42f6-4fcd-b3d1-9aa3bcda7439" />

#### 告知啟用此模型的收費方案細節
<img width="819" height="820" alt="image" src="https://github.com/user-attachments/assets/9db64c66-9f61-43f6-a518-b4b4e1eaef76" />

#### 成功啟用後的畫面
<img width="1147" height="721" alt="image" src="https://github.com/user-attachments/assets/4884fde3-9690-47e8-9662-125d38ae67a7" />


## 於 linux 環境下啟用 claude code

#### 下載 gcloud SDK 並登入 google 帳號
```
curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-linux-x86_64.tar.gz
tar zxvf google-cloud-cli-linux-x86_64.tar.gz
# 登入 Google 帳號，需注意 一定要使用 application-default 不可以直接 auth login 
google-cloud-sdk/bin/gcloud auth application-default login
```

#### 設定環變數
```
# Enable Vertex AI integration
export CLAUDE_CODE_USE_VERTEX=1
export CLOUD_ML_REGION=global
export ANTHROPIC_VERTEX_PROJECT_ID= 此處輸入對應的 GCP 專案代碼

# Optional: Disable prompt caching if needed
export DISABLE_PROMPT_CACHING=1

# 官方網站不止這些內容，基本上只要設定以上的內容即可
```

#### 登入 claude code，如果一切沒有操作錯誤的情況下，就會順利看到以下畫面，需注意此時就不會有 login 及 logout 指令可以使用
<img width="1310" height="659" alt="image" src="https://github.com/user-attachments/assets/877e676a-5458-4fd9-8968-aab59e59fa68" />


## 於 windows 環境下啟用 claude code

#### 下載 gcloud SDK 並登入 google 帳號，開啟 power shell 後輸入以下指令下載 SDK 並直接觸發安裝
```
(New-Object Net.WebClient).DownloadFile("https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe", "$env:Temp\GoogleCloudSDKInstaller.exe")
& $env:Temp\GoogleCloudSDKInstaller.exe
```
<img width="855" height="733" alt="image" src="https://github.com/user-attachments/assets/c8656307-35c1-46f2-b213-f7a39122d141" />

#### 安裝完畢後桌面會出現 Google Cloud SDK 的 CMD 快捷鍵，點兩下開啟 cmd 畫面 (上一動安裝時會問要不要裝，如果不裝的話，要自己找路徑哦)
<img width="78" height="85" alt="image" src="https://github.com/user-attachments/assets/9674eb56-70dd-4144-a2a9-835fcdbb608a" />

#### 第一次進入時會進行提示，請依自身的狀況輸入
<img width="1894" height="501" alt="image" src="https://github.com/user-attachments/assets/fce33816-b5c8-4d1f-b0c4-a5706c7fafff" />

#### 登入 google 帳號，跟在 Linux 下的指令一樣，請注意不要漏掉 application-default
```
google-cloud-sdk/bin/gcloud auth application-default login
```
<img width="1893" height="255" alt="image" src="https://github.com/user-attachments/assets/7b1f91b2-4206-46ba-8d13-4ec6c23a0995" />

#### 設定環變數，進入系統設定
<img width="1197" height="932" alt="image" src="https://github.com/user-attachments/assets/1b786223-f315-43bc-ba3c-704b459335c6" />
<img width="479" height="528" alt="image" src="https://github.com/user-attachments/assets/ae5afbda-2a0d-43e4-9b32-4db52889ad10" />

```
# 將以下環境變數輸入進去
CLAUDE_CODE_USE_VERTEX=1
CLOUD_ML_REGION=global
ANTHROPIC_VERTEX_PROJECT_ID=此處輸入對應的 GCP 專案代碼
export DISABLE_PROMPT_CACHING=1
```
<img width="615" height="583" alt="image" src="https://github.com/user-attachments/assets/ce71212a-87b4-491c-a2aa-32ae1a444511" />


#### 登入 claude code，如果一切沒有操作錯誤的情況下，就會順利看到以下畫面，需注意此時就不會有 login 及 logout 指令可以使用，註:以下畫面為透過 Cursor 啟用 Terminal 模式及啟用 Claude code plugin 的 chat windows 呈現
<img width="1352" height="737" alt="image" src="https://github.com/user-attachments/assets/2296e234-ea05-448b-b43c-c517af5bdf7b" />


