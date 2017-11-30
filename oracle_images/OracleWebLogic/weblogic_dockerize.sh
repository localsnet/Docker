#!/bin/bash
#Building a Docker Image for WebLogic 
ORCL=~/repos_git/oracle_images
DIST=~/repos_git/dist_oracle
#1.Git clone the Oracle Docker project repository
git clone https://github.com/oracle/docker-images.git

mv docker-images oracle_images && cd oracle_images

#2.Download required JRE file

cd $ORCL/OracleJava/java-8

#Copy/Download work jre file here

# New version  JRE didn't work, got error "need JDK"
#wget -c http://javadl.oracle.com/webapps/download/AutoDL?BundleId=227542_e758a0de34e24606bca991d704f6dcbf && mv AutoDL* jre-8u151-linux-x64.tar.gz
wget --no-check-certificate -c --header "Cookie: oraclelicense=accept-securebackup-cookie" http://download.oracle.com/otn-pub/java/jdk/8u151-b12/e758a0de34e24606bca991d704f6dcbf/jdk-8u151-linux-x64.tar.gz

#Edit Dockerfile for JRE version
sed -i 's/server-jre-8u\*-linux-x64.tar.gz/jdk-8u151-linux-x64.tar.gz/g' Dockerfile

#3.Build the first image ( OL7-slim + JRE)
./build.sh

#4.Build the second image adding WebLogic 12.1.3 generic
cd $ORCL/OracleWebLogic/dockerfiles/

#Move/Download file fmw_12.1.3.0.0_wls.jar here
mv $DIST/fmw_12.1.3.0.0_wls.jar .
./buildDockerImage.sh -v 12.1.3 -g -c

#5. Extend the Oracle WebLogic image by creating a sample empty domain
cd $ORCL/OracleWebLogic/samples/1213-domain/
./build.sh weblogic1

#6. Run Admin server container #1
docker run -d --name=wlsadmin -p 7001:7001 1213-domain
sleep 5
#7. Create Cluster with 2 nodes

#Node1 container #2

docker run -d --name managed_srv_1 --link wlsadmin:wlsadmin -p 7003:7003 -e MS_PORT=7003  1213-domain createServer.sh
sleep 5
#Node2 container #3

docker run -d --name managed_srv_2 --link wlsadmin:wlsadmin -p 7004:7004 -e MS_PORT=7004  1213-domain createServer.sh
sleep 5
