from plone import api
import logging

PROFILE_ID = 'profile-convert_datagridfields:default'


def reset_datagridfields(context, logger=None):
    """Reset some data grid fields to empty rich text fields.

    Some data grid fields were replaced by a rich text field showing new contained objects. """

    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger('uwosh.oie.studyabroadstudent')

    catalog = api.portal.get_tool('portal_catalog')
    brains = catalog(portal_type='OIEStudyAbroadProgram')
    count = 0
    for brain in brains:
        obj = brain.getObject()
        obj.courses = u'<em>There are currently no courses</em>'
        obj.add_course_link = u'<em>You can add courses after saving this program</em>'
        obj.health_safety_security_documents = u'<em>There are currently no documents</em>'
        obj.add_health_document_link = '<em>You can add health documents after saving this program</em>'
        obj.travelDatesTransitionsAndDestinations = u'<em>There are currently no transitions</em>'
        obj.add_transition_link = u'<em>You can add transitions after saving this program</em>'
        logger.info('updating %s' % obj.title)
        count += 1

    logger.info('%s datagridfields reset.' % count)
