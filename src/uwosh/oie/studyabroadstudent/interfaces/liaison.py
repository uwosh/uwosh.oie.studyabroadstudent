# -*- coding: utf-8 -*-
from collective import dexteritytextindexer
from plone.directives import form
from plone.namedfile import field
from plone.supermodel import model
from Products.CMFPlone.RegistrationTool import checkEmailAddress
from Products.CMFPlone.RegistrationTool import EmailAddressInvalid
from uwosh.oie.studyabroadstudent import _
from uwosh.oie.studyabroadstudent.vocabularies import RegistryValueVocabulary
from uwosh.oie.studyabroadstudent.vocabularies import socialmediaservice
from zope import schema
from zope.interface import Interface
from zope.schema import ValidationError


class InvalidEmailAddress(ValidationError):
    """Invalid email address"""


def validate_email(value):
    try:
        checkEmailAddress(value)
    except EmailAddressInvalid:
        raise InvalidEmailAddress(value)
    return True


class IOIELiaison(Interface):
    """The Liaison to the OIE communicates decisions related to program
development and delivery to the Program Manager in the OIE and
communicates program changes and updates to his/her unit administration.
There is only one Liaison per program;  all decision-making at the
unit level must be communicated to the OIE through the designated
liaison. The Liaison may also include the OIE Program Manager and/or
other OIE staff in conversations or seek input when appropriate.
The Liaison may also serve as the On-site Program Leader and may
also teach one or more of the program courses.
"""
    dexteritytextindexer.searchable('title')

    form.mode(title='hidden')
    title = schema.TextLine(
        title=_(u'Full Name'),
        required=False,
        default=_(u'will be auto-generated on save'),
    )
    dexteritytextindexer.searchable('first_name')
    first_name = schema.TextLine(
        title=_(u'First Name'),
        required=True,
    )
    dexteritytextindexer.searchable('middle_name')
    middle_name = schema.TextLine(
        title=_(u'Middle Name'),
        required=False,
    )
    dexteritytextindexer.searchable('last_name')
    last_name = schema.TextLine(
        title=_(u'Last Name'),
        required=True,
    )
    dexteritytextindexer.searchable('job_title')
    job_title = schema.TextLine(
        title=_(u'Job Title'),
        required=True,
    )
    dexteritytextindexer.searchable('office_phone')
    office_phone = schema.TextLine(
        title=_(u'Office Phone'),
        description=_(
            u'Please include country code (if outside US) and area code',
        ),
        required=True,
    )
    dexteritytextindexer.searchable('mobile_phone_us')
    mobile_phone_us = schema.TextLine(
        title=_(u'Mobile Phone (US)'),
        description=_(
            u'Please include country code (if outside US) and area code',
        ),
        required=True,
    )
    dexteritytextindexer.searchable('email')
    email = schema.TextLine(
        title=_(u'Email'),
        required=True,
        constraint=validate_email,
    )
    dexteritytextindexer.searchable('other_service')
    other_service = schema.Choice(
        title=_(u'e.g., Line, Skype, Viber, WeChat, WhatsApp'),
        required=False,
        vocabulary=socialmediaservice,
    )
    dexteritytextindexer.searchable('other_username')
    other_username = schema.TextLine(
        title=_(u'username or ID for the above service'),
        required=False,
    )
    dexteritytextindexer.searchable('office_building')
    office_building = schema.Choice(
        title=_(u'Office Building'),
        required=True,
        source=RegistryValueVocabulary('oiestudyabroadstudent.building'),
    )
    dexteritytextindexer.searchable('office_room')
    office_room = schema.TextLine(
        title=_(u'Office Room'),
        required=True,
    )
    dexteritytextindexer.searchable('college_or_unit')
    college_or_unit = schema.Choice(
        title=_(u'College or Unit'),
        description=_(u''),
        required=True,
        source=RegistryValueVocabulary(
            'oiestudyabroadstudent.college_or_unit',
        ),
    )
    role_and_responsibility = field.NamedFile(
        title=_('Role & Responsibility'),
        description=_(
            u'Upload a signed Program Liaison Role & Responsibilities form',
        ),
    )
    #######################################################
    model.fieldset(
        'Marketing Material',
        label=_(u'Marketing Material'),
        fields=['number_study_abroad_away_fair_flyers',
                'number_study_abroad_away_fair_posters',
                'number_study_abroad_away_fair_brochures'],
    )
    number_study_abroad_away_fair_flyers = schema.Int(
        title=_(u'Number of Study Abroad/Away Fair Flyers'),
        description=_(u'Indicate the number (max: 999) of flyers to be sent to you at the beginning of each semester. OIE can respond to additional requests for materials at any time'),  # noqa
        min=0,
        max=999,
    )
    number_study_abroad_away_fair_posters = schema.Int(
        title=_(u'Number of Study Abroad/Away Fair Posters'),
        description=_(u'Indicate the number (max: 99) of posters to be sent to you at the beginning of each semester. OIE can respond to additional requests for materials at any time'),  # noqa
        min=0,
        max=99,
    )
    number_study_abroad_away_fair_brochures = schema.Int(
        title=_(u'Number of Study Abroad/Away Fair Brochures'),
        description=_(u'Indicate the number (max: 999) of brochures to be sent to you at the beginning of each semester. OIE can respond to additional requests for materials at any time'),  # noqa
        min=0,
        max=999,
    )
