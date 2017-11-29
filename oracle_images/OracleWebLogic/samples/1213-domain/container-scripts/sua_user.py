from weblogic.management.security.authentication import UserEditorMBean
print "Connecting to server..."
connect('weblogic','weblogic1','t3://wlsadmin:7001')
atnr=cmo.getSecurityConfiguration().getDefaultRealm().lookupAuthenticationProvider("DefaultAuthenticator")
print "Creating a user ..."
try:
 atnr.createUser('sua_all','Q1w2e3r4t5','user')
 print "Created user successfully"
except Exception:
 print "User already exists"

