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
