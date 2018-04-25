# -*- coding: utf-8 -*-
from plone import api
from plone.i18n.normalizer.interfaces import IIDNormalizer
from zope.component import queryUtility
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from uwosh.oie.studyabroadstudent import _
from currencies import Currency


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

graduation_month_vocabulary = SimpleVocabulary(
    [SimpleTerm(value=u'05', title=_(u'May')),
     SimpleTerm(value=u'08', title=_(u'August')),
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
        SimpleTerm(value=u'Student at another University (please complete and submit the "Special Student" form)',
                   title=_(u'Student at another University (please complete and submit the "Special Student" form)')),
        SimpleTerm(value=u'I am not a Student (please complete and submit the "Special Student" form)',
                   title=_(u'I am not a Student (please complete and submit the "Special Student" form)')),
    ]
)

bus_vocabulary = SimpleVocabulary(
    [
        SimpleTerm(value=u'I will take the group bus from Oshkosh to the airport',
                   title=_(u'I will take the group bus from Oshkosh to the airport')),
        SimpleTerm(value=u'I will arrange for my own transportation from Oshkosh to the airport.',
                   title=_(u'I will arrange for my own transportation from Oshkosh to the airport.')),
    ]
)

fly_vocabulary = SimpleVocabulary(
    [
        SimpleTerm(value=u'I will fly with the group', title=_(u'I will fly with the group')),
        SimpleTerm(value=u'I will deviate from the group itinerary',
                   title=_(u'I will deviate from the group itinerary')),
    ]
)

orientation_conflict_vocabulary = SimpleVocabulary(
    [
        SimpleTerm(value=u'No', title=_(u'No')),
        SimpleTerm(value=u'Yes, I have a conflict on (enter the date next):',
                   title=_(u'Yes, I have a conflict on (enter the date next):')),
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
        SimpleTerm(value=u'Yes, I am aware of the application requirements for my program',
                   title=_(u'Yes, I am aware of the application requirements for my program')),
        SimpleTerm(value=u'There are no additional application requirements for my program',
                   title=_(u'There are no additional application requirements for my program')),
    ]
)

load_or_overload = SimpleVocabulary(
    [
        SimpleTerm(value=u'Part of load', title=_(u'Part of load'), token='load'),
        SimpleTerm(value=u'Overload', title=_(u'Overload'), token='overload'),
    ]
)

replacement_costs = SimpleVocabulary(
    [
        SimpleTerm(value=u'No replacement costs due to the College',
                   title=_(u'No replacement costs due to the College'), token='not-due'),
        SimpleTerm(value=u'Replacement costs due to the College', title=_(u'Replacement costs due to the College'),
                   token='due'),
    ]
)

paid_by = SimpleVocabulary(
    [
        SimpleTerm(value=u'Paid by the College', title=_(u'Paid by the College'), token='college'),
        SimpleTerm(value=u'Paid by external partner', title=_(u'Paid by external partner'), token='external'),
        SimpleTerm(value=u'Paid by study away students', title=_(u'Paid by study away students'), token='students')
    ]
)

rate_or_lump_sum = SimpleVocabulary(
    [
        SimpleTerm(value=u'2.5% per credit (faculty rate)', title=_(u'2.5% per credit (faculty rate)'), token='2.5'),
        SimpleTerm(value=u'3.33% per credit (academic staff rate)', title=_(u'3.33% per credit (academic staff rate)'),
                   token='3.33'),
        SimpleTerm(value=u'Lump sum', title=_(u'Lump sum'), token='lump-sum'),
    ]
)

socialmediaservice = SimpleVocabulary(
    [
        SimpleTerm(value=u'Skype', title=_(u'Skype'), token='skype'),
        SimpleTerm(value=u'Viber', title=_(u'Viber'), token='viber'),
        SimpleTerm(value=u'WeChat', title=_(u'WeChat'), token='wechat'),
        SimpleTerm(value=u'WhatsApp', title=_(u'WhatsApp'), token='whatsapp'),
        SimpleTerm(value=u'Facebook', title=_(u'Facebook'), token='facebook'),
        SimpleTerm(value=u'Twitter', title=_(u'Twitter'), token='twitter'),
    ]
)

contactrelationship = SimpleVocabulary(
    [
        SimpleTerm(value=u'father', title=_(u'father'), token='father'),
        SimpleTerm(value=u'mother', title=_(u'mother'), token='mother'),
        SimpleTerm(value=u'grandfather', title=_(u'grandfather'), token='grandfather'),
        SimpleTerm(value=u'grandmother', title=_(u'grandmother'), token='grandmother'),
        SimpleTerm(value=u'uncle', title=_(u'uncle'), token='uncle'),
        SimpleTerm(value=u'aunt', title=_(u'aunt'), token='aunt'),
        SimpleTerm(value=u'brother', title=_(u'brother'), token='brother'),
        SimpleTerm(value=u'sister', title=_(u'sister'), token='sister'),
        SimpleTerm(value=u'spouse', title=_(u'spouse'), token='spouse'),
        SimpleTerm(value=u'adult child', title=_(u'adult child'), token='adult-child'),
        SimpleTerm(value=u'other relative', title=_(u'other relative'), token='other-relative'),
    ]
)

departure_transfer_vocabulary = SimpleVocabulary(
    [
        SimpleTerm(u'-- choose one --'),
        SimpleTerm(u'I will transfer from Oshkosh to the airport with the group'),
        SimpleTerm(u'I will transfer from Milwaukee to the airport with the group'),
        SimpleTerm(u'I will arrange my own transportation to the airport'),
        SimpleTerm(u'I will drive to my destination city (U.S. & Canada programs only)'),
    ]
)

departure_mode_transportation_vocabulary = SimpleVocabulary(
    [
        SimpleTerm(u'I will fly with the group'),
        SimpleTerm(u'I will apply for permission to arrange my own flight'),
        SimpleTerm(u'I will drive to my destination city (U.S. & Canada programs only)')
    ]
)

return_mode_transportation_vocabulary = SimpleVocabulary(
    [
        SimpleTerm(u'I will fly with the group'),
        SimpleTerm(u'I will apply for permission to arrange my own flight'),
        SimpleTerm(u'I will drive back to my home at the end of my program (U.S. and Canada programs only)')
    ]
)

return_transfer_vocabulary = SimpleVocabulary(
    [
        SimpleTerm(u'-- choose one --'),
        SimpleTerm(u'I will transfer from the airport to Oshkosh with the group'),
        SimpleTerm(u'I will transfer from the airport to Milwaukee with the group'),
        SimpleTerm(u'I will arrange my own transportation home from the airport'),
        SimpleTerm(u'I will drive back to my home at the end of my program (U.S. and Canada programs only)'),
    ]
)

program_cycle_vocabulary = SimpleVocabulary(
    [
        SimpleTerm(token=u'once', value=u'once', title=_(u'once')),
        SimpleTerm(token=u'annually', value=u'annually', title=_(u'annually')),
        SimpleTerm(token=u'every-2-years', value=u'every 2 years', title=_(u'every 2 years')),
        SimpleTerm(token=u'every-3-years', value=u'every 3 years', title=_(u'every 3 years')),
    ]
)

seat_assignment_protocol = SimpleVocabulary(
    [
        SimpleTerm(token=u'in-order', value=u'in-order', title=_(u'Seats are assigned in the order in which qualified applicants have completed STEPS I & II of the application process, provided STEP III has also been completed by the STEP III application deadline.  This means that you may be conditionally admitted following completion of steps I & II, but NOT receive a seat if you then fail to complete STEP III on time.  If you are on the waiting list, you may receive a seat if applicants who have been conditionally admitted have not completed STEP III by the deadline.  In the rare event that applications can be accepted after deadlines, seats are assigned in the order in which qualified applicants have completed all three steps.')),
        SimpleTerm(token=u'competitive', value=u'competitive', title=_(u'Seat assignments on this program are competitive.  Applicants who meet the STEP II application deadilne are placed in a pool for consideration.  Selections will take place just after the STEP II deadline & prior to the STEP III deadline.  Selection is conditional upon completion of STEP III by the STEP III application deadline.  This means that you may be conditionally selected following completion of steps I & II, but NOT receive a seat if you then fail to complete STEP III on time.  If you are on the waiting list, you may receive a seat if applicants who have been conditionally selected have not completed STEP III by the deadline.  In the rare event that applications can be accepted after deadlines, applicants are considered in the order in which they have completed all three steps.')),
    ]
)

salary_form = SimpleVocabulary(
    [
        SimpleTerm(u'Payment to Individual Form (PTF) - Direct Payment'),
        SimpleTerm(u'Transaction Transfer Request (TTR) - Replacement Costs'),
        SimpleTerm(u'Foundation'),
        SimpleTerm(u'Not Applicable'),
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
        brains = catalog(portal_type='OIEContact',
                         sort_on='sortable_title',
                         sort_order='ascending')
        terms = []
        for brain in brains:
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
        brains = catalog(portal_type='OIECalendarYear',
                         sort_on='sortable_title',
                         sort_order='ascending')
        terms = []
        for brain in brains:
            token = brain.getPath()
            terms.append(SimpleTerm(
                value=brain.UID,
                token=token,
                title=brain.Title.decode('utf8')
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
                title=brain.Title.decode('utf8')
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
                title=brain.Title.decode('utf8')
            ))
        return SimpleVocabulary(terms)


NewProgramsVocabulary = NewProgramsVocabularyFactory()


@implementer(IVocabularyFactory)
class ImmigrationStatusVocabularyFactory(object):

    def __call__(self, context):
        values = api.portal.get_registry_record('oiestudyabroadstudent.immigration_status')
        normalizer = queryUtility(IIDNormalizer)
        items = [SimpleTerm(value=i, token=normalizer.normalize(i, max_length=MAX_LENGTH), title=i) for i in values]
        return SimpleVocabulary(items)


ImmigrationStatusVocabulary = ImmigrationStatusVocabularyFactory()


@implementer(IVocabularyFactory)
class CourseVocabularyFactory(object):

    def __call__(self, context):
        values = api.portal.get_registry_record('oiestudyabroadstudent.course_subject_and_number')
        normalizer = queryUtility(IIDNormalizer)
        items = [SimpleTerm(value=i, token=normalizer.normalize(i, max_length=MAX_LENGTH), title=i) for i in values]
        return SimpleVocabulary(items)


CourseVocabulary = CourseVocabularyFactory()


@implementer(IVocabularyFactory)
class EducationLevelVocabularyFactory(object):

    def __call__(self, context):
        values = api.portal.get_registry_record('oiestudyabroadstudent.education_level')
        normalizer = queryUtility(IIDNormalizer)
        items = [SimpleTerm(value=i, token=normalizer.normalize(i, max_length=MAX_LENGTH), title=i) for i in values]
        return SimpleVocabulary(items)


EducationLevelVocabulary = EducationLevelVocabularyFactory()


@implementer(IVocabularyFactory)
class USStatesAndTerritoriesVocabularyFactory(object):

    def __call__(self, context):
        values = api.portal.get_registry_record('oiestudyabroadstudent.us_states_territories')
        normalizer = queryUtility(IIDNormalizer)
        items = [SimpleTerm(value=i, token=normalizer.normalize(i, max_length=MAX_LENGTH), title=i) for i in values]
        return SimpleVocabulary(items)


USStatesAndTerritoriesVocabulary = USStatesAndTerritoriesVocabularyFactory()


@implementer(IVocabularyFactory)
class CampusBuildingVocabularyFactory(object):

    def __call__(self, context):
        values = api.portal.get_registry_record('oiestudyabroadstudent.building')
        normalizer = queryUtility(IIDNormalizer)
        items = [SimpleTerm(value=i, token=normalizer.normalize(i, max_length=MAX_LENGTH), title=i) for i in values]
        return SimpleVocabulary(items)


CampusBuildingVocabulary = CampusBuildingVocabularyFactory()


@implementer(IVocabularyFactory)
class DepartureLocationVocabularyFactory(object):

    def __call__(self, context):
        values = api.portal.get_registry_record('oiestudyabroadstudent.locations')
        normalizer = queryUtility(IIDNormalizer)
        items = [SimpleTerm(value=i, token=normalizer.normalize(i, max_length=MAX_LENGTH), title=i) for i in values]
        return SimpleVocabulary(items)


DepartureLocationVocabulary = DepartureLocationVocabularyFactory()


@implementer(IVocabularyFactory)
class TransitionTypeVocabularyFactory(object):

    def __call__(self, context):
        values = api.portal.get_registry_record('oiestudyabroadstudent.transition_type')
        normalizer = queryUtility(IIDNormalizer)
        items = [SimpleTerm(value=i, token=normalizer.normalize(i, max_length=MAX_LENGTH), title=i) for i in values]
        return SimpleVocabulary(items)


TransitionTypeVocabulary = TransitionTypeVocabularyFactory()


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
                title=brain.Title.decode('utf8')
            ))
        return SimpleVocabulary(terms)


AirlineVocabulary = AirlineVocabularyFactory()


@implementer(IVocabularyFactory)
class AirportVocabularyFactory(object):

    def __call__(self, context):
        values = api.portal.get_registry_record('oiestudyabroadstudent.airport')
        normalizer = queryUtility(IIDNormalizer)
        items = [SimpleTerm(value=i, token=normalizer.normalize(i, max_length=MAX_LENGTH), title=i) for i in values]
        return SimpleVocabulary(items)


AirportVocabulary = AirportVocabularyFactory()


@implementer(IVocabularyFactory)
class RoomSizeVocabularyFactory(object):

    def __call__(self, context):
        values = api.portal.get_registry_record('oiestudyabroadstudent.room_size')
        normalizer = queryUtility(IIDNormalizer)
        items = [SimpleTerm(value=i, token=normalizer.normalize(i, max_length=MAX_LENGTH), title=i) for i in values]
        return SimpleVocabulary(items)


RoomSizeVocabulary = RoomSizeVocabularyFactory()


@implementer(IVocabularyFactory)
class StudentStatusVocabularyFactory(object):

    def __call__(self, context):
        values = api.portal.get_registry_record('oiestudyabroadstudent.student_status')
        normalizer = queryUtility(IIDNormalizer)
        items = [SimpleTerm(value=i, token=normalizer.normalize(i, max_length=MAX_LENGTH), title=i) for i in values]
        return SimpleVocabulary(items)


StudentStatusVocabulary = StudentStatusVocabularyFactory()


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
                title=brain.Title.decode('utf8')
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
                title=brain.Title.decode('utf8')
            ))
        return SimpleVocabulary(terms)


LiaisonVocabulary = LiaisonVocabularyFactory()


@implementer(IVocabularyFactory)
class ProgramOfStudyVocabularyFactory(object):

    def __call__(self, context):
        values = api.portal.get_registry_record('oiestudyabroadstudent.program_of_study')
        normalizer = queryUtility(IIDNormalizer)
        items = [SimpleTerm(value=i, token=normalizer.normalize(i, max_length=MAX_LENGTH), title=i) for i in values]
        return SimpleVocabulary(items)


ProgramOfStudyVocabulary = ProgramOfStudyVocabularyFactory()


@implementer(IVocabularyFactory)
class EnrollmentInstitutionVocabularyFactory(object):

    def __call__(self, context):
        values = api.portal.get_registry_record('oiestudyabroadstudent.enrollment_institution')
        normalizer = queryUtility(IIDNormalizer)
        items = [SimpleTerm(value=i, token=normalizer.normalize(i, max_length=MAX_LENGTH), title=i) for i in values]
        return SimpleVocabulary(items)


EnrollmentInstitutionVocabulary = EnrollmentInstitutionVocabularyFactory()


@implementer(IVocabularyFactory)
class CurrencyVocabularyFactory(object):

    def __call__(self, context):
        values = [v for v in Currency.money_formats.keys() if v != 'USD']
        values.sort()
        values.insert(0, 'USD')
        normalizer = queryUtility(IIDNormalizer)
        items = [SimpleTerm(value=i, token=normalizer.normalize(i, max_length=MAX_LENGTH), title=i) for i in values]
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
                title=brain.Title.decode('utf8')
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
                title=brain.Title.decode('utf8')
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
                title=brain.Title.decode('utf8')
            ))
        return SimpleVocabulary(terms)


ImageVocabulary = ImageVocabularyFactory()


@implementer(IVocabularyFactory)
class EligibilityRequirementVocabularyFactory(object):

    def __call__(self, context):
        values = api.portal.get_registry_record('oiestudyabroadstudent.eligibility_requirement')
        normalizer = queryUtility(IIDNormalizer)
        items = [SimpleTerm(value=i, token=normalizer.normalize(i, max_length=MAX_LENGTH), title=i) for i in values]
        return SimpleVocabulary(items)


EligibilityRequirementVocabulary = EligibilityRequirementVocabularyFactory()


@implementer(IVocabularyFactory)
class AirportTransferVocabularyFactory(object):

    def __call__(self, context):
        values = api.portal.get_registry_record('oiestudyabroadstudent.airport_transfer')
        normalizer = queryUtility(IIDNormalizer)
        items = [SimpleTerm(value=i, token=normalizer.normalize(i, max_length=MAX_LENGTH), title=i) for i in values]
        return SimpleVocabulary(items)


AirportTransferVocabulary = AirportTransferVocabularyFactory()


