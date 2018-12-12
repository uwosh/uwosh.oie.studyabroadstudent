# -*- coding: utf-8 -*-
from plone import api
from plone.app.textfield import RichText
from plone.app.textfield import RichTextValue
from plone.app.textfield.interfaces import ITransformer

import logging


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
        logger.info('updated rich text fields for {0}'.format(obj.title))
        count += 1

    logger.info('{0} items migrated'.format(count))


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
        logger.info('converted rich description for {0}'.format(obj.title))
        count += 1
    logger.info('{0} items migrated'.format(count))
