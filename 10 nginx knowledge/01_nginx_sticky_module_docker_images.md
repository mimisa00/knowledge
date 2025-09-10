# 建立 Nginx 含有 Sticky Module 的 Docker Image


### 解壓縮以下檔案放至目標目錄  
[nginx-sticky-1.16.1.tgz](https://github.com/mimisa00/os-env-note/blob/main/10%20advanced%20knowledge/nginx-sticky-1.16.1.tgz)
```
tar zxvf nginx-sticky-1.16.1.tgz
```
最後結果如下圖  
<img width="718" height="154" alt="image" src="https://github.com/user-attachments/assets/fa7a73ad-2e9f-473c-a5e1-8d0afc889599" />

### 進入該目錄後先編輯 Dockefile
```
#因為 Debian 10 (Buster) 已經 EOL (End of Life)，官方把套件倉庫移到 archive.debian.org，所以舊的 deb.debian.org 與 security.debian.org 都回傳 404
# 在 RUN apt-get update 之前加上以下內容
 
RUN sed -i 's|deb.debian.org|archive.debian.org|g' /etc/apt/sources.list \
 && sed -i 's|security.debian.org|archive.debian.org|g' /etc/apt/sources.list \
 && sed -i '/stretch-updates/d' /etc/apt/sources.list
 
tar zxvf nginx-sticky-1.16.1.tgz
```

### 下達以下指令建立 image 
```
docker build -t nginx-sticky:1.16.1 .
```

### 完成後即可產生有 sticky 功能的 nginx:1.16.1 Docker image 
<img width="732" height="54" alt="image" src="https://github.com/user-attachments/assets/04376c35-9595-4cb8-96cc-96b70cdf76ef" />
