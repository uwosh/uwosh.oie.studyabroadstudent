# -*- coding: utf-8 -*-
from currencies import Currency
from plone import api
from plone.app.vocabularies.terms import safe_simplevocabulary_from_values
from plone.i18n.normalizer.interfaces import IIDNormalizer
from uwosh.oie.studyabroadstudent import _
from zope.component import queryUtility
from zope.interface import implementer
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


MAX_LENGTH = 250

yes_no_none_vocabulary = SimpleVocabulary(
    [
        SimpleTerm(value=''),
        SimpleTerm(value='Yes'),
        SimpleTerm(value='No'),
    ],
)

yes_no_na_vocabulary = SimpleVocabulary(
    [
        SimpleTerm(value='n/a'),
        SimpleTerm(value='Yes'),
        SimpleTerm(value='No'),
    ],
)

month_vocabulary = SimpleVocabulary(
    [SimpleTerm(value=u'01', title=_(u'January')),
     SimpleTerm(value=u'02', title=_(u'February')),
     SimpleTerm(value=u'03', title=_(u'March')),
     SimpleTerm(value=u'04', title=_(u'April')),
     SimpleTerm(value=u'05', title=_(u'May')),
     SimpleTerm(value=u'06', title=_(u'June')),
     SimpleTerm(value=u'07', title=_(u'July')),
     SimpleTerm(value=u'08', title=_(u'August')),
     SimpleTerm(value=u'09', title=_(u'September')),
     SimpleTerm(value=u'10', title=_(u'October')),
     SimpleTerm(value=u'11', title=_(u'November')),
     SimpleTerm(value=u'12', title=_(u'December'))],
)

graduation_month_vocabulary = SimpleVocabulary(
    [SimpleTerm(value=u'05', title=_(u'May')),
     SimpleTerm(value=u'08', title=_(u'August')),
     SimpleTerm(value=u'12', title=_(u'December'))],
)

dayofmonth_vocabulary = SimpleVocabulary(
    [SimpleTerm(value=u'01'),
     SimpleTerm(value=u'02'),
     SimpleTerm(value=u'03'),
     SimpleTerm(value=u'04'),
     SimpleTerm(value=u'05'),
     SimpleTerm(value=u'06'),
     SimpleTerm(value=u'07'),
     SimpleTerm(value=u'08'),
     SimpleTerm(value=u'09'),
     SimpleTerm(value=u'10'),
     SimpleTerm(value=u'11'),
     SimpleTerm(value=u'12'),
     SimpleTerm(value=u'13'),
     SimpleTerm(value=u'14'),
     SimpleTerm(value=u'15'),
     SimpleTerm(value=u'16'),
     SimpleTerm(value=u'17'),
     SimpleTerm(value=u'18'),
     SimpleTerm(value=u'19'),
     SimpleTerm(value=u'20'),
     SimpleTerm(value=u'21'),
     SimpleTerm(value=u'22'),
     SimpleTerm(value=u'23'),
     SimpleTerm(value=u'24'),
     SimpleTerm(value=u'25'),
     SimpleTerm(value=u'26'),
     SimpleTerm(value=u'27'),
     SimpleTerm(value=u'28'),
     SimpleTerm(value=u'29'),
     SimpleTerm(value=u'30'),
     SimpleTerm(value=u'31'),
     ],
)

room_type_vocabulary = SimpleVocabulary(
    [
        SimpleTerm(value=u'Single Room', title=_(u'Single Room')),
        SimpleTerm(value=u'Double Room', title=_(u'Double Room')),
        SimpleTerm(value=u'Triple Room', title=_(u'Triple Room')),
    ],
)

smoking_vocabulary = SimpleVocabulary(
    [
        SimpleTerm(value=u'Smoking', title=_(u'Smoking')),
        SimpleTerm(value=u'Non-smoking', title=_(u'Non-smoking')),
        SimpleTerm(value=u'No Preference', title=_(u'No Preference')),
    ],
)

semester_vocabulary = SimpleVocabulary(
    [
        SimpleTerm(value=u'Fall', title=_(u'Fall')),
        SimpleTerm(value=u'Fall Interim', title=_(u'Fall Interim')),
        SimpleTerm(value=u'Spring', title=_(u'Spring')),
        SimpleTerm(value=u'Spring Interim', title=_(u'Spring Interim')),
        SimpleTerm(value=u'Summer', title=_(u'Summer')),
    ],
)

student_type_vocabulary = SimpleVocabulary(
    [
        SimpleTerm(value=u'UW Oshkosh Freshman', title=_(u'UW Oshkosh Freshman')),  # noqa
        SimpleTerm(value=u'UW Oshkosh Sophomore', title=_(u'UW Oshkosh Sophomore')),  # noqa
        SimpleTerm(value=u'UW Oshkosh Junior', title=_(u'UW Oshkosh Junior')),
        SimpleTerm(value=u'UW Oshkosh Senior', title=_(u'UW Oshkosh Senior')),
        SimpleTerm(value=u'UW Oshkosh Graduate Student', title=_(u'UW Oshkosh Graduate Student')),  # noqa
        SimpleTerm(value=u'Student at another University (please complete and submit the "Special Student" form)',  # noqa
                   title=_(u'Student at another University (please complete and submit the "Special Student" form)')),  # noqa
        SimpleTerm(value=u'I am not a Student (please complete and submit the "Special Student" form)',  # noqa
                   title=_(u'I am not a Student (please complete and submit the "Special Student" form)')),  # noqa
    ],
)

bus_vocabulary = SimpleVocabulary(
    [
        SimpleTerm(value=u'I will take the group bus from Oshkosh to the airport',  # noqa
                   title=_(u'I will take the group bus from Oshkosh to the airport')),  # noqa
        SimpleTerm(value=u'I will arrange for my own transportation from Oshkosh to the airport.',  # noqa
                   title=_(u'I will arrange for my own transportation from Oshkosh to the airport.')),  # noqa
    ],
)

fly_vocabulary = SimpleVocabulary(
    [
        SimpleTerm(value=u'I will fly with the group', title=_(u'I will fly with the group')),  # noqa
        SimpleTerm(value=u'I will deviate from the group itinerary',
                   title=_(u'I will deviate from the group itinerary')),
    ],
)

orientation_conflict_vocabulary = SimpleVocabulary(
    [
        SimpleTerm(value=u'No', title=_(u'No')),
        SimpleTerm(value=u'Yes, I have a conflict on (enter the date next):',
                   title=_(u'Yes, I have a conflict on (enter the date next):')),  # noqa
        SimpleTerm(value=u'No dates are listed', title=_(u'No dates are listed')),  # noqa
    ],
)

hold_vocabulary = SimpleVocabulary(
    [
        SimpleTerm(value=u'HOLD', title=_(u'HOLD')),
        SimpleTerm(value=u'PROCESS', title=_(u'PROCESS')),
    ],
)

aware_vocabulary = SimpleVocabulary(
    [
        SimpleTerm(value=u'Yes, I am aware of the application requirements for my program',  # noqa
                   title=_(u'Yes, I am aware of the application requirements for my program')),  # noqa
        SimpleTerm(value=u'There are no additional application requirements for my program',  # noqa
                   title=_(u'There are no additional application requirements for my program')),  # noqa
    ],
)

load_or_overload = SimpleVocabulary(
    [
        SimpleTerm(value=u'Part of load', title=_(u'Part of load'), token='load'),  # noqa
        SimpleTerm(value=u'Overload', title=_(u'Overload'), token='overload'),
    ],
)

replacement_costs = SimpleVocabulary(
    [
        SimpleTerm(value=u'No replacement costs due to the College',
                   title=_(u'No replacement costs due to the College'), token='not-due'),  # noqa
        SimpleTerm(value=u'Replacement costs due to the College', title=_(u'Replacement costs due to the College'),  # noqa
                   token='due'),
    ],
)

paid_by = SimpleVocabulary(
    [
        SimpleTerm(value=u'Paid by the College', title=_(u'Paid by the College'), token='college'),  # noqa
        SimpleTerm(value=u'Paid by external partner', title=_(u'Paid by external partner'), token='external'),  # noqa
        SimpleTerm(value=u'Paid by study away students', title=_(u'Paid by study away students'), token='students'),  # noqa
    ],
)

rate_or_lump_sum = SimpleVocabulary(
    [
        SimpleTerm(value=u'2.5% per credit (faculty rate)', title=_(u'2.5% per credit (faculty rate)'), token='2.5'),  # noqa
        SimpleTerm(value=u'3.33% per credit (academic staff rate)', title=_(u'3.33% per credit (academic staff rate)'), token='3.33'),  # noqa
        SimpleTerm(value=u'Lump sum', title=_(u'Lump sum'), token='lump-sum'),
    ],
)

socialmediaservice = SimpleVocabulary(
    [
        SimpleTerm(value=u'Skype', title=_(u'Skype'), token='skype'),
        SimpleTerm(value=u'Viber', title=_(u'Viber'), token='viber'),
        SimpleTerm(value=u'WeChat', title=_(u'WeChat'), token='wechat'),
        SimpleTerm(value=u'WhatsApp', title=_(u'WhatsApp'), token='whatsapp'),
        SimpleTerm(value=u'Facebook', title=_(u'Facebook'), token='facebook'),
        SimpleTerm(value=u'Twitter', title=_(u'Twitter'), token='twitter'),
    ],
)

contactrelationship = SimpleVocabulary(
    [
        SimpleTerm(value=u'father', title=_(u'father'), token='father'),
        SimpleTerm(value=u'mother', title=_(u'mother'), token='mother'),
        SimpleTerm(value=u'grandfather', title=_(u'grandfather'), token='grandfather'),  # noqa
        SimpleTerm(value=u'grandmother', title=_(u'grandmother'), token='grandmother'),  # noqa
        SimpleTerm(value=u'uncle', title=_(u'uncle'), token='uncle'),
        SimpleTerm(value=u'aunt', title=_(u'aunt'), token='aunt'),
        SimpleTerm(value=u'brother', title=_(u'brother'), token='brother'),
        SimpleTerm(value=u'sister', title=_(u'sister'), token='sister'),
        SimpleTerm(value=u'spouse', title=_(u'spouse'), token='spouse'),
        SimpleTerm(value=u'adult child', title=_(u'adult child'), token='adult-child'),  # noqa
        SimpleTerm(value=u'other relative', title=_(u'other relative'), token='other-relative'),  # noqa
    ],
)

departure_transfer_vocabulary = SimpleVocabulary(
    [
        SimpleTerm(u'-- choose one --'),
        SimpleTerm(u'I will transfer from Oshkosh with the group.'),
        SimpleTerm(u'I will transfer from Fond du Lac with the group.'),
        SimpleTerm(u'I will transfer from Milwaukee with the group.'),
        SimpleTerm(u'I will arrange my own transportation.'),
    ],
)

departure_mode_transportation_vocabulary = SimpleVocabulary(
    [
        SimpleTerm(u'I will fly to and from my program site with the group.'),
        SimpleTerm(u'I will fly with the group to my program site but will apply for permission to arrange an alternative flight home.'),  # noqa
        SimpleTerm(u'I will apply for permission to fly to my program site on an alternative flight but will return from my program site with the group.'),  # noqa
        SimpleTerm(u'I will apply for permission to fly to and from my program site on an alternative flight.'),  # noqa
    ],
)

return_mode_transportation_vocabulary = SimpleVocabulary(
    [
        SimpleTerm(u'I will fly with the group'),
        SimpleTerm(u'I will apply for permission to arrange my own flight'),
        SimpleTerm(u'I will drive back to my home at the end of my program (U.S. and Canada programs only)'),  # noqa
    ],
)

return_transfer_vocabulary = SimpleVocabulary(
    [
        SimpleTerm(u'-- choose one --'),
        SimpleTerm(u'I will transfer back to Oshkosh with the group.'),
        SimpleTerm(u'I will transfer back to Fond du Lac with the group.'),
        SimpleTerm(u'I will transfer back to Milwaukee with the group.'),
        SimpleTerm(u'I will arrange my own transportation home.'),
    ],
)

program_cycle_vocabulary = SimpleVocabulary(
    [
        SimpleTerm(token=u'once', value=u'once', title=_(u'once')),
        SimpleTerm(token=u'annually', value=u'annually', title=_(u'annually')),
        SimpleTerm(token=u'every-2-years', value=u'every 2 years', title=_(u'every 2 years')),  # noqa
        SimpleTerm(token=u'every-3-years', value=u'every 3 years', title=_(u'every 3 years')),  # noqa
    ],
)

seat_assignment_protocol = SimpleVocabulary(
    [
        SimpleTerm(token=u'in-order', value=u'in-order', title=_(u'Seats are assigned in the order in which qualified applicants have completed STEPS I & II of the application process, provided STEP III has also been completed by the STEP III application deadline.  This means that you may be conditionally admitted following completion of steps I & II, but NOT receive a seat if you then fail to complete STEP III on time.  If you are on the waiting list, you may receive a seat if applicants who have been conditionally admitted have not completed STEP III by the deadline.  In the rare event that applications can be accepted after deadlines, seats are assigned in the order in which qualified applicants have completed all three steps.')),  # noqa
        SimpleTerm(token=u'competitive', value=u'competitive', title=_(u'Seat assignments on this program are competitive.  Applicants who meet the STEP II application deadilne are placed in a pool for consideration.  Selections will take place just after the STEP II deadline & prior to the STEP III deadline.  Selection is conditional upon completion of STEP III by the STEP III application deadline.  This means that you may be conditionally selected following completion of steps I & II, but NOT receive a seat if you then fail to complete STEP III on time.  If you are on the waiting list, you may receive a seat if applicants who have been conditionally selected have not completed STEP III by the deadline.  In the rare event that applications can be accepted after deadlines, applicants are considered in the order in which they have completed all three steps.')),  # noqa
    ],
)

salary_form = SimpleVocabulary(
    [
        SimpleTerm(u'Payment to Individual Form (PTF) - Direct Payment'),
        SimpleTerm(u'Transaction Transfer Request (TTR) - Replacement Costs'),
        SimpleTerm(u'Foundation'),
        SimpleTerm(u'Not Applicable'),
    ],
)

selection_criteria_vocabulary = SimpleVocabulary(
    [
        SimpleTerm(value='Set selection criteria'),
        SimpleTerm(value='There are no additional selection criteria'),
    ],
)


@implementer(IContextSourceBinder)
class RegistryValueVocabulary(object):

    def __init__(self, value_name):
        self.value_name = value_name

    def __call__(self, context):
        values = api.portal.get_registry_record(self.value_name)
        return safe_simplevocabulary_from_values(values)


@implementer(IVocabularyFactory)
class ContactsVocabularyFactory(object):

    def __call__(self, context):
        catalog = api.portal.get_tool('portal_catalog')
        brains = catalog(portal_type='OIEContact',
                         sort_on='sortable_title',
                         sort_order='ascending')
        terms = []
        for brain in brains:
            token = brain.getPath()
            terms.append(SimpleTerm(
                value=brain.UID,
                token=token,
                title=brain.Title.decode('utf8'),
            ))
        return SimpleVocabulary(terms)


ContactsVocabulary = ContactsVocabularyFactory()


@implementer(IVocabularyFactory)
class CalendarYearVocabularyFactory(object):

    def __call__(self, context):
        catalog = api.portal.get_tool('portal_catalog')
        brains = catalog(portal_type='OIECalendarYear',
                         sort_on='sortable_title',
                         sort_order='ascending')
        terms = []
        for brain in brains:
            token = brain.getPath()
            terms.append(SimpleTerm(
                value=brain.UID,
                token=token,
                title=brain.Title.decode('utf8'),
            ))
        return SimpleVocabulary(terms)


CalendarYearVocabulary = CalendarYearVocabularyFactory()


@implementer(IVocabularyFactory)
class CooperatingPartnerVocabularyFactory(object):

    def __call__(self, context):
        catalog = api.portal.get_tool('portal_catalog')
        brains = catalog(portal_type='OIECooperatingPartner',
                         sort_on='sortable_title',
                         sort_order='ascending')
        terms = []
        for brain in brains:
            token = brain.getPath()
            terms.append(SimpleTerm(
                value=brain.UID,
                token=token,
                title=brain.Title.decode('utf8'),
            ))
        return SimpleVocabulary(terms)


CooperatingPartnerVocabulary = CooperatingPartnerVocabularyFactory()


@implementer(IVocabularyFactory)
class NewProgramsVocabularyFactory(object):

    def __call__(self, context):
        catalog = api.portal.get_tool('portal_catalog')
        brains = catalog(portal_type='OIEStudyAbroadProgram',
                         sort_on='sortable_title',
                         sort_order='ascending')
        terms = []
        for brain in brains:
            token = brain.getPath()
            terms.append(SimpleTerm(
                value=brain.UID,
                token=token,
                title=brain.Title.decode('utf8'),
            ))
        return SimpleVocabulary(terms)


NewProgramsVocabulary = NewProgramsVocabularyFactory()


@implementer(IVocabularyFactory)
class AirlineVocabularyFactory(object):

    def __call__(self, context):
        catalog = api.portal.get_tool('portal_catalog')
        brains = catalog(portal_type='OIEAirline',
                         sort_on='sortable_title',
                         sort_order='ascending')
        terms = []
        for brain in brains:
            token = brain.getPath()
            terms.append(SimpleTerm(
                value=brain.UID,
                token=token,
                title=brain.Title.decode('utf8'),
            ))
        return SimpleVocabulary(terms)


AirlineVocabulary = AirlineVocabularyFactory()


@implementer(IVocabularyFactory)
class ProgramLeaderVocabularyFactory(object):

    def __call__(self, context):
        catalog = api.portal.get_tool('portal_catalog')
        brains = catalog(portal_type='OIEProgramLeader',
                         sort_on='sortable_title',
                         sort_order='ascending')
        terms = []
        for brain in brains:
            token = brain.getPath()
            terms.append(SimpleTerm(
                value=brain.UID,
                token=token,
                title=brain.Title.decode('utf8'),
            ))
        return SimpleVocabulary(terms)


ProgramLeaderVocabulary = ProgramLeaderVocabularyFactory()


@implementer(IVocabularyFactory)
class LiaisonVocabularyFactory(object):

    def __call__(self, context):
        catalog = api.portal.get_tool('portal_catalog')
        brains = catalog(portal_type='OIELiaison',
                         sort_on='sortable_title',
                         sort_order='ascending')
        terms = []
        for brain in brains:
            token = brain.getPath()
            terms.append(SimpleTerm(
                value=brain.UID,
                token=token,
                title=brain.Title.decode('utf8'),
            ))
        return SimpleVocabulary(terms)


LiaisonVocabulary = LiaisonVocabularyFactory()


@implementer(IVocabularyFactory)
class CurrencyVocabularyFactory(object):

    def __call__(self, context):
        values = [v for v in Currency.money_formats.keys() if v != 'USD']
        values.sort()
        values.insert(0, 'USD')
        normalizer = queryUtility(IIDNormalizer)
        items = [
            SimpleTerm(
                value=i,
                token=normalizer.normalize(i, max_length=MAX_LENGTH),
                title=i,
            ) for i in values
        ]
        return SimpleVocabulary(items)


CurrencyVocabulary = CurrencyVocabularyFactory()


@implementer(IVocabularyFactory)
class ProviderVocabularyFactory(object):

    def __call__(self, context):
        catalog = api.portal.get_tool('portal_catalog')
        brains = catalog(portal_type='OIECooperatingPartner',
                         sort_on='sortable_title',
                         sort_order='ascending')
        terms = []
        for brain in brains:
            token = brain.getPath()
            terms.append(SimpleTerm(
                value=brain.UID,
                token=token,
                title=brain.Title.decode('utf8'),
            ))
        return SimpleVocabulary(terms)


ProviderVocabulary = ProviderVocabularyFactory()


@implementer(IVocabularyFactory)
class FileVocabularyFactory(object):

    def __call__(self, context):
        catalog = api.portal.get_tool('portal_catalog')
        brains = catalog(portal_type='File',
                         sort_on='sortable_title',
                         sort_order='ascending')
        terms = []
        for brain in brains:
            token = brain.getPath()
            terms.append(SimpleTerm(
                value=brain.UID,
                token=token,
                title=brain.Title.decode('utf8'),
            ))
        return SimpleVocabulary(terms)


FileVocabulary = FileVocabularyFactory()


@implementer(IVocabularyFactory)
class ImageVocabularyFactory(object):

    def __call__(self, context):
        catalog = api.portal.get_tool('portal_catalog')
        brains = catalog(portal_type='Image',
                         sort_on='sortable_title',
                         sort_order='ascending')
        terms = []
        for brain in brains:
            token = brain.getPath()
            terms.append(SimpleTerm(
                value=brain.UID,
                token=token,
                title=brain.Title.decode('utf8'),
            ))
        return SimpleVocabulary(terms)


ImageVocabulary = ImageVocabularyFactory()
