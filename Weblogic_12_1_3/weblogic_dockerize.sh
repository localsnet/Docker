#!/bin/bash
#Building a Docker Image for WebLogic 

ORCL=~/dist_oracle/docker-images
DIST=~/dist_oracle

#1.Git clone the Oracle Docker project repository
git clone https://github.com/oracle/docker-images.git

#2.Download required JRE file

cd $ORCL/OracleJava/java-8

#Copy jre file here
cp $DIST/server-jre-8u151-linux-x64.tar.gz /$ORCL/OracleJava/java-8

#To download uncomment below
#wget --no-check-certificate -c --header "Cookie: oraclelicense=accept-securebackup-cookie" http://download.oracle.com/otn-pub/java/jdk/8u151-b12/e758a0de34e24606bca991d704f6dcbf/jdk-8u151-linux-x64.tar.gz

#Edit Dockerfile for JRE version
sed -i 's/server-jre-8u\*-linux-x64.tar.gz/server-jre-8u151-linux-x64.tar.gz/g' Dockerfile


#3.Build the first image ( OL7-slim + JRE)
echo "Build JRE"

./build.sh

#4.Build the second image adding WebLogic 12.1.3 generic
#Move/Download file fmw_12.1.3.0.0_wls.jar here

echo "Build Weblogic"

cp $DIST/fmw_12.1.3.0.0_wls.jar $ORCL/OracleWebLogic/dockerfiles/12.1.3

cd $ORCL/OracleWebLogic/dockerfiles/

./buildDockerImage.sh -v 12.1.3 -g -c

#5. Extend the Oracle WebLogic image by creating a sample empty domain
echo "Extend to Domain"

cp $DIST/*.py $DIST/createServer.sh $ORCL/OracleWebLogic/samples/1213-domain/container-scripts
cd $ORCL/OracleWebLogic/samples/1213-domain/
./build.sh weblogic1

#6. Run Admin server container #1
echo "Run containers"

#Node1 container #1
docker run -d --name=wlsadmin -p 7001:7001 1213-domain
sleep 5

#7. Create Cluster with 2 nodes

#Node2 container #2

docker run -d --name managed_srv_1 --link wlsadmin:wlsadmin -p 7003:7003 -e MS_PORT=7003  1213-domain createServer.sh
sleep 5

#Node3 container #3

docker run -d --name managed_srv_2 --link wlsadmin:wlsadmin -p 7004:7004 -e MS_PORT=7004  1213-domain createServer.sh
