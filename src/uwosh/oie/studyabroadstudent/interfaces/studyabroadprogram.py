# -*- coding: utf-8 -*-

from collective import dexteritytextindexer
from collective.z3cform.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield import DictRow
# from zope.interface import invariant
from plone import api
from plone.app.contenttypes.behaviors.leadimage import ILeadImage
from plone.app.textfield import RichText
from plone.app.versioningbehavior.behaviors import IVersionable
from plone.autoform.directives import read_permission
from plone.autoform.directives import widget
from plone.autoform.directives import write_permission
from plone.directives import form
from plone.namedfile import field
from plone.supermodel import model
from plone.supermodel.interfaces import FIELDSETS_KEY
from plone.supermodel.model import Fieldset
from Products.CMFPlone.RegistrationTool import checkEmailAddress
from Products.CMFPlone.RegistrationTool import EmailAddressInvalid
from uwosh.oie.studyabroadstudent import _
from uwosh.oie.studyabroadstudent.vocabularies import program_cycle_vocabulary
from uwosh.oie.studyabroadstudent.vocabularies import RegistryValueVocabulary
from uwosh.oie.studyabroadstudent.vocabularies import seat_assignment_protocol
from uwosh.oie.studyabroadstudent.vocabularies import yes_no_na_vocabulary
from uwosh.oie.studyabroadstudent.vocabularies import yes_no_none_vocabulary
# from z3c.form.interfaces import WidgetActionExecutionError
from z3c.form import validator
from zope import schema
from zope.interface import Interface
from zope.interface import Invalid
from zope.schema import ValidationError


class InvalidEmailAddress(ValidationError):
    """Invalid email address"""


def validate_email(value):
    try:
        checkEmailAddress(value)
    except EmailAddressInvalid:
        raise InvalidEmailAddress(value)
    return True


class ILearningObjectiveRowSchema(Interface):
    learning_objective = schema.TextLine(
        title=u"Enter one objective per row. Click on the \'+\' to add a row.",
    )


class IPreTravelDatesRowSchema(Interface):
    pretravel_start_datetime = schema.Datetime(
        title=_(u'Start'),
        required=True,
    )
    pretravel_end_datetime = schema.Datetime(
        title=_(u'End'),
        required=True,
    )
    pretravel_building = schema.Choice(
        title=_(u'Building'),
        source=RegistryValueVocabulary('oiestudyabroadstudent.building'),
        required=False,
    )
    pretravel_room = schema.TextLine(
        title=_(u'Room'),
        required=False,
    )
    pretravel_attendance_required = schema.Choice(
        title=_(u'Attendance Required?'),
        vocabulary=yes_no_na_vocabulary,
        required=False,
    )


class IPostTravelClassDatesRowSchema(Interface):
    posttravel_start_datetime = schema.Datetime(title=_(u'Start'))
    posttravel_end_datetime = schema.Datetime(title=_(u'End'))
    posttravel_building = schema.Choice(
        title=_(u'Building'),
        source=RegistryValueVocabulary('oiestudyabroadstudent.building'),
    )
    posttravel_room = schema.TextLine(title=_(u'Room'))
    posttravel_attendance_required = schema.Choice(
        title=_(u'Attendance Required?'),
        vocabulary=yes_no_na_vocabulary,
    )


class ICoLeadersRowSchema(Interface):
    coleader = schema.Choice(
        title=_(u'On-site Program Co-leader'),
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.program_leader',
    )


class IContributingEntityRowSchema(Interface):
    contributing_entity_contact_name = schema.TextLine(
        title=_(u'Contributing Entity Contact Name'),
    )
    contributing_entity_contact_phone_us = schema.TextLine(
        title=_(u'Contact Tel (US number)'),
    )
    contributing_entity_contact_phone_other = schema.TextLine(
        title=_(u'Contact Tel (other)'),
    )
    contributing_entity_contact_email = schema.TextLine(
        title=_(u'Contact Email'),
        constraint=validate_email,
    )
    contributing_entity_contribution_amount = schema.Float(
        title=_(u'Contribution Amount'),
        min=0.0,
    )
    contributing_entity_contribution_currency = schema.Choice(
        title=_(u'Contribution Currency'),
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.currency',
    )


class IReviewerEmailRowSchema(Interface):
    reviewer_email_row = schema.TextLine(
        title=_(u'Reviewer Email Address'),
        constraint=validate_email,
        # TODO autocomplete from campus email addresses? Or commonly entered  # noqa
        #  email addresses? Rely on browser?
    )


class ILeadershipCommentsRowSchema(Interface):
    comment = schema.Text(
        title=_(u'Add a comment'),
    )


class IOIEUserCommentsRowSchema(Interface):
    comment = schema.Text(
        title=_(u'Add a comment'),
    )


settings = Fieldset(
    'settings',
    label=_(u'Settings'),
    fields=['changeNote'],
)
fieldsets = IVersionable.getTaggedValue(FIELDSETS_KEY)
fieldsets.append(settings)

leadimage_fieldset = Fieldset(
    'leadimage',
    label=_(u'Lead Image'),
    fields=['image', 'image_caption'],
)
try:
    leadimage_fieldsets = ILeadImage.getTaggedValue(FIELDSETS_KEY)
    leadimage_fieldsets.append(leadimage_fieldset)
except KeyError:
    ILeadImage.setTaggedValue(FIELDSETS_KEY, [leadimage_fieldset])


class IOIEStudyAbroadProgram(Interface):

    dexteritytextindexer.searchable('title')
    title = schema.TextLine(
        title=_(u'Program Title'),
        description=_(
            u'The full Program Title will be displayed in all OIE print and on-line marketing and in all official OIE program-related materials.  To avoid confusion and increase "brand" awareness for your program, consistently use this program name in full, exactly as it appears here, in your print and electronic media.  Do not include country or city names in this field. (max length 45 chars)'),  # noqa
        required=True,
        max_length=45,
    )

    dexteritytextindexer.searchable('description')
    description = schema.Text(
        title=_(u'Description'),
        description=_(
            u'A brief description that will show up in search results'),
        required=True,
    )

    dexteritytextindexer.searchable('rich_description')
    rich_description = RichText(
        title=_(u'Rich Text Description'),
        description=_(
            u'This is the description that will be used to promote your program.  Your description should capture the purpose of your program, include an overview of what students will be engaged in while abroad/away, and capture students’ interest! (max length 600 chars)'),  # noqa
        default_mime_type='text/plain',
        allowed_mime_types=('text/plain', 'text/html'),
        max_length=1000,
        # TODO: create a custom validator that renders text without HTML tags  # noqa
        #  to count words accurately
        required=True,
    )

    #######################################################
    model.fieldset(
        'comments_fieldset',
        label=_(u'Comments'),
        fields=['comments_oie_leaders', 'comments_oie_all'],
    )

    read_permission(comments_oie_leaders='OIE: View OIE leadership comments')
    write_permission(comments_oie_leaders='OIE: Modify OIE leadership comments')  # noqa
    widget(comments_oie_leaders=DataGridFieldFactory)
    comments_oie_leaders = schema.List(
        title=_(u'Comments for OIE leadership'),
        description=_(
            u'Comments entered here are visible by the OIE Program Manager, Program Liaison, Program Leaders/Co-leaders and site administrators.'),  # noqa
        required=False,
        value_type=DictRow(
            title=u'comments',
            schema=ILeadershipCommentsRowSchema,
        ),
    )

    read_permission(comments_oie_all='OIE: View all OIE user comments')
    write_permission(comments_oie_all='OIE: Modify all OIE user comments')
    widget(comments_oie_all=DataGridFieldFactory)
    comments_oie_all = schema.List(
        title=_(u'Comments for all OIE users'),
        description=_(u'Comments entered here are visible by all OIE professional staff.'),  # noqa
        required=False,
        value_type=DictRow(
            title=u'comments',
            schema=IOIEUserCommentsRowSchema,
        ),
    )

    #######################################################
    model.fieldset(
        'program_code_fieldset',
        label=_(u'Program Code'),
        fields=['calendar_year', 'term', 'college_or_unit', 'countries',
                'program_code'],
    )

    calendar_year = schema.Choice(
        title=_(u'Calendar Year'),
        description=_(
            u'Select the calendar year during which the program will run.  This is not the year associated with the term of study.  For example, a January interim program running from Jan 2-28, 2019 will be associated with "2019".   A program running Dec 28, 2018-Jan 28, 2019 will also be associated with "2019".'),  # noqa
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.calendar_year',
        required=True,
    )

    term = schema.Choice(
        title=_(u'Term'),
        description=_(u''),
        required=True,
        source=RegistryValueVocabulary('oiestudyabroadstudent.term'),
    )

    college_or_unit = schema.Choice(
        title=_(u'College or Unit'),
        description=_(u''),
        required=True,
        source=RegistryValueVocabulary(
            'oiestudyabroadstudent.college_or_unit',
        ),
    )

    countries = schema.List(
        title=_(u'Country or Countries'),
        description=_(u'Country names will be added to your "Program Title" and used in marketing.'),  # noqa
        required=True,
        value_type=schema.Choice(
            source=RegistryValueVocabulary(
                'oiestudyabroadstudent.countries',
            ),
        ),
    )

    program_code = schema.TextLine(
        title=_(u'Program Code'),
        description=_(u'(auto-generated)'),
        required=True,
        default=_(u'will be auto-generated'),
        readonly=True,
    )

    #######################################################
    model.fieldset(
        'academic_program_fieldset',
        label=_(u'Academic Program'),
        fields=['sponsoring_unit_or_department', 'program_type',
                'program_component', 'title', 'description',
                'rich_description', 'eligibility_requirement',
                'learning_objectives', 'equipment_and_space',
                'equipment_and_space_needs', 'guest_lectures',
                'initial_draft_program_schedule',
                'syllabus_and_supporting_docs', 'min_credits_earned',
                'max_credits_earned', 'language_of_study',
                'cooperating_partners'],
    )

    sponsoring_unit_or_department = schema.List(
        title=_(u'Sponsoring Unit or Department'),
        description=_(u'Select all that apply.'),
        required=True,
        value_type=schema.Choice(
            source=RegistryValueVocabulary(
                'oiestudyabroadstudent.sponsoring_unit_or_department',
            ),
        ),
    )

    program_type = schema.Choice(
        title=_(u'Program Type'),
        required=True,
        source=RegistryValueVocabulary('oiestudyabroadstudent.program_type'),
    )

    program_component = schema.Choice(
        title=_(u'Program Component'),
        required=True,
        source=RegistryValueVocabulary(
            'oiestudyabroadstudent.program_component',
        ),
    )

    eligibility_requirement = schema.Choice(
        title=u'Eligibility Requirement',
        description=u'Select the eligibility requirement for this program',
        required=False,
        source=RegistryValueVocabulary(
            'oiestudyabroadstudent.eligibility_requirement',
        ),
        default=None,
    )

    widget(
        'learning_objectives',
        DataGridFieldFactory,
    )
    learning_objectives = schema.List(
        title=_(u'Learning Objectives'),
        description=_(
            u'State the learning objectives for this program.  Include only one learning objective per text field. These learning objectives will be included in end-of-program assessment and may be used to support Higher Learning Commission and other accreditation processes. (Max: 12 entries)'),  # noqa
        required=True,
        value_type=DictRow(
            title=u'learning objective row',
            schema=ILearningObjectiveRowSchema,
        ),
    )

    equipment_and_space = schema.Choice(
        title=_(u'Equipment & Space'),
        description=_(u''),
        required=True,
        source=RegistryValueVocabulary(
            'oiestudyabroadstudent.equipment_and_space',
        ),
    )

    equipment_and_space_needs = RichText(
        title=_(u'Equipment & Space details'),
        description=_(u'if needed'),
        default_mime_type='text/plain',
        allowed_mime_types=('text/plain', 'text/html'),
        required=False,
        # TODO: validator: if equipment_and_space then this must have non  # noqa
        #  empty value
    )

    guest_lectures = schema.Choice(
        title=_(u'Guest Lectures'),
        description=_(u''),
        required=True,
        source=RegistryValueVocabulary('oiestudyabroadstudent.guest_lectures'),
    )

    initial_draft_program_schedule = field.NamedFile(
        title=_(u'Initial Draft Program Schedule'),
        description=_(u'Complete the OIE itinerary form and upload here.'),
        required=True,
    )

    syllabus_and_supporting_docs = field.NamedFile(
        title=_(u'Syllabus & Other Supporting Documents'),
        description=_(
            u'Upload your syllabus plus other related documents (if any).  If you update your syllabus, replace this copy with the updated copy.  This field will remain editable until just prior to travel.'),  # noqa
        required=False,
    )

    min_credits_earned = schema.Choice(
        title=_(u'Minimum Number of Credits to be Earned by Each Applicant'),
        description=_(u''),
        required=True,
        source=RegistryValueVocabulary('oiestudyabroadstudent.credits'),
    )

    max_credits_earned = schema.Choice(
        title=_(u'Maximum Number of Credits to be Earned by Each Applicant'),
        description=_(u''),
        required=True,
        source=RegistryValueVocabulary('oiestudyabroadstudent.credits'),
    )

    language_of_study = schema.List(
        title=_(u'Language of Study'),
        description=_(
            u'Select all that apply. Contact the Office of International Education to add a language (abroad@uwosh.edu).'),  # noqa
        required=True,
        value_type=schema.Choice(
            source=RegistryValueVocabulary('oiestudyabroadstudent.language'),
        ),
    )

    cooperating_partners = schema.List(
        title=_(u'Cooperating Partners'),
        description=_(u'Only entities listed on the UW System Preferred Provider List or academic institutions with a current affiliation agreement with UWO may be selected here.  All other cooperating partners must be selected by following UW System procurement policies.'),  # noqa
        required=False,
        value_type=schema.Choice(
            vocabulary='uwosh.oie.studyabroadstudent.vocabularies.cooperatingpartner',  # noqa
        ),
    )

    #######################################################
    model.fieldset(
        'dates_destinations_fieldset',
        label=_(u'Dates and Destinations'),
        fields=['program_cycle', 'pretravel_dates',
                'travelDatesTransitionsAndDestinations',
                'add_transition_link', 'firstChoiceDatesFlexible',
                'postTravelClassDates'],
    ),

    program_cycle = schema.Choice(
        title=_(u'Program Cycle'),
        description=_(
            u'How often will this program be offered?  This information will display in some marketing materials.  If it isn''t possible to predict, leave this blank.'),  # noqa
        vocabulary=program_cycle_vocabulary,
    )

    widget(pretravel_dates=DataGridFieldFactory)
    pretravel_dates = schema.List(
        title=_(u'Pre-Travel Class & Orientation Dates'),
        description=_(
            u'Students expect to meet group members and their program leader or program advisor in a formal group setting at least once prior to travel. Check with your department chair and/or College administration on pre-travel requirements specific to your unit. OIE recommends holding program orientation dates after the OIE Orientation Materials Submission Deadline. This may allow you to reinforce, rather than fully introduce, information that will be presented in the OIE orientation. Students are expected to ensure, prior to confirming participation on a study abroad/away program, that they have no other obligations during your pre-travel class dates. Students with obligations during one or more dates/times must disclose this on their application and must have the approval of the Program Liaison to participate before the OIE will place the student on the program. For this reason, after we advertise these dates to students as mandatory, the dates shouldn’t be changed!'),  # noqa
        required=True,
        value_type=DictRow(
            title=u'Pre-Travel Dates',
            schema=IPreTravelDatesRowSchema,
        ),
    )

    form.mode(travelDatesTransitionsAndDestinations='display')
    travelDatesTransitionsAndDestinations = RichText(
        title=_(u'Travel Dates, Transitions & Destinations'),
        description=_(u'All transitions for this program are listed here.'),
        required=False,
        default=u'<em>There are currently no transitions</em>',
    )
    form.mode(add_transition_link='display')
    add_transition_link = RichText(
        required=False,
        default=u'<em>You can add transitions after saving this program</em>',
    )

    firstChoiceDatesFlexible = schema.Choice(
        title=_(u'My first-choice dates are flexible.'),
        description=_(u'If yes, your OIE Program Manager may recommend changes based on flight availability or program component scheduling.'),  # noqa
        vocabulary=yes_no_none_vocabulary,
        required=True,
    )

    widget('postTravelClassDates', DataGridFieldFactory)
    postTravelClassDates = schema.List(
        title=_(u'Post-travel Class Dates'),
        description=_(
            u'Participants are expected to ensure, prior to confirming participation on a study abroad/away program, that they have no other obligations during post-travel class dates.  Participants with obligations during one or more dates/times must disclose this on their application and must have the approval of the Program Liaison to participate before the OIE will place the participant on the program.  For this reason, after we advertise these dates to participants as mandatory, the dates shouldn’t be changed!'),  # noqa
        value_type=DictRow(
            title=u'Post-travel Class Dates',
            schema=IPostTravelClassDatesRowSchema,
        ),
        required=False,
    )

    #######################################################
    # TODO Applicant should not see this field during the "Initial" state.  # noqa
    #   Can this be made visible AFTER transitioning from this state?
    #
    model.fieldset(
        'departure_flight_fieldset',
        label=_('Departure'),
        fields=['airline', 'flightNumber', 'airport', 'departureDateTime',
                'arrivalAtDestinationAndInsuranceStartDate'],
    )

    airline = schema.Choice(
        title=_(u'Airline'),
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.airline',
        required=False,
    )

    flightNumber = schema.TextLine(
        title=_(u'Flight Number'),
        required=False,
    )

    airport = schema.Choice(
        title=_(u'Airport'),
        source=RegistryValueVocabulary('oiestudyabroadstudent.airport'),
        required=False,
    )

    departureDateTime = schema.Datetime(
        title=_(u'Departure Date and Time'),
        required=False,
    )

    arrivalAtDestinationAndInsuranceStartDate = schema.Datetime(
        title=_(u'Arrival at Destination & Insurance Start Date'),
        required=False,
    )

    #######################################################
    # TODO Applicant should not see this field during the "Initial" state.  # noqa
    #   Can this be made visible AFTER transitioning from this state?
    #
    model.fieldset(
        'departure_from_oshkosh_fieldset',
        label=_(u'Departure from Oshkosh'),
        fields=['transportationFromOshkoshToDepartureAirport',
                'airport_transfer', 'oshkoshDepartureLocation',
                'oshkoshMeetingDateTime', 'oshkoshDepartureDateTime',
                'milwaukeeDepartureDateTime',
                'airportArrivalDateTime'],
    )

    transportationFromOshkoshToDepartureAirport = schema.Choice(
        title=_(u'Transportation is provided from Oshkosh'),
        source=RegistryValueVocabulary(
            'oiestudyabroadstudent.airport_transfer',
        ),
        required=False,
    )

    oshkoshDepartureLocation = schema.Choice(
        title=_('Oshkosh Departure Location'),
        source=RegistryValueVocabulary('oiestudyabroadstudent.locations'),
        required=False,
        # TODO dropdown  [display only if "Transportation is provided from  # noqa
        #   Oshkosh is "yes"]
    )

    oshkoshMeetingDateTime = schema.Datetime(
        title=_(u'Oshkosh Meeting Date & Time'),
        required=False,
        # TODO =departure flight date/time minus 7.75 hours [display only if  # noqa
        #   "Transportation is provided from Oshkosh is "yes"]
    )

    oshkoshDepartureDateTime = schema.Datetime(
        title=_(u'Oshkosh Departure Date & Time'),
        required=False,
        # TODO =departure flight date/time minus 7.5 hours [display only if  # noqa
        #   "Transportation is provided from Oshkosh is "yes"]
    )

    milwaukeeDepartureDateTime = schema.Datetime(
        title=_('Milwaukee Departure Date & Time'),
        required=False,
        # TODO =departure flight date/time minus 6.0 hours [display only if  # noqa
        #   "Milwaukee Departure Location” is not null]
    )

    airportArrivalDateTime = schema.Datetime(
        title=_('Destination Arrival Date & Time'),
        required=False,
        # TODO '=departure flight date/time minus 3.5 hours [display only if  # noqa
        #   "Transportation is provided from Oshkosh is "yes"]
    )

    #######################################################
    # TODO Applicant should not see this field during the "Initial" state.  # noqa
    #   Can this be made visible AFTER transitioning from this state?
    #
    model.fieldset(
        'return_flight_fieldset',
        label=_('Return'),
        fields=['airlineReturn', 'flightNumberReturn', 'airportReturn',
                'returnDateTime', 'arrivalInWisconsinDate',
                'insuranceEndDate'],
    )

    airlineReturn = schema.Choice(
        title=_(u'Airline'),
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.airline',
        required=False,
    )

    flightNumberReturn = schema.TextLine(
        title=_(u'Flight Number'),
        required=False,
    )

    airportReturn = schema.Choice(
        title=_(u'Airport'),
        source=RegistryValueVocabulary('oiestudyabroadstudent.airport'),
        required=False,
    )

    returnDateTime = schema.Datetime(
        title=_(u'Return Date and Time'),
        required=False,
    )

    arrivalInWisconsinDate = schema.Datetime(
        title=_(u'Arrival at Final Destination Airport'),
        required=False,
    )

    insuranceEndDate = schema.Datetime(
        title=_(u'Insurance End Date'),
        required=False,
    )

    #######################################################
    # TODO Applicant should not see this field during the "Initial" state.  # noqa
    #   Can this be made visible AFTER transitioning from this state?
    #
    model.fieldset(
        'return_to_oshkosh_fieldset',
        label=_(u'Return to Oshkosh'),
        fields=['transportationFromArrivalAirportToOshkosh',
                'milwaukeeArrivalDateTime', 'oshkoshArrivalDateTime'],
    )

    transportationFromArrivalAirportToOshkosh = schema.Choice(
        title=_(u'Transportation is Provided Back to Oshkosh'),
        source=RegistryValueVocabulary(
            'oiestudyabroadstudent.airport_transfer',
        ),
        required=False,
    )

    milwaukeeArrivalDateTime = schema.Datetime(
        title=_('Milwaukee Arrival Date & Time'),
        required=False,
        # TODO '=arrival flight date/time plus 2.5 hours [display only if  # noqa
        #   "Transportation from Arrival airport to Oshkosh is "yes"]
    )

    oshkoshArrivalDateTime = schema.Datetime(
        title=_(u'Oshkosh Arrival Date & Time'),
        required=False,
        # TODO '=arrival flight date/time plus 4 hours [display only if  # noqa
        #   "Transportation from Arrival airport to Oshkosh is "yes"]
    )

    #######################################################
    model.fieldset(
        'participant_selection_fieldset',
        label=_(u'Participant Selection'),
        fields=['studentStatus', 'seatAssignmentProtocol',
                'liaisonReviewOfIndividualApplicants', 'approvalCriteria',
                'individualInterview', 'firstRecommendationRequired',
                'secondRecommendationRequired',
                'applicantQuestion1', 'applicantQuestion2',
                'applicantQuestion3', 'applicantQuestion4',
                'applicantQuestion5', 'cvRequired',
                'letterOfMotivationRequired', 'otherRequired'],
    ),

    studentStatus = schema.Choice(
        title=_(u'Student Status'),
        description=_(u'Choose one'),
        source=RegistryValueVocabulary('oiestudyabroadstudent.student_status'),
        required=True,
    )

    seatAssignmentProtocol = schema.Choice(
        title=_(u'Seat Assignment Protocol'),
        vocabulary=seat_assignment_protocol,
        required=True,
    )

    liaisonReviewOfIndividualApplicants = schema.Choice(
        title=_(u'Liaison Review of Individual Applicants'),
        description=_(
            u'For competitive programs or for programs that require each applicant to have specific background in addition to meeting course pre-requisites, indicate criteria to be used and select the method or methods to be employed to determine whether criteria have been met.  Do not include or duplicate course pre-requisites here.'),  # noqa
        vocabulary=yes_no_none_vocabulary,
        required=True,
    )

    approvalCriteria = schema.Text(
        title=_(u'Criteria to be used in the approval process include the following'),  # noqa
        required=False,
        # TODO validate that this is non-blank if  # noqa
        #  liaisonReviewOfIndividualApplicants == True
    )

    individualInterview = schema.Choice(
        title=_(u'The Program Liaison, Program Leader or Program Co-leader will interview each applicant'),  # noqa
        vocabulary=yes_no_none_vocabulary,
        required=False,
        # TODO yes/no (default=no; this question should be unavailable/greyed  # noqa
        #   out if "approvalcriteria" is not filled in)
    )

    firstRecommendationRequired = schema.Choice(
        title=_(u'1st Reference is required'),
        description=_(u'If "yes", this item appears in the Applicant Portal as an application item'),  # noqa
        vocabulary=yes_no_none_vocabulary,
        required=False,
        # TODO yes/no (default=no; this question should be unavailable/greyed  # noqa
        #   out if "approvalcriteria" is not filled in)
    )

    secondRecommendationRequired = schema.Choice(
        title=_(u'2nd Reference is required'),
        description=_(u'If "yes", this item appears in the Applicant Portal as an application item'),  # noqa
        vocabulary=yes_no_none_vocabulary,
        required=False,
        # TODO "yes/no (default=no; this question should be unavailable/greyed  # noqa
        #   out if "approvalcriteria" is not filled in). This cannot be ""yes""
        #   if ""A 1st Recommendation is required"" is ""no""."
    )

    applicantQuestion1 = schema.Text(
        title=_(u'Question 1'),
        description=_(
            u'You may add up to 5 short-answer questions to the participant application.  If a question appears here, it will be required of all applicants.  Questions cannot be made optional and cannot be applied to some applicants and not to others.'),  # noqa
        required=False,
        # TODO max 200 characters; this question should be unavailable/greyed  # noqa
        #  out if "approvalcriteria" is not filled in
    )

    applicantQuestion2 = schema.Text(
        title=_(u'Question 2'),
        description=_(
            u'If a question appears here, it will be required of all applicants.  Questions cannot be made optional and cannot be applied to some applicants and not to others.'),  # noqa
        required=False,
        # TODO max 200 characters; this question should be unavailable/greyed  # noqa
        #  out if "approvalcriteria" is not filled in
    )

    applicantQuestion3 = schema.Text(
        title=_(u'Question 3'),
        description=_(
            u'If a question appears here, it will be required of all applicants.  Questions cannot be made optional and cannot be applied to some applicants and not to others.'),  # noqa
        required=False,
        # TODO max 200 characters; this question should be unavailable/greyed  # noqa
        #  out if "approvalcriteria" is not filled in
    )

    applicantQuestion4 = schema.Text(
        title=_(u'Question 4'),
        description=_(
            u'If a question appears here, it will be required of all applicants.  Questions cannot be made optional and cannot be applied to some applicants and not to others.'),  # noqa
        required=False,
        # TODO max 200 characters; this question should be unavailable/greyed  # noqa
        #   out if "approvalcriteria" is not filled in
    )

    applicantQuestion5 = schema.Text(
        title=_(u'Question 5'),
        description=_(
            u'If a question appears here, it will be required of all applicants.  Questions cannot be made optional and cannot be applied to some applicants and not to others.'),  # noqa
        required=False,
        # TODO max 200 characters; this question should be unavailable/greyed  # noqa
        #   out if "approvalcriteria" is not filled in
    )

    cvRequired = schema.Choice(
        title=_(u'CV or Resume'),
        description=_(
            u'If "yes", this item appears in the Applicant Portal as an application item.'),  # noqa
        vocabulary=yes_no_none_vocabulary,
        required=True,
        # TODO yes/no (default=no; this question should be unavailable/greyed  # noqa
        #   out if "approvalcriteria" is not filled in)
    )

    letterOfMotivationRequired = schema.Choice(
        title=_(u'Letter of Motivation'),
        description=_(u'If "yes", this item appears in the Applicant Portal as an application item.'),  # noqa
        vocabulary=yes_no_none_vocabulary,
        required=True,
        # TODO yes/no (default=no; this question should be unavailable/greyed  # noqa
        #   out if "approvalcriteria" is not filled in)
    )

    otherRequired = schema.Text(
        title=_(u'Other'),
        required=False,
        # TODO "this question should be unavailable/greyed out if  # noqa
        #  "approvalcriteria" is not filled in"
    )

    #######################################################
    model.fieldset(
        'liaison_and_leadership_fieldset',
        label=_(u'Liaison to the OIE'),
        fields=['liaison', 'program_leader', 'program_coleaders'],
    )
    liaison = schema.Choice(
        title=_(u'Liaison to the OIE'),
        description=_(
            u'The Liaison to the OIE communicates decisions related to program development and delivery to the Program Manager in the OIE and communicates program changes and updates to his/her unit administration. There is only one Liaison per program;  all decisions made at the unit level must be communicated to the OIE through the designated liaison.  The Liaison may also serve as the On-site Program Leader and may teach one or more of the program courses.'),  # noqa
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.liaison',
        required=False,
    )
    program_leader = schema.Choice(
        title=_(u'On-site Program Leader'),
        description=_(
            u'The On-site Program Leader is responsible for providing leadership for the group and for overseeing group health and safety.  The On-site Program Leader may also teach one or more of the program courses.  Select "no" if there will be NO Program Leader from UW Oshkosh accompanying the group.  Select "yes" and complete fields below related to Program Leadership if there will be a Program Leader from UW Oshkosh accompanying the group.'),  # noqa
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.program_leader',
        required=False,
    )
    widget('program_coleaders', DataGridFieldFactory)
    program_coleaders = schema.List(
        title=_(u'On-site Program Leader (choose 0-4)'),
        description=_(
            u'The On-site Program Leader is responsible for providing leadership for the group and for overseeing group health and safety.  The On-site Program Leader may also teach one or more of the program courses.'),  # noqa
        value_type=DictRow(
            title=u'co-leaders',
            schema=ICoLeadersRowSchema,
        ),
        required=False,
    )

    #######################################################
    model.fieldset(
        'courses_fieldset',
        label=_(u'Courses'),
        fields=['courses', 'add_course_link'],
    )
    form.mode(courses='display')
    courses = RichText(
        title=u'UW Oshkosh Course Subject & Number',
        description=u'Include all courses that will be taught through this program.  Do not include courses that will be taught entirely at UWO, even when these courses are offered in preparation for the program away.  List existing courses only.  If the course you intend to use is not an existing course, your department must submit the course for formal approval through normal university channels prior to applying to use the course abroad/away.  Contact the OIE to add a course (abroad@uwosh.edu).',  # noqa
        required=False,
        default=u'<em>There are currently no courses</em>',
    )
    form.mode(add_course_link='display')
    add_course_link = RichText(
        required=False,
        default=u'<em>You can add courses after saving this program</em>',
    )

    #######################################################
    model.fieldset(
        'contributions_fieldset',
        label=_(u'Contributions'),
        fields=['contributions_label', 'contributing_entity'],
    )
    form.mode(contributions_label='display')
    contributions_label = schema.TextLine(
        description=_(
            'If the College, Department, an external agency, external partner, or grant will contribute financially to the program, list the official name of the entity that is contributing, contributor contact details, and the amount of the contribution.'),  # noqa
    )
    widget('contributing_entity', DataGridFieldFactory)
    contributing_entity = schema.List(
        title=_(u'Specify Contributing Entity or Entities'),
        description=_(u'(max: 5)'),
        required=False,
        value_type=DictRow(
            title=u'Contributing Entity',
            schema=IContributingEntityRowSchema,
        ),
    )

    #######################################################
    model.fieldset(
        'reviewers_fieldset',
        label=_(u'Reviewers'),
        fields=['reviewers_label', 'reviewer_emails'],
    )
    form.mode(reviewers_label='display')
    reviewers_label = schema.TextLine(
        description=_(
            u'Type an email address for every Committee Chair, Department Chair and Dean: •  who supervises a Liaison, On-site Program Leader or On-site Program Co-leader listed in this application and/or •  is associated with a course offered through this program. Do not include email addresses for committee members who review applications.'),  # noqa3
        # TODO Each program may have a different number of "Chair reviewers"  # noqa
        #   and "Dean/Unit Director reviewers".  Who reviews an application
        #   will change depending on who is leading the program and which
        #   courses are offered.  How can this be handled?
    )
    widget('reviewer_emails', DataGridFieldFactory)
    reviewer_emails = schema.List(
        title=_(u'Reviewer Emails'),
        description=_(u'(max: 6)'),
        required=False,
        value_type=DictRow(
            title=u'Reviewer Emails',
            schema=IReviewerEmailRowSchema,
        ),
    )

    #######################################################
    model.fieldset(
        'oie_review_fieldset',
        label=_(u'OIE Review'),
        fields=['program_schedule', 'director_recommendations',
                'health_safety_security_documents',
                'add_health_document_link', 'application_deadlines_label',
                'step_1_and_2_application_deadline',
                'step_3_application_deadline', 'step_4_application_deadline',
                'application_items_label',
                'flight_deviation_request_return_flight_only',
                'flight_deviation_request_roundtrip_or_outbound_flight',
                'hessen_isu_application', 'hessen_iwu_application',
                'graduate_registration_form_and_graduate_special_non_degree_information_form',  # noqa
                'transfer_credit_prior_approval_form',
                'application_items_travel_label',
                'drivers_license_copy_for_india_visa_application',
                'biographical_page_of_your_signed_passport',
                'original_passport',
                'official_passport_photo_for_india_visa_application',
                'digital_passport_photo',
                'passport_size_photo', 'indian_visa_application',
                'visa_required_for_us_citizens',
                'yellow_fever_vaccination_certificate',
                'application_items_background_label',
                'credit_overload_form',
                'application_items_other_label'],
    )
    program_schedule = schema.Choice(
        title=_(u'Program Schedule'),
        description=_(u'The OIE Program Manager checks this box to confirm that the program schedule has been viewed.  Checking this box does not mean that activities on the schedule have been approved.  Further Risk Assessment will be completed after this initial review.'),  # noqa
        vocabulary=yes_no_none_vocabulary,
        required=False,
        # TODO check box or workflow? (for now, this will be just a check  # noqa
        #   box.  It could become part of the workflow in the future.  The
        #   checkbox must be checked to move through the workflow.
    )
    director_recommendations = RichText(
        title=_(u'OIE Director Recommendation'),
        description=_(u'Include site-specific Health, Safety & Security remarks when appropriate.'),  # noqa
        default_mime_type='text/plain',
        allowed_mime_types=('text/plain', 'text/html'),
        max_length=2500,
        required=False,
    )
    form.mode(health_safety_security_documents='display')
    health_safety_security_documents = RichText(
        title=_(u'Health, Safety & Security Documents'),
        description=_(
            u'For all sites, upload the OIE Risk Assessment, Department of State Country Information, and CDC country-specific information.  When warranted, upload additional risk forms and/or supporting documentation.'),  # noqa
        required=False,
        default=u'<em>There are currently no documents</em>',
    )
    form.mode(add_health_document_link='display')
    add_health_document_link = RichText(
        required=False,
        default=u'<em>You can add health documents after saving this program</em>',  # noqa
    )
    form.mode(application_deadlines_label='display')
    application_deadlines_label = schema.TextLine(
        description=_(u'Application Deadlines'),
        required=False,
    )
    step_1_and_2_application_deadline = schema.Date(
        title=_(u'STEPs I & II Application Deadline'),
        description=_(u'The STEPs I & II application deadline must be the OIE default student application date, or a date that is two weeks prior to the contracted date to release airline tickets, whichever is earlier.  Alternatively, the Program Liaison may identify an even earlier deadline, provided OIE can provide sufficient staffing in the week leading up to the proposed deadline.  Default student application deadlines are: Last Friday in February (summer & fall semester programs); 2nd Friday in September (fall interim programs); last Friday in September (spring semester programs); 1st Friday of Spring Semester (spring interim programs).'),  # noqa
        required=False,
    )
    step_3_application_deadline = schema.Date(
        title=_(u'STEP III Application Deadline'),
        description=_(u'The STEP III application deadline must be the OIE default student application date, or a date that is one week prior to the contracted date to release airline tickets, whichever is earlier.  Alternatively, the Program Liaison may identify an even earlier deadline, provided OIE can provide sufficient staffing in the week leading up to the proposed deadline.  Default student application deadlines are: 1st Friday in March (summer & fall semester programs); 3rd Friday in September (fall interim programs); 1st Friday in October (spring semester programs); 2nd Friday of Spring Semester (spring interim programs).'),  # noqa
        required=False,
    )
    step_4_application_deadline = schema.Date(
        title=_(u'STEP IV Application Deadline'),
        description=_(u'The STEP IV application deadline must take into consideration external deadlines and processing time in the OIE from the point of receiving completed application documents, and the anticipated dates on which documents can be sent to external partners and received by them.'),  # noqa
        required=False,
    )

    form.mode(application_items_label='display')
    application_items_label = schema.TextLine(
        title=_(u'Application Items - Internal Forms'),
        description=_(
            u'If checked "yes", the items below will appear in the Participant Portal as an application item.'),  # noqa
        # TODO Let's talk through this one.  Is there a way for us to select  # noqa
        #   the documents that need to be displayed in the application by group
        #   and for individual participants?
    )
    flight_deviation_request_return_flight_only = schema.Choice(
        title=_(u'Application for Permission to Follow an Alternative Schedule on the Return Flight Only'),  # noqa
        description=_(
            u' Select ''yes'' for all independent travel programs where OIE does not hold space on a group flight and for all programs on which OIE holds space on a group flight but may allow deviations on the return flight only on a case-by-case basis.'),  # noqa
        vocabulary=yes_no_none_vocabulary,
        required=False,
        # TODO default=none  # noqa
    )
    flight_deviation_request_roundtrip_or_outbound_flight = schema.Choice(
        title=_(u'Application for Permission to Follow an Alternative Schedule on the Outbound Flight Only or on My Roundtrip Flights'),  # noqa
        description=_(
            u'Select ''yes'' for all independent travel programs where OIE does not hold space on a group flight and for all programs on which OIE holds space on a group flight but may allow deviations on the outbound or roundtrip flights on a case-by-case basis.'),  # noqa
        vocabulary=yes_no_none_vocabulary,
        required=False,
        # TODO default=none  # noqa
    )
    hessen_isu_application = schema.Choice(
        title=_(u'Hessen/Wisconsin ISU Student Exchange Application'),
        description=_(
            u'Select ''yes'' if this program is included in the Hessen/Wisconsin Student Exchange AND the program is an ISU (International Summer University).'),  # noqa
        vocabulary=yes_no_none_vocabulary,
        required=False,
        # TODO default=none  # noqa
    )
    hessen_iwu_application = schema.Choice(
        title=_(u'Hessen/Wisconsin IWU Student Exchange Application'),
        description=_(
            u'Select ''yes'' if this program is included in the Hessen/Wisconsin Student Exchange AND the program is an IWU (International Winter University).'),  # noqa
        vocabulary=yes_no_none_vocabulary,
        required=False,
        # TODO default=none  # noqa
    )
    graduate_registration_form_and_graduate_special_non_degree_information_form = schema.Choice(  # noqa
        title=_(u'Special/Non-Degree Registration - Graduate Level'),
        description=_(
            u'Select ''yes'' 1) if the program allows undergraduate level course enrollment by graduate level students or 2) if the program offers graduate level courses and accepts applicants who will not be UW Oshkosh degree-seeking students during the term that the program runs.'),  # noqa
        vocabulary=yes_no_none_vocabulary,
        required=False,
        # TODO default=none  # noqa
    )
    transfer_credit_prior_approval_form = schema.Choice(
        title=_(u'Transfer Credit Prior Approval Form'),
        description=_(
            u'Select ''yes'' if one or more applicants may be enrolled in a host institution course that is eligible for transfer back to UW Oshkosh, without simultaneous enrollment at UW Oshkosh.'),  # noqa
        vocabulary=yes_no_none_vocabulary,
        required=False,
        # TODO default=none  # noqa
    )
    form.mode(application_items_travel_label='display')
    application_items_travel_label = schema.TextLine(
        title=_(u'Application Items – Travel & Identification'),
        description=_(
            u'If checked "yes", the items below will appear in the Participant Portal as an application item.'),  # noqa
    )
    drivers_license_copy_for_india_visa_application = schema.Choice(
        title=_(u'Driver\'s License or State Issued I.D. – Color Copy'),
        description=_(
            u'Select ''yes'' if required by external partners or by the foreign consulate to apply for a visa.'),  # noqa
        vocabulary=yes_no_none_vocabulary,
        required=False,
         # TODO default=none  # noqa
   )
    biographical_page_of_your_signed_passport = schema.Choice(
        title=_(u'Passport-Digital Copy of Biographical Page of Your SIGNED Passport'),  # noqa
        description=_(
            u'Select ''yes'' if required by external partners.'),
        vocabulary=yes_no_none_vocabulary,
        required=False,
        # TODO default=none  # noqa
    )
    original_passport = schema.Choice(
        title=_(u'Passport-Original SIGNED Passport'),
        description=_(
            u'Select ''yes'' if this is required to apply for a visa.'),
        vocabulary=yes_no_none_vocabulary,
        required=False,
        # TODO default=none  # noqa
    )
    official_passport_photo_for_india_visa_application = schema.Choice(
        title=_(u'Photo: Official Paper Passport Photo'),
        description=_(
            u'Select ''yes'' if required by external partners or if required to apply for a visa with photo requirements that are consistent with an official U.S. passport photo.'),  # noqa
        vocabulary=yes_no_none_vocabulary,
        required=False,
        # TODO default=none  # noqa
    )
    digital_passport_photo = schema.Choice(
        title=_(u'Photo: Official Digital Passport Photo'),
        description=_(
            u'Select ''yes'' if required by external partners or if required to apply for a visa with photo requirements that are consistent with an official U.S. passport photo.'),  # noqa
        vocabulary=yes_no_none_vocabulary,
        required=False,
         # TODO default=none  # noqa
   )
    passport_size_photo = schema.Choice(
        title=_(u'Photo: Paper'),
        description=_(u'Select ''yes'' if required by external partners or if required to apply for a visa with photo requirements that are not consistent with an official U.S. passport photo.'),  # noqa
        vocabulary=yes_no_none_vocabulary,
        required=False,
        # TODO default=none  # noqa
    )
    indian_visa_application = schema.Choice(
        title=_(u'Photo: Digital'),
        description=_(u'Select ''yes'' if required by external partners or if required to apply for a visa with photo requirements that are not consistent with an official U.S. passport photo.'),  # noqa
        vocabulary=yes_no_none_vocabulary,
        required=False,
        # TODO default=none  # noqa
    )
    visa_required_for_us_citizens = schema.Choice(
        title=_(u'Visa Application - All U.S. Citizens'),
        description=_(u'Select ''yes'' if a visa is required of U.S. citizens.'),  # noqa
        vocabulary=yes_no_none_vocabulary,
        required=False,
        # TODO default=none  # noqa
    )
    yellow_fever_vaccination_certificate = schema.Choice(
        title=_(u'Yellow Fever Vaccination Certificate'),
        description=_(
            u'Required ONLY IF you will have traveled to any of the countries listed on this website within 90 days of departure to your program site abroad.  A copy of the certificate should be sent in with your visa application as a precaution against visa denial.  wwwnc.cdc.gov/travel/yellowbook/2016/infectious-diseases-related-to-travel/yellow-fever'),  # noqa
        vocabulary=yes_no_none_vocabulary,
        required=False,
         # TODO default=none  # noqa
    )
    form.mode(application_items_background_label='display')
    application_items_background_label = schema.TextLine(
        title=_(u'Application Items – Background Check'),
        description=_(
            u'If checked "yes", the items below will appear in the Participant Portal as an application item.'),  # noqa
    )
    credit_overload_form = schema.Choice(
        title=_(u'Criminal Background Check'),
        description=_(
            u'Select ''yes'' if a foreign government requires this as part of the visa application process, if an external partner requires this as part of the visa application process, if participants will work with children who have not yet reached the age of majority in their home country, or if participants will work with children who are 17 years old or younger, whichever is the higher of the two ages. Use this option for a Criminal Background Check only when an FBI report is not specifically required.'),  # noqa
        vocabulary=yes_no_none_vocabulary,
        required=False,
         # TODO default=none  # noqa
   )
    form.mode(application_items_other_label='display')
    application_items_other_label = schema.TextLine(
        title=_(u'Application Items – Other'),
        description=_(
            u'If checked "yes", the items below will appear in the Participant Portal as an application item.'),  # noqa
    )

    #######################################################
    model.fieldset(
        'proposals_fieldset',
        label=_(u'Proposals'),
        fields=['proposals_label', 'request_for_proposal',
                'request_for_proposal_due_date', 'provider_proposals_label',
                'provider_01', 'provider_01_awarded_contract', 'proposal_01',
                'provider_02',
                'provider_02_awarded_contract', 'proposal_02', 'provider_03',
                'provider_03_awarded_contract',
                'proposal_03'],
    )
    form.mode(proposals_label='display')
    proposals_label = schema.TextLine(
        description=_(u'Required prior to submitting for Liaison review'),
    )
    request_for_proposal = field.NamedFile(
        title=_('Request for Proposals (RFP)'),
        description=_(
            u'Upload a draft RFP for review.  Replace draft with updated RFPs until the review process is completed.  The RFP in place as of the "Pending Receipt of Provider Proposals" state will be the one shared with providers in the formal Request for Proposals.  Therefore, do not replace the final RFP after the review process has ended.'),  # noqa
        required=False,
        # TODO Project Phase XXX: we would like to be able to upload the RFP  # noqa
        #   here, type in the names & email addresses of the vendors to whom
        #   the proposal will be sent, and require that the vendors upload
        #   their proposals to our system (rather than send them by email).  If
        #   selected, the vendor should be able to type in contact details for
        #   two references, upload their business license and insurance
        #   certificate into our system, and type in validty dates for their
        #   insurance. We'd like to be able to track vendors by Program, add
        #   insurance certificates annually, and use the system in a way that
        #   wouldn't allow us to contract with a vendor who has an expired
        #   insurance certificate.
    )
    request_for_proposal_due_date = schema.Date(
        title=_(u'Request for Proposals Due'),
        required=False,
    )
    form.mode(provider_proposals_label='display')
    provider_proposals_label = schema.TextLine(
        description=_(
            u'"Provider Proposals: At least 1 provider proposal must be selected and uploaded plus 1 flight proposal uploaded prior to using the ""Review Provider Proposal"" function. A yes/no contracting decision must be made for every provider and flight proposal prior to using the ""publish fee"" function.'),  # noqa
    )
    provider_01 = schema.Choice(
        title=_(u'Provider 01'),
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.provider',
        required=False,
        # TODO NOTE: in order to "add new" provider, OIE must  # noqa
        # 	complete a secondary vetting process.  PHASE XX of this
        # 	project: add a workflow and associated fields (provider
        # 	contact info, upload field for insurance docs, #  upload
        # 	field for business license, etc.) that allows us to track
        # 	our vetting progress and make a provider #  "available" in
        # 	the system only after vetting and only while insurance
        # 	certificates are valid.
    )
    provider_01_awarded_contract = schema.Choice(
        title=_(u'Provider 01 Awarded Contract'),
        vocabulary=yes_no_none_vocabulary,
        required=False,
        # TODO default=none  # noqa
    )
    proposal_01 = field.NamedFile(
        title=_('Proposal 01'),
        description=_(
            u'Upload a clean copy of proposal 01.  Proposal notes may be included by attaching these to the end of the clean proposal document.'),  # noqa
        required=False,
    )
    provider_02 = schema.Choice(
        title=_(u'Provider 02'),
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.provider',
        # TODO NOTE: in order to "add new" provider, OIE must complete a  # noqa
        #  secondary vetting process.  PHASE XX of this project: add a
        #  workflow and associated fields (provider contact info, upload
        #  field for insurance docs, upload field for business license, etc.)
        #  that allows us to track our vetting progress and make a provider
        #  "available" in the system only after vetting and only while
        #  insurance certificates are valid.
        required=False,
    )
    provider_02_awarded_contract = schema.Choice(
        title=_(u'Provider 02 Awarded Contract'),
        vocabulary=yes_no_none_vocabulary,
        required=False,
        # TODO default=none  # noqa
    )
    proposal_02 = field.NamedFile(
        title=_('Proposal 02'),
        description=_(
            u'Upload a clean copy of proposal 03.  Proposal notes may be included by attaching these to the end of the clean proposal document.'),  # noqa
        required=False,
    )
    provider_03 = schema.Choice(
        title=_(u'Provider 03'),
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.provider',
        # TODO NOTE: in order to "add new" provider, OIE must complete a  # noqa
        #  secondary vetting process.  PHASE XX of this project: add a
        #  workflow and associated fields (provider contact info, upload
        #  field for insurance docs, upload field for business license, etc.)
        #  that allows us to track our vetting progress and make a provider
        #  "available" in the system only after vetting and only while
        #  insurance certificates are valid.
        required=False,
    )
    provider_03_awarded_contract = schema.Choice(
        title=_(u'Provider 03 Awarded Contract'),
        vocabulary=yes_no_none_vocabulary,
        required=False,
    )
    proposal_03 = field.NamedFile(
        title=_('Proposal 03'),
        description=_(
            u'Upload a clean copy of proposal 03.  Proposal notes may be included by attaching these to the end of the clean proposal document.'),  # noqa
        required=False,
    )

    #######################################################
    model.fieldset(
        'finances_fieldset',
        label=_(u'Finances'),
        fields=['finances_label', 'anticipated_number_of_applicants_min',
                'anticipated_number_of_applicants_max',
                'budget_spreadsheet', 'fecop_worksheet',
                'required_prior_to_publishing_initial_fee_label',
                'program_fee', 'required_prior_to_confirming_to_run_label',
                'first_participant_fee_statement_',
                'first_participant_fee_spreadsheet',
                'required_prior_to_publishing_initial_fee_label_2',
                'final_participant_fee_statement',
                'final_participant_fee_spreadsheet',
                'required_prior_to_confirming_ter_received_label',
                'travel_expense_report',
                'required_prior_to_processing_refunds_label',
                'participant_fees_paid_in_full',
                'compensation_paperwork',
                'participant_refund_spreadsheet',
                'required_prior_to_archiving_program_label',
                'account_transfers',
                'program_revenue', 'final_budget_documentation',
                'close_account'],
    )
    form.mode(finances_label='display')
    finances_label = schema.TextLine(
        description=_(u'Required to Determine Program Fee'),
    )
    anticipated_number_of_applicants_min = schema.Int(
        title=_('Anticipated Number of Applicants (Minimum)'),
        min=0,
        max=999,
        required=False,
    )
    anticipated_number_of_applicants_max = schema.Int(
        title=_('Anticipated Number of Applicants (Maximum)'),
        min=0,
        max=999,
        required=False,
    )
    budget_spreadsheet = field.NamedFile(
        title=_(u'Budget Spreadsheet'),
        description=_(
            u'Upload a draft budget spreadsheet for review.  Replace this draft with updated budget spreadsheets until the review process is complete.  The budget spreadsheet in place as of the end of the review process must be maintained as a reference for the published program fee estimate.  Do not replace the final budget spreadsheet after the review process has ended.'),  # noqa
        required=False,
    )
    fecop_worksheet = field.NamedFile(
        title=_(u'Full Estimated Cost of Participation (FECOP) Worksheet'),
        description=_(
            u'Upload a draft FECOP worksheet for review.  Replace this draft with updated FECOPs until the review process is complete.  The FECOP in place as of the "Application Intake in Progress" state will be the one shared with participants for application purposes.  Therefore, do not replace this FECOP after the review process has ended.'),  # noqa
        required=False,
    )

    form.mode(required_prior_to_publishing_initial_fee_label='display')
    required_prior_to_publishing_initial_fee_label = schema.TextLine(
        description=_(u'Required Prior to Publishing Initial Fee'),
    )
    program_fee = schema.Text(
        title=_(u'Full Estimated Cost of Participation'),
        description=_(u'Add the official Full Estimated Cost of Participation from the FECOP ($XXXX based on a minimum of XX participants).  If the official estimate on the FECOP is a fee range, the fee at the top end of the range must be used here.  Information in this field will display as the official Full Estimated Cost of Participation on the OIE website upon transition to "Application Intake in Progress".'),  # noqa
        default=u'TBA',
        required=False,
    )

    form.mode(required_prior_to_confirming_to_run_label='display')
    required_prior_to_confirming_to_run_label = schema.TextLine(
        description=_(u'Required Prior to Confirming to Run'),
    )
    first_participant_fee_statement_ = field.NamedFile(
        title=_(u'First Participant Fee Statement'),
        description=_(
            'Upload the first fee statement for participants.  This statement will display in the participant portal upon transition to "Pending Final Program Fee".  Participants deviating from the advertised program may require an alternative fee statement.'),  # noqa
        required=False,
        # TODO Display this fee statement in the particpant portal.  # noqa
    )
    first_participant_fee_spreadsheet = field.NamedFile(
        title=_(u'First Participant Fee Spreadsheet'),
        description=_(
            'Upload the first fee spreadsheet.  This spreadsheet will be accessed by student accounts for billing purposes.'),  # noqa
        required=False,
        # TODO Phase XXX: the system could generate this spreadsheet, with  # noqa
        #  access in student accounts.
    )

    form.mode(required_prior_to_publishing_initial_fee_label_2='display')
    required_prior_to_publishing_initial_fee_label_2 = schema.TextLine(
        description=_(
            u'Required Prior to Publishing Final Fee: Provider proposals and flight proposals on "Proposals" tab must also be complete.'),  # noqa
    )
    final_participant_fee_statement = field.NamedFile(
        title=_(u'Final Participant Fee Statement'),
        description=_(
            'Upload the final fee statement for participants.  This statement will display in the participant portal upon transition to "Final Payment Billing in Progress".  Participants deviating from the advertised program may require an alternative fee statement.'),  # noqa
        required=False,
        # TODO Display this fee statement in the particpant portal.  # noqa
    )
    final_participant_fee_spreadsheet = field.NamedFile(
        title=_(u'Final Participant Fee Spreadsheet'),
        description=_(
            'Upload the final fee spreadsheet.  This spreadsheet will be accessed by student accounts for billing purposes.'),  # noqa
        required=False,
        # TODO Phase XXX: the system could generate this spreadsheet, with  # noqa
        #  access in student accounts.
    )

    form.mode(required_prior_to_confirming_ter_received_label='display')
    required_prior_to_confirming_ter_received_label = schema.TextLine(
        description=_(u'Required Prior to Confirming that the TER has been Received'),  # noqa
    )
    travel_expense_report = field.NamedFile(
        title=_(u'Travel Expense Report'),
        description=_(
            'Upload a digital copy of OIE Travel Expense Report Accounting forms plus all related receipts.  Receipts must be numbered to match line items on the accounting form and must be organized in number order.'),  # noqa
        required=False,
        # TODO This field must be associated with each individual Program  # noqa
        #  Leader & Program Co-leader.
    )

    form.mode(required_prior_to_processing_refunds_label='display')
    required_prior_to_processing_refunds_label = schema.TextLine(
        description=_(u'Required Prior to Processing Refunds'),
    )
    participant_fees_paid_in_full = schema.Choice(
        title=_(u'Participant Fees Paid in Full'),
        vocabulary=yes_no_none_vocabulary,
        required=False,
    )
    compensation_paperwork = field.NamedFile(
        title=_(u'Compensation Paperwork'),
        description=_('Upload compensation paperwork. Include, for example, HR forms, IPAR form, and/or messaging that explains any difference from compensation approval in the "Application to Lead a Group Program Abroad/Away"'),  # noqa
        required=False,
        # TODO "This field must be associated with each individual Program  # noqa
        #  Leader & Program Co-leader.
    )
    participant_refund_spreadsheet = field.NamedFile(
        title=_(u'Participant Refund Spreadsheet'),
        description=_(
            'Upload the participant refund spreadsheet.  This spreadsheet will be accessed by student accounts for account adjustment purposes.'),  # noqa
        required=False,
    )

    form.mode(required_prior_to_archiving_program_label='display')
    required_prior_to_archiving_program_label = schema.TextLine(
        description=_(u'Required Prior to Archiving Program'),
    )
    account_transfers = schema.Choice(
        title=_(u'Account Transfers'),
        description=_(u'Confirm that all transfers into and out of the account are complete.'),  # noqa
        vocabulary=yes_no_none_vocabulary,
        required=False,
    )
    program_revenue = schema.Choice(
        title=_(u'Program Revenue'),
        description=_(
            u'Confirm that all program revenue has been received.  Confirm that the correct program revenue amount is in the account.'),  # noqa
        vocabulary=yes_no_none_vocabulary,
        required=False,
    )
    final_budget_documentation = field.NamedFile(
        title=_(u'Final Budget Documentation'),
        description=_(
            'Upload the final budget spreadsheet & supporting financial documents.  Do not upload Travel Expense Report or related receipts here.'),  # noqa
        required=False,
    )
    close_account = field.NamedFile(
        title=_(u'Close Account'),
        description=_('Upload request to close the account.'),
        required=False,
    )

    #######################################################
    model.fieldset(
        'pre_departure_fieldset',
        label=_(u'Pre-departure'),
        fields=['orientation_label', 'program_leader_orientation_packet',
                'partner_orientation',
                'required_prior_to_confirming_program_to_run_label',
                'participant_orientation_url',
                'proof_of_service_label', 'final_itinerary',
                'bus_contract_departure', 'bus_contract_return',
                'e_tickets', 'vouchers', 'insurance_invoice', 'visas',
                'other'],
    )

    form.mode(orientation_label='display')
    orientation_label = schema.TextLine(
        description=_(u'Orientation'),
    )
    program_leader_orientation_packet = field.NamedFile(
        title=_(u'Program Leader Orientation Packet'),
        description=_('Upload the Program Leader/Co-leader Orientation packet'),  # noqa
        required=False,
    )
    partner_orientation = field.NamedFile(
        title=_(u'Partner Orientation'),
        description=_('Upload partner pre-arrival documents, waiver forms, emergency protocols, etc., if any'),  # noqa
        required=False,
    )

    form.mode(required_prior_to_confirming_program_to_run_label='display')
    required_prior_to_confirming_program_to_run_label = schema.TextLine(
        description=_(u'Required Prior to Confirming Program to Run'),
    )
    participant_orientation_url = schema.URI(
        title=_(u'Participant Orientation'),
        description=_(u'Add detail on how to complete orientation.  Detail will show as participant instructions in the Participant Portal.'),  # noqa
        required=False,
    )

    form.mode(proof_of_service_label='display')
    proof_of_service_label = schema.TextLine(
        description=_(u'Required Prior to Scheduling the Operational Briefing'),  # noqa
    )
    final_itinerary = field.NamedFile(
        title=_(u'Final Itinerary'),
        description=_('Upload a clean copy of the official, final program itinerary.'),  # noqa
        required=False,
    )
    bus_contract_departure = field.NamedFile(
        title=_(u'Bus Contract (departure)'),
        description=_('Upload the bus contract.'),
        required=False,
    )
    bus_contract_return = field.NamedFile(
        title=_(u'Bus Contract (return)'),
        description=_('Upload the bus contract.'),
        required=False,
    )
    e_tickets = field.NamedFile(
        title=_(u'E-tickets'),
        description=_(
            'Upload group e-tickets.  Individual traveler tickets are uploaded by the individual through the participant portal.'),  # noqa
        required=False,
    )
    vouchers = field.NamedFile(
        title=_(u'Vouchers'),
        description=_('Upload payment vouchers.'),
        required=False,
    )
    insurance_invoice = field.NamedFile(
        title=_(u'Insurance Invoice'),
        description=_(
            'Upload the insurance invoice (the document that includes the partricipant ID) for all Program Leaders, Program Co-leaders and program participants.'),  # noqa
        required=False,
    )
    visas = field.NamedFile(
        title=_(u'Visas'),
        description=_('Upload visa copies.'),
        required=False,
    )
    other = field.NamedFile(
        title=_(u'Other'),
        description=_(''),
        required=False,
    )

    #######################################################
    model.fieldset(
        'reporting_fieldset',
        label=_(u'Reporting'),
        fields=['participant_evaluations',
                'post_program_evaluation',
                'incident_report',
                'total_number_of_high_school_students',
                'total_number_of_uw_oshkosh_freshmen',
                'total_number_of_uw_oshkosh_sophomores',
                'total_number_of_uw_oshkosh_juniors',
                'total_number_of_uw_oshkosh_seniors',
                'total_number_of_uw_oshkosh_graduate_students',
                'total_number_of_other_university_undergraduate_students',
                'total_number_of_other_university_graduate_students',
                'total_number_of_uw_oshkosh_program_leaders',
                'total_number_of_community_members'],
    )
    participant_evaluations = field.NamedFile(
        title=_(u'Participant Evaluations'),
        description=_('Upload participant evaluations.'),
        required=False,
    )
    post_program_evaluation = field.NamedFile(
        title=_(u'Post-program Evaluation'),
        description=_('Upload Liaison and/or Program Leader and/or Program Co-leader program evaluation.'),  # noqa
        required=False,
    )
    incident_report = field.NamedFile(
        title=_(u'Incident Report'),
        description=_('Upload incident report.'),
        required=False,
    )
    total_number_of_high_school_students = schema.Int(
        title=_(u'Total Number of High School Students'),
        required=False,
        # TODO calculate  # noqa
    )
    total_number_of_uw_oshkosh_freshmen = schema.Int(
        title=_(u'Total Number of UW Oshkosh Freshmen'),
        required=False,
        # TODO calculate  # noqa
    )
    total_number_of_uw_oshkosh_sophomores = schema.Int(
        title=_(u'Total Number of UW Oshkosh Sophomores'),
        required=False,
        # TODO calculate  # noqa
    )
    total_number_of_uw_oshkosh_juniors = schema.Int(
        title=_(u'Total Number of UW Oshkosh Juniors'),
        required=False,
        # TODO calculate  # noqa
    )
    total_number_of_uw_oshkosh_seniors = schema.Int(
        title=_(u'Total Number of UW Oshkosh Seniors'),
        required=False,
        # TODO calculate  # noqa
    )
    total_number_of_uw_oshkosh_graduate_students = schema.Int(
        title=_(u'Total Number of UW Oshkosh Graduate Students'),
        required=False,
        # TODO calculate  # noqa
    )
    total_number_of_other_university_undergraduate_students = schema.Int(
        title=_(u'Total Number of Other University Undergraduate Students'),
        required=False,
        # TODO calculate  # noqa
    )
    total_number_of_other_university_graduate_students = schema.Int(
        title=_(u'Total Number of Other University Graduate Students'),
        required=False,
        # TODO calculate  # noqa
    )
    total_number_of_uw_oshkosh_program_leaders = schema.Int(
        title=_(u'Total Number of UW Oshkosh Program Leaders'),
        required=False,
        # TODO calculate  # noqa
    )
    total_number_of_community_members = schema.Int(
        title=_(u'Total Number of Community Members'),
        required=False,
        # TODO calculate  # noqa
    )

    #######################################################
    model.fieldset(
        'program_dates_fieldset',
        label=_(u'Program Dates'),
        fields=['first_day_of_spring_semester_classes',
                'last_day_of_spring_semester_classes',
                'first_day_of_spring_interim_classes',
                'last_day_of_spring_interim_classes',
                'official_spring_graduation_date',
                'first_day_of_summer_i_classes',
                'last_day_of_summer_i_classes',
                'first_day_of_summer_ii_classes',
                'last_day_of_summer_ii_classes',
                'official_summer_graduation_date',
                'first_day_of_fall_semester_classes',
                'last_day_of_fall_semester_classes',
                'first_day_of_winter_interim_classes',
                'last_day_of_winter_interim_classes',
                'official_fall_graduation_date',
                'spring_interim_summer_fall_semester_participant_orientation_deadline',  # noqa
                'spring_interim_summer_fall_semester_in_person_orientation',
                'winter_interim_spring_semester_participant_orientation_deadline',  # noqa
                'winter_interim_spring_semester_in_person_orientation',
                'spring_interim_summer_fall_semester_payment_deadline_1',
                'spring_interim_payment_deadline_2',
                'summer_payment_deadline_2',
                'fall_semester_payment_deadline_2',
                'winter_interim_spring_payment_deadline_1',
                'winter_interim_spring_payment_deadline_2'],
    )

    first_day_of_spring_semester_classes = schema.Date(
        title=u'First day of Spring Semester Classes',
        description=u'will be copied from the selected calendar year on first save',  # noqa
        required=False,
    )

    last_day_of_spring_semester_classes = schema.Date(
        title=u'Last day of Spring Semester Classes',
        description=u'will be copied from the selected calendar year on first save',  # noqa
        required=False,
    )

    first_day_of_spring_interim_classes = schema.Date(
        title=u'First day of Spring Interim Classes',
        description=u'will be copied from the selected calendar year on first save',  # noqa
        required=False,
    )

    last_day_of_spring_interim_classes = schema.Date(
        title=u'Last day of Spring Interim Classes',
        description=u'will be copied from the selected calendar year on first save',  # noqa
        required=False,
    )

    official_spring_graduation_date = schema.Date(
        title=u'official spring graduation date',
        description=u'will be copied from the selected calendar year on first save',  # noqa
        required=False,
    )

    first_day_of_summer_i_classes = schema.Date(
        title=u'First day of Spring Interim Classes',
        description=u'will be copied from the selected calendar year on first save',  # noqa
        required=False,
    )

    last_day_of_summer_i_classes = schema.Date(
        title=u'Last day of Summer I Classes',
        description=u'will be copied from the selected calendar year on first save',  # noqa
        required=False,
    )

    first_day_of_summer_ii_classes = schema.Date(
        title=u'First day of Summer II Classes',
        description=u'will be copied from the selected calendar year on first save',  # noqa
        required=False,
    )

    last_day_of_summer_ii_classes = schema.Date(
        title=u'Last day of Summer II Classes',
        description=u'will be copied from the selected calendar year on first save',  # noqa
        required=False,
    )

    official_summer_graduation_date = schema.Date(
        title=u'Official Summer Graduation Date',
        description=u'will be copied from the selected calendar year on first save',  # noqa
        required=False,
    )

    first_day_of_fall_semester_classes = schema.Date(
        title=u'First day of Fall Semester Classes',
        description=u'will be copied from the selected calendar year on first save',  # noqa
        required=False,
    )

    last_day_of_fall_semester_classes = schema.Date(
        title=u'Last day of Fall Semester Classes',
        description=u'will be copied from the selected calendar year on first save',  # noqa
        required=False,
    )

    first_day_of_winter_interim_classes = schema.Date(
        title=u'First day of Winter Interim Classes',
        description=u'will be copied from the selected calendar year on first save',  # noqa
        required=False,
    )

    last_day_of_winter_interim_classes = schema.Date(
        title=u'Last day of Winter Interim Classes',
        description=u'will be copied from the selected calendar year on first save',  # noqa
        required=False,
    )

    official_fall_graduation_date = schema.Date(
        title=u'Official Fall Graduation Date',
        description=u'will be copied from the selected calendar year on first save',  # noqa
        required=False,
    )

    spring_interim_summer_fall_semester_participant_orientation_deadline = \
        schema.Datetime(
            title=u'Spring Interim, Summer & Fall Semester Participant Orientation Deadline',  # noqa
            description=u'will be copied from the selected calendar year on first save',  # noqa
            required=False,
        )

    spring_interim_summer_fall_semester_in_person_orientation = \
        schema.Datetime(
            title=u'Spring Interim, Summer & Fall Semester In-person Orientation',  # noqa
            description=u'will be copied from the selected calendar year on first save',  # noqa
            required=False,
        )

    winter_interim_spring_semester_participant_orientation_deadline = \
        schema.Datetime(
            title=u'Winter Interim & Spring Semester Participant Orientation Deadline',  # noqa
            description=u'will be copied from the selected calendar year on first save',  # noqa
            required=False,
        )

    winter_interim_spring_semester_in_person_orientation = schema.Datetime(
        title=u'Winter Interim & Spring Semester In-person Orientation',
        description=u'will be copied from the selected calendar year on first save',  # noqa
        required=False,
    )

    spring_interim_summer_fall_semester_payment_deadline_1 = schema.Date(
        title=u'Spring Interim, Summer & Fall Semester Payment Deadline 1',
        description=u'will be copied from the selected calendar year on first save',  # noqa
        required=False,
    )

    spring_interim_payment_deadline_2 = schema.Date(
        title=u'Spring Interim Payment Deadline 2',
        description=u'will be copied from the selected calendar year on first save',  # noqa
        required=False,
    )

    summer_payment_deadline_2 = schema.Date(
        title=u'Sunmmer Payment Deadline 2',
        description=u'will be copied from the selected calendar year on first save',  # noqa
        required=False,
    )

    fall_semester_payment_deadline_2 = schema.Date(
        title=u'Fall Semester Payment Deadline 2',
        description=u'will be copied from the selected calendar year on first save',  # noqa
        required=False,
    )

    winter_interim_spring_payment_deadline_1 = schema.Date(
        title=u'Winter Interim & Spring Semester Payment Deadline 1',
        description=u'will be copied from the selected calendar year on first save',  # noqa
        required=False,
    )

    winter_interim_spring_payment_deadline_2 = schema.Date(
        title=u'Winter Interim & Spring Semester Payment Deadline 2',
        description=u'will be copied from the selected calendar year on first save',  # noqa
        required=False,
    )


class TitleRequiredValidator(validator.SimpleFieldValidator):
    def validate(self, value):
        state = api.content.get_state(obj=self.context)
        if state == 'initial':
            if not value or not value.strip():
                raise Invalid(
                    _(
                        u'Title is required in state ''{0}'''.format(
                            state,
                        ),
                    ),
                )


validator.WidgetValidatorDiscriminators(TitleRequiredValidator,
                                        field=IOIEStudyAbroadProgram['title'])


class DescriptionRequiredValidator(validator.SimpleFieldValidator):
    def validate(self, value):
        state = api.content.get_state(obj=self.context)
        if state == 'initial':
            if not value or not value.strip():
                raise Invalid(
                    _(
                        u'Description is required in state ''{0}'''.format(
                            state,
                        ),
                    ),
                )


validator.WidgetValidatorDiscriminators(
    DescriptionRequiredValidator,
    field=IOIEStudyAbroadProgram['description'],
)
