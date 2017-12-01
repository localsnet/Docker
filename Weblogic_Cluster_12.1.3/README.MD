Building the Weblogic 12.1.3 Cluster with simple domain, based on official Oracle Docker repository https://github.com/oracle/docker-images/tree/master/OracleWebLogic .

The simple script weblogic_dockerize.sh just build images and run 3 containers: Admin Server and 2 Managed Servers as part of Cluster.
The next original files were modified to make the settings for Cluster:
createServer.sh - added running sua_user.py by wlst to create a new user
create-wls-domain.py - added part of WLST commands as a response file to set up the configuration.
sua_user.py - it contents the WLST online  commands to create a new user for deployed app "sua"
