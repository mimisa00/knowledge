# TOMCAT 開啟JMX，需注意防火牆問題
```
----- setenv.sh -----
-Djava.rmi.server.hostname=192.168.54.78 \
-Dcom.sun.management.jmxremote.rmi.port=9000 \
-Dcom.sun.management.jmxremote=true \
-Dcom.sun.management.jmxremote.port=9000 \
-Dcom.sun.management.jmxremote.ssl=false \
-Dcom.sun.management.jmxremote.authenticate=false \
```
