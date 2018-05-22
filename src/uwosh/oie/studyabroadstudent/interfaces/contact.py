# -*- coding: utf-8 -*-

from uwosh.oie.studyabroadstudent import _
from zope import schema
from zope.interface import Interface
from collective import dexteritytextindexer
from uwosh.oie.studyabroadstudent.vocabularies import socialmediaservice
from zope.schema import ValidationError
from Products.CMFPlone.RegistrationTool import checkEmailAddress, EmailAddressInvalid
from plone.directives import form


class InvalidEmailAddress(ValidationError):
    "Invalid email address"


def validate_email(value):
    try:
        checkEmailAddress(value)
    except EmailAddressInvalid:
        raise InvalidEmailAddress(value)
    return True


class IOIEContact(Interface):
    dexteritytextindexer.searchable('title')
    form.mode(title="display")
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
        required=False,
    )
    dexteritytextindexer.searchable('phone')
    phone = schema.TextLine(
        title=_(u'Phone'),
        description=_(u'Please include country code (if outside US) and area code'),
        required=False,
    )
    dexteritytextindexer.searchable('mobile_phone')
    mobile_phone = schema.TextLine(
        title=_(u'Mobile Phone'),
        description=_(u'Please include country code (if outside US) and area code'),
        required=False,
    )
    dexteritytextindexer.searchable('email')
    email = schema.TextLine(
        title=_(u'Email'),
        required=False,
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
