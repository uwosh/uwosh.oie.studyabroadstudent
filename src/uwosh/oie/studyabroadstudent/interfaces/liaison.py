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


class IOIELiaison(Interface):
    """The Liaison to the OIE communicates decisions related to program development and delivery to the Program Manager
    in the OIE and communicates program changes and updates to his/her unit administration. There is only one Liaison
    per program;  all decision-making at the unit level must be communicated to the OIE through the designated liaison.
    The Liaison may also include the OIE Program Manager and/or other OIE staff in conversations or seek input when
    appropriate. The Liaison may also serve as the On-site Program Leader and may also teach one or more of the program
    courses."""
    # TODO Some of these fields also need to be matched to "participant" fields so that we can pull a roster that includes all participants, leaders and co-leaders.
    # TODO Would it be possible for Liaisons and Leaders to log into the system to set up a profile, to include the data with the * in this section, before the application is completed?  This kind of information remains the same over time and wouldn't have to be repeated for each program.  It would also make things less complicated for the Liaison to complete this application if the Leader/Co-leader details were already in the system.
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
        required=True,
    )
    dexteritytextindexer.searchable('office_phone')
    office_phone = schema.TextLine(
        title=_(u'Office Phone'),
        description=_(u'Please include country code (if outside US) and area code'),
        required=True,
    )
    dexteritytextindexer.searchable('mobile_phone_us')
    mobile_phone_us = schema.TextLine(
        title=_(u'Mobile Phone (US)'),
        description=_(u'Please include country code (if outside US) and area code'),
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
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.building',
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
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.college_or_unit',
    )
    role_and_responsibility = field.NamedFile(
        title=_('Role & Responsibility'),
        description=_(u'Upload a signed Program Liaison Role & Responsibilities form'),
    )
    #######################################################
    model.fieldset(
        'Marketing Material',
        label=_(u"Marketing Material"),
        fields=['number_study_abroad_away_fair_flyers', 'number_study_abroad_away_fair_posters', 'number_study_abroad_away_fair_brochures'],
    )
    number_study_abroad_away_fair_flyers = schema.Int(
        title=_(u'Number of Study Abroad/Away Fair Flyers'),
        description=_(u'Indicate the number (max: 999) of flyers, posters and brochures to be sent to you at the beginning of each semester. OIE can respond to additional requests for materials at any time'),
        min=0,
        max=999,
    )
    number_study_abroad_away_fair_posters = schema.Int(
        title=_(u'Number of Study Abroad/Away Fair Posters'),
        description=_(u'Indicate the number (max: 99) of posters, posters and brochures to be sent to you at the beginning of each semester. OIE can respond to additional requests for materials at any time'),
        min=0,
        max=99,
    )
    number_study_abroad_away_fair_brochures = schema.Int(
        title=_(u'Number of Study Abroad/Away Fair Brochures'),
        description=_(u'Indicate the number (max: 999) of brochures, posters and brochures to be sent to you at the beginning of each semester. OIE can respond to additional requests for materials at any time'),
        min=0,
        max=999,
    )



