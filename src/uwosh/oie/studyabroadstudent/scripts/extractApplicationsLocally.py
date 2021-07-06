# invoke like this:
# bin/instance run extractApplicationsLocally.py > extractlocallyoutput.out

from uwosh.oie.studyabroadstudent.listApplicationIDsoutput import application_ids
from xmlrpc.client import ServerProxy

# get the localhost site Manager login credentials from environment variables
import os


local_user = os.environ['LOCALUSER']
if not local_user:
    print('missing environment variable value "LOCALUSER"')  # noqa: T001
    exit(1)
local_passwd = os.environ['LOCALPASSWD']
if not local_passwd:
    print('missing environment variable value "LOCALPASSWD"')  # noqa: T001
    exit(1)
local_site_id = os.environ['LOCALSITEID']
if not local_site_id:
    print('missing environment variable value "LOCALSITEID"')  # noqa: T001
    exit(1)

# ok to use HTTP for localhost
server = ServerProxy(
    'http://{u}:{p}@localhost:8080/{s}'.format(
        u=local_user,
        p=local_passwd,
        s=local_site_id,
    ),
)

print('app_data = [')  # noqa: T001

for id in application_ids:
    print(server.extractApplication(id))  # noqa: T001

print(']')  # noqa: T001
