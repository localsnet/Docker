# Version: 0.0.1
FROM alpine
MAINTAINER local "local@example.com"
ADD myip.sh /home
CMD ["sh", "-c", "/home/myip.sh ; nohup ping 8.8.8.8 > timeout.txt &"]
