#!/Users/kim/PloneBuilds/Plone-5.0.4-unified-clean/zinstance/bin/python
#
# invoke like this:
# bin/instance run extractApplicationsRemotely.py > extractApplicationsRemotely-output-201708101325.out

import xmlrpclib
from uwosh.oie.studyabroadstudent.listApplicationIDsoutput import application_ids
from datetime import datetime, date
import DateTime
import argparse
import logging
import os

logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(
    description='...')
parser.add_argument('--remote-user', dest='remoteuser', help='specify the username to use to log into the remote site')
parser.add_argument('--remote-password', dest='remotepassword', help='specify the password to use to log into the remote site')
parser.add_argument('--remote-server', dest='remoteserver', help='specify the URL of the remote site, without the leading http:// or https://, but optionally including the port')
parser.add_argument('--http-ok', dest='http_ok', default='no', help='specify yes if you think it is safe to use HTTP, otherwise will default to using HTTPS')
parser.add_argument('--skip-ids', dest='skip_ids', default='no', help='specify yes to skip extracting IDs that have already been extracted, otherwise extracts all IDs listed in application_ids.py')
parser.add_argument('--id-file', dest='id_file', default='', help='specify the filename to read that contains previous output of this script to skip extracting IDs that have already been extracted')
args, _ = parser.parse_known_args()

if args.remoteuser or args.remotepassword or args.remoteserver:
    remote_user = args.remoteuser
    remote_passwd = args.remotepassword
    remote_server = args.remoteserver
else:
    # if not provided on command line, get the remote site URL and Manager login credentials from environment variables
    remote_user = os.environ['REMOTEUSER']
    if not user:
        print "missing both command line argument and environment variable value 'REMOTEUSER'"
        exit (1)
    remote_passwd = os.environ['REMOTEPASSWD']
    if not remote_passwd:
        print "missing both command line argument and environment variable value 'REMOTEPASSWD'"
        exit (1)
    remote_server = os.environ['REMOTESERVER']
    if not remote_server:
        print "missing both command line argument and environment variable value 'REMOTESERVER'"
        exit (1)

if args.http_ok != 'no':
    HTTPSONLY = False
else:
    HTTPSONLY = True

if args.skip_ids != 'no':
    if not args.id_file or args.id_file != '':
        # TODO read the file, extract IDs, populate the already_read array
        already_read = []
        f = open(args.id_file, 'r')
        for line in f:
            if line.startswith("['"):
                application_id = line[2:(line.find("'", 2))]
                already_read.append(application_id)
        print "read IDs file successfully, going to skip %s contained IDs" % len(already_read)
        SKIP_IDS = True
    else:
        try:
            from uwosh.oie.studyabroadstudent.already_read import already_read
            SKIP_IDS = True
        except:
            SKIP_IDS = False
            print "Unable to read list of IDs to skip"
            exit(1)
else:
    SKIP_IDS = False

# assume HTTPS because HTTP is unsafe
if HTTPSONLY:
    server=xmlrpclib.ServerProxy('https://%s:%s@%s' % (remote_user, remote_passwd, remote_server))
else:
    server=xmlrpclib.ServerProxy('http://%s:%s@%s' % (remote_user, remote_passwd, remote_server))

for id in application_ids:
    if SKIP_IDS and id in already_read:
        #print "skipping", id
        pass
    else:
        print server.extractApplication(id)
