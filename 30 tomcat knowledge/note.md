# TOMCAT 開啟JMX，需注意防火牆問題
```
----- /tomcat/bin/setenv.sh -----
-Djava.rmi.server.hostname=192.168.54.78 \
-Dcom.sun.management.jmxremote.rmi.port=9000 \
-Dcom.sun.management.jmxremote=true \
-Dcom.sun.management.jmxremote.port=9000 \
-Dcom.sun.management.jmxremote.ssl=false \
-Dcom.sun.management.jmxremote.authenticate=false \
```

```
# dump jvm memory (可能需要切換身份..例如切到glassfish)
su glassfish
cd /tmp
jmap -dump:format=b,file=jvm_mem_dump.hprof ${PID}
# dump jvm thread
su glassfish
cd /opt/tomcat/temp
jstack -l ${PID} >> jvm_thread_dumps.log
```

# TOMCAT 發生高併發請求時，需注意 maxThreads 不足問題，預設僅接受同時處理 200 筆請求
```
    ----- /tomcat/conf/server.xml -----
    <!-- A "Connector" represents an endpoint by which requests are received
         and responses are returned. Documentation at :
         Java HTTP Connector: /docs/config/http.html (blocking & non-blocking)
         Java AJP  Connector: /docs/config/ajp.html
         APR (HTTP/AJP) Connector: /docs/apr.html
         Define a non-SSL/TLS HTTP/1.1 Connector on port 8080
    -->
    <Connector port="8080" protocol="HTTP/1.1"
	           maxThreads="200"
             connectionTimeout="20000"
             maxPostSize="16777216"
             redirectPort="8443" />
```

# TOMCAT 管理後台帳號管理
```
----- /tomcat/conf/tomcat-users.xml -----
<!-- 可開啟後台 GUI -->
<user username="username1" password="password" roles="manager-gui,manager-script,manager-jmx,manager-status,admin-script,admin-gui"/>
<!-- 可透過輸入帳號密碼請求服務 API -->
<user username="username2" password="password" roles="admin"/>
```
