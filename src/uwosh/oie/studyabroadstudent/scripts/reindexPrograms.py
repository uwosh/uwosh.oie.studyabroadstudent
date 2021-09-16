# invoke like this:
# bin/instance -O run importApplications.py

from plone import api
from zope.component.hooks import getSite, setSite

import argparse
import logging
import transaction

logger = logging.getLogger('uwosh.oie.studyabroadstudent')

parser = argparse.ArgumentParser(
    description='...')
parser.add_argument(
    '--site-id',
    dest='site_id',
    default='OIE',
    help='the ID of the site in which to create the applications; defaults to "OIE"',  # noqa
)

args, _ = parser.parse_known_args()

# Sets the current site as the active site
setSite(app[args.site_id])  # noqa
site = getSite()  # noqa

# Enable the context manager to switch the user
with api.env.adopt_user(username='admin'):
    # You're now posing as admin!

    catalog = site.portal_catalog

    programs = [
        brain.getObject()
        for brain in catalog(portal_type='OIEStudyAbroadProgram')
    ]
    for program in programs:
        logger.info(f'Reindexing {program.title}')
        program.reindexObject()

# final commit transaction
transaction.commit()
# Perform ZEO client synchronization (if running in clustered mode)
app._p_jar.sync()  # noqa: F821

