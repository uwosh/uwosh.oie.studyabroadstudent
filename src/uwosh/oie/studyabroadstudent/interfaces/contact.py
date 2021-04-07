
from collective import dexteritytextindexer
from plone.autoform.directives import mode
from Products.CMFPlone.RegistrationTool import EmailAddressInvalid, checkEmailAddress
from uwosh.oie.studyabroadstudent import _
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


class IOIEContact(Interface):
    dexteritytextindexer.searchable('title')
    mode(title='hidden')
    title = schema.TextLine(
        title=_('Full Name'),
        required=False,
        default=_('will be auto-generated on save'),
    )
    dexteritytextindexer.searchable('first_name')
    first_name = schema.TextLine(
        title=_('First Name'),
        required=True,
    )
    dexteritytextindexer.searchable('middle_name')
    middle_name = schema.TextLine(
        title=_('Middle Name'),
        required=False,
    )
    dexteritytextindexer.searchable('last_name')
    last_name = schema.TextLine(
        title=_('Last Name'),
        required=True,
    )
    dexteritytextindexer.searchable('job_title')
    job_title = schema.TextLine(
        title=_('Job Title'),
        required=False,
    )
    dexteritytextindexer.searchable('phone')
    phone = schema.TextLine(
        title=_('Phone'),
        description=_('Please include country code (if outside US) and area code'),  # noqa
        required=False,
    )
    dexteritytextindexer.searchable('mobile_phone')
    mobile_phone = schema.TextLine(
        title=_('Mobile Phone'),
        description=_('Please include country code (if outside US) and area code'),  # noqa
        required=False,
    )
    dexteritytextindexer.searchable('email')
    email = schema.TextLine(
        title=_('Email'),
        required=False,
        constraint=validate_email,
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
