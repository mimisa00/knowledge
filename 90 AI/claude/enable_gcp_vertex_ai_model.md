# 透過 GCP Vertex AI 啟用 Claude Code 

### 官方說明
https://docs.claude.com/zh-TW/docs/claude-code/google-vertex-ai

#### 前置作業 - 先到 GCP 平台啟用 Vertex AI 提供的 Claude Model
<img width="1883" height="906" alt="image" src="https://github.com/user-attachments/assets/b0df8bf1-ab75-4a69-ba6e-e0e901fc5347" />

#### 選擇 Anthropic
<img width="1912" height="904" alt="image" src="https://github.com/user-attachments/assets/0a370a02-1dff-40a8-81da-d28e13b0ee28" />

#### 選擇啟用模型
<img width="1898" height="895" alt="image" src="https://github.com/user-attachments/assets/3693798e-5f9a-4f02-8597-fdd24a1946dd" />
<img width="1556" height="892" alt="image" src="https://github.com/user-attachments/assets/a94c601d-d6f7-487b-888a-30ccabb6308b" />

#### 如果 Vertex API 尚未啟用會提示需要先啟用 Vertex API 
<img width="1667" height="863" alt="image" src="https://github.com/user-attachments/assets/5b5ac3ea-a488-4bbc-9971-8fa455a2f4ba" />

#### 填寫必要資訊 - 此頁面資料主要是 google 要將客戶資訊分享給 Anthropic，除了要取得客戶同意以外，也有利之後的帳務作業
<img width="622" height="907" alt="image" src="https://github.com/user-attachments/assets/e3d116ab-1ebd-42c5-b55e-337a1c55fcc2" />

#### 告知啟用此模型的收費方案細節
<img width="819" height="820" alt="image" src="https://github.com/user-attachments/assets/e8638104-923e-40c6-8f4c-dc7d11f24fc0" />

#### 成功啟用後的畫面
<img width="1147" height="721" alt="image" src="https://github.com/user-attachments/assets/46b20edb-375e-4db7-b2d7-0dc621d81f76" />


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
<img width="1310" height="659" alt="image" src="https://github.com/user-attachments/assets/08d2c4c1-1305-40cf-a6fe-c45545a29d8a" />


## 於 windows 環境下啟用 claude code

#### 下載 gcloud SDK 並登入 google 帳號，開啟 power shell 後輸入以下指令下載 SDK 並直接觸發安裝
```
(New-Object Net.WebClient).DownloadFile("https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe", "$env:Temp\GoogleCloudSDKInstaller.exe")
& $env:Temp\GoogleCloudSDKInstaller.exe
```
<img width="855" height="733" alt="image" src="https://github.com/user-attachments/assets/3eb00fac-5b44-4ccd-a8d3-ae06f537c6b9" />

#### 安裝完畢後桌面會出現 Google Cloud SDK 的 CMD 快捷鍵，點兩下開啟 cmd 畫面 (上一動安裝時會問要不要裝，如果不裝的話，要自己找路徑哦)
<img width="78" height="85" alt="image" src="https://github.com/user-attachments/assets/183411d5-d2a5-4e6f-bb5b-88037f0083d9" />

#### 第一次進入時會進行提示，請依自身的狀況輸入
<img width="1894" height="501" alt="image" src="https://github.com/user-attachments/assets/7df2ff55-452a-49ca-ae9b-b0c486b23fdf" />

#### 登入 google 帳號，跟在 Linux 下的指令一樣，請注意不要漏掉 application-default
```
google-cloud-sdk/bin/gcloud auth application-default login
```
<img width="1893" height="255" alt="image" src="https://github.com/user-attachments/assets/67f14c56-6d74-4ff5-95b1-96eff4402fbd" />

#### 設定環變數，進入系統設定
<img width="1197" height="932" alt="image" src="https://github.com/user-attachments/assets/225df10d-96cf-42ba-b7e7-fb6cb06b0933" />
<img width="479" height="528" alt="image" src="https://github.com/user-attachments/assets/eacfe6bc-77b4-4c2e-b70c-46dee256a93d" />
```
# 將以下環境變數輸入進去
CLAUDE_CODE_USE_VERTEX=1
CLOUD_ML_REGION=global
ANTHROPIC_VERTEX_PROJECT_ID=此處輸入對應的 GCP 專案代碼
export DISABLE_PROMPT_CACHING=1
```
<img width="615" height="583" alt="image" src="https://github.com/user-attachments/assets/42794c96-75e5-439a-a6e8-d228cca8f127" />

#### 登入 claude code，如果一切沒有操作錯誤的情況下，就會順利看到以下畫面，需注意此時就不會有 login 及 logout 指令可以使用，註:以下畫面為透過 Cursor 啟用 Terminal 模式及啟用 Claude code plugin 的 chat windows 呈現
<img width="1352" height="737" alt="image" src="https://github.com/user-attachments/assets/e42dbfb9-ec13-4eab-b6bc-6998480c0fbc" />

