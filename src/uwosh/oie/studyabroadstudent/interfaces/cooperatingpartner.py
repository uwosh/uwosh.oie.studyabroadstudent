from collective import dexteritytextindexer
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform.directives import widget
from Products.CMFPlone.RegistrationTool import EmailAddressInvalid, checkEmailAddress
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
        title=_('Partner Web Address'),
        required=True,
    )
    dexteritytextindexer.searchable('hq_address_1')
    hq_address_1 = schema.TextLine(
        title=_('Address 1'),
        description=_('must be a real address, not a post office box or similar'),  # noqa
        required=True,
    )
    dexteritytextindexer.searchable('hq_address_2')
    hq_address_2 = schema.TextLine(
        title=_('Address 2'),
        description=_('must be a real address, not a post office box or similar'),  # noqa
        required=False,
    )
    dexteritytextindexer.searchable('hq_city')
    hq_city = schema.TextLine(
        title=_('City'),
        description=_(''),
        required=True,
    )
    dexteritytextindexer.searchable('hq_state')
    hq_state = schema.TextLine(
        title=_('State'),
        description=_('(or province or equivalent)'),
        required=True,
    )
    dexteritytextindexer.searchable('hq_mailing_code')
    hq_mailing_code = schema.TextLine(
        title=_('Mailing Code'),
        description=_('Zip or Postal Code or equivalent'),
        required=True,
    )
    dexteritytextindexer.searchable('hq_country')
    hq_country = schema.TextLine(
        title=_('Country'),
        description=_(''),
        required=True,
    )
    dexteritytextindexer.searchable('telephone')
    telephone = schema.TextLine(
        title=_('Telephone'),
        description=_('Please include country code (if outside US) and area code'),  # noqa
        required=True,
    )
    dexteritytextindexer.searchable('mobile')
    mobile = schema.TextLine(
        title=_('Mobile Phone'),
        description=_('Please include country code (if outside US) and area code'),  # noqa
        required=True,
    )
    dexteritytextindexer.searchable('email')
    email = schema.TextLine(
        title=_('Email'),
        constraint=validate_email,
        required=True,
    )
    dexteritytextindexer.searchable('other_service')
    other_service = schema.Choice(
        title=_('e.g., Line, Skype, Viber, WeChat, WhatsApp'),
        required=False,
        vocabulary=socialmediaservice,
    )
    dexteritytextindexer.searchable('other_username')
    other_username = schema.TextLine(
        title=_('username or ID for the above service'),
        required=False,
    )
