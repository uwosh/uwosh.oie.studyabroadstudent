from plone import api
from plone.app.textfield import RichText, RichTextValue
from plone.app.textfield.interfaces import ITransformer

import logging
from uwosh.oie.studyabroadstudent.setuphandlers import _create_account


from plone.registry.interfaces import IRegistry
from Products.CMFPlone.interfaces import IMarkupSchema
from Products.CMFPlone.interfaces import ISiteSchema
from Products.CMFPlone.resources.browser.cook import cookWhenChangingSettings
from Products.CMFCore.utils import getToolByName
from zope.component import getUtility

import six
PROFILE_ID = 'profile-convert_datagridfields:default'


def reset_datagridfields(context, logger=None):
    """Reset some data grid fields to empty rich text fields.
    Some data grid fields were replaced by a rich text field showing new
    contained objects. """

    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger('uwosh.oie.studyabroadstudent')

    catalog = api.portal.get_tool('portal_catalog')
    brains = catalog(portal_type='OIEStudyAbroadProgram')
    count = 0
    for brain in brains:
        obj = brain.getObject()
        if not isinstance(obj.courses, RichText):
            obj.courses = \
                RichTextValue(raw='<em>There are currently no courses</em>')
        if (getattr(obj.add_course_link, 'raw', None) and
            len(obj.add_course_link.raw) == 0) or \
            (not getattr(obj.add_course_link, 'raw', None) and
             len(obj.add_course_link) == 0):
            obj.add_course_link = \
                RichTextValue(
                    raw='<em>You can add courses after saving this program</em>',  # noqa
                )
        if not isinstance(obj.health_safety_security_documents, RichText):
            obj.health_safety_security_documents = \
                RichTextValue(
                    raw='<em>There are currently no documents</em>',
                )
        if (getattr(obj.add_health_document_link, 'raw', None) and
            len(obj.add_health_document_link.raw) == 0) or \
            (not getattr(obj.add_health_document_link, 'raw', None) and
             len(obj.add_health_document_link) == 0):
            obj.add_health_document_link = \
                RichTextValue(
                    raw='<em>You can add health documents after saving this program</em>',  # noqa
                )
        if not isinstance(obj.travelDatesTransitionsAndDestinations, RichText):
            obj.travelDatesTransitionsAndDestinations = \
                RichTextValue(
                    raw='<em>There are currently no transitions</em>',
                )
        if (getattr(obj.add_transition_link, 'raw', None) and
            len(obj.add_transition_link.raw) == 0) or \
            (not getattr(obj.add_transition_link, 'raw', None) and
             len(obj.add_transition_link) == 0):
            obj.add_transition_link = \
                RichTextValue(
                    raw='<em>You can add transitions after saving this program</em>',  # noqa
                )
        logger.info(f'updated rich text fields for {obj.title}')
        count += 1

    logger.info(f'{count} items migrated')


def handle_richtext_description(context, logger=None):
    """Convert old Program richtext description fields to regular text, and
    move their value to the new rich_description field"""
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger('uwosh.oie.studyabroadstudent')
    catalog = api.portal.get_tool('portal_catalog')
    brains = catalog(portal_type='OIEStudyAbroadProgram')
    count = 0
    for brain in brains:
        obj = brain.getObject()
        description = obj.description, RichText
        if isinstance(description, RichTextValue):
            obj.rich_description = description
            transformer = ITransformer(obj)
            obj.description = transformer(obj.description, 'text/plain')
        logger.info(f'converted rich description for {obj.title}')
        count += 1
    logger.info(f'{count} items migrated')


def handle_files_upgrade(context, logger=None):
    """zope.schema.ASCII inherits from NativeString.
    With Python 2 this is the same as Bytes, but with Python 3 not:
    you get a WrongType error when saving the site-controlpanel.
    """
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger('uwosh.oie.studyabroadstudent')
    OIE_PREFIX = 'oiestudyabroadstudent'

    from plone.registry import field
    from plone.registry import Record

    registry = getUtility(IRegistry)
    for file_title in [
        'state_of_wisconsin_need_based_travel_grant_form',
        'special_student_form_for_undergraduate_admissions',
        'disciplinary_clearance_form',
        'uwo_logo',
    ]:
        record_key = f'{OIE_PREFIX}.{file_title}'
        record = registry.records[record_key]
        if not isinstance(record.field, field.ASCII):
            # All is well.
            registry.registerInterface(ISiteSchema, prefix=OIE_PREFIX)
            continue
        # Keep the original value so we can restore it.
        original_value = record.value
        # Delete the bad record.
        del registry.records[record_key]
        # Make sure the site schema is fully registered again.
        # This should recreate the field correctly.
        registry.registerInterface(ISiteSchema, prefix=OIE_PREFIX)
        if original_value is None:
            # Nothing left to do.
            continue
        new_record = registry.records[record_key]
        if isinstance(original_value, six.text_type):
            # fromUnicode could be called from Text in Python 3.
            new_value = new_record.field.fromUnicode(original_value)
        elif isinstance(original_value, bytes):
            # Unlikely, but let's be careful.
            new_value = original_value
        else:
            # Anything else is broken.
            continue
        # Save the new value.
        new_record.value = new_value
        logger.info(f'Replaced {record_key} ASCII (native string) field with Bytes field.')


def upgrade_to_1004(context, logger=None):
    PROFILE_ID = 'profile-uwosh.oie.studyabroadstudent:1_0_4'
    setup = getToolByName(context, 'portal_setup')
    setup.runAllImportStepsFromProfile(PROFILE_ID)
    catalog = api.portal.get_tool('portal_catalog')
    for brain in catalog(portal_type='OIEStudyAbroadProgram'):
        catalog.reindexObject(brain.getObject())
    home_page = api.content.create(
        type='OIEHomePage',
        title='Discover Programs Home Page',
        description='This page shows the discover programs page at the site root',
        container=api.portal.get(),
    )
    api.content.transition(
        obj=home_page,
        to_state='published'
    )

def upgrade_to_1005(context, logger=None):
    PROFILE_ID = 'profile-uwosh.oie.studyabroadstudent:1_0_5'
    setup = getToolByName(context, 'portal_setup')
    setup.runAllImportStepsFromProfile(PROFILE_ID)
    _create_account(
        'brian.duncan+Anonymous@wildcardcorp.com',
        'Anonymous_User',
        ['Anonymous'],
    )


def reindex_programs(context, logger=None):
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger('uwosh.oie.studyabroadstudent')
    catalog = api.portal.get_tool('portal_catalog')
    programs = [
        brain.getObject()
        for brain in catalog(portal_type='OIEStudyAbroadProgram')
    ]
    for program in programs:
        logger.info(f'Reindexing {program.title}')
        program.reindexObject()


def upgrade_to_1006(context, logger=None):
    PROFILE_ID = 'profile-uwosh.oie.studyabroadstudent:1_0_6'
    setup = getToolByName(context, 'portal_setup')
    setup.runAllImportStepsFromProfile(PROFILE_ID)

def upgrade_to_1007(context, logger=None):
    PROFILE_ID = 'profile-uwosh.oie.studyabroadstudent:1_0_7'
    setup = getToolByName(context, 'portal_setup')
    setup.runAllImportStepsFromProfile(PROFILE_ID)

def upgrade_to_1008(context, logger=None):
    PROFILE_ID = 'profile-uwosh.oie.studyabroadstudent:1_0_8'
    workflow_tool = getToolByName(context, 'portal_workflow')
    workflow_tool.participant.transitions.deleteTransitions([
        'request-agreement',
        'application-complete',
        'agreement-submitted',
        'move-to-step-iii-check-for-application',
        'move-to-step-iii-conditionally-admitted',
        'move-to-step-iii-pending-materials-review',
        'confirm-alternate-schedule',
        'request-alternate-flight',
    ])
    workflow_tool.participant.states.deleteStates([
        'addressing-site-health,-safety-or-security-incident',
    ])

    setup = getToolByName(context, 'portal_setup')
    setup.runAllImportStepsFromProfile(PROFILE_ID)


def upgrade_to_1009(context, logger=None):
    workflow_tool = getToolByName(context, 'portal_workflow')
    if workflow_tool.participant.transitions.get('omit-special-student-status-application'):
        workflow_tool.participant.transitions.deleteTransitions([
            'omit-special-student-status-application',
        ])
    if not workflow_tool.participant.transitions.get('do-not-require-a-special-student-status-application'):
        workflow_tool.participant.transitions.addTransition('do-not-require-a-special-student-status-application')
    transition_definition = workflow_tool.participant.transitions['do-not-require-a-special-student-status-application']
    transition_definition.setProperties(
        title='Do Not Require a Special Student Status Application',
        new_state_id='background-check',
        actbox_name='Do Not Require a Special Student Status Application',
        actbox_url='%(content_url)s/content_status_modify?workflow_action=do-not-require-a-special-student-status-application',
    )
    exit_transitions = {
        'checking-for-special-student-status': (
            'apply-for-special-student-status-graduate',
            'apply-for-special-student-status-undergraduate',
            'do-not-require-a-special-student-status-application',
        ),
        'pending-special-student-status-undergraduate': (
            'confirm-special-student-status-undergraduate',
            'decline-special-student-status-undergraduate',
            'withdraw',
        ),
        'pending-special-student-status-graduate': (
            'confirm-special-student-status-graduate',
            'decline-special-student-status-graduate',
            'withdraw',
        )
    }
    for key, value in exit_transitions.items():
        workflow_tool.participant.states.get(key).transitions = value
