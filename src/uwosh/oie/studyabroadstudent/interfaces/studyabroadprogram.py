# -*- coding: utf-8 -*-

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
    load_or_overload, replacement_costs, paid_by, rate_or_lump_sum, socialmediaservice, contactrelationship, \
    graduation_month_vocabulary, departure_transfer_vocabulary, departure_mode_transportation_vocabulary, \
    return_mode_transportation_vocabulary, return_transfer_vocabulary, program_cycle_vocabulary, \
    seat_assignment_protocol


class ILearningObjectiveRowSchema(Interface):
    learning_objective = schema.TextLine(title=u"Enter one objective per row. Click on the \'+\' to add a row.")


class IPreTravelDatesRowSchema(Interface):
    # pretravel_date = schema.Date(title=_(u'Date'))
    pretravel_start_datetime = schema.Datetime(title=_(u'Start'))
    # pretravel_start_time = schema.Time(title=_(u'Start Time'), vocabulary='uwosh.oie.studyabroadstudent.vocabularies.timeofday')
    # pretravel_end_time = schema.Time(title=_(u'End Time'), vocabulary='uwosh.oie.studyabroadstudent.vocabularies.timeofday')
    # pretravel_end_datetime = schema.DateTime(title=_(u'End Time'))
    pretravel_end_datetime = schema.Datetime(title=_(u'End'))
    pretravel_building = schema.Choice(title=_(u'Building'), vocabulary='uwosh.oie.studyabroadstudent.vocabularies.building')
    pretravel_room = schema.TextLine(title=_(u'Room'))
    pretravel_attendance_required = schema.Choice(title=_(u'Attendance Required?'), vocabulary=yes_no_na_vocabulary)


class ITravelDatesTransitionsDestinationsRowSchema(Interface):
    transitionDate = schema.Date(title=_(u'Transition Date'))
    destinationCity = schema.TextLine(title=_(u'Destination City'))
    destinationCountry = schema.Choice(title=_(u'Destination Country'), vocabulary='uwosh.oie.studyabroadstudent.vocabularies.countries')
    accommodation = schema.Choice(title=_(u'Accommodation'), vocabulary='uwosh.oie.studyabroadstudent.vocabularies.accommodation')
    # accommodationRoomSizes = schema.Choice(title=_(u'Room Size(s)'), vocabulary='uwosh.oie.studyabroadstudent.vocabularies.room_size')
    # TODO multi select widget doesn't respond to arrow clicks
    accommodationRoomSizes = schema.List(title=_(u'Room Size(s)'), value_type=schema.Choice(vocabulary='uwosh.oie.studyabroadstudent.vocabularies.room_size'))
    transitionType = schema.Choice(title=_(u'Transition Type'), vocabulary='uwosh.oie.studyabroadstudent.vocabularies.transition_type')


class IPostTravelClassDatesRowSchema(Interface):
    posttravel_start_datetime = schema.Datetime(title=_(u'Start'))
    posttravel_end_datetime = schema.Datetime(title=_(u'End'))
    posttravel_building = schema.Choice(title=_(u'Building'), vocabulary='uwosh.oie.studyabroadstudent.vocabularies.building')
    posttravel_room = schema.TextLine(title=_(u'Room'))
    posttravel_attendance_required = schema.Choice(title=_(u'Attendance Required?'), vocabulary=yes_no_na_vocabulary)


# class IApplicantQuestionsRowSchema(Interface):
#     question1 = schema.Text(title=_(u'Question 1'))
#     question2 = schema.Text(title=_(u'Question 2'))
#     question3 = schema.Text(title=_(u'Question 3'))
#     question4 = schema.Text(title=_(u'Question 4'))
#     question5 = schema.Text(title=_(u'Question 5'))


class ICoLeadersRowSchema(Interface):
    coleader = schema.Choice(title=_(u'On-site Program Co-leader'), vocabulary='uwosh.oie.studyabroadstudent.vocabularies.program_leader')


class ICourseRowSchema(Interface):
    course = schema.Choice(
        title=_(u'UW Oshkosh Course Subject & Number'),
        description=_(u'Add all courses associated with your program, including courses that will be taught partially at UW Oshkosh and partially while away on the program.  Do not include courses that will be taught entirely at UWO, even when these courses are offered in preparation for the program away.  Contact the OIE to add a course (abroad@uwosh.edu).'),
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.course'
    )
    credits_earned = schema.Int(
        title=_(u'UW Oshkosh Credits Earned'),
        description=_(u'Enter the number of credits that participants will earn for each individual course.  If you are offering a course that can be taught for a range of credits on your program (e.g. 3-5 credits), you must enter the course into this system multiple times, giving the course a different credit value each time that you enter it.')
    )
    class_start_date = schema.Date(
        title=_(u'Class Start Date')
        # TODO Auto-generate the first day of the term in which this program runs from the calendar?????  Maybe this isn't possible.
    )
    class_end_date = schema.Date(
        title=_(u'Class End Date')
        # TODO If the "PeopleSoft Class End Date" is AFTER the Official Graduation Date, prompt the coursebuilder to complete the "Course End Date Extension Form".
    )
    min_credits = schema.Int(
        title=_(u'Course Prerequisites: minimum number of credits'),
        description=_(u'If this course requires a minimum number of completed credits prior to the course start date, indicate this here'),
        min=0,
        max=999
    )
    gpa = schema.Int(
        title=_(u'Course Prerequisites: GPA'),
        description=_(u'If this course requires a minimum GPA prior to the course start date, indicate this here.'),
        min=0,
        max=999
    )
    completed_courses = schema.Text(
        title=_(u'Course Prerequisites: completed courses'),
        description=_(u'If this course requires that other courses be completed, or that a particular grade be earned in an earlier course, prior to the course start date, indicate this here.')
    )

class IOIEStudyAbroadProgram(Interface):

    title = schema.TextLine(
        title=_(u'Program Title'),
        description=_(u'The full Program Title will be displayed in all OIE print and on-line marketing and in all official OIE program-related materials.  To avoid confusion and increase "brand" awareness for your program, consistently use this program name in full, exactly as it appears here, in your print and electronic media.  Do not include country or city names in this field. (max length 45 chars)'),
        required=True,
        max_length=45,
    )

    description = RichText(
        title=_(u'Description'),
        description=_(u'This is the description that will be used to promote your program.  Your description should capture the purpose of your program, include an overview of what students will be engaged in while abroad/away, and capture students’ interest! (max length 600 chars)'),
        default_mime_type='text/plain',
        allowed_mime_types=('text/plain', 'text/html',),
        max_length=600,
        required=False,
    )

    #######################################################
    model.fieldset(
        'unorganized',
        label=_(u"Unorganized"),
        fields=[]
    )

    #######################################################
    model.fieldset(
        'comments_fieldset',
        label=_(u"Comments"),
        fields=['comments_all', 'comments_oie_leaders', 'comments_oie_all' ]
    )

    comments_all = schema.Text(
        title=_(u'Public Comments'),
        description=_(u'Comments entered here are visible by all system users.'),
        required=False,
    )

    comments_oie_leaders = schema.Text(
        title=_(u'Comments for OIE leadership'),
        description=_(u'Comments entered here are visible by the OIE Program Manager, Program Liaison, Program Leaders/Co-leaders and site administrators.'),
        required=False,
    )

    comments_oie_all = schema.Text(
        title=_(u'Comments for all OIE users'),
        description=_(u'Comments entered here are visible by all OIE professional staff.'),
        required=False,
    )

    #######################################################
    model.fieldset(
        'program_code_fieldset',
        label=_(u"Program Code"),
        fields=['calendar_year', 'term', 'college_or_unit', 'countries', 'program_code',]
    )

    calendar_year = schema.Choice(
        title=_(u'Calendar Year'),
        description=_(u'Use the year during which the program runs; this is not the year that is associated with the term of study.  For example, a January interim program running from Jan 2-28, 2017 will be associated with "2017".   A program running Dec 28, 2016-Jan 28, 2017 will also be associated with "2017".'),
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.calendar_year',
        required=True,
    )

    term = schema.Choice(
        title=_(u'Term'),
        description=_(u''),
        required=True,
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.term',
    )

    college_or_unit = schema.Choice(
        title=_(u'College or Unit'),
        description=_(u''),
        required=True,
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.college_or_unit',
    )

    countries = schema.List(
        title=_(u'Country or Countries'),
        description=_(u''),
        required=True,
        value_type=schema.Choice(vocabulary='uwosh.oie.studyabroadstudent.vocabularies.countries')
    )

    program_code = schema.TextLine(
        title=_(u'Program Code'),
        description=_(u'(auto-generated)'),
        required=True,
        default=_(u'will be auto-generated'),
        readonly=True
    )

    #######################################################
    model.fieldset(
        'academic_program_fieldset',
        label=_(u"Academic Program"),
        fields=['sponsoring_unit_or_department', 'program_type', 'program_component', 'title', 'description',
                'learning_objectives', 'equipment_and_space', 'equipment_and_space_needs', 'guest_lectures',
                'initial_draft_program_schedule', 'syllabus_and_supporting_docs', 'min_credits_earned',
                'max_credits_earned', 'language_of_study', 'cooperating_partners']
    )

    sponsoring_unit_or_department = schema.List(
        title=_(u'Sponsoring Unit or Department'),
        description=_(u'Select all that apply.'),
        required=True,
        value_type=schema.Choice(vocabulary='uwosh.oie.studyabroadstudent.vocabularies.sponsoring_unit_or_department'),
    )

    program_type = schema.Choice(
        title=_(u'Program Type'),
        required=True,
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.program_type',
    )

    program_component = schema.Choice(
        title=_(u'Program Component'),
        required=True,
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.program_component',
    )

    widget(
        'learning_objectives',
        DataGridFieldFactory,
    )
    learning_objectives = schema.List(
        title=_(u'Learning Objectives'),
        description=_(u'State the learning objectives for this program.  Include only one learning objective per text field. These learning objectives will be included in end-of-program assessment and may be used to support Higher Learning Commission and other accreditation processes.'),
        required=False,
        value_type=DictRow(title=u"learning objective row", schema=ILearningObjectiveRowSchema)
    )

    equipment_and_space = schema.Choice(
        title=_(u'Equipment & Space'),
        description=_(u''),
        required=True,
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.equipment_and_space',
    )

    equipment_and_space_needs = RichText(
        title=_(u'Equipment & Space details'),
        description=_(u'if needed'),
        required=False,
    )

    guest_lectures = schema.Choice(
        title=_(u'Guest Lectures'),
        description=_(u''),
        required=True,
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.guest_lectures',
    )

    initial_draft_program_schedule = field.NamedFile(
        title=_(u'Initial Draft Program Schedule'),
        description=_(u'Complete the OIE itinerary form and upload here.'),
        required=False,
    )

    syllabus_and_supporting_docs = field.NamedFile(
        title=_(u'Syllabus & Other Supporting Documents'),
        description=_(u'Upload your syllabus plus other related documents (if any).  If you update your syllabus, replace this copy with the updated copy.  This field will remain editable until just prior to travel.'),
        required=False,
    )

    min_credits_earned = schema.Choice(
        title=_(u'Minimum Number of Credits to be Earned by Each Applicant'),
        description=_(u''),
        required=False,
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.credits',
    )

    max_credits_earned = schema.Choice(
        title=_(u'Maximum Number of Credits to be Earned by Each Applicant'),
        description=_(u''),
        required=False,
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.credits',
    )

    language_of_study = schema.List(
        title=_(u'Language of Study'),
        description=_(u'Select all that apply. Contact the Office of International Education to add a language (abroad@uwosh.edu).'),
        required=True,
        value_type=schema.Choice(vocabulary='uwosh.oie.studyabroadstudent.vocabularies.language'),
    )

    cooperating_partners = schema.List(
        title=_(u'Cooperating Partners'),
        description=_(u''),
        required=False,
        value_type=schema.Choice(vocabulary='uwosh.oie.studyabroadstudent.vocabularies.cooperatingpartner')
    )

    #######################################################
    model.fieldset(
        'dates_destinations',
        label=_(u"Dates and Destinations"),
        fields=['program_cycle', 'pretravel_dates'],
    ),

    program_cycle = schema.Choice(
        title=_(u'Program Cycle'),
        description=_(u'How often will this program be offered?  This information will display in some marketing materials.  If it isn''t possible to predict, leave this blank.'),
        vocabulary=program_cycle_vocabulary,
    )

    widget(
        'pretravel_dates',
        DataGridFieldFactory,
    )

    pretravel_dates = schema.List(
        title=_(u'Pre-Travel Class & Orientation Dates'),
        description=_(u'Students expect to meet group members and their program leader or program advisor in a formal group setting at least once prior to travel.  Check with your department chair and/or College administration on pre-travel requirements specific to your unit. Students are expected to ensure, prior to confirming participation on a study abroad/away program, that they have no other obligations during your pre-travel class dates.  Students with obligations during one or more dates/times must disclose this on their application and must have the approval of the Program Liaison to participate before the OIE will place the student on the program.  For this reason, after we advertise these dates to students as mandatory, the dates shouldn''t be changed!'),
        required=False,
        value_type=DictRow(title=u"Pre-Travel Dates", schema=IPreTravelDatesRowSchema)
    )

    #######################################################
    # TODO Applicant should not see this field during the "Initial" state.  Can this be made visible AFTER transitioning from this state?
    #
    model.fieldset(
        'DeparturefromOshkosh',
        label=_(u'Departure from Oshkosh'),
        fields=['transportationFromOshkoshToDepartureAirport', 'oshkoshDepartureLocation', 'oshkoshMeetingDateTime',
                'oshkoshDepartureDateTime', 'milwaukeeDepartureDateTime', 'airportArrivalDateTime']
    )

    transportationFromOshkoshToDepartureAirport = schema.Choice(
        title=_(u'Transportation from Oshkosh to departure airport'),
        vocabulary=yes_no_none_vocabulary,
    )

    oshkoshDepartureLocation = schema.Choice(
        title=_('Oshkosh Departure Location'),
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.departure_location',
        # TODO dropdown  [display only if "Transportation from Oshkosh to departure airport is "yes"]
    )

    oshkoshMeetingDateTime = schema.Datetime(
        title=_(u'Oshkosh Meeting Date & Time'),
        # TODO =departure flight date/time minus 7.75 hours [display only if "Transportation from Oshkosh to departure airport is "yes"]
    )

    oshkoshDepartureDateTime = schema.Datetime(
        title=_(u'Oshkosh Departure Date & Time'),
        # TODO [display only if "Transportation from Oshkosh to departure airport is "yes"]
    )

    milwaukeeDepartureDateTime = schema.Datetime(
        title=_('Milwaukee Departure Date & Time'),
        # TODO [display only if "Transportation from Milwaukee to departure airport is "yes"]
    )

    airportArrivalDateTime = schema.Datetime(
        title=_('Airport Arrival Date & Time'),
        # TODO '=departure flight date/time minus 3.5 hours [display only if "Transportation from Oshkosh to departure airport is "yes"]
    )

    #######################################################
    # TODO Applicant should not see this field during the "Initial" state.  Can this be made visible AFTER transitioning from this state?
    #
    model.fieldset(
        'Departure Flight',
        label=_('Departure Flight'),
        fields=['airline', 'flightNumber', 'airport', 'departureDateTime', 'arrivalAtDestinationAndInsuranceStartDate',
                'travelDatesTransitionsAndDestinations', 'firstChoiceDatesFlexible', 'postTravelClassDates']
    )

    airline = schema.Choice(
        title=_(u'Airline'),
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.airline'
    )

    flightNumber = schema.TextLine(
        title=_(u'Flight Number'),
    )

    airport = schema.Choice(
        title=_(u'Airport'),
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.airport'
    )

    departureDateTime = schema.Datetime(
        title=_(u'Departure Date and Time'),
    )

    arrivalAtDestinationAndInsuranceStartDate = schema.Datetime(
        title=_(u'Arrival at Destination & Insurance Start Date')
    )

    widget('travelDatesTransitionsAndDestinations', DataGridFieldFactory)
    travelDatesTransitionsAndDestinations = schema.List(
        title=_(u'Travel Dates, Transitions & Destinations'),
        value_type=DictRow(title=u"learning objective row", schema=ITravelDatesTransitionsDestinationsRowSchema)
    )

    firstChoiceDatesFlexible = schema.Choice(
        title=_(u'Are your first-choice dates flexible?'),
        description=_(u'If yes, your OIE Program Manager will meet with you to discuss transition dates'),
        vocabulary=yes_no_none_vocabulary
    )

    widget('postTravelClassDates', DataGridFieldFactory)
    postTravelClassDates = schema.List(
        title=_(u'Post-travel Class Dates'),
        description=_(u'Participants are expected to ensure, prior to confirming participation on a study abroad/away program, that they have no other obligations during your post-travel class dates.  Participants with obligations during one or more dates/times must disclose this on their application and must have the approval of the Program Liaison to participate before the OIE will place the participant on the program.  For this reason, after we advertise these dates to participants as mandatory, the dates shouldn’t be changed!'),
        value_type=DictRow(title=u'Post-travel Class Dates', schema=IPostTravelClassDatesRowSchema)
    )

    #######################################################
    # TODO Applicant should not see this field during the "Initial" state.  Can this be made visible AFTER transitioning from this state?
    #
    model.fieldset(
        'Return Flight',
        label=_('Return Flight'),
        fields=['airlineReturn', 'flightNumberReturn', 'airportReturn', 'returnDateTime', 'arrivalInWisconsinDate',
                'insuranceEndDate',]
    )

    airlineReturn = schema.Choice(
        title=_(u'Airline'),
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.airline'
    )

    flightNumberReturn = schema.TextLine(
        title=_(u'Flight Number'),
    )

    airportReturn = schema.Choice(
        title=_(u'Airport'),
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.airport'
    )

    returnDateTime = schema.Datetime(
        title=_(u'Return Date and Time'),
    )

    arrivalInWisconsinDate = schema.Datetime(
        title=_(u'Arrival in Wisconsin')
    )

    insuranceEndDate = schema.Datetime(
        title=_(u'Insurance End Date')
    )

    #######################################################
    # TODO Applicant should not see this field during the "Initial" state.  Can this be made visible AFTER transitioning from this state?
    #
    model.fieldset(
        'Return to Oshkosh',
        label=_(u'Return to Oshkosh'),
        fields=['transportationFromArrivalAirportToOshkosh', 'milwaukeeArrivalDateTime', 'oshkoshArrivalDateTime']
    )

    transportationFromArrivalAirportToOshkosh = schema.Choice(
        title=_(u'Transportation from arrival airport to Oshkosh'),
        vocabulary=yes_no_none_vocabulary,
    )

    milwaukeeArrivalDateTime = schema.Datetime(
        title=_('Milwaukee Arrival Date & Time'),
        # TODO '=arrival flight date/time plus 2.5 hours [display only if "Transportation from Arrival airport to Oshkosh is "yes"]
    )

    oshkoshArrivalDateTime = schema.Datetime(
    title=_(u'Oshkosh Arrival Date & Time'),
        # TODO '=arrival flight date/time plus 4 hours [display only if "Transportation from Arrival airport to Oshkosh is "yes"]
    )

    #######################################################
    model.fieldset(
        'Participant Selection',
        label=_(u"Participant Selection"),
        fields=['studentStatus', 'seatAssignmentProtocol', 'liaisonReviewOfIndividualApplicants', 'approvalCriteria',
                'individualInterview', 'firstRecommendationRequired', 'secondRecommendationRequired',
                'applicantQuestion1', 'applicantQuestion2', 'applicantQuestion3', 'applicantQuestion4',
                'applicantQuestion5', 'cvRequired', 'letterOfMotivationRequired'],
    ),

    studentStatus = schema.Choice(
        title=_(u'Student Status'),
        description=_(u'Choose one'),
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.student_status',
    )

    seatAssignmentProtocol = schema.Choice(
        title=_(u'Seat Assignment Protocol'),
        vocabulary=seat_assignment_protocol,
    )

    liaisonReviewOfIndividualApplicants = schema.Choice(
        title=_(u'Liaison Review of Individual Applicants'),
        description=_(u'For competitive programs or for progarms that require each applicant to have specific background in addition to meeting course pre-requisites, indicate criteria to be used and select the method or methods to be employed to determine whether criteria have been met.  Do not include or duplicate course pre-requisites here.'),
        vocabulary=yes_no_none_vocabulary,
    )

    approvalCriteria = schema.Text(
        title=_(u'Criteria to be used in the approval process include the following'),
    )

    individualInterview = schema.Choice(
        title=_(u'The Program Liaison, Program Leader or Program Co-leader will interview each applicant'),
        vocabulary=yes_no_none_vocabulary,
        # TODO yes/no (default=no if text box above is filled in; this question should be unavailable/greyed out if the text box above is not filled in)
    )

    firstRecommendationRequired = schema.Choice(
        title=_(u'1st Recommendation is required'),
        description=_(u'If "yes", this item appears in the Applicant Portal as an application item'),
        vocabulary=yes_no_na_vocabulary
        # TODO yes/no (default=no if text box above is filled in; this question should be unavailable/greyed out if the text box above is not filled in)
    )

    secondRecommendationRequired = schema.Choice(
        title=_(u'2nd Recommendation is required'),
        description=_(u'If "yes", this item appears in the Applicant Portal as an application item'),
        vocabulary=yes_no_na_vocabulary
        # TODO "yes/no (default=no if text box above is filled in; this question should be unavailable/greyed out if the text box above is not filled in). This cannot be ""yes"" if ""A 1st Recommendation is required"" is ""no""."
    )

    # widget('applicantQuestions', DataGridFieldFactory)
    # applicantQuestions = schema.List(
    #     title=_(u'All applicants must respond to these questions'),
    #     description = _(u'Type one question per text box.  These questions will be required of all applicants.  Questions cannot be made optional and cannot be applied to some applicants and not to others.'),
    #     value_type = DictRow(title=u'applicantQuestions', schema=IApplicantQuestionsRowSchema),
    # )

    applicantQuestion1 = schema.Text(
        title=_(u'All applicants must respond to this question 1'),
        description = _(u'These questions will be required of all applicants.  Questions cannot be made optional and cannot be applied to some applicants and not to others.'),
    )

    applicantQuestion2 = schema.Text(
        title=_(u'All applicants must respond to this question 2'),
        description = _(u'These questions will be required of all applicants.  Questions cannot be made optional and cannot be applied to some applicants and not to others.'),
    )

    applicantQuestion3 = schema.Text(
        title=_(u'All applicants must respond to this question 3'),
        description = _(u'These questions will be required of all applicants.  Questions cannot be made optional and cannot be applied to some applicants and not to others.'),
    )

    applicantQuestion4 = schema.Text(
        title=_(u'All applicants must respond to this question 4'),
        description = _(u'These questions will be required of all applicants.  Questions cannot be made optional and cannot be applied to some applicants and not to others.'),
    )

    applicantQuestion5 = schema.Text(
        title=_(u'All applicants must respond to this question 5'),
        description = _(u'These questions will be required of all applicants.  Questions cannot be made optional and cannot be applied to some applicants and not to others.'),
    )

    cvRequired = schema.Choice(
        title=_(u'CV Required'),
        description=_(u'Complete this in English if studying in English; complete this in German if studying in German'),
        vocabulary=yes_no_na_vocabulary
        # TODO yes/no (default=no if text box above is filled in; this question should be unavailable/greyed out if the text box above is not filled in)
    )

    letterOfMotivationRequired = schema.Choice(
        title=_(u'Letter of Motivation Required'),
        description=_(u'This must be typed'),
        vocabulary=yes_no_na_vocabulary
        # TODO yes/no (default=no if text box above is filled in; this question should be unavailable/greyed out if the text box above is not filled in)
    )

    otherRequired = schema.Text(
        title=_(u'Other Requirement(s)'),
        # TODO "this question should be unavailable/greyed out if the text box above is not filled in"
    )

    #######################################################
    model.fieldset(
        'Liaison & Leadership',
        label=_(u"Liaison & Leadership"),
        fields=['liaison', 'program_leader', 'program_coleaders'],
    )
    liaison = schema.Choice(
        title=_(u'Program Liaison to the OIE'),
        description=_(u'The Liaison to the OIE communicates decisions related to program development and delivery to the Program Manager in the OIE and communicates program changes and updates to his/her unit administration. There is only one Liaison per program;  all decision-making at the unit level must be communicated to the OIE through the designated liaison. The Liaison may also include the OIE Program Manager and/or other OIE staff in conversations or seek input when appropriate. The Liaison may also serve as the On-site Program Leader and may also teach one or more of the program courses.'),
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.liaison',
    )
    program_leader = schema.Choice(
        title=_(u'On-site Program Leader'),
        description=_(u'The On-site Program Leader is responsible for providing leadership for the group and for overseeing group health and safety.  The On-site Program Leader may also teach one or more of the program courses.'),
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.program_leader',
    )
    widget('program_coleaders', DataGridFieldFactory)
    program_coleaders = schema.List(
        title=_(u'On-site Program Leader (choose 0-4)'),
        description=_(u'The On-site Program Leader is responsible for providing leadership for the group and for overseeing group health and safety.  The On-site Program Leader may also teach one or more of the program courses.'),
        value_type=DictRow(title=u"co-leaders", schema=ICoLeadersRowSchema),
        required=False,
    )

    #######################################################
    model.fieldset(
        'Courses',
        label=_(u"Courses"),
        fields=[],
    )
    widget('courses', DataGridFieldFactory)
    courses = schema.List(
        title=_(u'Courses'),
        description=_(u'List existing courses only.  If the course you intend to use is not an existing course, your department must submit the course for formal approval through normal university channels prior to applying to use the course abroad/away.  UW Oshkosh Curriculum Policies and Procedures do not allow the use of a contractual course, i.e. independent study or related readings, for an organized, off-campus course.'),
        value_type=DictRow(title=u'Course', schema=ICourseRowSchema),
    )

    #######################################################
    model.fieldset(
        'program_dates_fieldset',
        label=_(u"Program Dates"),
        fields=['first_day_of_spring_semester_classes', 'last_day_of_spring_semester_classes',
              'first_day_of_spring_interim_classes', 'last_day_of_spring_interim_classes',
              'official_spring_graduation_date', 'first_day_of_summer_i_classes', 'last_day_of_summer_i_classes',
              'first_day_of_summer_ii_classes', 'last_day_of_summer_ii_classes',
              'official_summer_graduation_date', 'first_day_of_fall_semester_classes',
              'last_day_of_fall_semester_classes', 'first_day_of_winter_interim_classes',
              'last_day_of_winter_interim_classes', 'official_fall_graduation_date',
              'spring_interim_summer_fall_semester_participant_orientation_deadline',
              'spring_interim_summer_fall_semester_in_person_orientation',
              'winter_interim_spring_semester_participant_orientation_deadline',
              'winter_interim_spring_semester_in_person_orientation',
              'spring_interim_summer_fall_semester_payment_deadline_1', 'spring_interim_payment_deadline_2',
              'sunmmer_payment_deadline_2', 'fall_semester_payment_deadline_2',
              'winter_interim_spring_payment_deadline_1', 'winter_interim_spring_payment_deadline_2']
    )

    first_day_of_spring_semester_classes = schema.Date(
        title=u'First day of Spring Semester Classes',
        required=False,
        default=date(2017, 01, 01),
    )

    last_day_of_spring_semester_classes = schema.Date(
        title=u'Last day of Spring Semester Classes',
        required=False,
        default=date(2017, 01, 01),
    )

    first_day_of_spring_interim_classes = schema.Date(
        title=u'First day of Spring Interim Classes',
        required=False,
        default=date(2017, 01, 01),
    )

    last_day_of_spring_interim_classes = schema.Date(
        title=u'Last day of Spring Interim Classes',
        required=False,
        default=date(2017, 01, 01),
    )

    official_spring_graduation_date = schema.Date(
        title=u'official spring graduation date',
        required=False,
        default=date(2017, 01, 01),
    )

    first_day_of_summer_i_classes = schema.Date(
        title=u'First day of Spring Interim Classes',
        required=False,
        default=date(2017, 01, 01),
    )

    last_day_of_summer_i_classes = schema.Date(
        title=u'Last day of Summer I Classes',
        required=False,
        default=date(2017, 01, 01),
    )

    first_day_of_summer_ii_classes = schema.Date(
        title=u'First day of Summer II Classes',
        required=False,
        default=date(2017, 01, 01),
    )

    last_day_of_summer_ii_classes = schema.Date(
        title=u'Last day of Summer II Classes',
        required=False,
        default=date(2017, 01, 01),
    )

    official_summer_graduation_date = schema.Date(
        title=u'Official Summer Graduation Date',
        required=False,
        default=date(2017, 01, 01),
    )

    first_day_of_fall_semester_classes = schema.Date(
        title=u'First day of Fall Semester Classes',
        required=False,
        default=date(2017, 01, 01),
    )

    last_day_of_fall_semester_classes = schema.Date(
        title=u'Last day of Fall Semester Classes',
        required=False,
        default=date(2017, 01, 01),
    )

    first_day_of_winter_interim_classes = schema.Date(
        title=u'First day of Winter Interim Classes',
        required=False,
        default=date(2017, 01, 01),
    )

    last_day_of_winter_interim_classes = schema.Date(
        title=u'Last day of Winter Interim Classes',
        required=False,
        default=date(2017, 01, 01),
    )

    official_fall_graduation_date = schema.Date(
        title=u'Official Fall Graduation Date',
        required=False,
        default=date(2017, 01, 01),
    )

    spring_interim_summer_fall_semester_participant_orientation_deadline = schema.Date(
        title=u'Spring Interim, Summer & Fall Semester Participant Orientation Deadline',
        required=False,
        default=date(2017, 01, 01),
    )

    spring_interim_summer_fall_semester_in_person_orientation = schema.Date(
        title=u'Spring Interim, Summer & Fall Semester In-person Orientation',
        required=False,
        default=date(2017, 01, 01),
    )

    winter_interim_spring_semester_participant_orientation_deadline = schema.Date(
        title=u'Winter Interim & Spring Semester Participant Orientation Deadline',
        required=False,
        default=date(2017, 01, 01),
    )

    winter_interim_spring_semester_in_person_orientation = schema.Date(
        title=u'Winter Interim & Spring Semester In-person Orientation',
        required=False,
        default=date(2017, 01, 01),
    )

    spring_interim_summer_fall_semester_payment_deadline_1 = schema.Date(
        title=u'Spring Interim, Summer & Fall Semester Payment Deadline 1',
        required=False,
        default=date(2017, 01, 01),
    )

    spring_interim_payment_deadline_2 = schema.Date(
        title=u'Spring Interim Payment Deadline 2',
        required=False,
        default=date(2017, 01, 01),
    )

    sunmmer_payment_deadline_2 = schema.Date(
        title=u'Sunmmer Payment Deadline 2',
        required=False,
        default=date(2017, 01, 01),
    )

    fall_semester_payment_deadline_2 = schema.Date(
        title=u'Fall Semester Payment Deadline 2',
        required=False,
        default=date(2017, 01, 01),
    )

    winter_interim_spring_payment_deadline_1 = schema.Date(
        title=u'Winter Interim & Spring Semester Payment Deadline 1',
        required=False,
        default=date(2017, 01, 01),
    )

    winter_interim_spring_payment_deadline_2 = schema.Date(
        title=u'Winter Interim & Spring Semester Payment Deadline 2',
        required=False,
        default=date(2017, 01, 01),
    )



#"Syllabus & Other Supporting Documents
#Upload your syllabus plus other related documents (if any).  If you update your syllabus, replace this copy with the updated copy.  This field will remain editable until just prior to travel."
#"Number of Credits to be Earned by Each Applicant
#Minimum
#Maximum"
#"Language of Study
#Select all that apply.  Contact the Office of International Education to add a language (abroad@uwosh.edu)."
#"Cooperating Partners
#Only entities listed on the UW System Preferred Provider List or academic institutions with a current affiliation agreement with UWO may be selected here.  All other cooperating partners must be selected by following UW System procurement policies."

class IOIEStudyAbroadParticipant(Interface):

    dexteritytextindexer.searchable('title')
    title = schema.TextLine(
        title=_(u'Title'),
        required=True,
        readonly=True,
        default=_(u'will be auto-generated'),
    )

    #######################################################
    model.fieldset(
        'progress',
        label=_(u"Progress"),
        fields=['seatNumber', 'waitlistNumber' ]
    )

    seatNumber = schema.TextLine(
        title=_(u'Seat Number'),
        required=False,
    )

    waitlistNumber = schema.TextLine(
        title=_(u'Waitlist Number'),
        required=False,
    )

    #######################################################
    model.fieldset(
        'interest',
        label=_(u"Express Interest"),
        fields=['email', 'programName', 'programName2', 'programName3' ]
    )

    dexteritytextindexer.searchable('email')
    email = schema.TextLine(
        title=_(u'Email Address'),
        description=_(u'UW Oshkosh students must use a @uwosh.edu email address.  Acceptable email addresses for other applicants include school and company addresses.'),
        required=True,
    )

    dexteritytextindexer.searchable('programName')
    programName = schema.Choice(
        title=_(u'Program Name (first choice)'),
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.newprograms',
        required=True,
    )


    dexteritytextindexer.searchable('programName2')
    programName2 = schema.Choice(
        title=_(u'Program Name (second choice)'),
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.newprograms',
        required=False,
    )

    dexteritytextindexer.searchable('programName3')
    programName3 = schema.Choice(
        title=_(u'Program Name (third choice)'),
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.newprograms',
        required=False,
    )

    #######################################################
    model.fieldset(
        'step1',
        label=_(u"Step 1"),
        fields=['studentId' ]
    )

    dexteritytextindexer.searchable('studentID')
    studentID = schema.TextLine(
        title=_(u'UW Oshkosh Student ID'),
        description=_(u'(if applicable)'),
        required=False,
    )

    #######################################################
    model.fieldset(
        'contact',
        label=_(u"Contact Information"),
        fields=['mainPhone', 'otherPhone', 'otherContactService', 'otherContactID', 'localAddr',
                'localAddrApt', 'localCity', 'localState', 'localZip', 'homeAddr1', 'homeAddrApt',
                'homeCity', 'homeState', 'homeZip', 'homeCountry', ]
    )

    mainPhone = schema.TextLine(
        title=_(u'Main phone'),
        description=_(u'Please include country code (if outside US) and area code'),
        required=True,
    )

    otherPhone = schema.TextLine(
        title=_(u'Other phone'),
        description=_(u'Please include country code (if outside US) and area code'),
        required=False,
    )

    otherContactService = schema.Choice(
        title=_(u'Other contact service'),
        description=_(u'Please choose one'),
        required=False,
        vocabulary=socialmediaservice,
    )

    otherContactID = schema.TextLine(
        title=_(u'Other contact service username or ID'),
        description=_(u'Please enter your username or ID on the service you chose above'),
        required=False,
    )

    localAddr = schema.TextLine(
        title=_(u'Local Address'),
        required=True,
    )

    localAddrApt = schema.TextLine(
        title=_(u'Local Address Apartment Number'),
        required=False,
    )

    localCity = schema.TextLine(
        title=_(u'Local City'),
        required=True,
    )

    localState = schema.TextLine(
        title=_(u'Local State'),
        default=_(u'WI'),
        required=True,
    )

    localZip = schema.TextLine(
        title=_(u'Local Zip Code'),
        default=_(u'54901'),
        required=True,
    )

    homeAddr1 = schema.TextLine(
        title=_(u'Home Address'),
        required=True,
    )

    homeAddrApt = schema.TextLine(
        title=_(u'Home Address Apartment Number'),
        required=False,
    )

    homeCity = schema.TextLine(
        title=_(u'Home City'),
        description=_(u''),
        required=True,
    )

    homeState = schema.TextLine(
        title=_(u'Home State'),
        description=_(u''),
        required=True,
    )

    homeZip = schema.TextLine(
        title=_(u'Home Zip Code'),
        description=_(u''),
        required=True,
    )

    homeCountry = schema.TextLine(
        title=_(u'Home Country'),
        required=True,
    )

    #######################################################
    model.fieldset(
        'emergency_contact',
        label=_(u"Emergency Contact"),
        fields=['emerg1fullname', 'emerg1relationship', 'emerg1mail_personal',
                'emerg1mail_work', 'emerg1phone_main', 'emerg1phone_other',
                'emerg2fullname', 'emerg2relationship', 'emerg2mail_personal',
                'emerg2mail_work', 'emerg2phone_main', 'emerg2phone_other',
                'emerg3fullname', 'emerg3relationship', 'emerg3mail_personal',
                'emerg3mail_work', 'emerg3phone_main', 'emerg3phone_other',
                'emerg4fullname', 'emerg4relationship', 'emerg4mail_personal',
                'emerg4mail_work', 'emerg4phone_main', 'emerg4phone_other',
                ]
    )

    emerg1fullname = schema.TextLine(
        title=_(u'Emergency Contact 1 Full Name'),
        #        required=True,
        required=False,
    )

    emerg1relationship = schema.Choice(
        title=_(u'Emergency Contact 1 Relationship to You'),
        required=False,
        vocabulary=contactrelationship,
    )

    emerg1mail_personal = schema.TextLine(
        title=_(u'Emergency Contact 1 Personal Email'),
        description=_(u'Strongly recommended'),
        required=False,
        # write_permission="UWOshOIE: Modify revisable fields",
    )

    emerg1mail_work = schema.TextLine(
        title=_(u'Emergency Contact 1 Work Email'),
        description=_(u'Strongly recommended'),
        required=False,
        # write_permission="UWOshOIE: Modify revisable fields",
    )

    emerg1phone_main = schema.TextLine(
        title=_(u'Emergency Contact 1 Main Phone'),
        description=_(u'Please include country code (if outside US) and area code'),
        #        required=True,
        required=False,
    )

    emerg1phone_other = schema.TextLine(
        title=_(u'Emergency Contact 1 Other Phone'),
        description=_(u'Please include country code (if outside US) and area code'),
        #        required=True,
        required=False,
    )

    ###############

    emerg2fullname = schema.TextLine(
        title=_(u'Emergency Contact 2 Full Name'),
        #        required=True,
        required=False,
    )

    emerg2relationship = schema.Choice(
        title=_(u'Emergency Contact 2 Relationship to You'),
        required=False,
        vocabulary=contactrelationship,
    )

    emerg2mail_personal = schema.TextLine(
        title=_(u'Emergency Contact 2 Personal Email'),
        description=_(u'Strongly recommended'),
        required=False,
        # write_permission="UWOshOIE: Modify revisable fields",
    )

    emerg2mail_work = schema.TextLine(
        title=_(u'Emergency Contact 2 Work Email'),
        description=_(u'Strongly recommended'),
        required=False,
        # write_permission="UWOshOIE: Modify revisable fields",
    )

    emerg2phone_main = schema.TextLine(
        title=_(u'Emergency Contact 2 Main Phone'),
        description=_(u'Please include country code (if outside US) and area code'),
        #        required=True,
        required=False,
    )

    emerg2phone_other = schema.TextLine(
        title=_(u'Emergency Contact 2 Other Phone'),
        description=_(u'Please include country code (if outside US) and area code'),
        #        required=True,
        required=False,
    )

    #############

    emerg3fullname = schema.TextLine(
        title=_(u'Emergency Contact 3 Full Name'),
        #        required=True,
        required=False,
    )

    emerg3relationship = schema.Choice(
        title=_(u'Emergency Contact 3 Relationship to You'),
        required=False,
        vocabulary=contactrelationship,
    )

    emerg3mail_personal = schema.TextLine(
        title=_(u'Emergency Contact 3 Personal Email'),
        description=_(u'Strongly recommended'),
        required=False,
        # write_permission="UWOshOIE: Modify revisable fields",
    )

    emerg3mail_work = schema.TextLine(
        title=_(u'Emergency Contact 3 Work Email'),
        description=_(u'Strongly recommended'),
        required=False,
        # write_permission="UWOshOIE: Modify revisable fields",
    )

    emerg3phone_main = schema.TextLine(
        title=_(u'Emergency Contact 3 Main Phone'),
        description=_(u'Please include country code (if outside US) and area code'),
        #        required=True,
        required=False,
    )

    emerg3phone_other = schema.TextLine(
        title=_(u'Emergency Contact 3 Other Phone'),
        description=_(u'Please include country code (if outside US) and area code'),
        #        required=True,
        required=False,
    )

    #############

    emerg4fullname = schema.TextLine(
        title=_(u'Emergency Contact 4 Full Name'),
        #        required=True,
        required=False,
    )

    emerg4relationship = schema.Choice(
        title=_(u'Emergency Contact 4 Relationship to You'),
        required=False,
        vocabulary=contactrelationship,
    )

    emerg4mail_personal = schema.TextLine(
        title=_(u'Emergency Contact 4 Personal Email'),
        description=_(u'Strongly recommended'),
        required=False,
        # write_permission="UWOshOIE: Modify revisable fields",
    )

    emerg4mail_work = schema.TextLine(
        title=_(u'Emergency Contact 4 Work Email'),
        description=_(u'Strongly recommended'),
        required=False,
        # write_permission="UWOshOIE: Modify revisable fields",
    )

    emerg4phone_main = schema.TextLine(
        title=_(u'Emergency Contact 4 Main Phone'),
        description=_(u'Please include country code (if outside US) and area code'),
        #        required=True,
        required=False,
    )

    emerg4phone_other = schema.TextLine(
        title=_(u'Emergency Contact 4 Other Phone'),
        description=_(u'Please include country code (if outside US) and area code'),
        #        required=True,
        required=False,
    )

    #######################################################
    model.fieldset(
        'demographics',
        label=_(u"Demographics"),
        fields=['stateResidency', 'countrycitizenship', 'immigrationStatus', 'countryBirth',
                'ethnicity', 'ethnicityOther', ]
    )

    stateResidency = schema.Choice(
        title=_(u'State Residency'),
        description=_(u''),
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.us_states_territories',
        required=True,
    )

    countrycitizenship = schema.Choice(
        title=_(u'Country of Citizenship'),
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.countries',
        required=True,
    )

    immigrationStatus = schema.Choice(
        title=_(u'Immigration Status'),
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.immigrationstatus',
        required=True,
    )

    countryBirth = schema.Choice(
        title=_(u'Country of Birth'),
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.countries',
        required=True,
    )

    ethnicity = schema.Choice(
        title=_(u'Ethnicity'),
        description=_(u''),
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.ethnicities',
        required=False,
    )

    ethnicityOther = schema.TextLine(
        title=_(u'Other Ethnicity'),
        description=_(u'Enter ethnicity if you selected Other'),
        required=False,
    )

    #######################################################
    model.fieldset(
        'education',
        label=_(u"Education"),
        fields=['educationLevel', 'universityEnrolledUWO', 'universityEnrolledOther', 'cumulativeGPA',
                'major1', 'major2', 'minor1', 'minor2', 'graduationYear', 'graduationMonth']
    )

    educationLevel = schema.Choice(
        title=_(u'Education Level'),
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.education_level',
        required=False,
    )

    universityEnrolledUWO = schema.Choice(
        title=_(u'Are you enrolled at UW Oshkosh?'),
        description=_(u''),
        required=True,
        vocabulary=yes_no_none_vocabulary,
    )

    universityEnrolledOther = schema.TextLine(
        title=_(u'Name of other university'),
        description=_(u'No abbreviations please'),
        required=False,
    )

    cumulativeGPA = schema.Float(
        title=_(u'Cumulative GPA'),
        description=_(u'out of 4.0 (use 0.0 if not a student)'),
        required=False,
    )

    major1 = schema.Choice(
        title=_(u'First Major'),
        required=False,
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.majors',
    )

    major2 = schema.Choice(
        title=_(u'Second Major'),
        required=False,
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.majors',
    )

    minor1 = schema.TextLine(
        title=_(u'Minor 1'),
        required=False,
    )

    minor2 = schema.TextLine(
        title=_(u'Minor 2'),
        required=False,
    )

    # graduationYear = schema.Choice(
    #     title=_(u'Expected Graduation Year'),
    #     description=_(u''),
    #     required=False,
    #     vocabulary='uwosh.oie.studyabroadstudent.vocabularies.calendar_year',
    # )

    graduationYear = schema.Int(
        title=_(u'Expected Graduation Year'),
        description=_(u'enter the full 4-digit year'),
        min=2018,
        max=2100,
        required=False,
    )

    graduationMonth = schema.Choice(
        title=_(u'Expected Graduation Month'),
        vocabulary=graduation_month_vocabulary,
        required=False,
    )

    #######################################################
    model.fieldset(
        'courses',
        label=_(u"Courses"),
        fields=['courses']
    )

    courses = schema.List(
        title=_(u'Course Selection'),
        description=_(u'Request enrollment in these courses'),
        value_type=schema.Choice(vocabulary='uwosh.oie.studyabroadstudent.vocabularies.course')
    )

    #######################################################
    model.fieldset(
        'date',
        label=_(u"Dates"),
        fields=['interviewDate', 'orientationDeadline', 'prePostTravelClassDates', 'paymentDeadlines',
                'programDepartureDate', 'airportTransferDeparture', 'departureModeOfTransportation',
                'programReturnDate', 'returnModeOfTransportation', 'airportTransferReturn',
                'requestToDeviateFromProgramDates']
    )

    interviewDate= schema.Date(
        title=_(u'Interview Date'),
        description=_(u'Applicants to this program must contact the Program Leader to schedule an interview. Your interview date may or may not need to occur prior to the STEP II application deadline. You must make your interview appointment prior to submiiting this application. Indicate your interview date here. (For some programs, students choose from a list of dates/times/locations.  For others, they set this up with an individual and report this to OIE. Most programs, however, don''t require an interview).'),
        required=False,
    )

    orientationDeadline = schema.Choice(
        title=_(u'I have read the statement below and understand.'),
        description=_(u'I understand that the Office of International Education Orientation deadline is (DATE from PROGRAM WORKFLOW SHOULD APPEAR HERE).  I understand that all Office of International Education orientation requirements must be completed by this date.  If not completed by this date, I understand that the Office of International Education will begin the process of removing me from my program and that the Withdrawal & Refund Policy will apply. '),
        vocabulary=yes_no_none_vocabulary,
        required=True,
        # TODO insert date from program object
    )

    prePostTravelClassDates = schema.Choice(
        title=_(u'Pre- & Post-Travel Class Dates'),
        description=_(u'Select ''Yes'' if you have no conflicts with pre- or post-travel class dates or orientation dates. Select ''No'' if you have a conflict on one or more dates.'),
        vocabulary=yes_no_none_vocabulary,
        required=True,
        # TODO insert date from program object
    )

    paymentDeadlines = schema.Choice(
        title=_(u'Payment Deadlines'),
        description=_(u'I understand that the payment deadlines are (DATES from PROGRAM WORKFLOW SHOULD APPEAR HERE).  I understand that all payments must be made in full by this date, or I must submit the "Notice of Financial Aid Award for Study Abroad" form if making my payments using financial aid, a scholarship that I have already received, veterans benefits or an outside loan.  If not submitted by this date, I understand that the Office of International Education will begin the process of removing me from my program and that the Withdrawal & Refund Policy will apply. '),
        vocabulary=yes_no_none_vocabulary,
        required=True,
        # TODO insert date from program object
    )

    programDepartureDate = schema.Date(
        title=_(u'Program Departure Date'),
        description=_(u'will appear only when "transfer provided" is selected on the "program workflow"'),
        required=False,
        # TODO insert date from program object when in transfer provided state
    )

    airportTransferDeparture = schema.Choice(
        title=_(u'Airport Transfer (for Departure)'),
        description=_(u'Choose one'),
        vocabulary=departure_transfer_vocabulary,
        required=False,
        # TODO this should appear only when "transfer provided" is selected on the "program workflow"
    )

    departureModeOfTransportation = schema.Choice(
        title=_(u'Departure-Mode of Transportation'),
        description=_(u'Choose one'),
        vocabulary=departure_mode_transportation_vocabulary,
        required=False,
        # TODO this should appear only when "transfer provided" is selected on the "program workflow"
    )

    programReturnDate = schema.Date(
        title=_(u'Program Return Date'),
        description=_(u'will appear only when "transfer provided" is selected on the "program workflow"'),
        required=False,
        # TODO insert date from program object when in transfer provided state
    )

    returnModeOfTransportation = schema.Choice(
        title=_(u'Return-Mode of Transportation'),
        description=_(u'Choose one'),
        vocabulary=return_mode_transportation_vocabulary,
        required=False,
        # TODO this should appear only when "transfer provided" is selected on the "program workflow"
    )

    airportTransferReturn = schema.Choice(
        title=_(u'Airport Transfer (for Return)'),
        description=_(u'Choose one'),
        vocabulary=return_transfer_vocabulary,
        required=False,
        # TODO this should appear only when "transfer provided" is selected on the "program workflow"
    )

    requestToDeviateFromProgramDates = schema.Choice(
        title=_(u'Request to Deviate from Program Dates'),
        description=_(u'Select ''Yes'' once you have printed, read, signed and uploaded this PDF'),
        vocabulary=yes_no_none_vocabulary,
        required=False,
        # TODO need link to the PDF document
    )

    #######################################################
    model.fieldset(
        'shortanswerquestions',
        label=_(u"Short Answer Questions"),
        fields=[]
    )



    #     emerg1workPhone = schema.TextLine(
#         title=_(u'Emergency Contact 1 Work Phone'),
#         description=_(u'Strongly recommended.  Please include country code (if outside US) and area code'),
#         # write_permission="UWOshOIE: Modify revisable fields",
#         required=False,
#     )
#
#     emerg1mobilePhone = schema.TextLine(
#         title=_(u'Emergency Contact 1 Mobile Phone'),
#         description=_(u'Strongly recommended.  Please include country code (if outside US) and area code'),
#         required=False,
#         # write_permission="UWOshOIE: Modify revisable fields",
#     )
#
#     emerg2name = schema.TextLine(
#         title=_(u'Emergency Contact 2 Name'),
#         required=False,
#         # write_permission="UWOshOIE: Modify revisable fields",
#     )
#
#     emerg2addr1 = schema.TextLine(
#         title=_(u'Emergency Contact 2 Address Line 1'),
#         required=False,
#         # write_permission="UWOshOIE: Modify revisable fields",
#     )
#
#     emerg2addr2 = schema.TextLine(
#         title=_(u'Emergency Contact 2 Address Line 2'),
#         required=False,
#         # write_permission="UWOshOIE: Modify revisable fields",
#     )
#
#     emerg2city = schema.TextLine(
#         title=_(u'Emergency Contact 2 City'),
#         required=False,
#         # write_permission="UWOshOIE: Modify revisable fields",
#     )
#
#     emerg2state = schema.TextLine(
#         title=_(u'Emergency Contact 2 State'),
#         required=False,
#         # write_permission="UWOshOIE: Modify revisable fields",
#     )
#
#     emerg2zip = schema.TextLine(
#         title=_(u'Emergency Contact 2 Zip Code'),
#         required=False,
#         # write_permission="UWOshOIE: Modify revisable fields",
#     )
#
#     emerg2country = schema.TextLine(
#         title=_(u'Emergency Contact 2 Country'),
#         required=False,
#         # write_permission="UWOshOIE: Modify revisable fields",
#     )
#
#     emerg2homePhone = schema.TextLine(
#         title=_(u'Emergency Contact 2 Home Phone'),
#         description=_(u'Please include country code (if outside US) and area code'),
#         required=False,
#         # write_permission="UWOshOIE: Modify revisable fields",
#     )
#
#     emerg2workPhone = schema.TextLine(
#         title=_(u'Emergency Contact 2 Work Phone'),
#         description=_(u'Please include country code (if outside US) and area code'),
#         required=False,
#         # write_permission="UWOshOIE: Modify revisable fields",
#     )
#
#     emerg2mobilePhone = schema.TextLine(
#         title=_(u'Emergency Contact 2 Mobile Phone'),
#         description=_(u'Please include country code (if outside US) and area code'),
#         required=False,
#         # write_permission="UWOshOIE: Modify revisable fields",
#     )
#
#     emerg2email = schema.TextLine(
#         title=_(u'Emergency Contact 2 Email'),
#         required=False,
#         # write_permission="UWOshOIE: Modify revisable fields",
#     )
#
#     emerg3name = schema.TextLine(
#         title=_(u'Emergency Contact 3 Name'),
#         required=False,
#         # write_permission="UWOshOIE: Modify revisable fields",
#     )
#
#     emerg3addr1 = schema.TextLine(
#         title=_(u'Emergency Contact 3 Address Line 1'),
#         required=False,
#         # write_permission="UWOshOIE: Modify revisable fields",
#     )
#
#     emerg3addr2 = schema.TextLine(
#         title=_(u'Emergency Contact 3 Address Line 2'),
#         required=False,
#         # write_permission="UWOshOIE: Modify revisable fields",
#     )
#
#     emerg3city = schema.TextLine(
#         title=_(u'Emergency Contact 3 City'),
#         required=False,
#         # write_permission="UWOshOIE: Modify revisable fields",
#     )
#
#     emerg3state = schema.TextLine(
#         title=_(u'Emergency Contact 3 State'),
#         required=False,
#         # write_permission="UWOshOIE: Modify revisable fields",
#     )
#
#     emerg3zip = schema.TextLine(
#         title=_(u'Emergency Contact 3 Zip Code'),
#         required=False,
#         # write_permission="UWOshOIE: Modify revisable fields",
#     )
#
#     emerg3country = schema.TextLine(
#         title=_(u'Emergency Contact 3 Country'),
#         required=False,
#         # write_permission="UWOshOIE: Modify revisable fields",
#     )
#
#     emerg3homePhone = schema.TextLine(
#         title=_(u'Emergency Contact 3 Home Phone'),
#         description=_(u'Please include country code (if outside US) and area code'),
#         required=False,
#         # write_permission="UWOshOIE: Modify revisable fields",
#     )
#
#     emerg3workPhone = schema.TextLine(
#         title=_(u'Emergency Contact 3 Work Phone'),
#         description=_(u'Please include country code (if outside US) and area code'),
#         required=False,
#         # write_permission="UWOshOIE: Modify revisable fields",
#     )
#
#     emerg3mobilePhone = schema.TextLine(
#         title=_(u'Emergency Contact 3 Mobile Phone'),
#         description=_(u'Please include country code (if outside US) and area code'),
#         required=False,
#         # write_permission="UWOshOIE: Modify revisable fields",
#     )
#
#     emerg3email = schema.TextLine(
#         title=_(u'Emergency Contact 3 Email'),
#         required=False,
#         # write_permission="UWOshOIE: Modify revisable fields",
#     )
#
#
#
#     dexteritytextindexer.searchable('firstName')
#     firstName = schema.TextLine(
#         title=_(u'First Name'),
#         required=True,
#     )
#
#     dexteritytextindexer.searchable('middleName')
#     middleName = schema.TextLine(
#         title=_(u'Middle Name'),
#         required=False,
#     )
#
#     dexteritytextindexer.searchable('lastName')
#     lastName = schema.TextLine(
#         title=_(u'Last Name'),
#         required=True,
#     )
#
#     model.fieldset(
#         'addresses',
#         label=_(u"Addresses"),
#         fields=[ ]
#     )
#
#     homePhone = schema.TextLine(
#         title=_(u'Home Telephone'),
#         description=_(u'Please include country code (if outside US) and area code'),
#         required=True,
#     )
#
#     citizenshipOther = schema.TextLine(
#         title=_(u'Other Citizenship Country'),
#         description=_(u'Enter country of citizenship if you selected Other'),
#         required=False,
#     )
#
#     stateResidencyOther = schema.TextLine(
#         title=_(u'Other State Residency'),
#         description=_(u'Enter state of residency if you selected Other'),
#         required=False,
#     )
#
#     dateOfBirth = schema.Date(
#         title=_(u'Birthday'),
#         required=True,
#     )
#
#     placeOfBirth = schema.TextLine(
#         title=_(u'Place of Birth'),
#         description=_(u'Enter city, state, and country'),
#         required=True,
#     )
#
#     gender = schema.Choice(
#         title=_(u'Gender'),
#         description=_(u''),
#         vocabulary='uwosh.oie.studyabroadstudent.vocabularies.genders',
#         required=False,
#     )
#
#     marriageStatus = schema.Choice(
#         title=_(u'Marital Status'),
#         description=_(u''),
#         vocabulary='uwosh.oie.studyabroadstudent.vocabularies.marriage_statuses',
#         required=False,
#     )
#
#     model.fieldset(
#         'passport',
#         label=_(u"Passport"),
#         fields=['passportName', 'passportNumber', 'passportIssueOffice', 'passportExpDate']
#     )
#
#     passportName = schema.TextLine(
#         title=_(u'Passport Full Name'),
#         description=_(u'Enter your full name EXACTLY as it appears on your passport or passport application'),
#         required=False,
#     )
#
#     passportNumber = schema.TextLine(
#         title=_(u'Passport Number'),
#         description=_(u''),
#         required=False,
#     )
#
#     passportIssueOffice = schema.TextLine(
#         title=_(u'Passport Issuing Office'),
#         description=_(u'e.g. New Orleans or U.S. Department of State'),
#         required=False,
#     )
#
#     passportExpDate = schema.Date(
#         title=_(u'Passport Expiry'),
#         required=True,
#     )
#
#     model.fieldset(
#         'additional_questions',
#         label=_(u"Additional Questions"),
#         fields=['questionAcadCareerPlan', 'questionLangCulturalSkills', 'questionPrevTravel',
#                 'questionWorkExp', 'questionEuroBizTravSem', 'questionStuExchComp', ]
#     )
#
#     questionAcadCareerPlan = schema.Text(
#         title=_(u'Academic and Career Plan'),
#         description=_(u'a) Briefly, what are your short- and long-term academic and career goals? <br> b) Why would you like to participate in this program? <br> c) What do you expect to gain from your experience?'),
# #        required=True,
#         required=False,
#     )
#
#     questionLangCulturalSkills = schema.Text(
#         title=_(u'Language and Cultural Skills'),
#         description=_(u'a) Have you studied a foreign language? If so, what is your level of fluency? <br> b) Have you completed any University-level courses on the culture or history of your destination? If so, explain. <br> c) Have you ever been immersed in a language and/or culture abroad? If so, please explain. <br> d) Do you plan to use a foreign language in a professional setting? If yes, please explain.'),
# #        required=True,
#         required=False,
#     )
#
#     questionPrevTravel = schema.Text(
#         title=_(u'Previous Travel Experience'),
#         description=_(u'Have you traveled abroad? If so, list the places to which you have traveled along with the dates and purpose.'),
# #        required=True,
#         required=False,
#     )
#
#     questionWorkExp = schema.Text(
#         title=_(u'Work Experience'),
#         description=_(u'a) Who is your current employer? <br> b) If relevant to your study abroad program, list and describe your responsibilities from current and previous jobs.'),
# #        required=True,
#         required=False,
#     )
#
#     questionEuroBizTravSem = schema.Text(
#         title=_(u'European Business Travel Seminar Only'),
#         description=_(u'Include the name of the company(ies) you are currently working for and your title(s).'),
#         required=False,
#     )
#
#     questionStuExchComp = schema.Text(
#         title=_(u'Student Exchange and Competitive Programs Only'),
#         description=_(u'Add anything else you think we should consider when reviewing your application.'),
#         required=False,
#     )
#
#     model.fieldset(
#         'medical',
#         label=_(u"Medical"),
#         fields=['doctorLastname', 'doctorFirstname', 'doctorPhone', 'medicalInsuranceCompany',
#                 'medicalPolicyHolder', 'medicalPolicyGroupNumber', 'foodAllergies',
#                 'hasDifficultyWalking', 'maxWalkingDistance']
#     )
#
#     doctorLastname = schema.TextLine(
#         title=_(u'Last Name of your Family Doctor'),
# #        required=True,
#         required=False,
#     )
#
#     doctorFirstname = schema.TextLine(
#         title=_(u'First Name of your Family Doctor'),
# #        required=True,
#         required=False,
#     )
#
#     doctorPhone = schema.TextLine(
#         title=_(u'Doctor''s Phone Number'),
#         description=_(u'Please include country code (if outside US) and area code'),
# #        required=True,
#         required=False,
#     )
#
#     medicalInsuranceCompany = schema.TextLine(
#         title=_(u'Name of Insurance Company'),
# #        required=True,
#         required=False,
#     )
#
#     medicalPolicyHolder = schema.TextLine(
#         title=_(u'Name of Policy Holder'),
# #        required=True,
#         required=False,
#     )
#
#     medicalPolicyGroupNumber = schema.TextLine(
#         title=_(u'Policy / Group Number'),
# #        required=True,
#         required=False,
#     )
#
#     foodAllergies = schema.TextLine(
#         title=_(u'Allergies'),
#         description=_(u'List any allergies (food, pet, etc.)'),
#         required=False,
#     )
#
#     hasDifficultyWalking = schema.Choice(
#         title=_(u'Difficulty Walking'),
#         description=_(u'Do you have a condition which would make it difficult to walk long distances?'),
#         vocabulary=yes_no_none_vocabulary,
# #        required=True,
#         required=False,
#     )
#
#     maxWalkingDistance = schema.TextLine(
# #    maxWalkingDistance = schema.Int(
#         title=_(u'Max Walking Distance'),
#         description=_(u'If so, what is the maximum number of minutes you can walk?'),
#         required=False,
#     )
#
#     model.fieldset(
#         'medical2',
#         label=_(u"Medical II"),
#         fields=['medicalReadStatement']
#     )
#
#     medicalReadStatement = schema.Choice(
#         title=_(u'I have read the statement below and understand.'),
#         description=_(u'""Pre-existing medical and mental health conditions are often intensified by travel to or living in a foreign environment.  Before committing to a study abroad program, consider how your new environment may affect your personal health both physically and mentally.  For example, your new environment may introduce you to new diseases, such as malaria or yellow fever, or new stresses which may cause additional complications for a person with a preexisting condition.<br> <br> The OIE strongly recommends that you have a physical, talk with a medical provider about any preexisting conditions and recommended and/or required immunizations, talk with a psychiatrist or counselor about any preexisting conditions and take care of any dental work before departure.<br> <br> If you choose not to complete this section before program acceptance, you must forward information related to the following to the OIE within one week of the application deadline for your program.  Failure to disclose medical or mental health conditions will make it extremely difficult for staff at UW Oshkosh and abroad to assist you in an emergency and may cause health professionals abroad to take actions which could lead to serious medical consequences, including death.<br> <br> NOTE ON MEDICATIONS: You are responsible for ensuring that your medications can be carried into the foreign country.  If your medical status changes after completing this application, you must inform the OIE.""'),
#         vocabulary=yes_no_none_vocabulary,
# #        required=True,
#         required=False,
#     )
#
#     model.fieldset(
#         'medical3',
#         label=_(u"Medical III"),
#         fields=['medicalHealthProblems', 'medicalHealthProblems_takenMedication',
#                 'medicalHealthProblems_medications', 'medicalHealthProblems_stable',
#                 'medicalHealthProblems_underCare', 'medicalHealthProblems_whatCondition',
#                 'medicalHealthProblems_willingToPrescribe',
#                 'medicalHealthProblems_additionalInfo', 'medicalMentalProblems',
#                 'medicalMentalProblems_takenMedication', 'medicalMentalProblems_medications',
#                 'medicalMentalProblems_currentDose', 'medicalMentalProblems_stable',
#                 'medicalMentalProblems_underCare', 'medicalMentalProblems_condition',
#                 'medicalMentalProblems_enoughMedication', 'medicalMentalProblems_additionalInfo',
#                 'medicalRegistered', 'medicalRegistered_office',
#                 'medicalRegistered_accommodations', 'medicalAccessOK', ]
#     )
#
#     medicalHealthProblems = schema.Text(
#         title=_(u'Health Problems'),
#         description=_(u'List and describe any recent (within the past five years) or continuing health problems, including physical disabilities or medical conditions; learning disabilities; drug, plant, food, animal, or insect sting allergies (include information pertaining to reactions); and/or surgeries that should be brought to the attention of the lead faculty members, liaison abroad and/or host family abroad. Complete this section now or by the Friday following the application deadline.  Write ''n/a'' in blanks where appropriate.'),
#         required=False,
#     )
#
#     medicalHealthProblems_takenMedication = schema.Choice(
#         title=_(u'Has Taken Medication'),
#         description=_(u'Are you taking or have you ever taken medication related to your physical health?'),
#         vocabulary=yes_no_none_vocabulary,
# #        required=True,
#         required=False,
#     )
#
#     medicalHealthProblems_medications = schema.Text(
#         title=_(u'Medication List'),
#         description=_(u'If so, list the medications you have taken over the past year. Write ''n/a'' in blanks where appropriate.'),
#         required=False,
#     )
#
#     medicalHealthProblems_stable = schema.Choice(
#         title=_(u'Are you stable on this medication?'),
#         vocabulary=yes_no_na_vocabulary,
# #        required=True,
#         required=False,
#     )
#
#     medicalHealthProblems_underCare = schema.Choice(
#         title=_(u'Are you currently under the care of a doctor or other health care professional?'),
#         vocabulary=yes_no_none_vocabulary,
# #        required=True,
#         required=False,
#     )
#
#     medicalHealthProblems_whatCondition = schema.Text(
#         title=_(u'Medical Conditions'),
#         description=_(u'If you are currently under the care of a doctor or other health care professional, for what condition? Write ''n/a'' in blanks where appropriate.'),
#         required=False,
#     )
#
#     medicalHealthProblems_willingToPrescribe = schema.Choice(
#         title=_(u'Enough Medication'),
#         description=_(u'Is your current physician willing to prescribe enough medication to last throughout your planned program abroad?'),
#         vocabulary=yes_no_na_vocabulary,
# #        required=True,
#         required=False,
#     )
#
#     medicalHealthProblems_additionalInfo = schema.Text(
#         title=_(u'Additional Health Info'),
#         description=_(u'Is there any additional information related to your physical health which may be helpful for program organizers, liaisons and host families to know? Write ''none'' in blank if appropriate.'),
#         required=False,
#     )
#
#     medicalMentalProblems = schema.Text(
#         title=_(u'Mental Health Problems'),
#         description=_(u'List and describe any recent or continuing mental health problems, including anxiety, depression, bipolar disorder, substance abuse (alcohol or drugs), eating disorders (anorexia/bulimia), etc. that should be brought to the attention of the lead faculty members, liaison abroad and/or host family abroad.  Include the following information: diagnosis, dates of treatment, names & locations of treating professionals, and recovery status.'),
#         required=False,
#     )
#
#     medicalMentalProblems_takenMedication = schema.Choice(
#         title=_(u'Are you taking/have you ever taken medication related to your mental health?  '),
#         vocabulary=yes_no_none_vocabulary,
# #        required=True,
#         required=False,
#     )
#
#     medicalMentalProblems_medications = schema.Text(
#         title=_(u'Mental Health Medications'),
#         description=_(u'If so, list the medications taken over the past year. Write ''n/a'' in blanks where appropriate.'),
#         required=False,
#     )
#
#     medicalMentalProblems_currentDose = schema.Text(
#         title=_(u'Mental Health Medications Dosage'),
#         description=_(u'What is the current dose? Write ''n/a'' in text area when appropriate.'),
#         required=False,
#     )
#
#     medicalMentalProblems_stable = schema.Choice(
#         title=_(u'Are you stable on this medication?'),
#         vocabulary=yes_no_na_vocabulary,
# #        required=True,
#         required=False,
#     )
#
#     medicalMentalProblems_underCare = schema.Choice(
#         title=_(u'Mental Health Care'),
#         description=_(u'Are you currently or have you ever been under the care of a psychiatrist or other medical provider, substance abuse counselor or other mental health professional?'),
#         vocabulary=yes_no_none_vocabulary,
# #        required=True,
#         required=False,
#     )
#
#     medicalMentalProblems_condition = schema.Text(
#         title=_(u'Mental Health Care Conditions'),
#         description=_(u'If yes, for what condition? Write ''n/a'' in text area when appropriate.'),
#         required=False,
#     )
#
#     medicalMentalProblems_enoughMedication = schema.Choice(
#         title=_(u'Sufficient Mental Health Medication'),
#         description=_(u'Is your current medical provider willing to prescribe enough medication to last for the duration of your planned program abroad?'),
#         vocabulary=yes_no_na_vocabulary,
# #        required=True,
#         required=False,
#     )
#
#     medicalMentalProblems_additionalInfo = schema.Text(
#         title=_(u'Mental Health Additional Information'),
#         description=_(u'Is there any additional information related to your mental health which may be helpful for program organizers, liaisons and host families to know? Write ''none'' in text area if there isn''t any.'),
#         required=False,
#     )
#
#     medicalRegistered = schema.Choice(
#         title=_(u'Registered with UW Oshkosh for Accommodations'),
#         description=_(u'Are you currently registered with the University of Wisconsin Oshkosh (with offices such as the Dean of Students office or Project Success) or with your university for medical or mental-health related accommodations?'),
#         vocabulary=yes_no_none_vocabulary,
# #        required=True,
#         required=False,
#     )
#
#     medicalRegistered_office = schema.TextLine(
#         title=_(u'UW Oshkosh Office Accommodations'),
#         description=_(u'If so, with which office have you registered? Write ''none'' in text area if you have not registered.'),
#         required=False,
#     )
#
#     medicalRegistered_accommodations = schema.Text(
#         title=_(u'Medical Authorized Accommodations'),
#         description=_(u'What accommodations have been authorized for you? Write ''n/a'' in text area when appropriate.'),
#         required=False,
#     )
#
#     medicalAccessOK = schema.Choice(
#         title=_(u'Medical Access Granted'),
#         description=_(u'""I understand and agree that this information will be accessed by the following people: faculty leader(s) (for faculty-led programs), exchange liaison(s) abroad (for student exchange programs), program organizers outside of UW Oshkosh, my host family, staff in the OIE, and staff in the Dean of Students Office.""'),
#         vocabulary=yes_no_none_vocabulary,
# #        required=True,
#         required=False,
#     )
#
#     model.fieldset(
#         'preferences',
#         label=_(u"Preferences"),
#         fields=['smokingPreferred', 'isVegetarian', 'additionalNeeds', ]
#     )
#
#     smokingPreferred = schema.Choice(
#         title=_(u'Smoking Preference'),
#         vocabulary=smoking_vocabulary,
#         default= 'No Preference',
#         required=False,
#     )
#
#     isVegetarian = schema.Choice(
#         title=_(u'Are you vegetarian?'),
#         vocabulary=yes_no_none_vocabulary,
#         #default="No",
# #        required=True,
#         required=False,
#     )
#
#     additionalNeeds = schema.Text(
#         title=_(u'Additional Needs'),
#         description=_(u'Is there anything else your host families or the OIE should know about your accommodation needs?'),
#         required=False,
#     )
#
#     dexteritytextindexer.searchable('programYear')
#     programYear = schema.TextLine(
# #    programYear = schema.Int(
#         title=_(u'Program Year'),
#         description=_(u'Enter the year you will actually be attending the program (YYYY)'),
# #        required=True,
#         required=False,
#         #write_permission="UWOshOIE: Modify normal fields",
#     )
#
#     programSemester = schema.Choice(
#         title=_(u'Semester'),
#         vocabulary=semester_vocabulary,
# #        required=True,
#         required=False,
#         #write_permission="UWOshOIE: Modify normal fields",
#     )
#
#     studentType = schema.Choice(
#         title=_(u'Student Type'),
#         vocabulary=student_type_vocabulary,
# #        required=True,
#         required=False,
#         #write_permission="UWOshOIE: Modify normal fields",
#     )
#
#     emphasis1 = schema.TextLine(
#         title=_(u'Emphasis/Licensure 1'),
#         required=False,
#         #write_permission="UWOshOIE: Modify normal fields",
#     )
#
#     emphasis2 = schema.TextLine(
#         title=_(u'Emphasis/Licensure 2'),
#         required=False,
#         #write_permission="UWOshOIE: Modify normal fields",
#     )
#
#     model.fieldset(
#         'transportation',
#         label=_(u"Transportation"),
#         fields=['willTakeBus', 'willFlyWithGroup', 'departureDate', 'returnDate', 'agreeToCosts']
#     )
#
#     willTakeBus = schema.Choice(
#         title=_(u'Bus'),
#         description=_(u'Please note: while a group bus is an option for most programs, not all programs offer this option.'),
# #        required=True,
#         required=False,
#         #write_permission="UWOshOIE: Modify revisable fields",
#         vocabulary=bus_vocabulary,
#     )
#
#     willFlyWithGroup = schema.Choice(
#         title=_(u'Flights'),
# #        required=True,
#         required=False,
#         vocabulary=fly_vocabulary,
#         #write_permission="UWOshOIE: Modify normal fields",
#     )
#
#     departureDate = schema.Date(
#         title=_(u'Planned Departure Date'),
#         description=_(u'Specify if you are deviating from the group itinerary.'),
#         required=False,
#         #write_permission="UWOshOIE: Modify normal fields",
#     )
#
#     returnDate = schema.Date(
#         title=_(u'Planned Return Date'),
#         description=_(u'Specify if you are deviating from the group itinerary.'),
#         required=False,
#         #write_permission="UWOshOIE: Modify normal fields",
#     )
#
#     agreeToCosts = schema.TextLine(
#         title=_(u'Agree to Costs'),
#         description=_(u'I understand that if I choose not to fly on dates recommended by the OIE or by my hosts abroad, I remain responsible for the full program cost, regardless of whether I participate in all events or make use of all services. Enter your initials'),
# #        required=True,
#         required=False,
#         #write_permission="UWOshOIE: Modify normal fields",
#     )
#
#     model.fieldset(
#         'orientation',
#         label=_(u"Orientation"),
#         fields=['orientationDate1', 'orientationHours1', 'orientationDate2', 'orientationHours2',
#                 'numberOfGuests', 'orientationConflict', 'conflictDate']
#     )
#
#     orientationDate1 = schema.Date(
#         title=_(u'I will attend the family orientation on'),
#         description=_(u'Enter one date and time for the four-hour session, or enter two dates and times for the two-hour sessions'),
# #        required=True,
#         required=False,
#         #write_permission="UWOshOIE: Modify normal fields",
#     )
#
#     orientationHours1 = schema.Choice(
#         title=_(u'Orientation Session 1 \"hours\"'),
#         description=_(u''),
#         vocabulary='uwosh.oie.studyabroadstudent.vocabularies.session_hours',
# #        required=True,
#         required=False,
#         #write_permission="UWOshOIE: Modify normal fields",
#     )
#
#     orientationDate2 = schema.Date(
#         title=_(u'Orientation Session part 2 (Date)'),
#         description=_(u'if applicable'),
#         required=False,
#         #write_permission="UWOshOIE: Modify normal fields",
#     )
#
#     orientationHours2 = schema.Bool(
#         title=_(u'Will attend orientation Session part 2 from 3pm - 5pm'),
#         description=_(u'if applicable'),
#         required=False,
#         #write_permission="UWOshOIE: Modify normal fields",
#     )
#
#     numberOfGuests = schema.TextLine(
# #    numberOfGuests = schema.Int(
#         title=_(u'Number of Guests'),
#         description=_(u'The following number of people will attend with me'),
# #        required=True,
#         required=False,
#         #write_permission="UWOshOIE: Modify revisable fields",
#     )
#
#     orientationConflict = schema.Choice(
#         title=_(u'Schedule Conflict'),
#         description=_(u'Do you have a conflict with any of the other pre-travel academic and/or orientation sessions?'),
# #        required=True,
#         required=False,
#         vocabulary=orientation_conflict_vocabulary,
#         #write_permission="UWOshOIE: Modify normal fields",
#     )
#
#     conflictDate = schema.Date(
#         title=_(u'Date of your conflict'),
#         description=_(u'if you selected Yes above'),
#         required=False,
#         #write_permission="UWOshOIE: Modify normal fields",
#     )
#
#
#     subject1 = schema.Choice(
#         title=_(u'Course 1 subject'),
# #        required=True,
#         required=False,
#         vocabulary='uwosh.oie.studyabroadstudent.vocabularies.subjects',
#         #write_permission="UWOshOIE: Modify normal fields",
#     )
#
#     course1 = schema.TextLine(
#         title=_(u'Course Number 1'),
# #        required=True,
#         required=False,
#         #write_permission="UWOshOIE: Modify normal fields",
#     )
#
#     credits1 = schema.Float(
#         title=_(u'Credits 1'),
# #        required=True,
#         required=False,
#         #write_permission="UWOshOIE: Modify normal fields",
#     )
#
#     subject2 = schema.Choice(
#         title=_(u'Course 2 subject'),
# #        required=True,
#         required=False,
#         vocabulary='uwosh.oie.studyabroadstudent.vocabularies.subjects',
#         #write_permission="UWOshOIE: Modify normal fields",
#     )
#
#     course2 = schema.TextLine(
#         title=_(u'Course Number 2'),
# #        required=True,
#         required=False,
#         #write_permission="UWOshOIE: Modify normal fields",
#     )
#
#     credits2 = schema.Float(
#         title=_(u'Credits 2'),
# #        required=True,
#         required=False,
#         #write_permission="UWOshOIE: Modify normal fields",
#     )
#
#     subject3 = schema.Choice(
#         title=_(u'Course 3 subject'),
# #        required=True,
#         required=False,
#         vocabulary='uwosh.oie.studyabroadstudent.vocabularies.subjects',
#         #write_permission="UWOshOIE: Modify normal fields",
#     )
#
#     course3 = schema.TextLine(
#         title=_(u'Course Number 3'),
# #        required=True,
#         required=False,
#         #write_permission="UWOshOIE: Modify normal fields",
#     )
#
#     credits3 = schema.Float(
#         title=_(u'Credits 3'),
# #        required=True,
#         required=False,
#         #write_permission="UWOshOIE: Modify normal fields",
#     )
#
#     subject4 = schema.Choice(
#         title=_(u'Course 4 subject'),
# #        required=True,
#         required=False,
#         vocabulary='uwosh.oie.studyabroadstudent.vocabularies.subjects',
#         #write_permission="UWOshOIE: Modify normal fields",
#     )
#
#     course4 = schema.TextLine(
#         title=_(u'Course Number 4'),
# #        required=True,
#         required=False,
#         #write_permission="UWOshOIE: Modify normal fields",
#     )
#
#     credits4 = schema.Float(
#         title=_(u'Credits 4'),
# #        required=True,
#         required=False,
#         #write_permission="UWOshOIE: Modify normal fields",
#     )
#
#     subject5 = schema.Choice(
#         title=_(u'Course 5 subject'),
# #        required=True,
#         required=False,
#         vocabulary='uwosh.oie.studyabroadstudent.vocabularies.subjects',
#         #write_permission="UWOshOIE: Modify normal fields",
#     )
#
#     course5 = schema.TextLine(
#         title=_(u'Course Number 5'),
# #        required=True,
#         required=False,
#         #write_permission="UWOshOIE: Modify normal fields",
#     )
#
#     credits5 = schema.Float(
#         title=_(u'Credits 5'),
# #        required=True,
#         required=False,
#         #write_permission="UWOshOIE: Modify normal fields",
#     )
#
#     subject6 = schema.Choice(
#         title=_(u'Course 6 subject'),
# #        required=True,
#         required=False,
#         vocabulary='uwosh.oie.studyabroadstudent.vocabularies.subjects',
#         #write_permission="UWOshOIE: Modify normal fields",
#     )
#
#     course6 = schema.TextLine(
#         title=_(u'Course Number 6'),
# #        required=True,
#         required=False,
#         #write_permission="UWOshOIE: Modify normal fields",
#     )
#
#     credits6 = schema.Float(
#         title=_(u'Credits 6'),
# #        required=True,
#         required=False,
#         #write_permission="UWOshOIE: Modify normal fields",
#     )
#
#     readSyllabus = schema.Bool(
#         title=_(u'Has Read Syllabus'),
#         description=_(u'I have read the syllabus for the one-credit course International Studies 333'),
# #        required=True,
#         required=False,
#         #write_permission="UWOshOIE: Modify normal fields",
#     )
#
#     enrolledIS333 = schema.Bool(
#         title=_(u'Enroll me in International Studies 333'),
#         description=_(u'You will only be enrolled if you have read the syllabus'),
#         required=False,
#         #write_permission="UWOshOIE: Modify normal fields",
#     )
#
#     model.fieldset(
#         'financial_aid',
#         label=_(u"Financial Aid"),
#         fields=['applyForAid', 'holdApplication', 'financialAidGranted']
#     )
#
#     applyForAid = schema.Choice(
#         title=_(u'Are you applying for financial aid?'),
#         description=_(u'If you are not applying for financial aid, skip to the next section.'),
# #        required=True,
#         required=False,
#         vocabulary=yes_no_none_vocabulary,
#         #write_permission="UWOshOIE: Modify normal fields",
#     )
#
#     holdApplication = schema.Choice(
#         title=_(u'Should the OIE hold or process your application?'),
#         description=_(u'HOLD your Study Abroad Application (i.e. you will only study abroad IF financial aid is available; at this point the application fee is still refundable but the OIE is not reserving a seat for you), or PROCESS your Study Abroad Applciation (i.e. you will study abroad regardless of your aid package; at this point the application fee is non-refundable and the OIE will reserve your seat.'),
# #        required=True,
#         required=False,
#         vocabulary=hold_vocabulary,
#         #write_permission="UWOshOIE: Modify normal fields",
#     )
#
#     financialAidGranted = schema.Bool(
#         title=_(u'Financial Aid Granted?'),
#         description=_(u'Set by Financial Aid staff only'),
#         required=False,
#         #write_permission="UWOshOIE: Modify Financial Aid fields",
#     )
#
#     model.fieldset(
#         'accommodation_preferences',
#         label=_(u"Accommodation Preferences"),
#         fields=['roomType', 'roommateName1', 'roommateName2', ]
#     )
#
#     roomType = schema.Choice(
#         title=_(u'Room Type'),
# #        required=True,
#         required=False,
#         vocabulary=room_type_vocabulary,
#         #write_permission="UWOshOIE: Modify revisable fields",
#     )
#
#     roommateName1 = schema.TextLine(
#         title=_(u'Roommate 1 Name'),
#         required=False,
#         #write_permission="UWOshOIE: Modify revisable fields",
#     )
#
#     roommateName2 = schema.TextLine(
#         title=_(u'Roommate 2 Name'),
#         required=False,
#         #write_permission="UWOshOIE: Modify revisable fields",
#     )
#
#     model.fieldset(
#         'expectations',
#         label=_(u"Expectations"),
#         fields=['questionExpectations', ]
#     )
#
#     questionExpectations = schema.Text(
#         title=_(u'Your Expectations For'),
#         description=_(u'a) this program as a whole? <br> b) the pre-travel general orientation session? <br> c) the pre-travel academic sessions? <br> d) your hosts (host institution, family, etc.) in the foreign country (if applicable)?'),
# #        required=True,
#         required=False,
#         #write_permission="UWOshOIE: Modify normal fields",
#     )
#
#     model.fieldset(
#         'verification',
#         label=_(u"Verification"),
#         fields=['awareOfAllMaterials', 'UWOshkoshRelease', 'certification', ]
#     )
#
#     awareOfAllMaterials = schema.Choice(
#         title=_(u'Are you aware of the application requirements for your program?'),
#         description=_(u'Additional application requirements for select programs are listed on individual program web pages.  Not all programs have additional requirements.'),
# #        required=True,
#         required=False,
#         vocabulary=aware_vocabulary,
#         #write_permission="UWOshOIE: Modify normal fields",
#     )
#
#     UWOshkoshRelease = schema.Choice(
#         title=_(u'Release of Liability'),
#         description=_(u'I hereby agree to hold harmless and indemnify the Board of Regents of the University of Wisconsin System and the University of Wisconsin Oshkosh, their officers, agents and employees, from any and all liability, loss, damages, costs or expenses which are sustained, incurred or required arising out of my actions.'),
# #        required=True,
#         required=False,
#         vocabulary=yes_no_none_vocabulary,
#         #write_permission="UWOshOIE: Modify normal fields",
#     )
#
#     certification = schema.Choice(
#         title=_(u'Certification'),
#         description=_(u'I certify that the information stated above is true and correct.  If accepted to the program, I agree to follow all payment and withdrawal policies and to regularly check my UW Oshkosh email account for program information beginning today.  If I am a non-UW Oshkosh student, I will use and submit an email address that I check regularly.'),
# #        required=True,
#         required=False,
#         vocabulary=yes_no_none_vocabulary,
#         #write_permission="UWOshOIE: Modify normal fields",
#     )
#
#
# #########################
# #OFFICE USE ONLY SECTION
# #########################
#
#     model.fieldset(
#         'office_use_only',
#         label=_(u"OFFICE USE ONLY"),
#         fields=['seatNumber', 'completionDate', 'applicationIsComplete',
#                 'comments', 'applicationFeeOK', 'UWSystemStatementOK', 'UWOshkoshStatementOK',
#                 'withdrawalRefund', 'transcriptsOK', 'programSpecificMaterialsRequired',
#                 'programSpecificMaterialsOK', 'specialStudentFormRequired',
#                 'specialStudentFormOK', 'creditOverloadFormRequired', 'creditOverloadFormOK',
#                 'medicalOK', 'medicalForm', 'passportOK', 'metPassportDeadline',
#                 'programSpecificMaterialsRequiredStepIII', 'programSpecificMaterialsOKStepIII',
#                 'attendedOrientation', 'cisiDates', 'cisiNumberOfMonths', 'programFee',
#                 'tuitionPayment', 'depositOnTime', 'payment2OnTime', 'applicationFeeRefund',
#                 'foreignCourse1', 'foreignCourse2', 'foreignCourse3', 'foreignCourse4',
#                 'foreignCourse5', 'foreignCourse6', 'papersOK', 'noMoreMaterials',
#                 'programMaterials', 'programFee2', ]
#     )
#
#     completionDate = schema.Date(
#         title=_(u'Date Application Was Completed'),
#         description=_(u'This is the date in which the application was completed.'),
#         required=False,
#     )
#
#     applicationIsComplete = schema.Bool(
#         title=_(u'Application is Complete'),
#         required=False,
#     )
#
#     comments = schema.Text(
#         title=_(u'Comments'),
#         required=False,
#     )
#
#     applicationFeeOK = schema.Bool(
#         title=_(u'Application Fee Submitted'),
#         required=False,
#     )
#
#     UWSystemStatementOK = schema.Bool(
#         title=_(u'UW System Statement of Responsibility Submitted'),
#         required=False,
#     )
#
#     UWOshkoshStatementOK = schema.Bool(
#         title=_(u'UW Oshkosh Statement of Responsibility Submitted'),
#         description=_(u'This is the date in which the application was completed.'),
#         required=False,
#     )
#
#     withdrawalRefund = schema.Bool(
#         title=_(u'Withdrawal and Refund Form Submitted'),
#         required=False,
#     )
#
#     transcriptsOK = schema.Bool(
#         title=_(u'Transcripts Submitted'),
#         required=False,
#     )
#
#     programSpecificMaterialsRequired = schema.Choice(
#         title=_(u'Program-Specific Materials Required(Step II)?'),
#         required=False,
#         vocabulary=yes_no_none_vocabulary
#     )
#
#     programSpecificMaterialsOK = schema.Bool(
#         title=_(u'Program-Specific Materials Submitted(Step II)'),
#         required=False,
#     )
#
#     specialStudentFormRequired = schema.Choice(
#         title=_(u'Special Student Form Required'),
#         required=False,
#         vocabulary=yes_no_none_vocabulary
#     )
#
#     specialStudentFormOK = schema.Bool(
#         title=_(u'Special Student Form Submitted'),
#         required=False,
#     )
#
#     creditOverloadFormRequired = schema.Choice(
#         title=_(u'Credit Overload Form Required'),
#         required=False,
#         vocabulary=yes_no_none_vocabulary
#     )
#
#     creditOverloadFormOK = schema.Bool(
#         title=_(u'Credit Overload Form Submitted'),
#         required=False,
#     )
#
#     medicalOK = schema.Bool(
#         title=_(u'Medical information is Submitted/Updated'),
#         required=False,
#     )
#
#     medicalForm = schema.Text(
#         title=_(u'Medical Form'),
#         required=False,
#     )
#
#     passportOK = schema.Bool(
#         title=_(u'Passport information or receipt submitted'),
#         required=False,
#     )
#
#     metPassportDeadline = schema.Choice(
#         title=_(u'Passport Deadline Met'),
#         required=False,
#         vocabulary=yes_no_none_vocabulary
#     )
#
#     programSpecificMaterialsRequiredStepIII = schema.Choice(
#         title=_(u'Program-Specific Materials Required(Step III)?'),
#         required=False,
#         vocabulary=yes_no_none_vocabulary
#     )
#
#     programSpecificMaterialsOKStepIII = schema.Bool(
#         title=_(u'Program-Specific Materials Submitted(Step III)'),
#         required=False,
#     )
#
#     attendedOrientation = schema.Choice(
#         title=_(u'Attended Orientation'),
#         required=False,
#         vocabulary=yes_no_none_vocabulary
#     )
#
#     cisiDates = schema.TextLine(
#         title=_(u'Health Insurance Dates'),
#         description=_(u'Cultural Insurance Services International'),
#         required=False,
#     )
#
#     cisiNumberOfMonths = schema.TextLine(
# #    cisiNumberOfMonths = schema.Int(
#         title=_(u'Health Insurance Number of Months'),
#         description=_(u'Cultural Insurance Services International'),
#         required=False,
#     )
#
#     programFee = schema.Float(
#         title=_(u'Program Fee'),
#         description=_(u''),
#         required=False,
#     )
#
#     tuitionPayment = schema.Float(
#         title=_(u'Tuition Payment (student exchange only)'),
#         description=_(u''),
#         required=False,
#     )
#
#     depositOnTime = schema.Choice(
#         title=_(u'Deposit Paid on Time'),
#         description=_(u''),
#         vocabulary=yes_no_none_vocabulary,
#         required=False,
#     )
#
#     payment2OnTime = schema.Choice(
#         title=_(u'Final Payment Made on Time (except exchange students)'),
#         description=_(u''),
#         vocabulary=yes_no_none_vocabulary,
#         required=False,
#     )
#
#     applicationFeeRefund = schema.Choice(
#         title=_(u'Application Fee Refunded'),
#         description=_(u''),
#         vocabulary=yes_no_none_vocabulary,
#         required=False,
#     )
#
#     foreignCourse1 = schema.TextLine(
#         title=_(u'Foreign institution course 1'),
#         description=_(u''),
#         required=False,
#     )
#
#     foreignCourse2 = schema.TextLine(
#         title=_(u'Foreign institution course 2'),
#         description=_(u''),
#         required=False,
#     )
#
#     foreignCourse3 = schema.TextLine(
#         title=_(u'Foreign institution course 3'),
#         description=_(u''),
#         required=False,
#     )
#
#     foreignCourse4 = schema.TextLine(
#         title=_(u'Foreign institution course 4'),
#         description=_(u''),
#         required=False,
#     )
#
#     foreignCourse5 = schema.TextLine(
#         title=_(u'Foreign institution course 5'),
#         description=_(u''),
#         required=False,
#     )
#
#     foreignCourse6 = schema.TextLine(
#         title=_(u'Foreign institution course 6'),
#         description=_(u''),
#         required=False,
#     )
#
#     papersOK = schema.Bool(
#         title=_(u'Papers information is OK'),
#         description=_(u''),
#         required=False,
#     )
#
#     noMoreMaterials = schema.Bool(
#         title=_(u'No More Materials'),
#         description=_(u''),
#         required=False,
#     )
#
#     programMaterials = schema.Bool(
#         title=_(u'Program Materials'),
#         description=_(u''),
#         required=False,
#     )
#
#     programFee2 = schema.TextLine(
# #    programFee2 = schema.Int(
#         title=_(u'Program Fee 2'),
#         description=_(u''),
#         required=False,
#     )
