# 📌 Linux 防火牆常用指令範本

## 1. iptables (CentOS 6)
```
### 1.1 檢視防火牆規則
iptables -nL

### 1.2 新增允許規則
# 允許 TCP port 22 (SSH)
iptables -I INPUT -p tcp --dport 22 -j ACCEPT -m comment --comment "ssh"

# 允許 TCP port 8080
iptables -I INPUT -p tcp --dport 8080 -j ACCEPT -m comment --comment "web service"

# 允許 UDP port 1611
iptables -I INPUT -p udp --dport 1611 -j ACCEPT -m comment --comment "udp service"

### 1.3 儲存與重新載入規則
/etc/init.d/iptables save
/etc/init.d/iptables reload

### 1.4 刪除規則
# 刪除第一條規則
iptables -D INPUT 1


## 2. firewalld (CentOS 7+)

### 2.1 基本操作
# 查看所有服務
firewall-cmd --get-services

# 查看所有 zone
firewall-cmd --get-zones

# 查看預設 zone
firewall-cmd --get-default-zone

# 查看啟用中的 zone
firewall-cmd --get-active-zones

# 查看 zone 詳細設定
firewall-cmd --list-all --zone=public
firewall-cmd --list-all --zone=public --permanent

### 2.2 開啟 port
# 臨時開啟 TCP port 8080
firewall-cmd --zone=public --add-port=8080/tcp

# 永久開啟 TCP port 8080
firewall-cmd --zone=public --permanent --add-port=8080/tcp

---

### 2.3 關閉 port
# 臨時關閉
firewall-cmd --zone=public --remove-port=8080/tcp

# 永久關閉
firewall-cmd --zone=public --permanent --remove-port=8080/tcp

---

### 2.4 開啟服務
# 臨時開啟 https
firewall-cmd --zone=public --add-service=https

# 永久開啟 https
firewall-cmd --zone=public --permanent --add-service=https

---

### 2.5 關閉服務
# 臨時關閉 https
firewall-cmd --zone=public --remove-service=https

# 永久關閉 https
firewall-cmd --zone=public --permanent --remove-service=https

---

### 2.6 重新載入設定
firewall-cmd --reload

---

## 3. 常見情境

### 3.1 開啟 JMX Port 9000 (Tomcat)
# iptables
iptables -I INPUT -p tcp --dport 9000 -j ACCEPT -m comment --comment "tomcat for jmx"
service iptables save

# firewalld
firewall-cmd --zone=public --permanent --add-port=9000/tcp
firewall-cmd --reload

---

### 3.2 批次開啟多個 Port
# iptables
for port in 1433 1998 1999 6060; do
    iptables -I INPUT -p tcp --dport $port -j ACCEPT -m comment --comment "PPS6 ports"
done
service iptables save

# firewalld
firewall-cmd --zone=public --permanent --add-port=1433/tcp
firewall-cmd --zone=public --permanent --add-port=1998/tcp
firewall-cmd --zone=public --permanent --add-port=1999/tcp
firewall-cmd --zone=public --permanent --add-port=6060/tcp
firewall-cmd --reload
```
