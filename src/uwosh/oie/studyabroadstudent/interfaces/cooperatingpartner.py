# -*- coding: utf-8 -*-
from collective import dexteritytextindexer
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform.directives import widget
from Products.CMFPlone.RegistrationTool import checkEmailAddress
from Products.CMFPlone.RegistrationTool import EmailAddressInvalid
from uwosh.oie.studyabroadstudent import _
from uwosh.oie.studyabroadstudent.vocabularies import socialmediaservice
from z3c.relationfield.schema import RelationChoice
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


class IOIECooperatingPartner(Interface):

    widget(
        'primary_contact',
        RelatedItemsFieldWidget,
        pattern_options={
            'selectableTypes': ['OIEContact'],
        },
    )
    primary_contact = RelationChoice(
        title=_('Primary Contact'),
        vocabulary='plone.app.vocabularies.Catalog',
        required=True,
    )

    dexteritytextindexer.searchable('website')
    website = schema.URI(
        title=_(u'Partner Web Address'),
        required=True,
    )
    dexteritytextindexer.searchable('hq_address_1')
    hq_address_1 = schema.TextLine(
        title=_(u'Address 1'),
        description=_(u'must be a real address, not a post office box or similar'),  # noqa
        required=True,
    )
    dexteritytextindexer.searchable('hq_address_2')
    hq_address_2 = schema.TextLine(
        title=_(u'Address 2'),
        description=_(u'must be a real address, not a post office box or similar'),  # noqa
        required=False,
    )
    dexteritytextindexer.searchable('hq_city')
    hq_city = schema.TextLine(
        title=_(u'City'),
        description=_(u''),
        required=True,
    )
    dexteritytextindexer.searchable('hq_state')
    hq_state = schema.TextLine(
        title=_(u'State'),
        description=_(u'(or province or equivalent)'),
        required=True,
    )
    dexteritytextindexer.searchable('hq_mailing_code')
    hq_mailing_code = schema.TextLine(
        title=_(u'Mailing Code'),
        description=_(u'Zip or Postal Code or equivalent'),
        required=True,
    )
    dexteritytextindexer.searchable('hq_country')
    hq_country = schema.TextLine(
        title=_(u'Country'),
        description=_(u''),
        required=True,
    )
    dexteritytextindexer.searchable('telephone')
    telephone = schema.TextLine(
        title=_(u'Telephone'),
        description=_(u'Please include country code (if outside US) and area code'),  # noqa
        required=True,
    )
    dexteritytextindexer.searchable('mobile')
    mobile = schema.TextLine(
        title=_(u'Mobile Phone'),
        description=_(u'Please include country code (if outside US) and area code'),  # noqa
        required=True,
    )
    dexteritytextindexer.searchable('email')
    email = schema.TextLine(
        title=_(u'Email'),
        constraint=validate_email,
        required=True,
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
