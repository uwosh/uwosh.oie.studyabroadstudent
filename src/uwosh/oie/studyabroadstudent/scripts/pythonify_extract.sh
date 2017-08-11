#!/bin/sh
#
# invoke like this:
# ./pythonify_extract.sh extractApplicationsRemotely-output-201708101325.out > extractApplicationsRemotely-output-201708101325.py

echo 'app_data = ['
cat $1 | awk '{ if (length > 0) print $0, "," }'
# TO DO: find a way to ignore or comment out 'too many query results' lines
echo ']'
