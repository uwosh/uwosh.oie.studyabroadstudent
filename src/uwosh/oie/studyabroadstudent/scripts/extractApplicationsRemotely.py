#!/Users/kim/PloneBuilds/Plone-5.0.4-unified-clean/zinstance/bin/python
#
# invoke like this:
# bin/instance run extractApplicationsRemotely.py > extractApplicationsRemotely-output-201708101325.out

import xmlrpclib
from uwosh.oie.studyabroadstudent.listApplicationIDsoutput import application_ids
from datetime import datetime, date
import DateTime

# get the remote site URL and Manager login credentials from environment variables
import os
remote_user = os.environ['REMOTEUSER']
if not user:
    print "missing environment variable value 'REMOTEUSER'"
    exit (1)
remote_passwd = os.environ['REMOTEPASSWD']
if not passwd:
    print "missing environment variable value 'REMOTEPASSWD'"
    exit (1)
remote_server = os.environ['REMOTESERVER']
if not url:
    print "missing environment variable value 'REMOTESERVER'"
    exit (1)

# assume HTTPS because HTTP is unsafe
server=xmlrpclib.ServerProxy('https://%s:%s@%s' % (remote_user, remote_passwd, remote_server))

for id in application_ids:
    print server.extractApplication(id)
