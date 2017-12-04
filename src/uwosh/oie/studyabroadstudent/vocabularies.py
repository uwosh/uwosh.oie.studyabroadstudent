# -*- coding: utf-8 -*-
from plone import api
from plone.i18n.normalizer.interfaces import IIDNormalizer
from zope.component import queryUtility
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from uwosh.oie.studyabroadstudent import _

MAX_LENGTH = 250

yes_no_none_vocabulary = SimpleVocabulary(
    [
        SimpleTerm(value=''),
        SimpleTerm(value='Yes'),
        SimpleTerm(value='No'),
    ]
)

yes_no_na_vocabulary = SimpleVocabulary(
    [
        SimpleTerm(value='n/a'),
        SimpleTerm(value='Yes'),
        SimpleTerm(value='No'),
    ]
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
     SimpleTerm(value=u'12', title=_(u'December'))]
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
     SimpleTerm(value=u'31'), ]
)

room_type_vocabulary = SimpleVocabulary(
    [
        SimpleTerm(value=u'Single Room', title=_(u'Single Room')),
        SimpleTerm(value=u'Double Room', title=_(u'Double Room')),
        SimpleTerm(value=u'Triple Room', title=_(u'Triple Room')),
    ]
)

smoking_vocabulary = SimpleVocabulary(
    [
        SimpleTerm(value=u'Smoking', title=_(u'Smoking')),
        SimpleTerm(value=u'Non-smoking', title=_(u'Non-smoking')),
        SimpleTerm(value=u'No Preference', title=_(u'No Preference')),
    ]
)

semester_vocabulary = SimpleVocabulary(
    [
        SimpleTerm(value=u'Fall', title=_(u'Fall')),
        SimpleTerm(value=u'Fall Interim', title=_(u'Fall Interim')),
        SimpleTerm(value=u'Spring', title=_(u'Spring')),
        SimpleTerm(value=u'Spring Interim', title=_(u'Spring Interim')),
        SimpleTerm(value=u'Summer', title=_(u'Summer')),
    ]
)

student_type_vocabulary = SimpleVocabulary(
    [
        SimpleTerm(value=u'UW Oshkosh Freshman', title=_(u'UW Oshkosh Freshman')),
        SimpleTerm(value=u'UW Oshkosh Sophomore', title=_(u'UW Oshkosh Sophomore')),
        SimpleTerm(value=u'UW Oshkosh Junior', title=_(u'UW Oshkosh Junior')),
        SimpleTerm(value=u'UW Oshkosh Senior', title=_(u'UW Oshkosh Senior')),
        SimpleTerm(value=u'UW Oshkosh Graduate Student', title=_(u'UW Oshkosh Graduate Student')),
        SimpleTerm(value=u'Student at another University (please complete and submit the "Special Student" form)', title=_(u'Student at another University (please complete and submit the "Special Student" form)')),
        SimpleTerm(value=u'I am not a Student (please complete and submit the "Special Student" form)', title=_(u'I am not a Student (please complete and submit the "Special Student" form)')),
    ]
)

bus_vocabulary = SimpleVocabulary(
    [
        SimpleTerm(value=u'I will take the group bus from Oshkosh to the airport', title=_(u'I will take the group bus from Oshkosh to the airport')),
        SimpleTerm(value=u'I will arrange for my own transportation from Oshkosh to the airport.', title=_(u'I will arrange for my own transportation from Oshkosh to the airport.')),
    ]
)

fly_vocabulary = SimpleVocabulary(
    [
        SimpleTerm(value=u'I will fly with the group', title=_(u'I will fly with the group')),
        SimpleTerm(value=u'I will deviate from the group itinerary', title=_(u'I will deviate from the group itinerary')),
    ]
)

orientation_conflict_vocabulary = SimpleVocabulary(
    [
        SimpleTerm(value=u'No', title=_(u'No')),
        SimpleTerm(value=u'Yes, I have a conflict on (enter the date next):', title=_(u'Yes, I have a conflict on (enter the date next):')),
        SimpleTerm(value=u'No dates are listed', title=_(u'No dates are listed')),
    ]
)

hold_vocabulary = SimpleVocabulary(
    [
        SimpleTerm(value=u'HOLD', title=_(u'HOLD')),
        SimpleTerm(value=u'PROCESS', title=_(u'PROCESS')),
    ]
)

aware_vocabulary = SimpleVocabulary(
    [
        SimpleTerm(value=u'Yes, I am aware of the application requirements for my program', title=_(u'Yes, I am aware of the application requirements for my program')),
        SimpleTerm(value=u'There are no additional application requirements for my program', title=_(u'There are no additional application requirements for my program')),
    ]
)

@implementer(IVocabularyFactory)
class SubjectsVocabularyFactory(object):

    def __call__(self, context):
        values = api.portal.get_registry_record('oiestudyabroadstudent.subjects')
        normalizer = queryUtility(IIDNormalizer)
        items = [SimpleTerm(value=i, token=normalizer.normalize(i, max_length=MAX_LENGTH), title=i) for i in values]
        return SimpleVocabulary(items)

SubjectsVocabulary = SubjectsVocabularyFactory()

@implementer(IVocabularyFactory)
class MajorsVocabularyFactory(object):

    def __call__(self, context):
        values = api.portal.get_registry_record('oiestudyabroadstudent.majors')
        normalizer = queryUtility(IIDNormalizer)
        items = [SimpleTerm(value=i, token=normalizer.normalize(i, max_length=MAX_LENGTH), title=i) for i in values]
        return SimpleVocabulary(items)

MajorsVocabulary = MajorsVocabularyFactory()

@implementer(IVocabularyFactory)
class ProgramsVocabularyFactory(object):

    def __call__(self, context):
        values = api.portal.get_registry_record('oiestudyabroadstudent.programs')
        normalizer = queryUtility(IIDNormalizer)
        items = [SimpleTerm(value=i, token=normalizer.normalize(i, max_length=MAX_LENGTH), title=i) for i in values]
        return SimpleVocabulary(items)

ProgramsVocabulary = ProgramsVocabularyFactory()

@implementer(IVocabularyFactory)
class SessionHoursVocabularyFactory(object):

    def __call__(self, context):
        values = api.portal.get_registry_record('oiestudyabroadstudent.session_hours')
        normalizer = queryUtility(IIDNormalizer)
        items = [SimpleTerm(value=i, token=normalizer.normalize(i, max_length=MAX_LENGTH), title=i) for i in values]
        return SimpleVocabulary(items)

SessionHoursVocabulary = SessionHoursVocabularyFactory()

@implementer(IVocabularyFactory)
class EthnicitiesVocabularyFactory(object):

    def __call__(self, context):
        values = api.portal.get_registry_record('oiestudyabroadstudent.ethnicities')
        normalizer = queryUtility(IIDNormalizer)
        items = [SimpleTerm(value=i, token=normalizer.normalize(i, max_length=MAX_LENGTH), title=i) for i in values]
        return SimpleVocabulary(items)

EthnicitiesVocabulary = EthnicitiesVocabularyFactory()

@implementer(IVocabularyFactory)
class MarriageStatusesVocabularyFactory(object):

    def __call__(self, context):
        values = api.portal.get_registry_record('oiestudyabroadstudent.marriage_statuses')
        normalizer = queryUtility(IIDNormalizer)
        items = [SimpleTerm(value=i, token=normalizer.normalize(i, max_length=MAX_LENGTH), title=i) for i in values]
        return SimpleVocabulary(items)

MarriageStatusesVocabulary = MarriageStatusesVocabularyFactory()

@implementer(IVocabularyFactory)
class GendersVocabularyFactory(object):

    def __call__(self, context):
        values = api.portal.get_registry_record('oiestudyabroadstudent.genders')
        normalizer = queryUtility(IIDNormalizer)
        items = [SimpleTerm(value=i, token=normalizer.normalize(i, max_length=MAX_LENGTH), title=i) for i in values]
        return SimpleVocabulary(items)

GendersVocabulary = GendersVocabularyFactory()

@implementer(IVocabularyFactory)
class StatesForResidencyVocabularyFactory(object):

    def __call__(self, context):
        values = api.portal.get_registry_record('oiestudyabroadstudent.states_for_residency')
        normalizer = queryUtility(IIDNormalizer)
        items = [SimpleTerm(value=i, token=normalizer.normalize(i, max_length=MAX_LENGTH), title=i) for i in values]
        return SimpleVocabulary(items)

StatesForResidencyVocabulary = StatesForResidencyVocabularyFactory()

@implementer(IVocabularyFactory)
class CitizenshipVocabularyFactory(object):

    def __call__(self, context):
        values = api.portal.get_registry_record('oiestudyabroadstudent.citizenship')
        normalizer = queryUtility(IIDNormalizer)
        items = [SimpleTerm(value=i, token=normalizer.normalize(i, max_length=MAX_LENGTH), title=i) for i in values]
        return SimpleVocabulary(items)

CitizenshipVocabulary = CitizenshipVocabularyFactory()

@implementer(IVocabularyFactory)
class CountriesVocabularyFactory(object):

    def __call__(self, context):
        values = api.portal.get_registry_record('oiestudyabroadstudent.countries')
        normalizer = queryUtility(IIDNormalizer)
        items = [SimpleTerm(value=i, token=normalizer.normalize(i, max_length=MAX_LENGTH), title=i) for i in values]
        return SimpleVocabulary(items)

CountriesVocabulary = CountriesVocabularyFactory()

@implementer(IVocabularyFactory)
class ProgramTypeVocabularyFactory(object):

    def __call__(self, context):
        values = api.portal.get_registry_record('oiestudyabroadstudent.program_type')
        normalizer = queryUtility(IIDNormalizer)
        items = [SimpleTerm(value=i, token=normalizer.normalize(i, max_length=MAX_LENGTH), title=i) for i in values]
        return SimpleVocabulary(items)

ProgramTypeVocabulary = ProgramTypeVocabularyFactory()

@implementer(IVocabularyFactory)
class ProgramComponentVocabularyFactory(object):

    def __call__(self, context):
        values = api.portal.get_registry_record('oiestudyabroadstudent.program_component')
        normalizer = queryUtility(IIDNormalizer)
        items = [SimpleTerm(value=i, token=normalizer.normalize(i, max_length=MAX_LENGTH), title=i) for i in values]
        return SimpleVocabulary(items)

ProgramComponentVocabulary = ProgramComponentVocabularyFactory()

@implementer(IVocabularyFactory)
class EquipmentAndSpaceVocabularyFactory(object):

    def __call__(self, context):
        values = api.portal.get_registry_record('oiestudyabroadstudent.equipment_and_space')
        normalizer = queryUtility(IIDNormalizer)
        items = [SimpleTerm(value=i, token=normalizer.normalize(i, max_length=MAX_LENGTH), title=i) for i in values]
        return SimpleVocabulary(items)

EquipmentAndSpaceVocabulary = EquipmentAndSpaceVocabularyFactory()

@implementer(IVocabularyFactory)
class GuestLecturesVocabularyFactory(object):

    def __call__(self, context):
        values = api.portal.get_registry_record('oiestudyabroadstudent.guest_lectures')
        normalizer = queryUtility(IIDNormalizer)
        items = [SimpleTerm(value=i, token=normalizer.normalize(i, max_length=MAX_LENGTH), title=i) for i in values]
        return SimpleVocabulary(items)

GuestLecturesVocabulary = GuestLecturesVocabularyFactory()

@implementer(IVocabularyFactory)
class TermVocabularyFactory(object):

    def __call__(self, context):
        values = api.portal.get_registry_record('oiestudyabroadstudent.term')
        normalizer = queryUtility(IIDNormalizer)
        items = [SimpleTerm(value=i, token=normalizer.normalize(i, max_length=MAX_LENGTH), title=i) for i in values]
        return SimpleVocabulary(items)

TermVocabulary = TermVocabularyFactory()

@implementer(IVocabularyFactory)
class CollegeOrUnitVocabularyFactory(object):

    def __call__(self, context):
        values = api.portal.get_registry_record('oiestudyabroadstudent.college_or_unit')
        normalizer = queryUtility(IIDNormalizer)
        items = [SimpleTerm(value=i, token=normalizer.normalize(i, max_length=MAX_LENGTH), title=i) for i in values]
        return SimpleVocabulary(items)

CollegeOrUnitVocabulary = CollegeOrUnitVocabularyFactory()

@implementer(IVocabularyFactory)
class SponsoringUnitOrDepartmentVocabularyFactory(object):

    def __call__(self, context):
        values = api.portal.get_registry_record('oiestudyabroadstudent.sponsoring_unit_or_department')
        normalizer = queryUtility(IIDNormalizer)
        items = [SimpleTerm(value=i, token=normalizer.normalize(i, max_length=MAX_LENGTH), title=i) for i in values]
        return SimpleVocabulary(items)

SponsoringUnitOrDepartmentVocabulary = SponsoringUnitOrDepartmentVocabularyFactory()

@implementer(IVocabularyFactory)
class LanguageVocabularyFactory(object):

    def __call__(self, context):
        values = api.portal.get_registry_record('oiestudyabroadstudent.language')
        normalizer = queryUtility(IIDNormalizer)
        items = [SimpleTerm(value=i, token=normalizer.normalize(i, max_length=MAX_LENGTH), title=i) for i in values]
        return SimpleVocabulary(items)

LanguageVocabulary = LanguageVocabularyFactory()

@implementer(IVocabularyFactory)
class CreditsVocabularyFactory(object):

    def __call__(self, context):
        values = api.portal.get_registry_record('oiestudyabroadstudent.credits')
        normalizer = queryUtility(IIDNormalizer)
        items = [SimpleTerm(value=i, token=normalizer.normalize(i, max_length=MAX_LENGTH), title=i) for i in values]
        return SimpleVocabulary(items)

CreditsVocabulary = CreditsVocabularyFactory()

@implementer(IVocabularyFactory)
class ContactsVocabularyFactory(object):

    def __call__(self, context):
        catalog = api.portal.get_tool('portal_catalog')
        contact_brains = catalog(portal_type='OIEContact',
                                sort_on='sortable_title',
                                sort_order='ascending')
        terms = []
        for brain in contact_brains:
            token = brain.getPath()
            terms.append(SimpleTerm(
                value=brain.UID,
                token=token,
                title=brain.Title.decode('utf8')
            ))
        return SimpleVocabulary(terms)

ContactsVocabulary = ContactsVocabularyFactory()

@implementer(IVocabularyFactory)
class AccommodationVocabularyFactory(object):

    def __call__(self, context):
        values = api.portal.get_registry_record('oiestudyabroadstudent.accommodation')
        normalizer = queryUtility(IIDNormalizer)
        items = [SimpleTerm(value=i, token=normalizer.normalize(i, max_length=MAX_LENGTH), title=i) for i in values]
        return SimpleVocabulary(items)

AccommodationVocabulary = AccommodationVocabularyFactory()


@implementer(IVocabularyFactory)
class CalendarYearVocabularyFactory(object):

    def __call__(self, context):
        catalog = api.portal.get_tool('portal_catalog')
        contact_brains = catalog(portal_type='OIECalendarYear',
                                sort_on='sortable_title',
                                sort_order='ascending')
        terms = []
        for brain in contact_brains:
            token = brain.getPath()
            terms.append(SimpleTerm(
                value=brain.UID,
                token=token,
                title=brain.Title.decode('utf8')
            ))
        return SimpleVocabulary(terms)

CalendarYearVocabulary = CalendarYearVocabularyFactory()
