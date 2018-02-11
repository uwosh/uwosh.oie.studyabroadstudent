# -*- coding: utf-8 -*-

from datetime import date
from uwosh.oie.studyabroadstudent import _
from zope import schema
from zope.interface import Interface
from plone.supermodel import model
from plone.namedfile import field
from plone.app.textfield import RichText
from z3c.relationfield.schema import RelationChoice
from plone.autoform.directives import widget
from collective.z3cform.datagridfield import DataGridFieldFactory, DictRow
from uwosh.oie.studyabroadstudent.vocabularies import yes_no_none_vocabulary, yes_no_na_vocabulary, \
    dayofmonth_vocabulary, hold_vocabulary, aware_vocabulary, program_cycle_vocabulary, seat_assignment_protocol
from plone.directives import form

class ILearningObjectiveRowSchema(Interface):
    learning_objective = schema.TextLine(title=u"Enter one objective per row. Click on the \'+\' to add a row.")


class IPreTravelDatesRowSchema(Interface):
    # pretravel_date = schema.Date(title=_(u'Date'))
    pretravel_start_datetime = schema.Datetime(title=_(u'Start'))
    # pretravel_start_time = schema.Time(title=_(u'Start Time'), vocabulary='uwosh.oie.studyabroadstudent.vocabularies.timeofday')
    # pretravel_end_time = schema.Time(title=_(u'End Time'), vocabulary='uwosh.oie.studyabroadstudent.vocabularies.timeofday')
    # pretravel_end_datetime = schema.DateTime(title=_(u'End Time'))
    pretravel_end_datetime = schema.Datetime(title=_(u'End'))
    pretravel_building = schema.Choice(title=_(u'Building'),
                                       vocabulary='uwosh.oie.studyabroadstudent.vocabularies.building')
    pretravel_room = schema.TextLine(title=_(u'Room'))
    pretravel_attendance_required = schema.Choice(title=_(u'Attendance Required?'), vocabulary=yes_no_na_vocabulary)


class ITravelDatesTransitionsDestinationsRowSchema(Interface):
    transitionDate = schema.Date(title=_(u'Transition Date'))
    destinationCity = schema.TextLine(title=_(u'Destination City'))
    destinationCountry = schema.Choice(title=_(u'Destination Country'),
                                       vocabulary='uwosh.oie.studyabroadstudent.vocabularies.countries')
    accommodation = schema.Choice(title=_(u'Accommodation'),
                                  vocabulary='uwosh.oie.studyabroadstudent.vocabularies.accommodation')
    # accommodationRoomSizes = schema.Choice(title=_(u'Room Size(s)'), vocabulary='uwosh.oie.studyabroadstudent.vocabularies.room_size')
    # TODO multi select widget doesn't respond to arrow clicks
    accommodationRoomSizes = schema.List(title=_(u'Room Size(s)'), value_type=schema.Choice(
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.room_size'))
    transitionType = schema.Choice(title=_(u'Transition Type'),
                                   vocabulary='uwosh.oie.studyabroadstudent.vocabularies.transition_type')


class IPostTravelClassDatesRowSchema(Interface):
    posttravel_start_datetime = schema.Datetime(title=_(u'Start'))
    posttravel_end_datetime = schema.Datetime(title=_(u'End'))
    posttravel_building = schema.Choice(title=_(u'Building'),
                                        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.building')
    posttravel_room = schema.TextLine(title=_(u'Room'))
    posttravel_attendance_required = schema.Choice(title=_(u'Attendance Required?'), vocabulary=yes_no_na_vocabulary)


# class IApplicantQuestionsRowSchema(Interface):
#     question1 = schema.Text(title=_(u'Question 1'))
#     question2 = schema.Text(title=_(u'Question 2'))
#     question3 = schema.Text(title=_(u'Question 3'))
#     question4 = schema.Text(title=_(u'Question 4'))
#     question5 = schema.Text(title=_(u'Question 5'))


class ICoLeadersRowSchema(Interface):
    coleader = schema.Choice(title=_(u'On-site Program Co-leader'),
                             vocabulary='uwosh.oie.studyabroadstudent.vocabularies.program_leader')


class ICourseRowSchema(Interface):
    course = schema.Choice(
        title=_(u'UW Oshkosh Course Subject & Number'),
        description=_(
            u'Add all courses associated with your program, including courses that will be taught partially at UW Oshkosh and partially while away on the program.  Do not include courses that will be taught entirely at UWO, even when these courses are offered in preparation for the program away.  Contact the OIE to add a course (abroad@uwosh.edu).'),
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.course'
    )
    credits_earned = schema.Int(
        title=_(u'UW Oshkosh Credits Earned'),
        description=_(
            u'Enter the number of credits that participants will earn for each individual course.  If you are offering a course that can be taught for a range of credits on your program (e.g. 3-5 credits), you must enter the course into this system multiple times, giving the course a different credit value each time that you enter it.')
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
        description=_(
            u'If this course requires a minimum number of completed credits prior to the course start date, indicate this here'),
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
        description=_(
            u'If this course requires that other courses be completed, or that a particular grade be earned in an earlier course, prior to the course start date, indicate this here.')
    )
    program_of_study = schema.Choice(
        title=_(u'Course Prerequisites: program of study'),
        description=_(
            u'If this course requires admission to a particular program of study prior to the course start date, indicate this here.'),
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.program_of_study',
    )
    instruction_provided_by_host = schema.Choice(
        title=_(u'Instruction Provided by Host?'),
        description=_(
            u'Select the name of the person who will teach the course, if the course is to be taught by a UW Oshkosh professor.  Select "host" when instruction is provided by a partner.  Do not select the name of the "instructor-of-record" at UW Oshkosh when instruction is provided by a partner.'),
        vocabulary=yes_no_none_vocabulary,
    )
    instruction_provided_by = schema.Choice(
        title=_(u'Instruction Provided by (if not host)'),
        description=_(
            u'Select the name of the person who will teach the course, if the course is to be taught by a UW Oshkosh professor.  Select "host" when instruction is provided by a partner.  Do not select the name of the "instructor-of-record" at UW Oshkosh when instruction is provided by a partner.'),
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.program_leader',
        required=False,
    )
    course_enrollment_at = schema.Choice(
        title=_(u'Course Enrollment at'),
        description=_(
            u'Indicate the institution at which program participants will be enrolled for each individual course.'),
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.enrollment_institution',
        required=True,
    )
    foreign_institution = schema.Choice(
        title=_(u'Foreign Institution Name'),
        description=_(u''),
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.cooperatingpartner',
        required=True,
        # TODO Oshkosh must be the first option on this dropdown list
    )
    foreign_course_number = schema.Text(
        title=_(u'Foreign Course Number'),
        description=_(u'')
    )
    foreign_course_credits = schema.Int(
        title=_(u'Foreign Course Number of Credits'),
        description=_(u'max: 2 digits'),
        min=0,
        max=99,
    )
    foreign_course_review_date = schema.Date(
        title=_(u'Foreign Course Date of Most Recent Review'),
        description=_(u'')
    )
    foreign_course_reviewer_info = schema.TextLine(
        title=_(u'Foreign Course Reviewer Name, Title & College'),
        description=_(u'')
    )
    foreign_course_syllabus = field.NamedFile(
        title=_(u'Foreign Course Syllabus'),
        description=_(u'Upload the syllabus that corresponds to the most recent date of review'),
    )
    foreign_course_builder_email = schema.TextLine(
        title=_(u'PeopleSoft Course Builder'),
        description=_(u'Enter the email address of the person in your department who will build your course/s in PeopleSoft.  If instruction is provided by the host institution, with no concurrent enrollment at UWO, enter OIE@uwosh.edu into the email address field.'),
        #TODO validate email format
        #TODO "A message should be generated to the course builder email addresses associated with each course.  Course builders should have access to all ""Course Subject & Number"" related fields and must have permission to edit greyed out fields in this section only.
        #TODO Course builders may request instructions on how to build study abroad/away sections in PeopleSoft by emailing OIE@uwosh.edu.  Course builders enter the data requested below; Financial Services uses this data to properly set tuition & fees for each course."
    )
    ps_course_id = schema.Int(
        title=_(u'PeopleSoft Course ID'),
        min=0,
        #TODO Applicant should not see this field.  This is for OIE.  This field is specific to each Subject/Course # rather than to the program.
    )
    ps_class_id = schema.Int(
        title=_(u'PeopleSoft Class Number'),
        min=0,
        #TODO Applicant should not see this field.  This is for OIE.  This field is specific to each Subject/Course # rather than to the program.
    )
    ps_section_id = schema.Int(
        title=_(u'PeopleSoft Course Section Number'),
        min=0,
        #TODO Applicant should not see this field.  This is for OIE.  This field is specific to each Subject/Course # rather than to the program.
    )
    ps_section_letter = schema.TextLine(
        title=_(u'PeopleSoft Course Section Letter'),
        #TODO dropdown?
        #TODO Applicant should not see this field.  This is for OIE.  This field is specific to each Subject/Course # rather than to the program.
    )
    ps_grade_by_date = schema.Date(
        title=_(u'PeopleSoft "grade by" date'),
        #TODO Autogenerate the "PeopleSoft 'grade by' date" by adding 5 calendar days to the "PeopleSoft Class End Date".
        #TODO Applicant should not see this field.  This is for OIE.  This field is specific to each Subject/Course # rather than to the program.
    )
    tuition_and_fees = schema.Choice(
        title=_(u'Tuition & Fees'),
        vocabulary = yes_no_none_vocabulary,
        #TODO vocabulary?
        #TODO Applicant should not see this field.  This is for OIE.  This field is specific to each Subject/Course # rather than to the program.
    )
    tuition_and_fees = schema.Choice(
        title=_(u'External Studies Courses'),
        description=_(u'Confirm that any External Studies Courses have been graded.'),
        vocabulary = yes_no_none_vocabulary,
        #TODO Applicant should not see this field.  This is for OIE.  This field is specific to each Subject/Course # rather than to the program.
        #TODO This field must be associated with each Ext Studies Course listed in "Course Subject & Number".
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
        #TODO validate email format
    )
    contributing_entity_contribution_amount = schema.Float(
        title=_(u'Contribution Amount'),
        min=0.0,
    )
    contributing_entity_contribution_currency = schema.Choice(
        title=_(u'Contribution Currency'),
        vocabulary = 'uwosh.oie.studyabroadstudent.vocabularies.currency',
    )


class IReviewerEmailRowSchema(Interface):
    reviewer_email_row = schema.TextLine(
        title=_(u'Reviewer Email Address'),
        #TODO validate email format
        #TODO autocomplete from campus email addresses? Or commonly entered email addresses? Rely on browser?
    )


class IHealthSafetySecurityDocumentRowSchema(Interface):
    health_safety_security_document = field.NamedFile(
        title=_(u'Health, Safety, Security Document'),
    )


class IOIEStudyAbroadProgram(Interface):
    title = schema.TextLine(
        title=_(u'Program Title'),
        description=_(
            u'The full Program Title will be displayed in all OIE print and on-line marketing and in all official OIE program-related materials.  To avoid confusion and increase "brand" awareness for your program, consistently use this program name in full, exactly as it appears here, in your print and electronic media.  Do not include country or city names in this field. (max length 45 chars)'),
        required=True,
        max_length=45,
    )

    description = RichText(
        title=_(u'Description'),
        description=_(
            u'This is the description that will be used to promote your program.  Your description should capture the purpose of your program, include an overview of what students will be engaged in while abroad/away, and capture students’ interest! (max length 600 chars)'),
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
        fields=['comments_all', 'comments_oie_leaders', 'comments_oie_all']
    )

    comments_all = schema.Text(
        title=_(u'Public Comments'),
        description=_(u'Comments entered here are visible by all system users.'),
        required=False,
    )

    comments_oie_leaders = schema.Text(
        title=_(u'Comments for OIE leadership'),
        description=_(
            u'Comments entered here are visible by the OIE Program Manager, Program Liaison, Program Leaders/Co-leaders and site administrators.'),
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
        fields=['calendar_year', 'term', 'college_or_unit', 'countries', 'program_code', ]
    )

    calendar_year = schema.Choice(
        title=_(u'Calendar Year'),
        description=_(
            u'Use the year during which the program runs; this is not the year that is associated with the term of study.  For example, a January interim program running from Jan 2-28, 2017 will be associated with "2017".   A program running Dec 28, 2016-Jan 28, 2017 will also be associated with "2017".'),
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
        description=_(
            u'State the learning objectives for this program.  Include only one learning objective per text field. These learning objectives will be included in end-of-program assessment and may be used to support Higher Learning Commission and other accreditation processes.'),
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
        default_mime_type='text/plain',
        allowed_mime_types=('text/plain', 'text/html',),
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
        description=_(
            u'Upload your syllabus plus other related documents (if any).  If you update your syllabus, replace this copy with the updated copy.  This field will remain editable until just prior to travel.'),
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
        description=_(
            u'Select all that apply. Contact the Office of International Education to add a language (abroad@uwosh.edu).'),
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
        description=_(
            u'How often will this program be offered?  This information will display in some marketing materials.  If it isn''t possible to predict, leave this blank.'),
        vocabulary=program_cycle_vocabulary,
    )

    widget(
        'pretravel_dates',
        DataGridFieldFactory,
    )

    pretravel_dates = schema.List(
        title=_(u'Pre-Travel Class & Orientation Dates'),
        description=_(
            u'Students expect to meet group members and their program leader or program advisor in a formal group setting at least once prior to travel.  Check with your department chair and/or College administration on pre-travel requirements specific to your unit. Students are expected to ensure, prior to confirming participation on a study abroad/away program, that they have no other obligations during your pre-travel class dates.  Students with obligations during one or more dates/times must disclose this on their application and must have the approval of the Program Liaison to participate before the OIE will place the student on the program.  For this reason, after we advertise these dates to students as mandatory, the dates shouldn''t be changed!'),
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
        description=_(
            u'Participants are expected to ensure, prior to confirming participation on a study abroad/away program, that they have no other obligations during your post-travel class dates.  Participants with obligations during one or more dates/times must disclose this on their application and must have the approval of the Program Liaison to participate before the OIE will place the participant on the program.  For this reason, after we advertise these dates to participants as mandatory, the dates shouldn’t be changed!'),
        value_type=DictRow(title=u'Post-travel Class Dates', schema=IPostTravelClassDatesRowSchema)
    )

    #######################################################
    # TODO Applicant should not see this field during the "Initial" state.  Can this be made visible AFTER transitioning from this state?
    #
    model.fieldset(
        'Return Flight',
        label=_('Return Flight'),
        fields=['airlineReturn', 'flightNumberReturn', 'airportReturn', 'returnDateTime', 'arrivalInWisconsinDate',
                'insuranceEndDate', ]
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
                'applicantQuestion5', 'cvRequired', 'letterOfMotivationRequired', 'otherRequired'],
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
        description=_(
            u'For competitive programs or for progarms that require each applicant to have specific background in addition to meeting course pre-requisites, indicate criteria to be used and select the method or methods to be employed to determine whether criteria have been met.  Do not include or duplicate course pre-requisites here.'),
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
        description=_(
            u'These questions will be required of all applicants.  Questions cannot be made optional and cannot be applied to some applicants and not to others.'),
    )

    applicantQuestion2 = schema.Text(
        title=_(u'All applicants must respond to this question 2'),
        description=_(
            u'These questions will be required of all applicants.  Questions cannot be made optional and cannot be applied to some applicants and not to others.'),
    )

    applicantQuestion3 = schema.Text(
        title=_(u'All applicants must respond to this question 3'),
        description=_(
            u'These questions will be required of all applicants.  Questions cannot be made optional and cannot be applied to some applicants and not to others.'),
    )

    applicantQuestion4 = schema.Text(
        title=_(u'All applicants must respond to this question 4'),
        description=_(
            u'These questions will be required of all applicants.  Questions cannot be made optional and cannot be applied to some applicants and not to others.'),
    )

    applicantQuestion5 = schema.Text(
        title=_(u'All applicants must respond to this question 5'),
        description=_(
            u'These questions will be required of all applicants.  Questions cannot be made optional and cannot be applied to some applicants and not to others.'),
    )

    cvRequired = schema.Choice(
        title=_(u'CV Required'),
        description=_(
            u'Complete this in English if studying in English; complete this in German if studying in German'),
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
        description=_(
            u'The Liaison to the OIE communicates decisions related to program development and delivery to the Program Manager in the OIE and communicates program changes and updates to his/her unit administration. There is only one Liaison per program;  all decision-making at the unit level must be communicated to the OIE through the designated liaison. The Liaison may also include the OIE Program Manager and/or other OIE staff in conversations or seek input when appropriate. The Liaison may also serve as the On-site Program Leader and may also teach one or more of the program courses.'),
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.liaison',
    )
    program_leader = schema.Choice(
        title=_(u'On-site Program Leader'),
        description=_(
            u'The On-site Program Leader is responsible for providing leadership for the group and for overseeing group health and safety.  The On-site Program Leader may also teach one or more of the program courses.'),
        vocabulary='uwosh.oie.studyabroadstudent.vocabularies.program_leader',
    )
    widget('program_coleaders', DataGridFieldFactory)
    program_coleaders = schema.List(
        title=_(u'On-site Program Leader (choose 0-4)'),
        description=_(
            u'The On-site Program Leader is responsible for providing leadership for the group and for overseeing group health and safety.  The On-site Program Leader may also teach one or more of the program courses.'),
        value_type=DictRow(title=u"co-leaders", schema=ICoLeadersRowSchema),
        required=False,
    )

    #######################################################
    model.fieldset(
        'Courses',
        label=_(u"Courses"),
        fields=['courses'],
    )
    widget('courses', DataGridFieldFactory)
    courses = schema.List(
        title=_(u'Courses'),
        description=_(
            u'List existing courses only.  If the course you intend to use is not an existing course, your department must submit the course for formal approval through normal university channels prior to applying to use the course abroad/away.  UW Oshkosh Curriculum Policies and Procedures do not allow the use of a contractual course, i.e. independent study or related readings, for an organized, off-campus course.'),
        value_type=DictRow(title=u'Course', schema=ICourseRowSchema),
    )

    #######################################################
    model.fieldset(
        'Contributions',
        label=_(u"Contributions"),
        fields=['contributions_label', 'contributing_entity'],
    )
    form.mode(contributions_label='display')
    contributions_label = schema.TextLine(
        description=_('If the College, Department, an external agency, external partner, or grant will contribute financially to the program, list the official name of the entity that is contributing, contributor contact details, and the amount of the contribution.'),
    )
    widget('contributing_entity', DataGridFieldFactory)
    contributing_entity = schema.List(
        title=_(u'Specify Contributing Entity or Entities'),
        description=_(u'(max: 5)'),
        required=False,
        value_type=DictRow(title=u'Contributing Entity', schema=IContributingEntityRowSchema),
    )

    #######################################################
    model.fieldset(
        'Reviewers',
        label=_(u"Reviewers"),
        fields=['reviewers_label', 'reviewer_emails'],
    )
    form.mode(reviewers_label='display')
    reviewers_label = schema.TextLine(
        description=_(u'Type an email address for every Committee Chair, Department Chair and Dean: •  who supervises a Liaison, On-site Program Leader or On-site Program Co-leader listed in this application and/or •  is associated with a course offered through this program. Do not include email addresses for committee members who review applications.'),
        #TODO Each program may have a different number of "Chair reviewers" and "Dean/Unit Director reviewers".  Who reviews an application will change depending on who is leading the program and which courses are offered.  How can this be handled?
    )
    widget('reviewer_emails', DataGridFieldFactory)
    reviewer_emails = schema.List(
        title=_(u'Reviewer Emails'),
        description=_(u'(max: 6)'),
        required=False,
        value_type=DictRow(title=u'Reviewer Emails', schema=IReviewerEmailRowSchema),
    )

    #######################################################
    model.fieldset(
        'OIE Review',
        label=_(u"OIE Review"),
        fields=['program_schedule', 'director_recommendations', 'health_safety_security_documents'],
    )
    program_schedule = schema.Choice(
        title=_(u'Program Schedule'),
        description=_(u'?'), #TODO description?
        vocabulary=yes_no_none_vocabulary,
        #TODO check box or workflow?
    )
    director_recommendations = RichText(
        title=_(u'OIE Director Recommendation'),
        description=_(u'including site-specific Health, Safety & Security  remarks'),
        default_mime_type='text/plain',
        allowed_mime_types=('text/plain', 'text/html',),
        max_length=2500,
    )
    widget('health_safety_security_documents', DataGridFieldFactory)
    health_safety_security_documents = schema.List(
        title=_(u'Health, Safety & Security Documents'),
        description=_(u'For all sites, upload Department of State Country Information and CDC country-specific information.  For sites with a U.S. Travel Warning, or when otherwise warranted, upload OIE travel recommendation and supporting documents'),
        required=False,
        value_type=DictRow(title=_(u'File'), schema=IHealthSafetySecurityDocumentRowSchema),
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


# "Syllabus & Other Supporting Documents
# Upload your syllabus plus other related documents (if any).  If you update your syllabus, replace this copy with the updated copy.  This field will remain editable until just prior to travel."
# "Number of Credits to be Earned by Each Applicant
# Minimum
# Maximum"
# "Language of Study
# Select all that apply.  Contact the Office of International Education to add a language (abroad@uwosh.edu)."
# "Cooperating Partners
# Only entities listed on the UW System Preferred Provider List or academic institutions with a current affiliation agreement with UWO may be selected here.  All other cooperating partners must be selected by following UW System procurement policies."

