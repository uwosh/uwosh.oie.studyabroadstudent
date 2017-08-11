#!/Users/kim/PloneBuilds/Plone-5.0.4-unified-clean/zinstance/bin/python
#
# invoke like this:
# bin/instance run extractApplicationsLocally.py > extractlocallyoutput.out

import xmlrpclib
from uwosh.oie.studyabroadstudent.listApplicationIDsoutput import application_ids
from datetime import datetime, date
import DateTime

# get the localhost site Manager login credentials from environment variables
import os
local_user = os.environ['LOCALUSER']
if not local_user:
    print "missing environment variable value 'LOCALUSER'"
    exit (1)
local_passwd = os.environ['LOCALPASSWD']
if not local_passwd:
    print "missing environment variable value 'LOCALPASSWD'"
    exit (1)

# ok to use HTTP for localhost
server=xmlrpclib.ServerProxy('https://%s:%s@localhost:8080' % (local_user, local_passwd))

for id in application_ids:
    print server.extractApplication(id)