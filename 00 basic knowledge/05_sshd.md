# 📌 SSH 常用指令與設定範本
```
## 1. SSH 免密登入設定
# 由 A 主機登入到 B 主機，免密碼登入設定
ssh-copy-id user@<B主機IP>

# 範例：root 帳號免密登入到 192.168.53.202
ssh-copy-id root@192.168.53.202

---

## 2. SSH 設定檔修改

### 2.1 開啟 root 遠端登入
# 編輯 sshd 設定檔
vi /etc/ssh/sshd_config

# 找到並修改以下參數
PermitRootLogin yes

# 重新啟動 SSH 服務
systemctl restart sshd    # CentOS 7+
service sshd restart      # CentOS 6

---

### 2.2 修改預設 SSH Port
# 編輯設定檔
vi /etc/ssh/sshd_config

# 修改 Port 參數
Port 2222

# 開啟防火牆對應 port (CentOS 7+)
firewall-cmd --zone=public --permanent --add-port=2222/tcp
firewall-cmd --reload

---

### 2.3 限制可登入的使用者
# 在 sshd_config 中加入
AllowUsers user1 user2

---

## 3. SSH 服務管理

# 啟動 SSH 服務
systemctl start sshd

# 停止 SSH 服務
systemctl stop sshd

# 重啟 SSH 服務
systemctl restart sshd

# 查看 SSH 狀態
systemctl status sshd

---

## 4. SSH 其他常用操作

### 4.1 測試 SSH 連線
ssh -v user@<host>

### 4.2 使用指定金鑰登入
ssh -i /path/to/private_key user@<host>

### 4.3 SSH 隧道轉發
# 將本地 8080 轉發到遠端 80
ssh -L 8080:localhost:80 user@<host>

### 4.4 SCP 檔案傳輸
# 上傳檔案
scp /local/file user@<host>:/remote/path

# 下載檔案
scp user@<host>:/remote/file /local/path
```
