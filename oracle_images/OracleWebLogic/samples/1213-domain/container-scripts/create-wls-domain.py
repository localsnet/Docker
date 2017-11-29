# Copyright (c) 2014-2015 Oracle and/or its affiliates. All rights reserved.
#
# WebLogic on Docker Default Domain
#
# Domain, as defined in DOMAIN_NAME, will be created in this script. Name defaults to 'base_domain'.
#
# Since : October, 2014
# Author: bruno.borges@oracle.com
# ==============================================
domain_name  = os.environ.get("DOMAIN_NAME", "base_domain")
admin_port   = int(os.environ.get("ADMIN_PORT", "7001"))
admin_pass   = os.environ.get("ADMIN_PASSWORD")
cluster_name = os.environ.get("CLUSTER_NAME", "DockerCluster")
domain_path  = '/u01/oracle/user_projects/domains/%s' % domain_name
production_mode         = os.environ.get("PRODUCTION_MODE", "prod")

print('domain_name : [%s]' % domain_name);
print('admin_port  : [%s]' % admin_port);
print('cluster_name: [%s]' % cluster_name);
print('domain_path : [%s]' % domain_path);
print('production_mode : [%s]' % production_mode);

# Open default domain template
# ======================
readTemplate("/u01/oracle/wlserver/common/templates/wls/wls.jar")

set('Name', domain_name)
setOption('DomainName', domain_name)

# Disable Admin Console
# --------------------
# cmo.setConsoleEnabled(false)

# Configure the Administration Server and SSL port.
# =========================================================
cd('/Servers/AdminServer')
set('ListenAddress', '')
set('ListenPort', admin_port)

# Define the user password for weblogic
# =====================================
cd('/Security/%s/User/weblogic' % domain_name)
cmo.setPassword(admin_pass)


# Write the domain and close the domain template
# ==============================================
setOption('OverwriteDomain', 'true')
setOption('ServerStartMode', production_mode)

cd('/NMProperties')
set('ListenAddress','')
set('ListenPort',5556)
set('CrashRecoveryEnabled', 'true')
set('NativeVersionEnabled', 'true')
set('StartScriptEnabled', 'false')
set('SecureListener', 'false')
set('LogLevel', 'FINEST')

# Set the Node Manager user name and password (domain name will change after writeDomain)
cd('/SecurityConfiguration/base_domain')
set('NodeManagerUsername', 'weblogic')
set('NodeManagerPasswordEncrypted', admin_pass)

# Define a WebLogic Cluster
# =========================
cd('/')
create(cluster_name, 'Cluster')

cd('/Clusters/%s' % cluster_name)
cmo.setClusterMessagingMode('unicast')
# SUA

# create JTA
cd('/')
create('base_domain', 'JTA')
cd('/JTA/base_domain')
set('TimeoutSeconds', 300)
# Create a JDBC data source - SUA APP JDBC Data Source
cd('/')
create('SUA APP JDBC Data Source', 'JDBCSystemResource')
cd('/JDBCSystemResources/SUA APP JDBC Data Source')
set('Target', 'DockerCluster')
cd('/JDBCSystemResources/SUA APP JDBC Data Source/JdbcResource/SUA APP JDBC Data Source')
create('SUA APP JDBC Data Source', 'JDBCDriverParams')
cd('JDBCDriverParams/NO_NAME_0')
set('URL', 'jdbc:oracle:thin:@172.26.25.174:1521:orcl')
set('DriverName', 'oracle.jdbc.xa.client.OracleXADataSource')
set('PasswordEncrypted', 'sua_test')
create('Properties', 'Properties')
cd('Properties/NO_NAME_0')
create('user', 'Property')
cd('Property/user')
set('Value', 'sua_test')
cd('/JDBCSystemResources/SUA APP JDBC Data Source/JdbcResource/SUA APP JDBC Data Source')
create('SUA APP JDBC Data Source', 'JDBCDataSourceParams')
cd('JDBCDataSourceParams/NO_NAME_0')
set('JNDINames', 'sua_app/jdbc/DataSource')
cd('/JDBCSystemResources/SUA APP JDBC Data Source/JdbcResource/SUA APP JDBC Data Source')
create('SUA APP JDBC Data Source', 'JDBCConnectionPoolParams')
cd('JDBCConnectionPoolParams/NO_NAME_0')
set('InitSql', 'SQL call InitSession(\'APPLICATION\')')
cd('/JDBCSystemResources/SUA APP JDBC Data Source/JdbcResource/SUA APP JDBC Data Source')
create('SUA APP JDBC Data Source', 'JDBCXAParams')
cd('JDBCXAParams/NO_NAME_0')
set('XaSetTransactionTimeout', 'true')

# Create a JDBC data source - SUA REPORT JDBC Data Source
cd('/')
create('SUA REPORT JDBC Data Source', 'JDBCSystemResource')
cd('/JDBCSystemResources/SUA REPORT JDBC Data Source')
set('Target', 'DockerCluster')
cd('/JDBCSystemResources/SUA REPORT JDBC Data Source/JdbcResource/SUA REPORT JDBC Data Source')
create('SUA REPORT JDBC Data Source', 'JDBCDriverParams')
cd('JDBCDriverParams/NO_NAME_0')
set('URL', 'jdbc:oracle:thin:@172.26.25.174:1521:orcl')
set('DriverName', 'oracle.jdbc.xa.client.OracleXADataSource')
set('PasswordEncrypted', 'sua_test')
create('Properties', 'Properties')
cd('Properties/NO_NAME_0')
create('user', 'Property')
cd('Property/user')
set('Value', 'sua_test')
cd('/JDBCSystemResources/SUA REPORT JDBC Data Source/JdbcResource/SUA REPORT JDBC Data Source')
create('SUA REPORT JDBC Data Source', 'JDBCDataSourceParams')
cd('JDBCDataSourceParams/NO_NAME_0')
set('JNDINames', 'sua_report/jdbc/DataSource')
cd('/JDBCSystemResources/SUA REPORT JDBC Data Source/JdbcResource/SUA REPORT JDBC Data Source')
create('SUA REPORT JDBC Data Source', 'JDBCConnectionPoolParams')
cd('JDBCConnectionPoolParams/NO_NAME_0')
set('InitSql', 'SQL call InitSession(\'REPORT\')')
# Create a JDBC data source - SUA LKO JDBC Data Source
cd('/')
create('SUA LKO JDBC Data Source', 'JDBCSystemResource')
cd('/JDBCSystemResources/SUA LKO JDBC Data Source')
set('Target', 'DockerCluster')
cd('/JDBCSystemResources/SUA LKO JDBC Data Source/JdbcResource/SUA LKO JDBC Data Source')
create('SUA LKO JDBC Data Source', 'JDBCDriverParams')
cd('JDBCDriverParams/NO_NAME_0')
set('URL', 'jdbc:oracle:thin:@172.26.25.174:1521:orcl')
set('DriverName', 'oracle.jdbc.xa.client.OracleXADataSource')
set('PasswordEncrypted', 'nf_user')
create('Properties', 'Properties')
cd('Properties/NO_NAME_0')
create('user', 'Property')
cd('Property/user')
set('Value', 'nf_user')
cd('/JDBCSystemResources/SUA LKO JDBC Data Source/JdbcResource/SUA LKO JDBC Data Source')
create('SUA LKO JDBC Data Source', 'JDBCDataSourceParams')
cd('JDBCDataSourceParams/NO_NAME_0')
set('JNDINames', 'sua_lko/jdbc/DataSource')
cd('/JDBCSystemResources/SUA LKO JDBC Data Source/JdbcResource/SUA LKO JDBC Data Source')
create('SUA LKO JDBC Data Source', 'JDBCXAParams')
cd('JDBCXAParams/NO_NAME_0')
set('XaSetTransactionTimeout', 'true')
# Create a JDBC data source - SUA SUSS JDBC Data Source
cd('/')
create('SUA SUSS JDBC Data Source', 'JDBCSystemResource')
cd('/JDBCSystemResources/SUA SUSS JDBC Data Source')
set('Target', 'DockerCluster')
cd('/JDBCSystemResources/SUA SUSS JDBC Data Source/JdbcResource/SUA SUSS JDBC Data Source')
create('SUA SUSS JDBC Data Source', 'JDBCDriverParams')
cd('JDBCDriverParams/NO_NAME_0')
set('URL', 'jdbc:oracle:thin:@172.26.25.174:1521:orcl')
set('DriverName', 'oracle.jdbc.xa.client.OracleXADataSource')
set('PasswordEncrypted', 'sua_suss')
create('Properties', 'Properties')
cd('Properties/NO_NAME_0')
create('user', 'Property')
cd('Property/user')
set('Value', 'sua_suss')
cd('/JDBCSystemResources/SUA SUSS JDBC Data Source/JdbcResource/SUA SUSS JDBC Data Source')
create('SUA SUSS JDBC Data Source', 'JDBCDataSourceParams')
cd('JDBCDataSourceParams/NO_NAME_0')
set('JNDINames', 'sua_suss/jdbc/DataSource')
# Create a JMS Server
cd('/')
create('suaJMSServer', 'JMSServer')
cd('/JMSServers/suaJMSServer')
set('Target', 'DockerCluster')
# Create a JMS system resource
cd('/')
create('suaJMSModule', 'JMSSystemResource')
cd('/JMSSystemResources/suaJMSModule')
set('Target', 'DockerCluster')
create('suaSubModule', 'SubDeployment')
cd('/JMSSystemResources/suaJMSModule/SubDeployments/suaSubModule')
set('Targets', 'suaJMSServer')
cd('/JMSSystemResources/suaJMSModule/JmsResource/NO_NAME_0')
create('suaConnectionFactory', 'ConnectionFactory')
cd('ConnectionFactories/suaConnectionFactory')
set('JNDIName', 'jms/suaConnectionFactory')
set('SubDeploymentName', 'suaSubModule')
# Create SUA_AUDIT_QUEUE
cd('/JMSSystemResources/suaJMSModule/JmsResource/NO_NAME_0')
create('SUA_AUDIT_QUEUE', 'UniformDistributedQueue')
cd('UniformDistributedQueues/SUA_AUDIT_QUEUE')
set('JNDIName', 'jms/SUA_AUDIT_QUEUE')
set('SubDeploymentName', 'suaSubModule')
create('SUA_AUDIT_QUEUE', 'DeliveryFailureParams')
cd('DeliveryFailureParams/NO_NAME_0')
set('RedeliveryLimit', 2)
cd('/JMSSystemResources/suaJMSModule/JmsResource/NO_NAME_0')
cd('UniformDistributedQueues/SUA_AUDIT_QUEUE')
create('SUA_AUDIT_QUEUE', 'DeliveryParamsOverrides')
cd('DeliveryParamsOverrides/NO_NAME_0')
set('RedeliveryDelay', 120000)
# Create SUA_AUDIT_DEAD_QUEUE
cd('/JMSSystemResources/suaJMSModule/JmsResource/NO_NAME_0')
create('SUA_AUDIT_DEAD_QUEUE', 'UniformDistributedQueue')
cd('UniformDistributedQueues/SUA_AUDIT_DEAD_QUEUE')
set('JNDIName', 'jms/SUA_AUDIT_DEAD_QUEUE')
set('SubDeploymentName', 'suaSubModule')
# Create SUA_REPORT_QUEUE
cd('/JMSSystemResources/suaJMSModule/JmsResource/NO_NAME_0')
create('SUA_REPORT_QUEUE', 'UniformDistributedQueue')
cd('UniformDistributedQueues/SUA_REPORT_QUEUE')
set('JNDIName', 'jms/SUA_REPORT_QUEUE')
set('SubDeploymentName', 'suaSubModule')
# Create NOTIFICATION_EMAIL_QUEUE
cd('/JMSSystemResources/suaJMSModule/JmsResource/NO_NAME_0')
create('NOTIFICATION_EMAIL_QUEUE', 'UniformDistributedQueue')
cd('UniformDistributedQueues/NOTIFICATION_EMAIL_QUEUE')
set('JNDIName', 'jms/NOTIFICATION_EMAIL_QUEUE')
set('SubDeploymentName', 'suaSubModule')
# Create NOTIFICATION_QUEUE
cd('/JMSSystemResources/suaJMSModule/JmsResource/NO_NAME_0')
create('NOTIFICATION_QUEUE', 'UniformDistributedQueue')
cd('UniformDistributedQueues/NOTIFICATION_QUEUE')
set('JNDIName', 'jms/NOTIFICATION_QUEUE')
set('SubDeploymentName', 'suaSubModule')
# Create SUA_LOAD_TASK_QUEUE
cd('/JMSSystemResources/suaJMSModule/JmsResource/NO_NAME_0')
create('SUA_LOAD_TASK_QUEUE', 'UniformDistributedQueue')
cd('UniformDistributedQueues/SUA_LOAD_TASK_QUEUE')
set('JNDIName', 'jms/SUA_LOAD_TASK_QUEUE')
set('SubDeploymentName', 'suaSubModule')



# Write Domain
# ============
writeDomain(domain_path)
closeTemplate()

# Enable JAX-RS 2.0 by default on this domain
# ===========================================
readDomain(domain_path)
addTemplate('/u01/oracle/jaxrs2-template.jar')
assign('Library', 'jax-rs#2.0@2.5.1', 'Target', cluster_name)
assign('Library', 'jax-rs#2.0@2.5.1', 'Target', 'AdminServer')
updateDomain()
closeDomain()

# Exit WLST
# =========
exit()
