## Bot 運作原理
- 需至 bot father 建立專用機器人，privacy mode 需開啟內聯回應模式
- 透過程式定時監控 bot 本身在各個 chat 接收到的訊息，再控制 bot 回應相關 chat 呼應的動作


## 如何在 Telegram 操作 Bot 互動 
1. 創建一個 Group 然後將 bot 加到該窗口
2. 觸發 /start 指令然後會出現以下的控制表單  
   <img width="365" height="173" alt="image" src="https://github.com/user-attachments/assets/9c573eb9-e6da-4dc0-bec3-282f869e5692" />
3. 再依說明指示進行操作即可  
   <img width="511" height="334" alt="image" src="https://github.com/user-attachments/assets/655b3ff1-ab56-41f9-a3b4-240f5cbc19d2" />

## Bot 監聽程式運作環境說明  
> - 主架構 :  透過 Docker 啟動 python 運作
>> |file name	|note	|
>> | ------------- |:-------------:|
>> |Dockerfile	|容器運作環境描述文件	|
>> |bot.py	|監控 bot 訊息程式|
>> |coms.txt	|可以存取白名單的公司代碼|
>> |fw.log	|當異動白名單成功時留下 log|
>> |requirements.txt	|容器環境初始化時，安裝 python 所需參數|
>> |run_gcp-fw-bot.sh| 建立Docker Image 及 Container，觸發此腳本後 bot 則開始進行監聽 <br/> 啟動腳本將 TELEGRAM_TOKEN 做為環境變數提供給 bot.py 使用 <br/> 啟動腳本將 Cloud Run API URL，做為環境變數提供給 bot.py 使用<br/> 啟動腳本將 Cloud Run API AUTH ，做為環境變數提供給 bot.py 使用<br/>啟動腳本將 ALLOWED_CHAT_IDS ，做為環境變數提供給 bot.py 使用<br/>啟動腳本將 ALLOWED_USERS，做為環境變數提供給 bot.py 使用|
> - 除錯說明 :
>> ```
>> 可查閱 docker logs -f gcp-fw-bot 確認啟動時是否有錯誤訊息
>> 可查閱 fw.log 是否有任何異常訊息產生
>> bot.by 調整 logging level = DEBUG
>> ```
>> <img width="739" height="204" alt="image" src="https://github.com/user-attachments/assets/d7b1fc99-665b-4ee3-a7ef-276a6fbc02bb" />
> - 新增授權使用者 
>> 可透過 @userinfobot 查找自己的 id 然後將 id 加入到 run_gcp-fw-bot.sh 增加 telegram user id 到 ALLOWED_USERS中 即可獲得授權

## 注意事項
bot 創建後，預設僅接受指令訊息 /xxxx  
<img width="300" height="171" alt="image" src="https://github.com/user-attachments/assets/0434170e-69f4-44b4-ad09-abafae84c62c" />  
若要可以接收一般訊息，需將 bot Group Privacy mode 關閉 (https://core.telegram.org/bots/features#privacy-mode)   
請在 BotFather 窗口依照以下說明進行關閉
找出自己己創建機器人 > 點擊 Bot Settings > 點擊 Group Privacy > 點擊 Trun Off 關閉 Privacy mode 
<img width="611" height="950" alt="image" src="https://github.com/user-attachments/assets/a22d7e78-9d8e-43a2-a492-f61c254fdf82" />  
<img width="300" height="152" alt="image" src="https://github.com/user-attachments/assets/6513e3dc-0617-4f5b-be11-2a56ca794d88" />  
<img width="284" height="300" alt="image" src="https://github.com/user-attachments/assets/bda85bf3-a312-4b1c-9609-62452f005ef3" />  
<img width="300" height="84" alt="image" src="https://github.com/user-attachments/assets/d2b399de-a5d0-4566-9190-2cf13ee069a1" />  



