# -*- coding: utf-8 -*-

# use this code to create a Script (Python) in the portal_skins/custom
#   folder of the site using the Management Interface

catalog = context.portal_catalog  # noqa
# we do two queries so this works on both legacy and new sites
results1 = catalog.searchResults(portal_type='OIEStudentApplication')  # noqa
results2 = catalog.searchResults(  # noqa
    portal_type='OIEStudyAbroadStudentApplication',
)
print '# retrieved this many OIEStudentApplication object IDs: {0}'.format(  # noqa
    len(results1)+len(results2),
)
print 'application_ids = ', [o.id for o in results1+results2]  # noqa
return printed  # noqa
