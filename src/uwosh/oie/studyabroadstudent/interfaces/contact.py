from datetime import date
from uwosh.oie.studyabroadstudent import _
from zope import schema
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from plone.supermodel import model
from plone.namedfile import field
from collective import dexteritytextindexer
from plone.app.textfield import RichText
from z3c.relationfield.schema import RelationChoice
from plone.autoform.directives import widget
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from collective.z3cform.datagridfield import DataGridFieldFactory, DictRow
from uwosh.oie.studyabroadstudent.vocabularies import yes_no_none_vocabulary, yes_no_na_vocabulary, month_vocabulary, \
    dayofmonth_vocabulary, room_type_vocabulary, smoking_vocabulary, semester_vocabulary, student_type_vocabulary, \
    bus_vocabulary, fly_vocabulary, orientation_conflict_vocabulary, hold_vocabulary, aware_vocabulary, \
    socialmediaservice


class IOIEContact(Interface):
    dexteritytextindexer.searchable('title')
    title = schema.TextLine(
        title=_(u'Full Name'),
        required=True,
        readonly=True,
        default=_(u'will be auto-generated'),
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
        # TODO validate email
        required=False,
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
