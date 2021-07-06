from calendar import month_name
from currencies import Currency
from plone import api
from plone.app.vocabularies.terms import safe_simplevocabulary_from_values
from plone.i18n.normalizer.interfaces import IIDNormalizer
from uwosh.oie.studyabroadstudent import _
from uwosh.oie.studyabroadstudent.constants import DEFAULT_TUITION_AND_FEES
from zope.component import queryUtility
from zope.interface import implementer
from zope.schema.interfaces import IContextSourceBinder, IVocabularyFactory, ISource
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary


PROGRAMMANAGEMENT = 'programmanagement'

MAX_LENGTH = 250

yes_no_vocabulary = SimpleVocabulary(
    [
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
    [
        SimpleTerm(value=f'{index:02}', title=_(month_name[index]))
        for index in range(1, 13)
    ]
)

graduation_month_vocabulary = SimpleVocabulary(
    [
        SimpleTerm(value=f'{index:02}', title=_(month_name[index]))
        for index in [5, 8, 12]
    ]
)

dayofmonth_vocabulary = SimpleVocabulary(
    [
        SimpleTerm(value=f'{index:02}')
        for index in range(1, 32)
    ],
)

room_type_vocabulary = SimpleVocabulary(
    [
        SimpleTerm(
            value='Single Room',
            title=_('Single Room')
        ),
        SimpleTerm(
            value='Double Room',
            title=_('Double Room')
        ),
        SimpleTerm(
            value='Triple Room',
            title=_('Triple Room')
        ),
    ],
)

smoking_vocabulary = SimpleVocabulary(
    [
        SimpleTerm(
            value='Smoking',
            title=_('Smoking'),
        ),
        SimpleTerm(
            value='Non-smoking',
            title=_('Non-smoking'),
        ),
        SimpleTerm(
            value='No Preference',
            title=_('No Preference'),
        ),
    ],
)

semester_vocabulary = SimpleVocabulary(
    [
        SimpleTerm(
            value='Fall',
            title=_('Fall'),
        ),
        SimpleTerm(
            value='Fall Interim',
            title=_('Fall Interim'),
        ),
        SimpleTerm(
            value='Spring',
            title=_('Spring'),
        ),
        SimpleTerm(
            value='Spring Interim',
            title=_('Spring Interim'),
        ),
        SimpleTerm(
            value='Summer',
            title=_('Summer'),
        ),
    ],
)

student_type_vocabulary = SimpleVocabulary(
    [
        SimpleTerm(
            value='UW Oshkosh Freshman',
            title=_('UW Oshkosh Freshman'),
        ),
        SimpleTerm(
            value='UW Oshkosh Sophomore',
            title=_('UW Oshkosh Sophomore'),
        ),
        SimpleTerm(
            value='UW Oshkosh Junior',
            title=_('UW Oshkosh Junior'),
        ),
        SimpleTerm(
            value='UW Oshkosh Senior',
            title=_('UW Oshkosh Senior'),
        ),
        SimpleTerm(
            value='UW Oshkosh Graduate Student',
            title=_('UW Oshkosh Graduate Student'),
        ),
        SimpleTerm(
            value='Student at another University (please complete and submit the "Special Student" form)',
            title=_('Student at another University (please complete and submit the "Special Student" form)'),
        ),
        SimpleTerm(
            value='I am not a Student (please complete and submit the "Special Student" form)',
            title=_('I am not a Student (please complete and submit the "Special Student" form)'),
        ),
    ],
)

bus_vocabulary = SimpleVocabulary(
    [
        SimpleTerm(
            value='I will take the group bus from Oshkosh to the airport',
            title=_('I will take the group bus from Oshkosh to the airport')
        ),
        SimpleTerm(
            value='I will arrange for my own transportation from Oshkosh to the airport.',
            title=_('I will arrange for my own transportation from Oshkosh to the airport.'),
        ),
    ],
)

fly_vocabulary = SimpleVocabulary(
    [
        SimpleTerm(
            value='I will fly with the group',
            title=_('I will fly with the group'),
        ),
        SimpleTerm(
            value='I will deviate from the group itinerary',
            title=_('I will deviate from the group itinerary'),
        ),
    ],
)

orientation_conflict_vocabulary = SimpleVocabulary(
    [
        SimpleTerm(
            value='No',
            title=_('No'),
        ),
        SimpleTerm(
            value='Yes, I have a conflict on (enter the date next):',
            title=_('Yes, I have a conflict on (enter the date next):'),
        ),
        SimpleTerm(
            value='No dates are listed',
            title=_('No dates are listed'),
        ),
    ],
)

hold_vocabulary = SimpleVocabulary(
    [
        SimpleTerm(
            value='HOLD',
            title=_('HOLD'),
        ),
        SimpleTerm(
            value='PROCESS',
            title=_('PROCESS'),
        ),
    ],
)

aware_vocabulary = SimpleVocabulary(
    [
        SimpleTerm(
            value='Yes, I am aware of the application requirements for my program',
            title=_('Yes, I am aware of the application requirements for my program'),
        ),
        SimpleTerm(
            value='There are no additional application requirements for my program',
            title=_('There are no additional application requirements for my program'),
        ),
    ],
)

load_or_overload = SimpleVocabulary(
    [
        SimpleTerm(
            value='Part of load',
            title=_('Part of load'),
            token='load',
        ),
        SimpleTerm(
            value='Overload',
            title=_('Overload'),
            token='overload',
        ),
    ],
)

replacement_costs = SimpleVocabulary(
    [
        SimpleTerm(
            value='No replacement costs due to the College',
            title=_('No replacement costs due to the College'),
            token='not-due',
        ),
        SimpleTerm(
            value='Replacement costs due to the College',
            title=_('Replacement costs due to the College'),
            token='due'
        ),
    ],
)

paid_by = SimpleVocabulary(
    [
        SimpleTerm(
            value='Paid by the College',
            title=_('Paid by the College'),
            token='college'
        ),
        SimpleTerm(
            value='Paid by external partner',
            title=_('Paid by external partner'),
            token='external'
        ),
        SimpleTerm(
            value='Paid by study away students',
            title=_('Paid by study away students'),
            token='students'
        ),
    ],
)

rate_or_lump_sum = SimpleVocabulary(
    [
        SimpleTerm(
            value='2.5% per credit (faculty rate)',
            title=_('2.5% per credit (faculty rate)'),
            token='2.5'
        ),
        SimpleTerm(
            value='3.33% per credit (academic staff rate)',
            title=_('3.33% per credit (academic staff rate)'),
            token='3.33'
        ),
        SimpleTerm(
            value='Lump sum',
            title=_('Lump sum'),
            token='lump-sum'
        ),
    ],
)

socialmediaservice = SimpleVocabulary(
    [
        SimpleTerm(
            value='Skype',
            title=_('Skype'),
            token='skype',
        ),
        SimpleTerm(
            value='Viber',
            title=_('Viber'),
            token='viber',
        ),
        SimpleTerm(
            value='WeChat',
            title=_('WeChat'),
            token='wechat',
        ),
        SimpleTerm(
            value='WhatsApp',
            title=_('WhatsApp'),
            token='whatsapp',
        ),
        SimpleTerm(
            value='Facebook',
            title=_('Facebook'),
            token='facebook',
        ),
        SimpleTerm(
            value='Twitter',
            title=_('Twitter'),
            token='twitter',
        ),
    ],
)

contactrelationship = SimpleVocabulary(
    [
        SimpleTerm(
            value='father',
            title=_('father'),
            token='father',
        ),
        SimpleTerm(
            value='mother',
            title=_('mother'),
            token='mother',
        ),
        SimpleTerm(
            value='grandfather',
            title=_('grandfather'),
            token='grandfather',
        ),
        SimpleTerm(
            value='grandmother',
            title=_('grandmother'),
            token='grandmother',
        ),
        SimpleTerm(
            value='uncle',
            title=_('uncle'),
            token='uncle',
        ),
        SimpleTerm(
            value='aunt',
            title=_('aunt'),
            token='aunt',
        ),
        SimpleTerm(
            value='brother',
            title=_('brother'),
            token='brother',
        ),
        SimpleTerm(
            value='sister',
            title=_('sister'),
            token='sister',
        ),
        SimpleTerm(
            value='spouse',
            title=_('spouse'),
            token='spouse',
        ),
        SimpleTerm(
            value='adult child',
            title=_('adult child'),
            token='adult-child',
        ),
        SimpleTerm(
            value='other relative',
            title=_('other relative'),
            token='other-relative',
        ),
    ],
)

departure_transfer_vocabulary = SimpleVocabulary(
    [
        SimpleTerm('I will transfer from Oshkosh with the group.'),
        SimpleTerm('I will transfer from Fond du Lac with the group.'),
        SimpleTerm('I will transfer from Milwaukee with the group.'),
        SimpleTerm('I will arrange my own transportation.'),
    ],
)

departure_mode_transportation_vocabulary = SimpleVocabulary(
    [
        SimpleTerm('I will fly to and from my program site with the group.'),
        SimpleTerm(
            'I will fly with the group to my program site but will apply '
            'for permission to arrange an alternative flight home.'
        ),
        SimpleTerm(
            'I will apply for permission to fly to my program site on an alternative '
            'flight but will return from my program site with the group.'
        ),
        SimpleTerm(
            'I will apply for permission to fly to and from my program site on an alternative flight.'
        ),
    ],
)

return_mode_transportation_vocabulary = SimpleVocabulary(
    [
        SimpleTerm('I will fly with the group'),
        SimpleTerm('I will apply for permission to arrange my own flight'),
        SimpleTerm('I will drive back to my home at the end of my program (U.S. and Canada programs only)'),
    ],
)

return_transfer_vocabulary = SimpleVocabulary(
    [
        SimpleTerm('I will transfer back to Oshkosh with the group.'),
        SimpleTerm('I will transfer back to Fond du Lac with the group.'),
        SimpleTerm('I will transfer back to Milwaukee with the group.'),
        SimpleTerm('I will arrange my own transportation home.'),
    ],
)

program_cycle_vocabulary = SimpleVocabulary(
    [
        SimpleTerm(
            token='once',
            value='once',
            title=_('once'),
        ),
        SimpleTerm(
            token='annually',
            value='annually',
            title=_('annually'),
        ),
        SimpleTerm(
            token='every-2-years',
            value='every 2 years',
            title=_('every 2 years'),
        ),
        SimpleTerm(
            token='every-3-years',
            value='every 3 years',
            title=_('every 3 years'),
        ),
    ],
)

seat_assignment_protocol = SimpleVocabulary(
    [
        SimpleTerm(
            token='in-order',
            value='in-order',
            title=_(
                'Seats are assigned in the order in which qualified applicants have completed STEPS '
                'I & II of the application process, provided STEP III has also been completed by the '
                'STEP III application deadline. This means that you may be conditionally admitted '
                'following completion of steps I & II, but NOT receive a seat if you then fail to '
                'complete STEP III on time. If you are on the waiting list, you may receive a seat '
                'if applicants who have been conditionally admitted have not completed STEP III by '
                'the deadline. In the rare event that applications can be accepted after deadlines, '
                'seats are assigned in the order in which qualified applicants have completed all '
                'three steps.'
            ),
        ),
        SimpleTerm(
            token='competitive',
            value='competitive',
            title=_(
                'Seat assignments on this program are competitive.  Applicants who meet the STEP '
                'II application deadilne are placed in a pool for consideration.  Selections will '
                'take place just after the STEP II deadline & prior to the STEP III deadline. '
                'Selection is conditional upon completion of STEP III by the STEP III application '
                'deadline. This means that you may be conditionally selected following completion '
                'of steps I & II, but NOT receive a seat if you then fail to complete STEP III on '
                'time. If you are on the waiting list, you may receive a seat if applicants who have '
                'been conditionally selected have not completed STEP III by the deadline. In the '
                'rare event that applications can be accepted after deadlines, applicants are '
                'considered in the order in which they have completed all three steps.'
            ),
        ),
    ],
)

salary_form = SimpleVocabulary(
    [
        SimpleTerm('Payment to Individual Form (PTF) - Direct Payment'),
        SimpleTerm('Transaction Transfer Request (TTR) - Replacement Costs'),
        SimpleTerm('Foundation'),
        SimpleTerm('Not Applicable'),
    ],
)

selection_criteria_vocabulary = SimpleVocabulary(
    [
        SimpleTerm(
            title='Set selection criteria',
            value=True,
        ),
        SimpleTerm(
            title='There are no additional selection criteria',
            value=False,
        ),
    ],
)


def get_calendar_vocabulary_factory(portal_type):

    @implementer(IVocabularyFactory)
    class VocabularyFactory(object):
        def __call__(self, context):
            catalog = api.portal.get_tool('portal_catalog')
            brains = catalog(
                portal_type=portal_type,
                sort_on='sortable_title',
                sort_order='ascending',
            )
            terms = [
                SimpleTerm(
                    value=brain.UID,
                    token=brain.getPath(),
                    title=brain.Title,
                )
                for brain in brains
            ]
            return SimpleVocabulary(terms)
    return VocabularyFactory


ContactsVocabularyFactory = get_calendar_vocabulary_factory('OIEContact')
ContactsVocabulary = ContactsVocabularyFactory()
CalendarYearVocabularyFactory = get_calendar_vocabulary_factory('OIECalendarYear')
CalendarYearVocabulary = CalendarYearVocabularyFactory()
CooperatingPartnerVocabularyFactory = get_calendar_vocabulary_factory('OIECooperatingPartner')
CooperatingPartnerVocabulary = CooperatingPartnerVocabularyFactory()
NewProgramsVocabularyFactory = get_calendar_vocabulary_factory('OIEStudyAbroadProgram')
NewProgramsVocabulary = NewProgramsVocabularyFactory()
AirlineVocabularyFactory = get_calendar_vocabulary_factory('OIEAirline')
AirlineVocabulary = AirlineVocabularyFactory()
ProgramLeaderVocabularyFactory = get_calendar_vocabulary_factory('OIEProgramLeader')
ProgramLeaderVocabulary = ProgramLeaderVocabularyFactory()
LiaisonVocabularyFactory = get_calendar_vocabulary_factory('OIELiaison')
LiaisonVocabulary = LiaisonVocabularyFactory()
ProviderVocabularyFactory = get_calendar_vocabulary_factory('OIECooperatingPartner')
ProviderVocabulary = ProviderVocabularyFactory()
FileVocabularyFactory = get_calendar_vocabulary_factory('File')
FileVocabulary = FileVocabularyFactory()
ImageVocabularyFactory = get_calendar_vocabulary_factory('Image')
ImageVocabulary = ImageVocabularyFactory()


# @implementer(ISource, IContextSourceBinder)
@implementer(IVocabularyFactory)
class RegistryValueVocabulary(object):

    def __init__(self, value_name):
        self.value_name = value_name

    def __call__(self, context):
        values = api.portal.get_registry_record(self.value_name, default=False) or []
        return safe_simplevocabulary_from_values(values) # if values else SimpleVocabulary([])

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
class ProgramTransitionVocabularyFactory(object):

    def __call__(self, context):
        def getTitle(item):
            if item and len(item) > 0:
                return item[1].title
            return None

        pw = api.portal.get_tool('portal_workflow')
        program_workflow = pw[PROGRAMMANAGEMENT]
        program_transitions = program_workflow['transitions'].items()
        terms = []
        program_transitions_sorted = sorted(program_transitions, key=getTitle)
        for t_id, t_obj in program_transitions_sorted:
            terms.append(SimpleTerm(
                value=t_id,
                token=t_id,
                title=t_obj.title,
            ))
        return SimpleVocabulary(terms)


ProgramTransitionVocabulary = ProgramTransitionVocabularyFactory()


@implementer(IVocabularyFactory)
class ParticipantTransitionVocabularyFactory(object):

    def __call__(self, context):
        def getTitle(item):
            if item and len(item) > 0:
                return item[1].title
            return None

        pw = api.portal.get_tool('portal_workflow')
        program_workflow = pw['participant']
        program_transitions = program_workflow['transitions'].items()
        terms = []
        program_transitions_sorted = sorted(program_transitions, key=getTitle)
        for t_id, t_obj in program_transitions_sorted:
            terms.append(SimpleTerm(
                value=t_id,
                token=t_id,
                title=t_obj.title,
            ))
        return SimpleVocabulary(terms)


ParticipantTransitionVocabulary = ParticipantTransitionVocabularyFactory()


@implementer(IVocabularyFactory)
class TuitionAndFeesVocabularyFactory(object):

    def __call__(self, context):
        return safe_simplevocabulary_from_values(
            api.portal.get_registry_record(
                'studyabroadstudent.tuition_and_fees',
                default=DEFAULT_TUITION_AND_FEES,
            )
        )


TuitionAndFeesVocabulary = TuitionAndFeesVocabularyFactory()
